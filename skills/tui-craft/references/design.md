# Layout and visual craft

## Choose structure from the job

| Job | Useful shape | Narrow behavior |
|---|---|---|
| Read and reply, coordinate agents | Conversation list + transcript + composer | Current conversation wins; navigation/details open on demand |
| Select and inspect an object | List/detail | Enter opens detail; Back restores selection and scroll |
| Monitor several signals | Dashboard + actionable drill-down | Highest-priority summary and one selected section |
| Edit settings | Grouped fields or category list/detail | Labels above fields; scroll form, keep actions reachable |
| Choose and exit | Inline query + bounded results | Hide metadata/preview before primary labels |
| Browse hierarchy | Tree, columns, or drill-down | Keep breadcrumb and current level |

Use multiple panes only when simultaneous context helps. Do not replace an established conversation or document workflow with a dashboard of counters. A hybrid is fine when secondary views support the primary loop.

## Hierarchy and restraint

Give the main task most of the usable space. Use a clear primary/focus layer, normal content, secondary metadata, and quiet chrome. Keep important secondary text legible; terminal dim attributes and user palettes can erase it. Start with one accent and named roles such as text, muted, surface, focus, selection, success, warning, error. Map these into the project's theme, not a compulsory token inventory. Separate selection from focus: a selected object can remain visible while another pane owns input.

Align columns and related labels; use consistent one- or two-cell gutters and short group gaps as starting points. Whitespace may support reading and growth—do not fill every empty cell just to satisfy a density score. Prefer a divider, title, spacing, or surface before adding another box. Independently focused panes may benefit from borders. Review nesting, repeated labels, and markers that appear on every row; remove specific waste, not meaningful redundancy such as error text plus color.

For a larger design, do a brief craft pass: Does attention land on the task? Is the focused control obvious without color? Are labels, values, units, and metadata consistently aligned? Does the narrow view retain the main action? Does the interface look deliberate rather than arbitrarily decorated? A distinctive treatment should explain the content, not distract from it. No numeric craft score or three-concept gallery is required.

## Sizes and content

Derive breakpoints from minimum useful content widths, borders, gutters, and required controls. Start evaluation around 120×30, 80×24, and 60×20 unless deployment gives better sizes; these are probes, not standards. Check short as well as narrow windows. Below the honest minimum, show what size is needed and keep resize/exit active. Preserve drafts, selected IDs, and scroll anchors across all breakpoints; don't just hide a focused pane without relocating focus.

Bound one-line table rows; expose truncated content in detail/copy views. Wrap prose and messages at word/cell boundaries, with a policy for long unbroken paths/URLs. Use measured cell width and grapheme-safe slicing, never string length as columns. Include CJK, combining marks, emoji/ZWJ, tabs, long names, and translated labels. Decorative glyphs can have an ASCII fallback; user content must not be silently stripped to ASCII.

## States as behavior

Map only relevant states to an action and recovery: initial/empty, no search matches, loading, streaming/partial, success, validation error, recoverable failure, disconnected/stale, cancelled, disabled, too small. An empty state explains why and offers the next action. Loading must leave navigation/cancel responsive. A stale view labels its age while preserving useful last data. Errors retain user input and say what can be retried. Disabled actions explain why and cannot activate. Busy buttons guard duplicate submissions. Verify critical intersections (e.g. error while narrow), not a compulsory Cartesian product of every state and size.

Use labeled synthetic fixtures when real content is unavailable. A polished drawing is a design frame until its controls are implemented; the data's origin belongs in notes, not distracting UI decorations.
