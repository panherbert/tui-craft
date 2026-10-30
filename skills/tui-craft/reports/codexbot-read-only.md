# Independent read-only evaluation: conversation-centered project

Date: 2026-10-30. Project: `/Users/panherbert/Documents/Codex/CodexBot`.

Scope: assess whether `tui-craft` supports the existing product direction. Only source and documentation were read. No project code, tests, imports, commands, application process, server endpoint, model transport, or external service was executed. No project files were edited. This is static evidence, not a runtime audit.

## Result

The skill is a good fit for improving this project's terminal interface while retaining its conversation-centered model. Its instructions preserve the existing stack and product requirements; conversation navigation, transcript and composer remain primary, with agent communication and linked artifacts visible where work occurs. It does not require a dashboard, named agents, palette, framework migration, three concepts, or gallery. Project-specific facts remain in this evaluation, outside reusable skill instructions.

## Current facts observed in files

| Observation | Source | What it establishes |
|---|---|---|
| The terminal mockup is explicitly a conversation UI, with individual/group chats, named participants, human messages, and a selected-chat composer. | `mockups/README.md:3` | Current documented product intent. |
| Mockups are in-memory simulations, with no model calls, real commands, scheduled jobs, or claimed integration into the installed CLI. | `mockups/README.md:5`, `:45`, `:77` | These artifacts must be classified as prototypes, independently of how polished they appear. This says nothing about unrelated production CLI features. |
| The package uses Python >=3.9, no runtime dependencies in pyproject, and a separate CLI entry point; the terminal demo uses curses. | `pyproject.toml:9`, `:10`, `:13`; `mockups/tui_demo.py:787`, `:915` | A Textual migration should not be inferred from this skill's example fixtures. Inspect and retain this architecture unless a demonstrated need warrants a change. |
| A message has stable ID, sender, recipients, artifact association and delivery label; membership is checked. | `mockups/demo_model.py:111` | The current model has useful identity/routing boundaries to preserve. |
| Simulated task progress is expressed as named participant exchanges: research contract, patch, review defect, revision, review acceptance, approval and completion. | `mockups/demo_model.py:186` | Visible communication exists in the model, rather than only independent status indicators. Runtime visibility was not exercised. |
| Native keys and browser/pointer semantic actions share the demo model. The browser adapter and independent HTML mockup are separate surfaces. | `mockups/tui_demo.py:148`; `mockups/README.md:21`, `:25`, `:88` | Testing one surface must not be reported as proof of the other's controls. |
| Project research explicitly requires every agent-to-agent message, including temporary workers, to appear in the owning conversation, independently of execution thread identity. | `research/conversation-model.md:129`, `:139`, `:145` | This is a product requirement, stronger than a generic visual default; the skill's identity/causality guidance supports it. |
| Model and browser-adapter tests exist, including identity stability and viewport/overlay hit-target checks. | `mockups/test_demo_model.py`; `mockups/test_tui_browser.py` | Test intent and code are visible. These tests were not run in this evaluation and have no newly claimed pass status. |

## How the skill applies without changing the product

- `SKILL.md` requires inspecting the existing stack and preserving explicit user requirements. This keeps the conversation architecture and current curses implementation as the starting point.
- `references/conversation.md` requires actual assignments/questions/replies/handoffs/revisions in the appropriate scope, preserves stable identities, and says a spinner or task badge cannot substitute for communication. This matches the project's visibility requirement.
- The same reference separates membership, routing, wakeup and execution. It would not infer an unverified group wake policy from the fact that agents share a conversation.
- `references/interaction.md` calls for shared semantic actions, per-conversation drafts, focus ownership, and independent scroll behavior. These extend the existing model and renderer rather than dictate a replacement layout.
- `references/verification.md` distinguishes model, event, PTY and emulator evidence. It prevents browser screenshots or smoke counts from promoting this simulation to an integrated native terminal application.
- The small-improvement route allows targeted fixes. A complete audit or redesign is not required for each control change.

## Static limitations and risks surfaced, not runtime findings

1. **Declared prototype input limitation:** native composer/form handlers accept printable ASCII and append/delete at the tail (`mockups/tui_demo.py:118`, `:319`); `_edit_value` explicitly rejects non-ASCII/multiline text (`:158`). The skill would call for proper editable, cell-aware inputs when extending the prototype into a broader application. No terminal typing/paste test was performed.
2. **Width accounting risk:** transcript placement and mouse-target widths use Python `len` and `textwrap` (`mockups/tui_demo.py:441`, `:448`). That is compatible with the restricted ASCII input but needs reassessment before Unicode content is supported. No glyph misalignment was observed in a terminal.
3. **Minimum-size contract:** the renderer declares 80×24 and shows a too-small message below it (`mockups/tui_demo.py:552`). The skill's 60-column probe is a suggested evaluation size, not authority to override that project contract. If narrower operation becomes a requirement, design a current-conversation-first fallback.
4. **Too-small exit-hint risk:** the small-size message says `q quits`, while composer/form key routing consumes printable characters before global q (`mockups/tui_demo.py:555`, `:316`, `:319`, `:333`). Source suggests a mismatch if the window shrinks during editing. This is a targeted static risk to reproduce in a terminal, not a newly observed failure.
5. **Future async integration:** the demo advances scripted steps and uses blocking `get_wch` in its event loop (`mockups/tui_demo.py:807`). That does not establish support for streaming events arriving while idle. The skill would require a nonblocking event integration before claiming live agents; it need not alter the current simulated demo for this task.

No fixes were made. Appropriate future acceptance coverage would preserve the current direct/group chat loop while exercising a complete visible assignment → question/reply → handoff → review/revision → return chain, mouse and keyboard equivalents, per-chat drafts, paste, follow pause/resume, resize and real cleanup. Such work remains a future implementation task, not an action taken here.

## Proportional quick-design evaluation

Request: “Should a five-item inline picker have nested borders?”

Response using the skill:

> Usually no. Use a query line, five aligned results, a clear selection marker, and one short controls line. Nested borders consume space without helping this simple choose-and-exit flow. Keep a single boundary only if the surrounding host makes the picker hard to distinguish.

The response used the quick-design route and the layout/hierarchy section only. It did not request confirmation, propose three concepts, generate a mockup/gallery, run tools against the app, or require an exhaustive audit. This record exists because the evaluation requested one; it is not a required artifact for the ordinary quick question.
