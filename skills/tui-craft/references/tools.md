# Optional tools

No tool is required for a quick design answer. These helpers run locally, without network or a browser, and do not install dependencies. Run with Python 3.9+ (`python3 -B` avoids caches in the package). Examples require their separate pinned environment.

## pty_probe.py — process evidence

macOS/Linux, Python stdlib. Runs only the command you supply in a new POSIX PTY/process group. It sends UTF-8 text or control bytes, resizes, sends supported signals, checks ordered output byte fragments, records exit status, and compares selected termios input/output/canonical/echo flags before and after. Output is a new directory containing `result.json` and raw `output.bin`. Existing output directories are refused.

A scenario is JSON:

```json
{"size":[80,24],"steps":[
  {"expect":"READY"},
  {"resize":[60,18]},
  {"expect":"SIZE:60x18"},
  {"send":"q"}
]}
```

Operations: `expect` (ordered bytes since the prior match), `send` (JSON escapes such as `\u0003` for Ctrl+C), `resize` [columns, rows], `wait` 0..10 seconds, `signal` SIGINT/SIGTERM/SIGHUP/SIGCONT. Total `--timeout` is 8 seconds by default, at most 60. Use expectations instead of timing where possible; screen strings can be split by ANSI sequences, so raw substring checks are not semantic screen assertions. Output is capped at 4 MiB.

From the skill directory, after writing the scenario above to a new scratch file:

```sh
python3 -B scripts/pty_probe.py --scenario /tmp/scenario.json --out /tmp/new-probe-result -- python3 -B examples/tools/pty_fixture.py
python3 -B -m unittest discover -s examples/tools -v
```

Exit 0 means the scenario completed, the child's code matched `--expect-exit` (default 0), and sampled flags matched. Exit 1 is a failed observation; 2 is usage/environment failure. A timeout kills only the launched process group; same-group descendants are also cleaned up after completion. Commands that daemonize/escape the group are unsupported. Run isolated applications that are safe to terminate. No shell interpolation is applied to command arguments.

**Limits:** this is not an emulator and does not respond to terminal capability queries. It cannot establish cursor visibility, alternate-screen or mouse-mode restoration merely from termios, or prove physical clicks, clipboard delivery, IME, accessibility or appearance. Check emitted mode teardown plus actual terminal behavior separately. It does not emulate a shell's foreground job-control machinery; use a real shell for suspend/resume. Do not replay raw captures from unknown programs into your terminal. The fixture is only a tool test, not a TUI starter.

## package_skill.py — maintenance

Cross-platform Python stdlib. `check` checks this package's required structure, local Markdown file links and Python syntax; it does not validate every Markdown anchor, YAML feature or behavior. Also use the environment's skill-creator validator when available. `build` produces a deterministic ZIP rooted at `tui-craft/`, refusing an existing archive. `install` copies into a new `tui-craft` directory, refusing any existing destination; it does not overwrite other skills or edit configuration.

```sh
python3 -B scripts/package_skill.py check
python3 -B scripts/package_skill.py build --out /path/out/tui-craft.zip
python3 -B scripts/package_skill.py install --dest /path/to/user/skills
```

Default install root: `$CODEX_HOME/skills`, or `~/.codex/skills` if unset. The script rejects symlinks and common cache/build trees in the package. A copied folder is not proof of runtime discovery: verify with the host skill list/reload mechanism, or explicitly report discovery unconfirmed. Read [README](../README.md) for invocation and examples.
