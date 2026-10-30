# Runtime, lifecycle, and shell boundaries

## Nonblocking architecture

Keep event routing, business state, effects, and rendering distinguishable; use native framework patterns rather than forcing every stack into MVU. Put disk/network/subprocess work in asynchronous commands/workers and send results back to the UI owner. An async function containing blocking work still blocks. Bound queues, timeouts, retries, and retained output; cancel obsolete requests and reject late results by stable request ID/generation. Propagate failures into recoverable UI states. Avoid duplicate submits, leaked tasks/timers, and updates after unmount. Render on changes or intentional ticks, and stop animation when no longer needed. Measure latency/throughput on representative content before choosing optimization thresholds.

## Terminal ownership

Prefer framework-managed setup/teardown. Record any extra modes the app enables and pair their cleanup, including partial setup failure. On normal quit, interrupt, supported termination, exception/panic: stop workers/input, restore raw/canonical/echo behavior, mouse capture, bracketed paste, keyboard flags, cursor visibility/shape, screen buffer, styling, and any title/progress state the app changed. Undo extras before leaving their screen-specific mode stack. Avoid hard process exit before cleanup and pending output complete. SIGKILL/power loss cannot be cleaned up; don't promise otherwise.

External SIGTERM and raw-mode Ctrl+C are different events; framework defaults and exit statuses differ by version. Route supported signals into the normal UI shutdown boundary rather than drawing in a low-level handler. Verify the installed version, and check the final process exit code. Honor the application's documented status contract; POSIX 128+signal is common but is not a cross-platform mandate.

Temporary handoff is not final shutdown. For editor/shell or supported Unix suspend: pause input readers and rendering; restore terminal; run/wait or suspend; re-enter modes; reload data that may have changed; relayout and redraw. A repaint alone does not reload data. Avoid unmounting an app that must resume. Windows has no POSIX job-control suspend; provide a supported alternative. Don't advertise Ctrl+Z if it does nothing.

## Environment compatibility

Use current terminal dimensions, not startup dimensions. Keep resize/quit working in too-small mode. Check light/dark palettes, NO_COLOR, reduced motion, 16-color/monochrome, plain output, and normal fonts where applicable. Color alone never carries identity/status/focus. Don't require Nerd Fonts for ordinary operation. User content needs grapheme/cell-aware rendering; renderer and emulator may disagree about emoji widths even when tests pass.

Treat terminal capability queries as optional with bounded timeouts and a working fallback frame. Multiplexers, SSH, embedded hosts, Windows consoles and non-TTY streams are distinct environments; test the deployment targets and record versions/configuration. Do not claim all terminals support a protocol from an environment variable. Prefer the framework's supported mouse/paste/key protocols over independent raw readers. Logs go to a file/framework console or are emitted after restoration, not into the owned screen. Render untrusted content as text: escape markup and suppress control sequences/OSC commands that could alter terminal state; never execute pasted text as a side effect.

## Inline and CLI tools

Check the actual input/output TTYs. A picker may read candidates from stdin while reading keys and drawing on a controlling terminal; stdout contains only selected values. No controlling terminal means a documented noninteractive route or a clear error, never a hang. Preserve useful shell scrollback and remove transient chrome on completion. Define cancellation/no-match/error codes and whether selections are newline- or NUL-delimited. Keep JSON/NDJSON free of progress, ANSI, and prompts; diagnostics belong on stderr. Test pipes, closed consumers/broken pipes, redirected output, and NO_COLOR. A subprocess cannot change its parent's directory: a cd-on-exit feature needs an explicit shell integration, not a misleading claim.

A linear mode for accessibility should contain the same meaningful roles, results, errors and available actions, with stable blocks rather than constant cursor rewrites. A browser rendering a terminal canvas does not automatically make it accessible.
