# Behavioral verification and audits

## Evidence levels

| Layer | Good evidence for | Cannot establish |
|---|---|---|
| Static review / design frame | Structure, visible hierarchy, possible hit regions, risks | Any working input or integration |
| State/unit tests | Transitions, IDs, filtering, cancellation races, persistence boundaries | Screen layout or terminal decoding |
| Framework event harness | Click/key handlers, focus, editing, scroll state, responsive widgets | Actual terminal mouse/paste encoding, fonts, restoration |
| Render snapshot | Cell geometry at fixed dimensions/profile; visual regressions | Controls or human readability across terminals |
| PTY integration | Real process input bytes, resize/signals, cleanup flags/status | Physical pointer delivery, emulator rendering, clipboard, IME, screen reader |
| Actual terminal observation | End-to-end actions and appearance in the named emulator/host | Other platforms or unexercised states |

Use the cheapest layer that proves the behavior, plus terminal checks for changes crossing that boundary. A small visual fix need not run every lifecycle scenario. A new application needs its core journeys exercised in a terminal; if access is unavailable, deliver the implementation and say terminal verification is pending. Do not silently downgrade a requested working app to a mockup.

## Acceptance checklist (select relevant rows)

| Concern | Automated check | Terminal observation |
|---|---|---|
| Clicks | Dispatch actual widget clicks, assert state/result; target after resize/scroll; disabled and covered targets don't fire | Physical clicks hit intended cells; press/release doesn't double fire; mouse-off and native selection work |
| Keys/focus | Same journey via keys; Tab/Shift+Tab; modal trap/restore; printable keys edit text | Hints reach app through host; focus/caret visible in color and monochrome |
| Editing/paste | Mid-string insert/delete, selection, Home/End; multiline and large Paste event; no submit | Bracketed paste from clipboard, IME if in scope, newline binding in legacy terminal |
| Scroll | Wheel and key events to correct viewport; bounds; follow pause/resume; new-content count | Trackpad/wheel, nested editor vs history, selection/copy under capture |
| Resize/content | Wide, ordinary, narrow, short, below minimum; preserve drafts/IDs/anchors and recover focus/caret after too-small mode; long strings and CJK/combining/ZWJ | Drag-resize/reflow; correct glyph/cursor width with target font/locale |
| Async/state | Controlled slow/failing transport, cancellation, late replies, duplicate submit, reconnect, queue limits | Navigation/type/cancel stay responsive during real work; no flicker or log corruption |
| Forms | Validation focus; failed save keeps draft; successful save persists; cancel policy | Fields and actions reachable at short sizes, errors adjacent and readable |
| Exit/handoff | Process quit, raw Ctrl+C, SIGTERM where supported, forced error; compare terminal flags/status; worker shutdown | Cursor/echo/mouse clean after exit; suspend/resume or child handoff returns and reloads changed data |
| Shell/access | Non-TTY, stdout/stderr/status, NO_COLOR, plain mode, broken pipe | Light/dark/reduced motion and accessibility workflow on supported host |

Use deterministic clocks/transports and meaningful state assertions. A test that only asserts the screenshot exists or a button label appears is not an interaction test. Avoid fixed sleeps where an observable condition can be awaited. For new interactions, test at least one likely failure/regression, not only the happy path.

## Audit and handoff

For each finding: user impact, severity, reproduction, file/control, observed evidence, proposed correction, and retest. Order terminal corruption/data loss and broken main workflows before usability and cosmetic preferences. Separate confirmed failures from static risks, aesthetic suggestions and unknowns. If read-only, stop at findings and don't mutate the project or restart its servers.

Record command/version/environment, fixture data, results and limits in the [validation template](../assets/templates/validation.md). Keep observed results separate from planned checks. Report one of the three deliverable levels in SKILL.md; a simulated backend remains a prototype even with excellent interaction coverage. A PTY transcript is process evidence, not an emulator screenshot. Tools and example tests are optional; see [tools](tools.md).
