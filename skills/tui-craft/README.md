# tui-craft

A reusable skill for polished **working** terminal applications. Version 1.0.0. It supports full-screen TUIs, conversation/agent sessions, dashboards, lists, forms, inline tools, implementation and review. It preserves existing product and framework decisions, scales its workflow to the task, and separates appearance from verified behavior.

## Use

Invoke `$tui-craft` in a project, for example:

- “Use $tui-craft to improve this list's narrow layout without changing its navigation.”
- “Use $tui-craft to build a clickable conversation TUI with streaming replies.”
- “Use $tui-craft to audit focus, paste, mouse and exit behavior; keep the project read-only.”
- “Use $tui-craft to design an inline picker that keeps stdout machine-readable.”

Start at [SKILL.md](SKILL.md); it routes to focused references instead of loading the whole package. Design advice and templates need no dependencies. Python, Go, Rust and TypeScript implementation guidance is in [frameworks](references/frameworks.md). No mandatory galleries, three-concept exercises, repeated approvals, or framework migrations.

## Install without replacing another skill

Extract the ZIP into a scratch location; its root is `tui-craft/`. From that directory:

```sh
python3 -B scripts/package_skill.py check
python3 -B scripts/package_skill.py install
```

The installer targets `$CODEX_HOME/skills/tui-craft`, or `~/.codex/skills/tui-craft` when unset, and fails if it already exists. Use `--dest /another/user/skills` for another skill root. Existing skills with the upstream name `tui-design` coexist. Do not overwrite an existing `tui-craft` to upgrade accidentally; compare and deliberately manage the version first.

Reload the host skill catalog or start a fresh session, then invoke `$tui-craft`. For a Codex app-server host, `skills/list` with `forceReload: true` can check actual discovery ([official documentation](https://learn.chatgpt.com/docs/app-server#skills)). Installation and this delivery's discovery result are recorded separately in [validation](reports/validation.md).

## Optional tools and examples

Python **3.9+**, stdlib only: package checker/builder/installer. The PTY probe additionally needs **macOS or Linux** and a command safe to terminate. Neither depends on tmux, a browser, Node or external services. See [tool usage and limits](references/tools.md).

The [isolated examples](examples/README.md) need Python **3.12** plus pinned Textual/test dependencies, installed in a separate environment:

```sh
python3.12 -m venv /tmp/tui-craft-venv
/tmp/tui-craft-venv/bin/python -m pip install -r examples/requirements.txt
PYTHONDONTWRITEBYTECODE=1 /tmp/tui-craft-venv/bin/python -m pytest -q -p no:cacheprovider examples
```

Use a fresh environment path. These tests write only temporary fixture files. Settings demo saves only to an explicit path you supply. Examples are prototypes with synthetic content; they are not drop-in production starters or a required layout/theme.

## Maintain and package

Edit this skill independently of either upstream. Keep exact framework claims dated and recheck primary sources before updating them. Re-run changed behavior and tool tests, the package check, and the host skill-creator validator if available; record failures and unobserved checks honestly. Build to a fresh archive path:

```sh
python3 -B scripts/package_skill.py build --out /path/out/tui-craft-1.0.0.zip
```

The archive has deterministic file order/timestamps and includes no dependency environments or caches. [Synthesis](reports/synthesis.md) explains what was retained, rewritten or omitted. [Validation](reports/validation.md) separates executed results from limits. [Attribution](ATTRIBUTION.md) records source revisions and MIT notices; [LICENSE](LICENSE) covers this package's original work. Project-specific evaluation notes stay under `reports/`, outside the reusable instructions.
