"""Synthetic local list/detail prototype; Textual 8.2.8. No external service."""
from __future__ import annotations

from dataclasses import dataclass
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Resize
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Input, OptionList, Static
from textual.widgets.option_list import Option


@dataclass(frozen=True)
class Item:
    id: str
    title: str
    detail: str


def sample_items() -> list[Item]:
    return [Item(str(i), f"Item {i:02d} — 日本語 e\u0301", (f"Detail for item {i}. Long content stays readable.\n" * 50)) for i in range(40)]


class DetailScroll(VerticalScroll):
    can_focus = True


class ListDetail(App[None]):
    CSS = """
    Screen { layout: vertical; }
    #title { height: 1; text-style: bold; padding: 0 1; }
    #filter { height: 3; }
    #body { height: 1fr; }
    #list-pane { width: 35%; min-width: 20; }
    #items { height: 1fr; }
    #detail-pane { width: 1fr; }
    #detail { padding: 0 1; }
    #back, #refresh { height: 3; min-width: 10; }
    #status { height: 1; padding: 0 1; }
    #too-small { display: none; height: 1fr; }
    .narrow #list-pane, .narrow #detail-pane { width: 1fr; min-width: 0; }
    .narrow #detail-pane { display: none; }
    .narrow.open-detail #list-pane { display: none; }
    .narrow.open-detail #detail-pane { display: block; }
    .too-small #body, .too-small #filter { display: none; }
    .too-small #too-small { display: block; }
    DetailScroll:focus { border: heavy $accent; }
    """
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+c", "interrupt", "Quit", priority=True, show=False),
        Binding("escape", "back", "Back"),
        Binding("f5", "reload", "Refresh"),
    ]

    def __init__(self, items: list[Item] | None = None):
        super().__init__()
        self.items = sample_items() if items is None else items
        self.selected_id: str | None = None
        self.visible_ids: list[str] = []
        self.detail_open = False
        self._rebuilding = False

    def compose(self) -> ComposeResult:
        yield Static("Catalog · synthetic fixture", id="title")
        yield Input(placeholder="Filter items (printable keys type here)", id="filter")
        with Horizontal(id="body"):
            with Vertical(id="list-pane"):
                yield OptionList(id="items", markup=False)
                yield Button("Refresh", id="refresh")
            with Vertical(id="detail-pane"):
                yield Button("Back to list", id="back")
                with DetailScroll(id="detail-scroll"):
                    yield Static("Select an item", id="detail", markup=False)
        yield Static("Need at least 30 columns × 10 rows. Resize or Ctrl+Q to quit.", id="too-small")
        yield Static("", id="status", markup=False)
        yield Footer()

    def on_mount(self) -> None:
        self.populate()
        self.query_one("#items").focus()
        self.apply_size()

    def apply_size(self, size=None) -> None:
        size = size or self.size
        self.set_class(size.width < 70, "narrow")
        self.set_class(size.width < 30 or size.height < 10, "too-small")
        self.set_class(self.detail_open, "open-detail")

    def on_resize(self, event: Resize) -> None:
        # App.size can still describe the previous frame during this message.
        if event.size.width < 70 and self.focused is not None and self.focused.id in ("back", "detail-scroll"):
            self.detail_open = True
        self.apply_size(event.size)

    def populate(self) -> None:
        query = self.query_one("#filter", Input).value.casefold()
        matches = [item for item in self.items if query in item.title.casefold()]
        self.visible_ids = [item.id for item in matches]
        if self.selected_id not in self.visible_ids:
            self.selected_id = self.visible_ids[0] if self.visible_ids else None
        options = self.query_one("#items", OptionList)
        self._rebuilding = True
        options.clear_options().add_options(Option(item.title, id=item.id) for item in matches)
        options.highlighted = self.visible_ids.index(self.selected_id) if self.selected_id else None
        self._rebuilding = False
        self.query_one("#status", Static).update(f"{len(matches)} matches" if matches else "No matches. Edit the filter.")
        self.show_selected()

    def show_selected(self) -> None:
        item = next((item for item in self.items if item.id == self.selected_id), None)
        self.query_one("#detail", Static).update(f"{item.title}\n\n{item.detail}" if item else "No item selected")

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "filter":
            self.populate()

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        if self._rebuilding or event.option.id not in self.visible_ids:
            return
        # Ignore stale queued highlight messages from a replaced option set.
        current = self.query_one("#items", OptionList).highlighted
        if current is None or self.visible_ids[current] != event.option.id:
            return
        changed = event.option.id != self.selected_id
        self.selected_id = event.option.id
        self.show_selected()
        if changed:
            self.query_one("#detail-scroll", DetailScroll).scroll_home(animate=False)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.selected_id = event.option.id
        self.show_selected()
        self.detail_open = True
        self.apply_size()
        self.query_one("#detail-scroll").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.action_back()
        elif event.button.id == "refresh":
            self.action_reload()

    def action_reload(self) -> None:
        # Reverse ordering to make stable-ID selection observable.
        self.items = list(reversed(self.items))
        self.populate()

    def action_back(self) -> None:
        self.detail_open = False
        self.apply_size()
        self.query_one("#items").focus()

    def action_interrupt(self) -> None:
        self.exit(return_code=130)


if __name__ == "__main__":
    app = ListDetail()
    app.run()
    raise SystemExit(app.return_code)
