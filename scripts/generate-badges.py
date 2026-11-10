"""Writes the data behind the README's Headlamp and Strimzi badges.

Both values come from the code, so the badges cannot drift from it:

- Headlamp: version-compat in the newest <version>/artifacthub-pkg.yml.
- Strimzi: the API versions every resource class declares in src/resources/.
  Only versions supported by all of them are shown.

Usage: python3 scripts/generate-badges.py <output-dir>
The badges workflow runs this on every push to main.
"""
import glob
import json
import os
import re
import sys

import yaml


def release_key(path):
    parts = path.split('/')[0].split('-')[0].split('.')
    return tuple(int(p) if p.isdigit() else 0 for p in parts)


def api_version_key(version):
    m = re.fullmatch(r'v(\d+)(?:(alpha|beta)(\d+))?', version)
    if not m:
        return (0, 0, 0)
    stage = {'alpha': 1, 'beta': 2}.get(m.group(2), 3)
    return (int(m.group(1)), stage, int(m.group(3) or 0))


def headlamp_compat():
    files = sorted(glob.glob('*/artifacthub-pkg.yml'), key=release_key)
    if not files:
        sys.exit('no */artifacthub-pkg.yml found')
    with open(files[-1]) as f:
        compat = yaml.safe_load(f)['annotations']['headlamp/plugin/version-compat']
    return compat.replace('>=', '≥ ').replace('<=', '≤ ').strip()


def strimzi_versions():
    supported = None
    for path in sorted(glob.glob('src/resources/*.ts')):
        with open(path) as f:
            m = re.search(r'static apiVersion\s*=\s*(\[[^\]]*\]|[\'"][^\'"]+[\'"])', f.read())
        if not m:
            continue
        found = set(re.findall(r'kafka\.strimzi\.io/(v[0-9a-z]+)', m.group(1)))
        supported = found if supported is None else supported & found
    if not supported:
        sys.exit('no Strimzi API version is supported by every resource class')
    return ' | '.join(sorted(supported, key=api_version_key, reverse=True))


def write(out, name, label, message, color):
    badge = {'schemaVersion': 1, 'label': label, 'message': message, 'color': color}
    with open(os.path.join(out, name), 'w') as f:
        json.dump(badge, f)
        f.write('\n')
    print(f'{name}: {label} {message}')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    write(out, 'headlamp.json', 'Headlamp', headlamp_compat(), 'blue')
    write(out, 'strimzi.json', 'Strimzi API', strimzi_versions(), 'blue')


if __name__ == '__main__':
    main()
