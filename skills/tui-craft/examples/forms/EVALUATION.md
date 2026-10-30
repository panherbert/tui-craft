# Independent forward evaluation: list/detail, settings, small improvement

Date: 2026-10-30. This evaluation used `tui-craft/SKILL.md` and its design, interaction, runtime, framework and verification references, as an implementation agent. Work stayed in an isolated directory. No application repository, installed skill, server, account or external service was modified.

## Requests and observed outcomes

| Request | Artifact | Observed evidence |
|---|---|---|
| Clickable list/detail with filter, scrolling, stable selection and narrow fallback | `list_detail.py` | Headless Textual Pilot drove arrow selection, Refresh click, filter editing, list click, detail PageDown, empty/no-match, 60-column drill-down, Esc focus restoration, resize to 25×8 then 120×30. Selection remained on the same ID after reversed refresh; detail scroll remained unchanged. |
| Settings with explicit Save/Cancel, validation and supplied-path persistence | `settings_form.py` | Pilot edited mid-string, deleted, inserted punctuation/CJK/combining marks, injected multiline Paste, validated required name and numeric range, toggled checkbox, saved by keyboard and click, reloaded JSON, discarded edits, and tested a missing-parent write failure. Save failure retained the draft and allowed retry. Duplicate Save while a controlled thread write was in flight issued one commit without cancelling it. Invalid existing JSON remained a visible recoverable error. |
| A small existing-TUI improvement | `small_before.py`, `small_after.py`, `small-improvement.diff` | The baseline Apply button extended beyond a 40-column viewport. A single CSS width change made it reachable at 40 and 80 columns while preserving click and keyboard Apply behavior. No new framework, gallery, confirmation step or redesign. The fixture docstring also changed to identify before/after. |

Final command: `python -m pytest -q test_examples.py` from this directory, with Python 3.12.13, Textual 8.2.8, pytest 9.1.1, pytest-asyncio 1.4.0. Final result: **8 passed in 11.20 seconds**.

`frames/` contains framework-rendered SVG snapshots at list 100×28 / 60×20 and settings 60×20. These are supplementary static frame artifacts, not emulator screenshots or interaction proof. The tests assert actual state changes and geometry independently.

## Failures found and corrected

1. Resize checks initially failed in both apps because `App.size` still described the previous frame inside `on_resize`. Using the incoming `Resize.size` fixed responsive and too-small transitions. Narrow mode also retains a focused detail pane instead of hiding it.
2. A newly added malformed-file test found that queued Input.Changed events from form population overwrote the load error with “No unsaved edits.” Dirty-status updates now occur only when dirty state changes. The load error remains visible; subsequent Save repairs the supplied file.
3. During implementation review, an exclusive save worker would cancel an in-flight worker when Ctrl+S was pressed again. The save guard now runs in non-exclusive workers, with the first operation marking itself busy before the threaded effect. A controlled duplicate-submit regression test proves one commit and consistent UI completion.

## What the skill changed

- The action contract led to shared semantic actions for buttons and keys, with state assertions rather than label-only tests.
- Stable identities and preserved scroll informed the refresh behavior.
- Existing-stack and small-change routing kept the improvement to one CSS rule.
- Error/draft persistence and duplicate-submit guidance prompted meaningful failure tests.
- Scope and evidence language prevented claiming these local fixtures as integrated production applications.
- No repeated user questions or mandatory concepts were needed.

## Suggested narrow skill refinements

- In the Textual notes, mention reading resize dimensions from the incoming event when handling resize, then testing both directions across a breakpoint. The broader requirement already exists; this is a useful version-specific API detail demonstrated here.
- In the testing guidance, include delayed programmatic widget-change messages when checking initialization and error persistence. The general async/error contract covered the issue, but the concrete example may be useful if space permits.

## Limits: not tested or not claimed

These are **interactive local prototypes**, not verified terminal applications. Their fake catalog does not fetch real remote data. Settings persistence is real only to the explicitly supplied local file. No real terminal emulator, physical pointer, trackpad, clipboard, IME, screen reader, tmux/SSH/Windows, font rendering, SIGTERM, suspend/resume or terminal restoration was observed by this evaluator. The synthetic Paste event does not test bracketed-paste decoding. Unicode content was retained and rendered headlessly; glyph widths in a real emulator remain unobserved. The small fixture only guarantees the tested sizes, not arbitrary subminimum widths. The framework's Ctrl+Q cleanup path exists, but headless tests do not establish terminal mode restoration.
