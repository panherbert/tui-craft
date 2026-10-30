from __future__ import annotations

import asyncio
import json
import pytest
from textual.events import Paste
from textual.widgets import Input, Button, Checkbox, OptionList, Static
from list_detail import ListDetail, DetailScroll
from settings_form import Settings
from small_before import SmallApp as Before
from small_after import SmallApp as After

pytestmark = pytest.mark.asyncio


async def settled(pilot):
    await pilot.pause()


async def test_list_click_keyboard_filter_and_stable_refresh():
    app = ListDetail()
    async with app.run_test(size=(100, 28)) as pilot:
        await pilot.press("down", "down")
        await settled(pilot)
        assert app.selected_id == "2"
        await pilot.click("#refresh")
        await settled(pilot)
        assert app.selected_id == "2", "refresh must preserve stable identity, not index"
        options = app.query_one("#items", OptionList)
        assert options.get_option_at_index(options.highlighted).id == "2"
        await pilot.click("#filter")
        await pilot.press("0", "7")
        await settled(pilot)
        assert app.visible_ids == ["7"]
        await pilot.click("#items", offset=(3, 1))
        await settled(pilot)
        assert app.selected_id == "7"
        assert "Detail for item 7" in str(app.query_one("#detail", Static).content)
        assert app.focused.id == "detail-scroll"
        await pilot.press("pagedown")
        await settled(pilot)
        assert app.query_one("#detail-scroll", DetailScroll).scroll_y > 0
        await pilot.click("#filter")
        await pilot.press("end", "z", "q", "j", "slash")
        await settled(pilot)
        assert app.query_one("#filter", Input).value.endswith("zqj/")
        assert app.visible_ids == []
        assert "No matches" in str(app.query_one("#status", Static).content)


async def test_list_narrow_open_back_resize_and_empty():
    app = ListDetail()
    async with app.run_test(size=(60, 20)) as pilot:
        assert app.has_class("narrow")
        assert not app.query_one("#detail-pane").display
        await pilot.press("down", "enter")
        await settled(pilot)
        assert app.selected_id == "1"
        assert app.query_one("#detail-pane").display
        assert not app.query_one("#list-pane").display
        await pilot.press("escape")
        await settled(pilot)
        assert app.focused.id == "items"
        assert app.selected_id == "1"
        await pilot.resize_terminal(25, 8)
        await settled(pilot)
        assert app.has_class("too-small")
        await pilot.resize_terminal(120, 30)
        await settled(pilot)
        assert not app.has_class("too-small")
        assert app.selected_id == "1"
        assert app.query_one("#list-pane").display and app.query_one("#detail-pane").display
    async with ListDetail([]).run_test(size=(80, 24)) as pilot:
        await settled(pilot)
        assert pilot.app.selected_id is None
        assert "No matches" in str(pilot.app.query_one("#status", Static).content)


async def test_settings_edit_validate_save_cancel(tmp_path):
    path = tmp_path / "settings.json"
    app = Settings(path)
    async with app.run_test(size=(80, 24)) as pilot:
        await settled(pilot)
        assert app.ready
        name = app.query_one("#name", Input)
        await pilot.click("#name")
        await pilot.press("home", "shift+end", "backspace")
        await pilot.click("#save")
        await settled(pilot)
        assert not path.exists()
        assert app.focused.id == "name"
        assert "required" in str(app.query_one("#name-error", Static).content)
        await pilot.press("q", "j", "slash", "question_mark")
        assert name.value == "qj/?"
        await pilot.press("home", "right", "delete", "X", "end")
        assert name.value == "qX/?"
        # Input keeps the first line of a multiline paste and does not submit.
        name.post_message(Paste("日本語 e\u0301\nnot a command"))
        await settled(pilot)
        assert "日本語 e\u0301" in name.value
        assert not path.exists()
        await pilot.click("#interval")
        await pilot.press("home", "shift+end", "0")
        await pilot.press("ctrl+s")
        await settled(pilot)
        assert app.focused.id == "interval"
        assert not path.exists()
        await pilot.press("home", "shift+end", "6", "0")
        await pilot.click("#notifications")
        await pilot.press("ctrl+s")
        await app.workers.wait_for_complete()
        await settled(pilot)
        saved = json.loads(path.read_text())
        assert saved["name"] == name.value
        assert saved["interval"] == 60 and saved["notifications"] is False
        assert app.saved == saved and not app.dirty
        await pilot.click("#name")
        await pilot.press("end", "x")
        assert name.value != saved["name"]
        await pilot.click("#cancel")
        await settled(pilot)
        assert name.value == saved["name"]
        assert json.loads(path.read_text()) == saved
    reload_app = Settings(path)
    async with reload_app.run_test() as pilot:
        await settled(pilot)
        assert reload_app.query_one("#name", Input).value == saved["name"]


