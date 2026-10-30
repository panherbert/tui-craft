"""Settings prototype: writes only to the explicitly supplied settings path."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import tempfile

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Resize
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Checkbox, Footer, Input, Label, Static

DEFAULTS = {"name": "Sample workspace", "interval": 30, "notifications": True}


def read_settings(path: Path) -> dict:
    if not path.exists():
        return dict(DEFAULTS)
    value = json.loads(path.read_text())
    if (not isinstance(value, dict) or not isinstance(value.get("name"), str)
            or not value["name"].strip() or type(value.get("interval")) is not int
            or not 1 <= value["interval"] <= 3600 or type(value.get("notifications")) is not bool):
        raise ValueError("Invalid settings document")
    return {key: value[key] for key in DEFAULTS}


def write_settings(path: Path, value: dict) -> None:
    # Atomic replacement keeps a failed write from corrupting existing settings.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8", delete=False) as file:
            temporary = Path(file.name)
            json.dump(value, file, ensure_ascii=False, indent=2)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class Settings(App[None]):
    CSS = """
    Screen { layout: vertical; }
    #title { height: 1; text-style: bold; padding: 0 1; }
    #fields { height: 1fr; padding: 0 1; }
    Label { height: auto; }
    Input { width: 1fr; }
    .error { height: auto; color: $error; }
    #actions { height: 3; padding: 0 1; }
    Button { min-width: 10; margin-right: 1; }
    #status { height: 2; padding: 0 1; }
    #too-small { display: none; height: 1fr; }
    .too-small #fields, .too-small #actions { display: none; }
    .too-small #too-small { display: block; }
    """
    BINDINGS = [
        Binding("ctrl+s", "save", "Save", priority=True),
        Binding("escape", "cancel", "Discard edits"),
        Binding("ctrl+q", "quit", "Quit (discard)"),
        Binding("ctrl+c", "interrupt", "Quit", priority=True, show=False),
    ]

    def __init__(self, path: Path):
        super().__init__()
        self.path = Path(path)
        self.saved = dict(DEFAULTS)
        self.ready = False
        self.saving = False
        self.dirty = False

    def compose(self) -> ComposeResult:
        yield Static("Settings · local fixture", id="title")
        with VerticalScroll(id="fields"):
            yield Label("Workspace name (required)")
            yield Input(id="name")
            yield Static("", id="name-error", classes="error", markup=False)
            yield Label("Refresh interval (1–3600 seconds)")
            yield Input(id="interval")
            yield Static("", id="interval-error", classes="error", markup=False)
            yield Checkbox("Notifications", id="notifications")
        with Horizontal(id="actions"):
            yield Button("Save", id="save", variant="primary")
            yield Button("Cancel edits", id="cancel")
        yield Static("Need at least 30 columns × 10 rows. Resize or Ctrl+Q.", id="too-small")
        yield Static("Loading…", id="status", markup=False)
        yield Footer()

    async def on_mount(self) -> None:
        try:
            self.saved = await asyncio.to_thread(read_settings, self.path)
            message = "Loaded. Save writes only the supplied file."
        except (OSError, ValueError) as error:
            message = f"Load failed: {error}. Defaults shown; Save retries."
        self.restore_fields()
        self.ready = True
        self.query_one("#status", Static).update(message)
        self.query_one("#name").focus()
        self.apply_size(self.size)

    def on_resize(self, event: Resize) -> None:
        self.apply_size(event.size)

    def apply_size(self, size) -> None:
        self.set_class(size.width < 30 or size.height < 10, "too-small")

    def restore_fields(self) -> None:
        self.query_one("#name", Input).value = self.saved["name"]
        self.query_one("#interval", Input).value = str(self.saved["interval"])
        self.query_one("#notifications", Checkbox).value = self.saved["notifications"]
        self.query_one("#name-error", Static).update("")
        self.query_one("#interval-error", Static).update("")
        self.dirty = False

    def on_input_changed(self) -> None:
        self.update_dirty()

    def on_checkbox_changed(self) -> None:
        self.update_dirty()

    def update_dirty(self) -> None:
        if not self.ready or self.saving:
            return
        was_dirty = self.dirty
        self.dirty = (self.query_one("#name", Input).value != self.saved["name"] or
                      self.query_one("#interval", Input).value != str(self.saved["interval"]) or
                      self.query_one("#notifications", Checkbox).value != self.saved["notifications"])
        if was_dirty != self.dirty:
            self.query_one("#status", Static).update("Unsaved edits" if self.dirty else "No unsaved edits")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()

    @work
    async def action_save(self) -> None:
        if not self.ready or self.saving:
            return
        name = self.query_one("#name", Input).value.strip()
        raw_interval = self.query_one("#interval", Input).value
        name_error = "Name is required." if not name else ""
        try:
            interval = int(raw_interval)
            if not 1 <= interval <= 3600:
                raise ValueError
            interval_error = ""
        except ValueError:
            interval = 0
            interval_error = "Enter a whole number from 1 to 3600."
        self.query_one("#name-error", Static).update(name_error)
        self.query_one("#interval-error", Static).update(interval_error)
        if name_error or interval_error:
            self.query_one("#name" if name_error else "#interval").focus()
            self.query_one("#status", Static).update("Fix the marked fields; edits kept.")
            return
        value = dict(name=name, interval=interval, notifications=self.query_one("#notifications", Checkbox).value)
        self.saving = True
        self.query_one("#save", Button).disabled = True
        self.query_one("#cancel", Button).disabled = True
        self.query_one("#fields").disabled = True
        self.query_one("#status", Static).update("Saving…")
        try:
            await asyncio.to_thread(write_settings, self.path, value)
        except OSError as error:
            self.query_one("#status", Static).update(f"Save failed: {error}. Edits kept; retry Save.")
        else:
            self.saved = value
            self.dirty = False
            self.query_one("#status", Static).update("Saved")
        finally:
            self.saving = False
            self.query_one("#fields").disabled = False
            self.query_one("#save", Button).disabled = False
            self.query_one("#cancel", Button).disabled = False

    def action_cancel(self) -> None:
        if self.saving:
            return
        self.restore_fields()
        self.query_one("#status", Static).update("Edits discarded")
        self.query_one("#name").focus()

    def action_interrupt(self) -> None:
        self.exit(return_code=130)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Explicit destination; parent directory must exist")
    args = parser.parse_args()
    app = Settings(args.path)
    app.run()
    raise SystemExit(app.return_code)
