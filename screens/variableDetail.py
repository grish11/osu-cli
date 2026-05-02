from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, Link
from textual.containers import Vertical, Horizontal
from explanations import EXPLANATIONS


class VariableDetailScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]
    CSS_PATH = "variableDetail.tcss"

    def __init__(self, variableKey: str, displayLabel: str, currentValue: str, source: str,) -> None:
        super().__init__()
        self.variableKey = variableKey
        self.displayLabel = displayLabel
        self.currentValue = currentValue
        self.source = source

    def compose(self) -> ComposeResult:
        text, urls = EXPLANATIONS.get( self.variableKey, ("No explanation available.", []))
        yield Header(show_clock=True)
        with Vertical(id="detail-box"):
            with Horizontal(id="detail-header"):
                yield Static(f"{self.displayLabel}:", id="detail-title")
                yield Label(self.currentValue, id="detail-value")
            yield Static(text, id="detail-text")
            for url in urls:
                yield Link(url, url=url, classes="detail-link")
        yield Footer()

    def on_mount(self) -> None:
        if self.source == "audio":
            self.set_interval(3.5, self.refreshValue)

    @work(exclusive=True, thread=True)
    def refreshValue(self) -> None:
        if self.source == "audio":
            from screens.audio import getAudioInfo
            data = getAudioInfo()
        else:
            return

        if self.variableKey not in data:
            return
        valueLabel = self.query_one("#detail-value", Label)
        self.app.call_from_thread(valueLabel.update, data[self.variableKey])
