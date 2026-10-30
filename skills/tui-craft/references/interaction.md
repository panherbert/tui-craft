# Input, focus, and scrolling

## Action contract

For each changed control record: action, pointer target, keyboard route, enabled condition, affected state, and visible result. Share one semantic action between click and key handlers. A hover or button-shaped label is not a working control. Use framework widgets/hit testing where possible; custom cell hit rectangles must be rebuilt after resize and account for border, clipping, viewport offsets, and Unicode widths. Avoid triggering twice on mouse down and release. Modal hit testing must block covered controls.

Implement pointer focus, selection, tab navigation, buttons, and wheel behavior where the task calls for clicks. Enable only the required capture modes; expose a mouse-off option and explain native text-selection bypass for supported terminals. Do not promise a universal bypass modifier. Every pointer action has a keyboard route. If the current stack lacks native mouse widgets, explain the adapter work instead of delivering a keyboard-only app under a clickable label.

## Focus and text ownership

Maintain an explicit focus target and logical Tab/Shift+Tab order. Show focus without relying on color. On opening an overlay, move focus into it; on dismissal restore the previous valid target. Keep obscured controls inactive. Selection, focus, hover, and editing mode are different states. Avoid unsolicited focus changes during refresh or streaming.

Focused editors own printable characters, including q, j, k, /, ?, and digits. Global single-letter shortcuts apply only outside text entry. Keep normal caret motion, Home/End, Backspace/Delete, word motion where supported, selection/copy/paste, and predictable undo if the editor provides it. Prefer a tested input widget over a hand-built append-only string. Single-line versus multiline paste must be explicit; bracketed paste inserts data without submitting or executing commands. Test newlines, a large paste, and paste during work. Preserve drafts on navigation and failures.

Define Enter (submit or newline) and a discoverable portable alternate action. Shift+Enter/Ctrl+Enter may collide with Enter on legacy terminals; never make them the sole path. Even Ctrl+J delivery varies by host/driver—verify the actual bindings. A visible Send button reachable with Tab+Enter is a useful fallback. Completion that owns Tab also needs an obvious way to move focus.

## Navigation and discoverability

Choose familiar keys that match the app; don't impose a universal keymap. Arrows and Tab are useful baseline routes, vim aliases only outside editing. Esc usually dismisses/cancels one layer before exiting. Ctrl+C policy must be explicit: cancel active work or quit, without trapping the user. Preserve the project's supported suspend behavior and show a platform-appropriate alternative. Host prefixes and OS shortcuts may swallow keys; diagnostic tools can observe bytes but cannot prove why a key did not arrive.

Derive help/hints from active bindings where possible. Show a few contextual actions; full help or a palette is useful for larger apps, unnecessary for a tiny picker whose complete controls already fit. Don't consume '?' from an editor for global help.

## Scroll ownership and live updates

The wheel goes to the viewport under the pointer; keyboard scroll goes to the focused/explicitly targeted viewport. Test PageUp/Down, Home/End and boundaries in transcript, lists, detail and multiline editors independently. Keep selected objects by stable ID during sort/filter/refresh; if removed, choose a documented neighbor and explain it. Preserve detail scroll unless the object changes.

For live feeds, scrolling away pauses following. Keep the reading anchor while new items arrive; show a new-content count and an explicit return-to-latest control. Reflow on resize must not silently lose the user's place. Large lists/transcripts need bounded rendering/virtualization and a retention or loading policy; don't silently delete history to fix performance.

## Forms and settings

Choose explicit Apply/Save/Cancel or live apply based on persistence semantics. Don't claim a universal convention. Separate draft and saved state for explicit save; validate before committing and keep edits after failure. Validation on blur/submit is a calm default; after an error, revalidation can help. Mark required fields with text, not assumed framework magic. Focus the first invalid field and show an associated message. Reach Save even in a short viewport. Handle conditional fields without marooning focus. Confirm only consequential loss/destructive actions; routine reversible edits need no extra prompt.
