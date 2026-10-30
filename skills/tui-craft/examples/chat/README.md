# Clickable conversation fixture

An offline **interactive prototype**, built as a forward test of `tui-craft`. All participants and messages are synthetic. It performs no network requests, model calls, external commands, or persistent writes.

Run with Python 3.12 and `textual==8.2.8`:

```sh
python demo.py
```

Controls: click Studio/Notes or F2 to change conversation; F3 focuses history, F4 focuses the composer; Tab/Shift+Tab moves among native controls. Enter inserts a newline in the composer. Ctrl+S sends, or Tab to Send and press Enter. Click Stop or press Esc to cancel active work. Ctrl+C cancels active work, otherwise exits with status 130; Ctrl+Q exits normally. History PageUp/Home or wheel-up pauses following; Latest or End in history resumes it. Below 40×16 only the resize notice is shown; the previous focus and draft recover when enlarged.

Sending while already busy retains the draft and reports the conflict. Send `/error` to exercise a simulated transport failure. A failed request stays in history, and any newly typed draft is preserved. Conversation switching retains drafts, caret and history position. The simulation shows an explicit participant question, reply, and return.

Run headless checks with `pytest==9.1.1` and `pytest-asyncio==1.4.0`:

```sh
python -m pytest -q
```

The JSON files in `scenarios/` are optional inputs to the package's POSIX PTY probe. For example, from this directory (choose a fresh evidence directory):

```sh
python ../../scripts/pty_probe.py --scenario scenarios/send_quit.json --out /tmp/chat-send-evidence -- python demo.py
python ../../scripts/pty_probe.py --scenario scenarios/sigterm.json --out /tmp/chat-term-evidence --expect-exit 143 -- python demo.py
python ../../scripts/pty_probe.py --scenario scenarios/interrupt.json --out /tmp/chat-interrupt-evidence --expect-exit 130 -- python demo.py
```

Those relative paths assume the fixture is installed as `examples/chat/`. Read `EVALUATION.md` for observed evidence and limits. No terminal emulator, font, clipboard, or physical mouse behavior is proven by headless tests. This deliberately small fixture does not implement persistence, reconnect, authentication, transcript virtualization, or a production transport. It is not a general application starter.

`scenarios/mouse_send.json` sends SGR mouse press/release bytes to the Send target at 80×24. It tests the native decoder and hit handling with synthetic coordinates; it is not physical pointer observation. Run it like `send_quit.json`.
