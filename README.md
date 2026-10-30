# tui-craft

A reusable agent skill for polished, working terminal applications: conversation and agent sessions, dashboards, lists, forms, and inline tools.

It combines visual design judgment with implementation guidance for Python, Go, Rust, and TypeScript, preserving the project's existing stack and product model. Workflows scale from quick advice and small fixes to implementation and full audits. Static frames, interactive prototypes, and verified applications are explicitly distinguished.

## Install

Clone this repository and run the no-overwrite installer:

```sh
git clone https://github.com/panherbert/tui-craft.git
cd tui-craft
python3 -B skills/tui-craft/scripts/package_skill.py check
python3 -B skills/tui-craft/scripts/package_skill.py install
```

The default destination is `$CODEX_HOME/skills/tui-craft`, or `~/.codex/skills/tui-craft` when unset. Existing skills are never overwritten. Reload your agent's skill catalog and invoke `$tui-craft`.

Alternatively, download the installable ZIP and checksum from [Releases](https://github.com/panherbert/tui-craft/releases).

## Contents

- [Skill entry point](skills/tui-craft/SKILL.md)
- [Usage, dependencies, and maintenance](skills/tui-craft/README.md)
- [Runnable examples](skills/tui-craft/examples/README.md)
- [Synthesis decisions](skills/tui-craft/reports/synthesis.md)
- [Validation results and limitations](skills/tui-craft/reports/validation.md)
- [Attribution and source revisions](skills/tui-craft/ATTRIBUTION.md)

Version 1.0.0 was validated with 27 tests and four native PTY scenarios. Physical terminal/emulator and cross-platform checks remain explicitly unverified. The included application examples are isolated prototypes with simulated data; they do not imply production integration.

## License

MIT. See [LICENSE](LICENSE) and the [upstream notices](skills/tui-craft/licenses/). This is an independently named synthesis of gfargo/tui-design-skill and diegomarino/tui-design; both original skills can coexist with it.
