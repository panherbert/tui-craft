import asyncio
import pytest
from textual import events
from textual.widgets import TextArea, Button
from demo import ChatDemo, Transcript


async def settle(pilot, predicate, attempts=100):
    for _ in range(attempts):
        if predicate():
            return
        await pilot.pause(0.01)
    assert predicate(), "condition did not settle"


@pytest.mark.asyncio
async def test_mouse_send_paste_and_typing_during_reply():
    gate = asyncio.Event()
    app = ChatDemo(gate=gate, delay=0.001)
    async with app.run_test(size=(80, 24)) as pilot:
        editor = app.query_one("#composer", TextArea)
        editor.post_message(events.Paste("日本語 e\u0301 👩‍💻\nsecond line"))
        await pilot.pause()
        assert len(app.chat.messages) == 2  # paste never sends
        assert editor.text.endswith("\nsecond line")
        await pilot.click("#send")
        await settle(pilot, lambda: app.chat.busy)
        assert app.chat.messages[2].text.startswith("日本語")
        await pilot.press("q", "j", "/", "?", "left", "backspace", "X")
        assert editor.text == "qjX?"  # normal editing, no global q/j shortcuts
        assert app.chat.busy
        gate.set()
        await settle(pilot, lambda: not app.chat.busy)
        assert editor.text == "qjX?"
        assert app.chat.messages[-1].author == "Guide"
        assert any(m.author == "Scout → Guide" for m in app.chat.messages)


@pytest.mark.asyncio
async def test_switch_preserves_draft_keyboard_send_and_cancel_isolated():
    gate = asyncio.Event()
    app = ChatDemo(gate=gate)
    async with app.run_test(size=(80, 24)) as pilot:
        editor = app.query_one("#composer", TextArea)
        await pilot.press("a", "b", "left")
        await pilot.click("#notes")
        assert app.current == "notes" and editor.text == ""
        await pilot.press("n", "o", "t", "e")
        await pilot.press("f2")
        assert app.current == "studio" and editor.text == "ab"
        assert editor.cursor_location == (0, 1)
        await pilot.press("ctrl+s")
        await settle(pilot, lambda: app.chat.busy)
        await pilot.press("N", "E", "W")
        await pilot.press("ctrl+s")  # busy policy retains draft, no duplicate user turn
        assert editor.text == "NEW"
        assert sum(m.author == "You" for m in app.chat.messages) == 1
        await pilot.click("#stop")
        assert not app.chat.busy
        generation = app.chat.generation
        gate.set()
        await pilot.pause()
        assert app.chat.generation == generation
        assert not any(m.author == "Scout → Guide" for m in app.chat.messages[2:])
        await pilot.press("f2")
        assert editor.text == "note"


@pytest.mark.asyncio
async def test_scroll_follow_resize_long_content_and_focus():
    app = ChatDemo(delay=0)
    async with app.run_test(size=(80, 24)) as pilot:
        for n in range(35):
            await app.append("studio", "Reader", f"{n}: long words 日本語 " * 4)
        await pilot.pause()
        history = app.query_one("#history", Transcript)
        assert history.max_scroll_y > 0
        await pilot.press("f3", "pageup")
        await pilot.pause()
        assert app.focused is history
        assert not app.chat.following
        anchor = history.scroll_y
        await app.append("studio", "Guide", "A new message")
        await pilot.pause()
        assert history.scroll_y == anchor and app.chat.unseen == 1
        await pilot.click("#latest")
        await pilot.pause()
        assert app.chat.following and app.chat.unseen == 0
        await pilot.resize_terminal(60, 20)
        assert app.query_one("#send", Button).region.right <= 60
        await pilot.press("f4", "q", "enter", "x")
        await pilot.resize_terminal(30, 10)
        assert app.screen.has_class("too-small")
        await pilot.resize_terminal(80, 24)
        assert app.query_one("#composer", TextArea).text == "q\nx"
        assert app.focused.id == "composer"
        await pilot.press("f4", "tab")
        assert app.focused.id == "send"
        await pilot.press("enter")
        await settle(pilot, lambda: not app.chat.busy)
        assert any(m.author == "You" and m.text == "q\nx" for m in app.chat.messages)


@pytest.mark.asyncio
async def test_failure_preserves_new_draft_and_quit():
    gate = asyncio.Event()
    app = ChatDemo(gate=gate)
    async with app.run_test(size=(80, 24)) as pilot:
        editor = app.query_one("#composer", TextArea)
        editor.load_text("/error")
        await pilot.click("#send")
        await pilot.press("r", "e", "t", "r", "y")
        gate.set()
        await settle(pilot, lambda: not app.chat.busy)
        assert app.chat.messages[-1].author == "Error"
        assert editor.text == "retry"
        await pilot.press("ctrl+q")
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_wheel_pauses_only_history_not_composer():
    app = ChatDemo()
    async with app.run_test(size=(80, 24)) as pilot:
        for n in range(30):
            await app.append("studio", "Guide", str(n))
        await pilot.pause()
        history = app.query_one("#history", Transcript)
        history.post_message(events.MouseScrollUp(history, 2, 2, 0, -1, 0, False, False, False))
        await pilot.pause()
        assert not app.chat.following
        await pilot.click("#latest")
        editor = app.query_one("#composer", TextArea)
        editor.post_message(events.MouseScrollUp(editor, 2, 2, 0, -1, 0, False, False, False))
        await pilot.pause()
        assert app.chat.following


@pytest.mark.asyncio
async def test_concurrent_replies_stay_in_their_chat_and_do_not_steal_focus():
    gate = asyncio.Event()
    app = ChatDemo(gate=gate, delay=0)
    async with app.run_test(size=(80, 24)) as pilot:
        editor = app.query_one("#composer", TextArea)
        editor.load_text("studio request")
        await pilot.press("ctrl+s")
        await pilot.click("#notes")
        editor.load_text("notes request")
        await pilot.press("ctrl+s")
        await pilot.press("n", "e", "x", "t")
        gate.set()
        await settle(pilot, lambda: all(not chat.busy for chat in app.chats.values()))
        assert [m.text for m in app.chats["studio"].messages if m.author == "You"] == ["studio request"]
        assert [m.text for m in app.chats["notes"].messages if m.author == "You"] == ["notes request"]
        assert not list(app.query("#m-studio-2"))
        assert app.focused is editor and editor.text == "next"
