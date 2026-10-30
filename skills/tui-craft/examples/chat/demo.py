"""Offline clickable chat fixture. Fake transport; no network, disk writes or model calls."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
import signal
import sys

from textual import events, on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Static, TextArea


@dataclass
class Message:
    author: str
    text: str


@dataclass
class Conversation:
    title: str
    messages: list[Message] = field(default_factory=list)
    draft: str = ""
    cursor: tuple[int, int] = (0, 0)
    scroll: float = 0
    following: bool = True
    unseen: int = 0
    generation: int = 0
    busy: bool = False
    status: str = "Ready · offline simulation"


class Transcript(VerticalScroll):
    can_focus = True

    def on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        self.app.pause_follow()

    def on_key(self, event: events.Key) -> None:
        if event.key in ("up", "pageup", "home"):
            self.app.pause_follow()
        elif event.key == "end":
            self.app.action_latest()


class ChatDemo(App):
    """One in-memory chat model, native controls, independently cancellable workers."""

    CSS = """
    Screen { layout: vertical; }
    #body { height: 1fr; }
    #chats, #actions { height: 3; }
    #chats Button, #actions Button { width: auto; min-width: 9; margin-right: 1; }
    #title, #status { height: 1; padding: 0 1; }
    #history { height: 1fr; padding: 0 1; border: solid $panel; }
    #history:focus { border: double $accent; }
    .message { height: auto; margin-bottom: 1; }
    #composer { height: 5; min-height: 3; border: solid $panel; }
    #composer:focus { border: double $accent; }
    #small { display: none; padding: 1; }
    Screen.too-small #body { display: none; }
    Screen.too-small #small { display: block; }
    """
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+c", "interrupt", "Stop / quit", priority=True, show=False),
        Binding("f2", "next_chat", "Chat", priority=True),
        Binding("f3", "history", "History", priority=True),
        Binding("f4", "compose", "Compose", priority=True),
        Binding("ctrl+s", "send", "Send", priority=True),
        Binding("escape", "cancel_reply", "Stop", priority=True, show=False),
    ]

    def __init__(self, *, delay: float = 0.06, gate: asyncio.Event | None = None):
        super().__init__()
        self.chats = {
            "studio": Conversation("Studio", [Message("Guide → Scout", "Please check the proposed change."), Message("Scout → Guide", "I will report here with the result.")]),
            "notes": Conversation("Notes", [Message("Guide", "A separate conversation with its own draft.")]),
        }
        self.current = "studio"
        self.delay, self.gate = delay, gate
        self.pending = {}
        self._term_handler = False
        self._focus_before_small = "composer"

    @property
    def chat(self) -> Conversation:
        return self.chats[self.current]

    def compose(self) -> ComposeResult:
        yield Static("Terminal too small. Use at least 40 × 16. Ctrl+Q quits.", id="small")
        with Vertical(id="body"):
            with Horizontal(id="chats"):
                yield Button("Studio", id="studio")
                yield Button("Notes", id="notes")
            yield Static(id="title", markup=False)
            yield Transcript(id="history")
            yield Static(id="status", markup=False)
            yield TextArea(id="composer", tab_behavior="focus", placeholder="Message · Enter newline · Tab then Enter sends")
            with Horizontal(id="actions"):
                yield Button("Send", id="send", variant="primary")
                yield Button("Stop", id="stop")
                yield Button("Latest", id="latest")
        yield Footer()

    async def on_mount(self) -> None:
        if sys.platform != "win32":
            try:
                asyncio.get_running_loop().add_signal_handler(signal.SIGTERM, lambda: self.exit(return_code=143))
                self._term_handler = True
            except (NotImplementedError, RuntimeError):
                pass
        await self.show_chat()
        self.query_one("#composer").focus()

    def on_unmount(self) -> None:
        if self._term_handler:
            asyncio.get_running_loop().remove_signal_handler(signal.SIGTERM)

    def on_resize(self, event: events.Resize) -> None:
        small = event.size.width < 40 or event.size.height < 16
        was_small = self.screen.has_class("too-small")
        if small and not was_small and self.focused is not None:
            self._focus_before_small = self.focused.id or "composer"
        self.screen.set_class(small, "too-small")
        if was_small and not small:
            self.call_after_refresh(lambda: self.query_one(f"#{self._focus_before_small}").focus())

    async def show_chat(self) -> None:
        history = self.query_one("#history", Transcript)
        await history.remove_children()
        for index, message in enumerate(self.chat.messages):
            await history.mount(self.message_widget(self.current, index, message))
        editor = self.query_one("#composer", TextArea)
        editor.load_text(self.chat.draft)
        editor.move_cursor(self.chat.cursor)
        self.update_status()
        if self.chat.following:
            history.scroll_end(animate=False, immediate=True)
        else:
            history.scroll_to(y=self.chat.scroll, animate=False, immediate=True)

    @staticmethod
    def message_widget(chat_id: str, index: int, message: Message) -> Static:
        return Static(f"{message.author}: {message.text}", id=f"m-{chat_id}-{index}", classes="message", markup=False)

    async def switch(self, chat_id: str) -> None:
        editor = self.query_one("#composer", TextArea)
        self.chat.draft, self.chat.cursor = editor.text, editor.cursor_location
        self.chat.scroll = self.query_one("#history").scroll_y
        self.current = chat_id
        await self.show_chat()
        editor.focus()

    @on(Button.Pressed)
    async def clicked(self, event: Button.Pressed) -> None:
        control = event.button.id
        if control in self.chats:
            await self.switch(control)
        elif control == "send":
            await self.action_send()
        elif control == "stop":
            self.action_cancel_reply()
        elif control == "latest":
            self.action_latest()

    async def action_next_chat(self) -> None:
        await self.switch("notes" if self.current == "studio" else "studio")

    def action_history(self) -> None:
        self.query_one("#history").focus()

    def action_compose(self) -> None:
        self.query_one("#composer").focus()

    def update_status(self) -> None:
        self.query_one("#title", Static).update(f"{self.chat.title} · participant exchange · simulated transport")
        follow = "following" if self.chat.following else f"paused · {self.chat.unseen} new · Latest resumes"
        self.query_one("#status", Static).update(f"{self.chat.status} | {follow}")
        self.query_one("#stop", Button).disabled = not self.chat.busy
        for name in self.chats:
            self.query_one(f"#{name}", Button).label = ("> " if name == self.current else "") + self.chats[name].title

    async def append(self, chat_id: str, author: str, text: str) -> int:
        chat = self.chats[chat_id]
        index = len(chat.messages)
        message = Message(author, text)
        chat.messages.append(message)
        if chat_id == self.current:
            await self.query_one("#history").mount(self.message_widget(chat_id, index, message))
            self.after_update(chat_id, new_message=True)
        return index

    def after_update(self, chat_id: str, *, new_message: bool = False) -> None:
        if chat_id != self.current:
            return
        if self.chat.following:
            self.query_one("#history").scroll_end(animate=False)
        elif new_message:
            self.chat.unseen += 1
        self.update_status()

    async def action_send(self) -> None:
        editor = self.query_one("#composer", TextArea)
        text = editor.text.strip()
        if not text:
            return
        if self.chat.busy:
            self.chat.status = "Already replying; draft retained"
            self.update_status()
            return
        chat_id, chat = self.current, self.chat
        chat.generation += 1
        chat.busy, chat.status = True, "Replying · Esc or Stop cancels"
        editor.load_text("")
        chat.draft = ""
        await self.append(chat_id, "You", text)
        editor.focus()
        self.pending[chat_id] = self.run_worker(self.reply(chat_id, chat.generation, text), group=chat_id, exclusive=True, exit_on_error=False)
        self.update_status()

    async def reply(self, chat_id: str, generation: int, text: str) -> None:
        chat = self.chats[chat_id]
        try:
            await self.append(chat_id, "Guide → Scout", "Could you check this request?")
            if self.gate is not None:
                await self.gate.wait()
            if text == "/error":
                raise RuntimeError("Simulated transport failure")
            index = await self.append(chat_id, "Scout → Guide", "")
            for chunk in ("Checked the request. ", "The reply stays in this conversation. ", "No external work ran."):
                await asyncio.sleep(self.delay)
                if chat.generation != generation:
                    return
                chat.messages[index].text += chunk
                if chat_id == self.current:
                    self.query_one(f"#m-{chat_id}-{index}", Static).update(f"Scout → Guide: {chat.messages[index].text}")
                    self.after_update(chat_id)
            await self.append(chat_id, "Guide", "Thanks, Scout. This simulated exchange is complete.")
            chat.status = "Complete · offline simulation"
        except asyncio.CancelledError:
            return
        except Exception as error:
            if chat.generation == generation:
                chat.status = "Failed · retry by sending again"
                await self.append(chat_id, "Error", str(error))
        finally:
            if chat.generation == generation:
                chat.busy = False
                self.after_update(chat_id)

    def action_cancel_reply(self) -> None:
        chat = self.chat
        if chat.busy:
            chat.generation += 1
            self.pending[self.current].cancel()
            chat.busy, chat.status = False, "Cancelled · completed messages retained"
            self.update_status()

    def action_interrupt(self) -> None:
        if self.chat.busy:
            self.action_cancel_reply()
        else:
            self.exit(return_code=130)

    def pause_follow(self) -> None:
        self.chat.following = False
        self.update_status()

    def action_latest(self) -> None:
        self.chat.following, self.chat.unseen = True, 0
        self.query_one("#history").scroll_end(animate=False)
        self.update_status()


if __name__ == "__main__":
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("This interactive fixture needs a terminal.", file=sys.stderr)
        raise SystemExit(2)
    app = ChatDemo()
    app.run()
    raise SystemExit(app.return_code)
