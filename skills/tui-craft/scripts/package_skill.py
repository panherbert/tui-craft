#!/usr/bin/env python3
"""Check, package, or install this skill. Python >=3.9, stdlib only; never overwrites.

check: structural/local-link/Python-syntax checks (not behavioral correctness).
build --out FILE.zip: deterministic archive rooted at tui-craft/.
install [--dest SKILLS_DIRECTORY]: new tui-craft child under user skills directory.
"""
import argparse
import ast
import os
from pathlib import Path
import re
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('SKILL.md', 'README.md', 'LICENSE', 'ATTRIBUTION.md', 'agents/openai.yaml',
            'references/design.md', 'references/interaction.md', 'references/conversation.md',
            'references/runtime.md', 'references/frameworks.md', 'references/verification.md',
            'references/tools.md', 'reports/synthesis.md', 'reports/validation.md')


def check(root):
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f'missing {name}')
    skill = (root / 'SKILL.md').read_text() if (root / 'SKILL.md').exists() else ''
    if not skill.startswith('---\n') or '\nname: tui-craft\n' not in skill or '\ndescription: ' not in skill:
        errors.append('invalid skill identity/frontmatter')
    paths = []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if path.is_symlink():
            errors.append(f'symlink not allowed: {rel}')
            continue
        if any(part in ('.venv', '__pycache__', '.pytest_cache', 'node_modules', '.git') for part in rel.parts):
            errors.append(f'build/cache directory not allowed: {rel}')
            continue
        if not path.is_file():
            continue
        paths.append(path)
        if path.suffix == '.py':
            try:
                ast.parse(path.read_text(), filename=str(rel))
            except SyntaxError as exc:
                errors.append(f'Python syntax: {rel}: {exc}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
                if '://' in target or target.startswith(('#', 'mailto:')):
                    continue
                target = target.split('#')[0]
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                    errors.append(f'broken or external local link: {rel}: {target}')
    if errors:
        raise ValueError('\n'.join(errors))
    return paths


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['check','build','install'])
    p.add_argument('--out', type=Path)
    p.add_argument('--dest', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex'))) / 'skills')
    a = p.parse_args()
    try:
        paths = check(ROOT)
        if a.action == 'build':
            if a.out is None:
                p.error('build requires --out FILE.zip')
            if a.out.resolve().is_relative_to(ROOT):
                p.error('archive must be outside the skill directory')
            a.out.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(a.out, 'x', compression=zipfile.ZIP_DEFLATED) as z:
                for path in paths:
                    info = zipfile.ZipInfo('tui-craft/' + path.relative_to(ROOT).as_posix(), (2026,1,1,0,0,0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    z.writestr(info, path.read_bytes())
            print(a.out)
        elif a.action == 'install':
            dest = a.dest.expanduser() / 'tui-craft'
            # copytree's no-existing-destination rule is intentional, including symlinks.
            shutil.copytree(ROOT, dest)
            print(dest)
        else:
            print(f'OK: {len(paths)} files; local links, required structure, and Python syntax')
        return 0
    except (OSError, ValueError) as exc:
        p.exit(1, f'package_skill: {exc}\n')

if __name__ == '__main__':
    sys.exit(main())
