from textual import work
from textual.app import ComposeResult
from textual.widgets import Header, Footer, DataTable
from textual.screen import Screen
import os

from screens.variableDetail import VariableDetailScreen


# Functions -------------------------------------------
def _parseIniFile(path: str) -> dict[str, str]:
    try:
        with open(os.path.expanduser(path), "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return {}

    result = {}
    for line in lines:
        parts = line.split(" = ")
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            result[key] = value
    return result


def getOsuSettings() -> dict[str, str]:
    empty = {
        "frameSync":     "—",
        "windowMode":    "—",
        "executionMode": "—",
        "renderer":      "—",
        "audioOffset":   "—",
    }

    framework = _parseIniFile("~/.local/share/osu/framework.ini")
    game = _parseIniFile("~/.local/share/osu/game.ini")

    if not framework and not game:
        return empty

    audioOffset = game.get("AudioOffset", "unknown")
    return {
        "frameSync":     framework.get("FrameSync", "unknown"),
        "windowMode":    framework.get("WindowMode", "unknown"),
        "executionMode": framework.get("ExecutionMode", "unknown"),
        "renderer":      framework.get("Renderer", "unknown"),
        "audioOffset":   f"{audioOffset}ms" if audioOffset != "unknown" else "unknown",
    }


# Screens ---------------------------------------------
ROW_LABELS = [
    ("frameSync",     "Frame sync"),
    ("windowMode",    "Window mode"),
    ("executionMode", "Execution mode"),
    ("renderer",      "Renderer"),
    ("audioOffset",   "Audio offset"),
]


class OsuLatencyScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_column("variable", key="variable")
        table.add_column("value", key="value")

        data = getOsuSettings()
        for key, label in ROW_LABELS:
            table.add_row(label, data[key], key=key)

        # config files rarely change, 10s is plenty
        self.set_interval(10.0, self.refreshValues)

    @work(exclusive=True, thread=True)
    def refreshValues(self) -> None:
        data = getOsuSettings()
        table = self.query_one(DataTable)
        for key, _ in ROW_LABELS:
            self.app.call_from_thread(
                table.update_cell, key, "value", data[key]
            )

    def on_data_table_row_selected(
        self, event: DataTable.RowSelected) -> None:
        key = event.row_key.value
        table = self.query_one(DataTable)
        currentValue = table.get_cell(event.row_key, "value")
        displayLabel = dict(ROW_LABELS)[key]
        self.app.push_screen(VariableDetailScreen(key, displayLabel, currentValue))
