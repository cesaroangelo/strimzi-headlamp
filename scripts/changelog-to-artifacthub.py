"""Fills the `changes` list of an Artifact Hub metadata file from CHANGELOG.md.

The release workflow copies the previous release's artifacthub-pkg.yml, so
without this the new version's page would list the previous version's
changes. Each bullet in the version's CHANGELOG section becomes one change,
using its first sentence; the full text stays in the CHANGELOG.

Usage:
  python3 scripts/changelog-to-artifacthub.py <version> [<artifacthub-pkg.yml>]

With only a version it checks that CHANGELOG.md has entries for it, so the
release workflow can stop before publishing anything.
"""
import json
import re
import sys

KINDS = {
    'added': 'added',
    'changed': 'changed',
    'deprecated': 'deprecated',
    'removed': 'removed',
    'fixed': 'fixed',
    'security': 'security',
}


def section(version):
    with open('CHANGELOG.md') as f:
        text = f.read()
    m = re.search(rf'^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)', text, re.M | re.S)
    if not m:
        sys.exit(f'CHANGELOG.md has no section for {version}')
    return m.group(1)


def changes(version):
    kind, items, current = 'changed', [], None
    for line in section(version).splitlines():
        heading = re.match(r'^###\s+(\w+)', line)
        if heading:
            kind = KINDS.get(heading.group(1).lower(), 'changed')
            current = None
        elif line.startswith('- '):
            current = [kind, line[2:].strip()]
            items.append(current)
        elif current and line.startswith('  ') and line.strip():
            current[1] += ' ' + line.strip()
        else:
            current = None
    if not items:
        sys.exit(f'CHANGELOG.md section for {version} has no entries')
    out = []
    for kind, text in items:
        text = re.sub(r'\s+', ' ', text.replace('`', '')).strip()
        first = re.split(r'(?<=[^.\s])\.\s', text, maxsplit=1)[0].rstrip('.')
        out.append((kind, first))
    return out


def render(items):
    lines = ['changes:']
    for kind, text in items:
        lines.append(f'  - kind: {kind}')
        lines.append(f'    description: {json.dumps(text, ensure_ascii=False)}')
    return '\n'.join(lines) + '\n'


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    items = changes(sys.argv[1])
    if len(sys.argv) == 2:
        print(f'CHANGELOG.md has {len(items)} entries for {sys.argv[1]}')
        return
    path = sys.argv[2]
    with open(path) as f:
        text = f.read()
    block = render(items)
    if re.search(r'^changes:\n', text, re.M):
        text = re.sub(r'^changes:\n(?:[ \t]+.*\n)*', block, text, count=1, flags=re.M)
    else:
        text = re.sub(r'^annotations:', block + 'annotations:', text, count=1, flags=re.M)
    with open(path, 'w') as f:
        f.write(text)
    print(f'{path}: {len(items)} changes from CHANGELOG.md')


if __name__ == '__main__':
    main()
