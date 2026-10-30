# Framework guidance

Inspect the project's installed versions, lockfile, input/render architecture and tests first. Keep a working stack. When a new choice is needed, compare widget/input/mouse support, lifecycle ownership, inline/full-screen fit, packaging and team language; no framework wins every case. Pin compatible dependencies and verify APIs against primary documentation for that version. These are dated notes (2026-10-30), not instructions to upgrade to latest.

## Python

Textual is useful for widget-heavy forms, lists, mouse interaction and async apps; Rich formats output but is not a full input/event framework. prompt_toolkit suits editors, REPLs and inline interaction. Existing curses/urwid code may be perfectly appropriate—inspect it before proposing a rewrite.

Textual 8.2.8: use App/widgets, TCSS and messages; native Input/TextArea/Button/scroll containers handle more than hand-built strings. `@work` runs async effects; blocking tasks need a thread worker, with `App.call_from_thread` or `post_message` to update safely. Cancelling a thread does not kill it: check cancellation and reject obsolete results. `exclusive=True` groups work by widget/group, so avoid accidentally cancelling another conversation's operation. Catch worker failures without throwing away drafts.

In a resize handler, use the incoming `Resize.size`; the app's stored size can still describe the prior frame. Test both directions across a breakpoint, including focus/caret recovery after a too-small view.

Use `App.run_test(size=(cols, rows))` and Pilot for keys/clicks/resize; assert business outcomes after event processing. Synthetic Paste events test widget behavior but not clipboard/terminal decoding. Notifications are disabled by default in run_test. `self.exit(return_code=...)` requires the entry point to propagate `app.return_code` after `app.run()` if callers need it. Textual's default Ctrl+C behavior is not a guaranteed quit; inspect bindings and choose cancel/copy/quit deliberately. `App.suspend()` hands the terminal temporarily to a child; `suspend_process` is platform-specific. Verify SIGTERM policy rather than assuming cleanup from run() covers external termination.

Primary sources: [testing](https://textual.textualize.io/guide/testing/), [workers](https://textual.textualize.io/guide/workers/), [tagged App source](https://github.com/Textualize/textual/blob/v8.2.8/src/textual/app.py), [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/stable/). Python fixture versions are pinned separately in examples; no framework installation is needed merely to read this skill.

## Go

Bubble Tea + Bubbles + Lip Gloss suit state/message-driven apps; tview/tcell offers a widget-oriented alternative, and existing gocui apps should be assessed on their needs. Use commands for I/O, then mutate state in Update, not from concurrent workers. Cancel effects with context and identify replies. Mouse reporting is not hit testing: define layout-aware targets or use widgets that implement it.

For Bubble Tea v2.1.0, use `charm.land/bubbletea/v2`; `View()` returns `tea.View`, key presses use `tea.KeyPressMsg`, and `AltScreen`/`MouseMode` live on the returned view. v1 examples with `WithAltScreen()` cannot simply be pasted into v2. Match Bubbles and Lip Gloss majors; their APIs and sizing changed too. Preserve a v1 project unless migration is part of the job. Check go.mod's required toolchain.

`Program.Run()` owns final cleanup. `ReleaseTerminal`/`RestoreTerminal` are handoff operations; RestoreTerminal resumes the TUI, it is not a defer-to-restore-the-shell function. Prefer `tea.ExecProcess` for interactive children, then reload changed data; `tea.Suspend`/`tea.ResumeMsg` require a supported platform and binding. Test Update transitions, width-aware rendered views, then real process lifecycle. Derive hints from the keymap. Verify any experimental teatest API against the pinned version.

Primary sources: [v2 upgrade guide](https://github.com/charmbracelet/bubbletea/blob/v2.1.0/UPGRADE_GUIDE_V2.md), [lifecycle](https://github.com/charmbracelet/bubbletea/blob/v2.1.0/tea.go), [child handoff](https://github.com/charmbracelet/bubbletea/blob/v2.1.0/exec.go), [Bubbles migration](https://github.com/charmbracelet/bubbles/blob/v2.2.1/UPGRADE_GUIDE_V2.md).

## Rust

Ratatui renders buffers; your app owns state, events, focus, hit testing and async policy. Crossterm provides terminal events; don't run competing readers or mix a blocking read with EventStream. Use channels/cancellation for background work and stable IDs for updates. tui-textarea or another maintained widget may be safer than inventing grapheme editing; evaluate its compatibility first. Cursive is a widget-oriented alternative.

Ratatui 0.30.2 has `ratatui::run` for init/closure/restore; older releases have different entry patterns. Install reporting hooks before the managed panic hook. Return through cleanup even when the loop fails. Additional mouse/paste/keyboard modes are your responsibility; restore them on partial setup failure, normal error and panic. SIGTERM does not automatically unwind cleanup. Stop input readers before editor handoff, reload on return, and handle reentry failure. Do not claim suspend works without implementing and testing it.

Use TestBackend buffer assertions and event/state tests; neither exercises a real terminal. Use renderer-compatible cell widths and grapheme-safe editing; byte offsets, char counts and display cells are not interchangeable. Resize from the current frame's area. Crossterm key release/repeat events need deliberate handling to avoid duplicate activation.

Primary sources: [0.30.2 initialization source](https://github.com/ratatui/ratatui/blob/ratatui-v0.30.2/ratatui/src/init.rs), [testing](https://ratatui.rs/recipes/testing/), [editor handoff](https://ratatui.rs/recipes/apps/spawn-vim/), [Crossterm events](https://docs.rs/crossterm/0.29.0/crossterm/event/index.html).

## TypeScript / JavaScript

Ink is useful when React/npm fits; small prompts may need only Clack/Inquirer. Do not add a state library or renderer just because it is in a default stack. For a mouse-heavy app, verify available mouse widgets/adapters before choosing Ink. Ink 8 does not provide DOM-style clickable components: do not invent `<Box onClick>`. A custom raw protocol parser and geometry hit testing require lifecycle and integration tests. An existing stack may already solve this better.

In Ink 8, gate each `useInput` by the active focus/mode; `useFocus` alone does not disable handlers. `usePaste` handles bracketed paste. Bound the viewport and render only visible list rows; clipping is not virtualization. `<Static>` is appropriate for completed inline output, not mutable content or an alternate-screen history store. Use abortable effects and ignore stale completions. Don't assume browser CSS or DOM events exist.

`useApp().exit` / unmount are final; wait for `waitUntilExit()` before post-run output. `suspendTerminal` is a resumable API available from 7.1, not Ink 6. `alternateScreen` is also version-dependent. Inspect signal handlers at the process boundary; don't stack competing handlers or call process.exit before teardown flushes. Check Node/React peer requirements from the actual package version. Test state and ink-testing-library frames/input, then real terminal decoding, mouse adapters and cleanup.

Primary sources: [Ink 8 API](https://github.com/vadimdemedes/ink/blob/v8.0.0/readme.md), [Ink 8 package requirements](https://github.com/vadimdemedes/ink/blob/v8.0.0/package.json), [input parser](https://github.com/vadimdemedes/ink/blob/v8.0.0/src/parse-keypress.ts).

## Verification boundary

The package's runnable examples exercise Python/Textual. Go, Rust and TypeScript notes were source/documentation checked; they are not claims of locally compiled or cross-platform-tested examples. Recheck exact APIs before writing code, and run that project's compiler/tests. Startup benchmarks from another repository/host are not a guarantee for this app.
