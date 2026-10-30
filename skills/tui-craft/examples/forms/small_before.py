"""Before fixture: fixed editor width pushes Apply outside narrow terminals."""
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Button


class SmallApp(App):
    CSS = """
    Horizontal { height: 3; }
    Input { width: 52; }
    Button { width: 12; min-width: 12; }
    """
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.applied = ""

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Input(value="Existing setting", id="value")
            yield Button("Apply", id="apply")

    def on_button_pressed(self) -> None:
        self.applied = self.query_one(Input).value


if __name__ == "__main__":
    SmallApp().run()
