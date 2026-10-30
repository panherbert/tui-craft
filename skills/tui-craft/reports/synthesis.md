# Synthesis decisions

This package combines decision-making principles, not whole source trees. Revisions and notices are in [attribution](../ATTRIBUTION.md). Review covered both SKILL.md files, relevant visual/interaction/lifecycle/framework guidance, chat/list/form/inline archetypes, source tools and representative starters, examples and tests. The manifest identifies inspected resources; long framework/pattern references were read selectively by relevant sections. It is not a claim that every historical evaluation transcript or every upstream script was read or rerun.

## What the contents do well

**gfargo:** framework-specific references contain concrete lifecycle and version pitfalls rather than only aesthetic advice: Bubble Tea v1/v2 API boundaries, Ratatui extra-mode cleanup, Textual worker/cancellation and testing behavior, Ink input gating and handoff. It gives shell output a first-class contract. Its sample extractor connects 62 marked snippets to 78 harness placeholders; the extractor's 13 tests passed locally. That verifies extraction consistency, not that all four language suites compile here. The sample templates include state and Unicode cursor tests. Its broad release/evaluation machinery is useful for that upstream but excessive for a personal skill.

**diegomarino:** visual-craft describes hierarchy, alignment, composition, surface/border economy and intentional content. Archetypes include chat/agent sessions, list/detail, forms and inline pickers. Mockkit/render/compare/capture tools make static geometry and capability assumptions inspectable. Source tests assert craft heuristics and frame properties; 13 craft tests and 3 key-naming tests passed locally (1 live key-probe test skipped because tmux was unavailable). The Textual Fleet starter actually has reactive list/detail selection and keyboard handling; its frame export depends on a private compositor API. Its use of len-based padding and hand-built rows is not a general Unicode/editor solution. Pixel matching does not demonstrate a clickable integrated app.

## Conflicts resolved

| Source tendency / conflict | tui-craft decision |
|---|---|
| Always run clutter/floor audits, even for other questions; always generate three concepts, state matrices and a gallery | Scale the workflow to the request. Small questions and patches stay small; alternatives and detailed audits are conditional. |
| Fixed 44-token schema, exact chrome budgets, prescribed palette, no dead space | Use project semantic roles and readable hierarchy. Numeric style budgets are heuristics, not correctness. Useful whitespace and user aesthetics win. |
| Single-cell glyph linting versus real Unicode input | Decoration may use conservative glyphs; user data needs cell/grapheme-aware rendering, editing and tests. No ASCII-only content policy. |
| Footer-only hints and universal single-letter shortcuts | Contextual help may live near a prompt; editors own printable keys. Keyboard fallback must survive host/protocol differences. |
| Queue every message while busy; prompt forces scroll; freeze entire screen for approval | Product defines queue/steer/reject policy. Preserve reading anchors; stabilize approval targets without freezing unrelated work. Prevent accidental acceptance from typing. |
| Mouse is optional acceleration versus requested clickable products | All requested pointer controls must work and share semantic actions with keys. Explicitly flag Ink's missing built-in mouse widgets. |
| Framework defaults and conflicting signal advice | Verify exact version/source; don't layer handlers blindly. Separate raw Ctrl+C, external SIGTERM, normal exit and temporary handoff; retain no universal exit-code mandate. |
| Build success judged by matching designed frames | Require state, event, process and terminal evidence appropriate to the claim. Frames and browser controls are never native terminal proof. |
| Framework/star-count/startup rankings | Keep existing stack; use measured app constraints. Date the primary-source notes; omit popularity claims and transferable speed guarantees. |

## Tooling selection

- Retained the *approach* of pinned framework examples, isolated captures, behavioral assertions and deterministic packaging.
- Added a small POSIX stdlib PTY probe with raw capture, ordered byte expectations, resize, signals, status and termios checks; it explicitly cannot validate emulator rendering or physical pointer delivery. Tests cover positive and negative observations, timeout and no-overwrite behavior.
- Added a portable package checker/builder/no-overwrite installer and compact brief/audit/validation templates.
- Did not vendor mockkit's large markup/theme/render/audit pipeline, browser gallery, vision reconstruction, color export collection, tmux capture shell script, key probe or model-comparison/evaluation harness. They are useful specialized upstream tools, but not needed to produce working controls and would enlarge dependencies/maintenance. The capture shell script assumes tmux >=3.2 and uses an approximate per-code-point width model; the key probe groups immediate input bursts and cannot identify why a key is absent. Neither was promoted to proof of all terminal behavior.
- New code is authored for this package; no upstream executable script was retained verbatim. This is deliberate synthesis, not an untested selection of copied scripts.

## Missing capabilities addressed

The combined sources still benefit from an explicit implementation contract: shared click/key actions, modal target isolation, editing/paste ownership, per-conversation drafts, stable run/message identities, stale reply rejection, visible agent communication, actual persistence/error paths, and truthful deliverable levels. These are centralized rather than duplicated across language manuals. Generic guidance contains no project paths, agent names, fixed palette or borrowed application layout.

Primary-source verification confirmed Bubble Tea v2 View/AltScreen/MouseMode changes, Ratatui managed restoration and extra-mode ownership, Ink's resumable handoff and lack of DOM mouse components, and Textual Pilot/workers. Framework notes are not local Go/Rust/TypeScript compile claims. The Python examples are actually executed. Unobserved environments and behavior remain listed in [validation](validation.md).