async def test_settings_failed_save_keeps_draft_and_keyboard_buttons(tmp_path):
    app = Settings(tmp_path / "missing-parent" / "settings.json")
    async with app.run_test(size=(40, 14)) as pilot:
        await settled(pilot)
        name = app.query_one("#name", Input)
        await pilot.click("#name")
        await pilot.press("end", "X")
        expected = name.value
        # Native tab order: name -> interval -> checkbox -> Save.
        await pilot.press("tab", "tab", "tab")
        assert app.focused.id == "save"
        await pilot.press("enter")
        await app.workers.wait_for_complete()
        await settled(pilot)
        assert "Save failed" in str(app.query_one("#status", Static).content)
        assert name.value == expected
        assert app.dirty
        assert not app.query_one("#save", Button).disabled
        await pilot.resize_terminal(25, 8)
        await settled(pilot)
        assert app.has_class("too-small")
        await pilot.resize_terminal(40, 14)
        await settled(pilot)
        assert name.value == expected
        await pilot.press("escape")
        await settled(pilot)
        assert name.value == app.saved["name"]


async def test_small_improvement_before_failure_and_after_behavior():
    async with Before().run_test(size=(40, 12)) as pilot:
        await settled(pilot)
        before = pilot.app.query_one("#apply", Button)
        assert before.region.right > 40, "demonstrate the actual baseline defect"
    for width in (40, 80):
        app = After()
        async with app.run_test(size=(width, 12)) as pilot:
            await settled(pilot)
            button = app.query_one("#apply", Button)
            assert button.region.right <= width
            assert app.query_one("#value", Input).region.width >= 8
            await pilot.click("#apply")
            await settled(pilot)
            assert app.applied == "Existing setting"
            await pilot.click("#value")
            await pilot.press("end", "X", "tab", "enter")
            await settled(pilot)
            assert app.applied == "Existing settingX"


async def test_refresh_preserves_detail_scroll_and_unicode_content():
    app = ListDetail()
    async with app.run_test(size=(100, 24)) as pilot:
        await pilot.press("enter", "pagedown", "pagedown")
        await settled(pilot)
        detail = app.query_one("#detail-scroll", DetailScroll)
        old_scroll = detail.scroll_y
        selected = app.selected_id
        assert old_scroll > 0
        await pilot.press("f5")
        await settled(pilot)
        assert app.selected_id == selected
        assert detail.scroll_y == old_scroll
        text = str(app.query_one("#detail", Static).content)
        assert "日本語 e\u0301" in text
        await pilot.resize_terminal(60, 20)
        await settled(pilot)
        assert app.query_one("#detail-pane").display
        assert app.focused.id == "detail-scroll"
        await pilot.press("escape")
        assert app.focused.id == "items"


async def test_duplicate_save_does_not_cancel_inflight_commit(tmp_path, monkeypatch):
    import threading
    import settings_form
    original = settings_form.write_settings
    started, release = threading.Event(), threading.Event()
    calls = []

    def slow_write(path, value):
        calls.append(value)
        started.set()
        if not release.wait(timeout=3):
            raise RuntimeError("test release missing")
        original(path, value)

    monkeypatch.setattr(settings_form, "write_settings", slow_write)
    app = Settings(tmp_path / "settings.json")
    async with app.run_test(size=(80, 24)) as pilot:
        await settled(pilot)
        await pilot.click("#save")
        assert await asyncio.to_thread(started.wait, 1)
        try:
            await pilot.press("ctrl+s", "ctrl+s")
            await settled(pilot)
            assert app.saving
            assert app.query_one("#save", Button).disabled
            assert len(calls) == 1
        finally:
            release.set()
        await app.workers.wait_for_complete()
        await settled(pilot)
        assert not app.saving
        assert json.loads(app.path.read_text()) == app.saved
        assert str(app.query_one("#status", Static).content) == "Saved"


async def test_settings_invalid_disk_document_is_recoverable(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"name": 27}')
    app = Settings(path)
    async with app.run_test() as pilot:
        await settled(pilot)
        assert app.ready
        assert "Load failed" in str(app.query_one("#status", Static).content)
        await pilot.click("#save")
        await app.workers.wait_for_complete()
        await settled(pilot)
        assert json.loads(path.read_text()) == app.saved
