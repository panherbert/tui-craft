# Runnable evaluation examples

Optional isolated fixtures, not mandatory scaffolding. All application examples use Textual 8.2.8 on Python 3.12; dependencies are pinned in [requirements.txt](requirements.txt). Follow the package [README](../README.md) to create a separate environment. Run the suite from the skill directory with bytecode/cache output disabled.

| Example | Run in an actual terminal | Behavioral checks |
|---|---|---|
| [Clickable chat](chat/README.md) | `python examples/chat/demo.py` | Click/key Send; multiline Unicode paste; edit while async work runs; drafts; visible participant exchanges; follow/cancel/focus/resize/errors |
| [List/detail](forms/README.md) | `python examples/forms/list_detail.py` | Click and arrows; filter; stable ID and scroll after refresh; narrow drill-down |
| [Settings](forms/README.md) | `python examples/forms/settings_form.py /tmp/new-settings-fixture.json` | Validation; editing; Save/Cancel; real supplied-path JSON persistence; failed save and duplicate submits |
| Small improvement | `python examples/forms/small_after.py` | Before fixture's clipped Apply button versus one-rule fix; preserve click/key action |
| Tool tests | `python -B -m unittest discover -s examples/tools -v` | PTY input/resize/signals/cleanup, dirty-exit detection, failures/timeout; packaging/no-overwrite tests |

Use the environment's Python. All participants and catalog entries are synthetic. Settings Save replaces the explicitly supplied file; use a new scratch destination. Read the per-fixture EVALUATION.md files for observations. Headless SVG frames are static evidence only. The package [validation report](../reports/validation.md) records the later PTY checks and their limitations.
