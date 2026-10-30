# Isolated TUI fixtures

These examples use synthetic content and Textual 8.2.8. They demonstrate behaviors and regression tests rather than a production application architecture. Read `EVALUATION.md` for the exact observed evidence and limitations.

Dependencies in an isolated Python 3.12 environment:

```sh
python -m pip install textual==8.2.8 pytest==9.1.1 pytest-asyncio==1.4.0
python -m pytest -q test_examples.py
python list_detail.py
python settings_form.py /tmp/my-tui-fixture-settings.json
python small_after.py
```

Use a new settings destination; Save replaces that file. Its parent directory must already exist. The fixture never chooses a personal configuration file or starts external services. Ctrl+Q exits; in settings, this explicitly discards uncommitted edits. Save/Cancel and refresh/list/detail buttons have keyboard equivalents. Escape returns from list detail or discards settings edits. F5 refreshes the synthetic list by reversing its order, so stable-ID selection is visible.

`small_before.py` intentionally contains the narrow-layout defect. `small_after.py` changes only its width rule plus the explanatory docstring. `small-improvement.diff` records the patch. `frames/` are headless SVG snapshots, not terminal verification.
