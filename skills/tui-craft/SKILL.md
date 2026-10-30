---
name: tui-craft
description: Design, implement, improve, or audit terminal applications and interactive CLI tools, including chat and agent sessions, dashboards, lists, forms, and inline pickers. Use for terminal layout, controls, streaming, lifecycle, and behavioral verification in existing or new projects. Not for ordinary web or native GUI design; browser mockups can be references but do not verify terminal behavior.
---

# TUI Craft

Produce terminal software that is clear to read and reliable to operate. Preserve the user's product model, stack, and explicit requirements over this skill's defaults. A design-only request does not authorize implementation; a request to implement includes wiring and verification, not just drawing controls.

## Start with scope and evidence

Inspect the existing entry point, dependencies/lockfile, UI event/render loop, tests, and relevant project guidance before proposing changes. Identify the primary user journey, what already works, terminal/host constraints, and the requested deliverable. Prefer the existing framework; recommend a change only for a demonstrated capability gap with migration cost explained.

Classify the surface: full-screen session, inline interactive tool, one-shot CLI, or embedded host panel. Full-screen usually owns the alternate screen; inline tools preserve useful scrollback and keep machine results separate from interactive chrome. See [runtime](references/runtime.md) for shell and terminal contracts.

Use reasonable defaults and state consequential assumptions. Ask only for missing information that changes the outcome; don't repeatedly seek confirmation for reversible work already requested. Do not touch unrelated files or live processes. Keep evaluation fixtures isolated.

## Choose the smallest useful workflow

| Task | Work and stopping point |
|---|---|
| Quick design question | Read the relevant section of [design](references/design.md) or [interaction](references/interaction.md). Recommend one concrete change with its tradeoff. No mandatory mock, report, tools, or exhaustive checklist. |
| Small improvement | Inspect the affected path, preserve surrounding behavior, patch it, and verify the changed journey plus its likely regression. Check a narrow size if layout changed. Do not turn it into a redesign. |
| New design / substantial redesign | Read design and interaction; add [conversation](references/conversation.md) for chat. Define the dominant loop, action/state contract, wide and narrow layouts, semantic styles, and representative real or labeled fixture content. Explore alternatives only when they resolve genuine uncertainty. Use the [brief](assets/templates/brief.md) if useful. |
| Implementation | Read [runtime](references/runtime.md), the matching section of [frameworks](references/frameworks.md), and [verification](references/verification.md). Build one end-to-end working journey, then complete relevant states and controls. Keep business state separate enough to test; wire visible affordances to real actions. |
| Full audit | Read verification and affected domain references. Inspect/run only within authorization. Order findings by user harm, with reproduction, evidence level, severity, and a concrete remedy. Use the [audit template](assets/templates/audit.md); record unknowns instead of guessing. |

Do not load all references for every task. The [examples](examples/README.md) are optional fixtures, not an application architecture or a mandated theme. [Tools](references/tools.md) are optional diagnostics with explicit limitations.

## Requirements versus preferences

**Correctness requirements, where applicable:** working visible controls; keyboard equivalents for pointer actions; visible focus; editable input and paste isolation; correct scroll ownership; stable identities during refresh; responsive layout without lost state; cell-aware Unicode handling; nonblocking work and cancellation; truthful errors and state; cleanup on supported exit paths. If a platform cannot support a required interaction, expose the limitation and a usable alternative—never draw a fake capability.

**Aesthetic defaults, adjustable to the project:** emphasize content and focus over chrome; use whitespace and alignment before nesting borders; prefer a restrained accent plus semantic status roles; use short contextual hints and readable line lengths. Borders, palettes, panel counts, fixed percentages, and particular keybindings are not universal laws. Preserve meaning in monochrome; aesthetic minimalism must not remove useful labels or non-color cues.

## Completion means evidence

Always distinguish these outcomes in the handoff:

- **Static design frame:** appearance only, including PNG, HTML gallery, ANSI art, or a frame renderer.
- **Interactive prototype:** controls mutate state, with simulated data or incomplete integrations clearly named.
- **Verified running application:** requested integrations and journeys exercised in a running terminal application, with environment, checks, and remaining limits recorded. Headless event tests or screenshots alone do not establish this level.

For implementation, verify the requested controls (mouse and keyboard), focus, editing/paste, scrolling, resize, Unicode/long data, error recovery, and clean exit at appropriate layers. Match the extent to the change; use [verification](references/verification.md) to distinguish automation from actual terminal observation. A browser adapter or gallery is never proof of native terminal controls. Report what ran, what passed, what failed, and what remains unobserved; don't promote a prototype because its screenshot looks finished.
