# Validation results

Date: 2026-10-30. Package version 1.0.0. Host: macOS; tool tests on Python 3.9.6 and application tests on Python 3.12.13 / Textual 8.2.8 / pytest 9.1.1 / pytest-asyncio 1.4.0. Reproducible dependency pins are in [requirements](../examples/requirements.txt). Dependencies were installed in an isolated temporary venv, not the application or global Python.

## Observed execution

| Evaluation | Actual result / evidence | Boundary |
|---|---|---|
| Clickable chat | 6 headless tests passed; [evaluation](../examples/chat/EVALUATION.md) | Click/key actions, paste/editing, concurrent scoped replies, drafts, follow, cancel, resize/focus, errors; simulated transport |
| List/detail + settings + small change | 8 headless tests passed; [evaluation](../examples/forms/EVALUATION.md) | Filter/click/keys, stable IDs/scroll, narrow drill-down; validation/persistence/failure/duplicate save; clipped button before versus one-rule fix |
| Chat native PTY send | [result](evidence/chat-pty-quit.json): bracketed Unicode/multiline paste, Send, simulated stream, resize, quit; exit 0; sampled termios restored | Actual process input and decoding, no clipboard or emulator observation |
| Chat native PTY mouse | [result](evidence/chat-pty-mouse.json): SGR press/release at Send target after pasted input; user message and completed reply observed; exit 0; flags restored | Real mouse protocol decoding/hit handling; synthetic coordinates, not physical pointer |
| Chat interrupt / termination | [Ctrl+C](evidence/chat-pty-interrupt.json) exit 130, [SIGTERM](evidence/chat-pty-sigterm.json) exit 143; flags restored | POSIX process behavior; emitted bytes do not prove all emulator modes restored |
| PTY helper | 9 tests passed on Python 3.9.6 | Input/resize, Ctrl+C, SIGTERM, exception cleanup, dirty-exit detection, missing expectation, timeout, invalid scenario, CLI artifacts/no overwrite |
| Packaging helper | Structural/local-link/syntax, deterministic archive, no-overwrite installation/archive, broken-link rejection exercised | Not a semantic validator of the skill |
| Upstream sample extractor | gfargo: 13 tests passed; 62 marked samples / 78 placeholders verified | No local Go/Rust/TypeScript compilation claim |
| Upstream craft/key probe | diegomarino: 13 craft tests and 3 key naming tests passed; 1 live test skipped (tmux absent) | Craft heuristics and key naming; tmux capture not run |
| Current project | [read-only evaluation](codexbot-read-only.md) | Current source/docs support conversation-centered design and visible scoped communication. No project execution, modifications, API calls or server restarts |
| Quick advice route | Inline-picker border question answered in one paragraph in read-only evaluation | No gallery, mandatory concepts, exhaustive audit or approval loop |

The source copies are pinned in [attribution](../ATTRIBUTION.md); source working trees were checked clean after the selected tests. The read-only evaluation's 13 inspected application/mockup files were hashed before and after. No hashes changed. This is scoped file evidence, not a claim to have monitored every file or process on the machine.

## Problems found and improvements made

- Forward implementation exposed stale `App.size` during Resize: examples now use the event size; the framework reference gained that narrow, tested correction.
- Too-small mode lost composer focus on expansion: fixed fixture focus recovery and added an explicit verification requirement for restoring focus/caret.
- Settings initialization events hid load errors: changed status updates and added a malformed-file recovery test.
- A duplicate-save/exclusive-worker design risk could cancel an in-flight commit: used a busy guard and verified exactly one write under repeated submission.
- The first PTY probe read the slave after process exit; macOS rejected the ioctl. It now reads the master; normal, interrupt, SIGTERM, exceptional and deliberately dirty fixtures pass their positive/negative assertions. All four chat PTY scenarios were rerun successfully after correction. Failure history is preserved in the chat evaluation.

## Explicitly unobserved / untested

No actual terminal emulator window was visually inspected or driven with a physical pointer/clipboard. Font/cell alignment, color contrast across user palettes, IME, screen readers, trackpads, native selection bypass, suspend/resume and editor handoff remain unobserved. Linux, Windows, SSH and multiplexer runs were not performed. The tools document these limits; no dependency install or tmux server was required.

Go, Rust and TypeScript guidance was checked against primary sources; no sample app in those languages was compiled here. The framework guide is dated and requires checking the target project's exact version. The example applications remain **interactive prototypes**. Only the settings fixture exercises real persistence, to an explicitly supplied temporary file. No real agent transport, production backend, authentication, scheduling, reconnect or complete large-history virtualization is implied.

## Package and runtime discovery

Combined packaged suite: **27 passed in 19.26 seconds** using the README command. `package_skill.py check` passed; the official skill-creator `quick_validate.py` reported **Skill is valid!**. The entry point is 44 lines and routes to seven focused references. No project-specific name/path was found in the reusable instructions or templates.

Installation/discovery is checked separately below; a folder copy is not treated as discovery evidence.


Installation completed at `~/.codex/skills/tui-craft` without an existing destination. No other skill was replaced. **Runtime discovery confirmed** by a fresh local Codex CLI 0.166.0 app-server: `skills/list`, `forceReload: true`, no extra roots; both the user home and an unrelated isolated fixture cwd returned `tui-craft`, scope `user`, `enabled: true`, zero skill errors. Its UI metadata was also returned. The server was closed after this read-only request; no model turn was started. This confirms fresh app-server discovery, not a visual check of an already-open desktop skill picker. See [discovery evidence](evidence/discovery.json).

The installable ZIP is rooted at `tui-craft/`; its checksum is distributed beside the archive. Package tests verified deterministic builds and refusal to overwrite an existing archive or skill. The final archive was integrity-checked and compared byte-for-byte against the installed package's files.
