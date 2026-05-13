from textual.app import ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.screen import Screen
from textual import work
from screens.variableDetail import VariableDetailScreen

import shutil
import subprocess
import json

def getDisplayInfo() -> dict[str, str]:
    try:
        result = subprocess.run(["hyprctl", "monitors", "-j"], capture_output=True, text=True)
        monitors = json.loads(result.stdout)
        if not monitors:
            return {"refreshRate": "N/A", "vrr": "N/A", "activelyTearing": "N/A"}
        m = monitors[0]
        return {
            "refreshRate":          str(round(m.get("refreshRate", 0), 2)) + "Hz",
            "vrr":                  str(m.get("vrr", "N/A")),
            "activelyTearing":      str(m.get("activelyTearing", "N/A")),
            "directScanoutTo":      str(m.get("directScanoutTo", "N/A")),
            "directScanoutBlockedBy": str(m.get("directScanoutBlockedBy", "N/A")),
            "solitary":             str(m.get("solitary", "N/A")),
        }
    except Exception:
        return {"refreshRate": "N/A", "vrr": "N/A", "activelyTearing": "N/A"}

ROWS = [
    ("refreshRate",           "Monitor Refresh Rate"),
    ("vrr",                   "VRR (Variable Refresh Rate)"),
    ("activelyTearing",       "Actively Tearing"),
    ("directScanoutTo",       "Direct Scanout Target"),
    ("directScanoutBlockedBy","Direct Scanout Blocked By"),
    ("solitary",              "Solitary Mode"),
]

class DisplayLatencyScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("r", "refresh", "Refresh"),
        ("k", "cursor_up", "Up"),
        ("j", "cursor_down", "Down"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_column("variable", key="variable")
        table.add_column("value  ** Ordered by impact on osu!lazer latency (high to low). Press 'r' to refresh.", key="value")
        data = getDisplayInfo()
        for key, label in ROWS:
            table.add_row(label, data[key], key=key)

    def on_key(self, event) -> None:
        table = self.query_one(DataTable)
        if event.key == "j":
            table.move_cursor(row=table.cursor_row + 1)
        elif event.key == "k":
            table.move_cursor(row=table.cursor_row - 1)

    @work(exclusive=True, thread=True)
    def action_refresh(self) -> None:
        data = getDisplayInfo()
        table = self.query_one(DataTable)
        for key, _ in ROWS:
            self.app.call_from_thread(table.update_cell, key, "value", data[key])

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        key = event.row_key.value
        table = self.query_one(DataTable)
        currentValue = table.get_cell(event.row_key, "value")
        displayLabel = dict(ROWS)[key]
        self.app.push_screen(VariableDetailScreen(key, displayLabel, currentValue, source="display"))
