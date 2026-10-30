# Chat forward evaluation

Date: 2026-10-30. Isolated fixture; CodexBot and installed skills were not touched. Evaluator read the draft SKILL.md and its conversation, interaction, runtime, verification and Python framework sections, then implemented the realistic chat request without changing the skill.

## Observed

Environment: macOS; CPython 3.12.13; Textual 8.2.8; pytest 9.1.1; pytest-asyncio 1.4.0. Command from fixture directory: `python -m pytest -q`. Final result: **6 passed in 6.29s**.

| Journey | Evidence | Result |
|---|---|---|
| Click Send after multiline Unicode paste | Native Textual Paste event and Pilot click; assert no send before click and matching user message after | Passed |
| Edit during a held asynchronous reply | Controlled transport gate; printable q/j/?/slash, caret motion and deletion; no focus steal or lost text | Passed |
| Per-chat draft and caret | Mouse and F2 switching; assert distinct drafts and restored insertion point | Passed |
| Keyboard Send, duplicate prevention and Stop | Ctrl+S and button Enter route to same semantic action; busy draft retained; Stop cancellation prevents late result | Passed |
| Explicit participant communication and concurrent scope | Assert question/reply/return author labels and separate conversation messages | Passed |
| Follow pause/resume | PageUp, synthetic wheel, new-content count, Latest; scroll anchor unchanged on append | Passed |
| Scroll ownership | Wheel on history pauses following; wheel on editor does not | Passed |
| Resize and too-small recovery | 80×24 → 60×20 → 30×10 → 80×24; Send within bounds; draft and focus restored | Passed |
| Failure and quit | Simulated transport error retains a new draft; Ctrl+Q returns 0 | Passed in headless harness |

The first test run had two incorrect assertions (editing arithmetic and a pre-seeded participant message mistaken for a late result). Corrected those assertions; this was not a functional fix. A later focus-recovery test motivated explicit restoration of the previously focused control after too-small mode; it passed after the change.

Three POSIX PTY scenarios were attempted with the draft `pty_probe.py`: send/paste/resize/quit, SIGTERM, and raw Ctrl+C. **The probe crashed after child exit** with macOS `termios.error: (25, 'Inappropriate ioctl for device')` while reading slave flags. Therefore these attempts did not establish terminal cleanup. The failure was reported to the package author for correction and rerun; no workaround or tool edit was made by this evaluator.

## Skill assessment

The routing and evidence-level distinctions were usable without a gallery or exhaustive audit. Native editors and shared click/key actions directly improved the implementation. The conversation guidance led to visible peer exchanges and per-chat drafts rather than a dashboard of agent counters. Grouping workers per conversation prevented cancellation coupling.

The skill already says focus must move when a pane is hidden; testing the even smaller resize notice exposed a concrete case. Recommend adding “restore focus/caret when returning from the too-small state” to the resize verification example. The PTY failure demonstrates why shipped diagnostic scripts need their own macOS/Linux tests and must distinguish unavailable observations from success.

## Untested / intentionally incomplete

This is an interactive prototype with a fake transport, not a verified integrated application. Headless tests do not prove physical mouse/trackpad delivery, actual clipboard decoding, IME, emulator glyph widths, color contrast, screen-reader behavior, or terminal restoration. No actual terminal emulator was visually observed. Suspend/resume, external editor handoff, Windows, SSH and multiplexers were not exercised. The fixture intentionally omits production history virtualization, persistence, reconnect and authentication. The source uses Textual's normal teardown but that statement alone is not lifecycle evidence.

## Package-author PTY rerun after correction

The probe now samples the master after child exit (macOS invalidates the slave). On 2026-10-30 all three supplied scenarios passed: send with bracketed Unicode/multiline paste, streamed result, resize and normal quit (0); idle raw Ctrl+C (130); external SIGTERM (143). Selected termios flags matched before/after in all three. See the JSON evidence under `reports/evidence/` in the skill package. These are process/PTY observations, not physical pointer, clipboard or emulator visual verification. The earlier failure record above is retained as the reason for the correction.
