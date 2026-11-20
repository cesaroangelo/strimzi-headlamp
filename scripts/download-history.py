"""Records release downloads and draws the README's downloads chart.

GitHub only reports the current total of each release asset, not its
history. This script adds today's total to downloads-history.json and
redraws downloads.svg from it, so the chart starts on the first run.

Usage: python3 scripts/download-history.py <dir> [total]
<dir> holds the history file; the badges workflow passes the badges branch.
Without [total], the script reads it from the GitHub API, using
GITHUB_REPOSITORY and GITHUB_TOKEN. Pass a number to preview the chart.
"""
import datetime
import html
import json
import math
import os
import sys
import urllib.request

HISTORY = 'downloads-history.json'
CHART = 'downloads.svg'

WIDTH, HEIGHT = 720, 260
LEFT, RIGHT, TOP, BOTTOM = 56, 24, 40, 40


def fetch_releases():
    repo = os.environ['GITHUB_REPOSITORY']
    headers = {'Accept': 'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    releases, page = [], 1
    while True:
        url = f'https://api.github.com/repos/{repo}/releases?per_page=100&page={page}'
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as r:
            batch = json.load(r)
        releases += batch
        if len(batch) < 100:
            return releases
        page += 1


def summarise(releases):
    total = sum(a['download_count'] for r in releases for a in r['assets'])
    marks = [
        {'version': r['tag_name'], 'date': r['published_at'][:10]}
        for r in releases
        if r.get('published_at') and not r.get('draft') and not r.get('prerelease')
    ]
    return total, sorted(marks, key=lambda m: m['date'])


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {'points': [], 'releases': []}


def record(history, day, total):
    """Sets today's total; a second run on the same day replaces it."""
    points = [p for p in history['points'] if p['date'] != day]
    points.append({'date': day, 'total': total})
    history['points'] = sorted(points, key=lambda p: p['date'])
    return history


def nice_max(value):
    """Smallest round axis top above value, split into four round steps."""
    tick = max(value, 1) / 4
    scale = 10 ** max(math.floor(math.log10(tick)), 0)
    for m in (1, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if tick <= m * scale and (m * scale) % 1 == 0:
            return int(4 * m * scale)
    return int(40 * scale)


def label(day):
    d = datetime.date.fromisoformat(day)
    return f'{d:%b} {d.day}, {d.year}'


def render(history):
    points = history['points']
    first = datetime.date.fromisoformat(points[0]['date'])
    last = datetime.date.fromisoformat(points[-1]['date'])
    span = max((last - first).days, 1)
    top = nice_max(max(p['total'] for p in points))
    plot_w = WIDTH - LEFT - RIGHT
    plot_h = HEIGHT - TOP - BOTTOM

    def x(day):
        d = (datetime.date.fromisoformat(day) - first).days
        return LEFT + (plot_w / 2 if len(points) == 1 else plot_w * d / span)

    def y(value):
        return TOP + plot_h - plot_h * value / top

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" '
        f'aria-label="Release downloads: {points[-1]["total"]} on {points[-1]["date"]}">',
        '<style>',
        'svg{--fg:#1f2328;--muted:#59636e;--grid:#d1d9e0;--line:#0969da;--bg:#ffffff}',
        '@media (prefers-color-scheme:dark){svg{--fg:#f0f6fc;--muted:#9198a1;'
        '--grid:#3d444d;--line:#4493f8;--bg:#0d1117}}',
        'text{font:12px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:var(--muted)}',
        '.title{font-size:14px;font-weight:600;fill:var(--fg)}',
        '.value{font-weight:600;fill:var(--fg)}',
        '.grid{stroke:var(--grid);stroke-width:1}',
        '.mark{stroke:var(--grid);stroke-width:1;stroke-dasharray:3 3}',
        '.line{fill:none;stroke:var(--line);stroke-width:2;stroke-linejoin:round}',
        '.area{fill:var(--line);opacity:.12}',
        '.dot{fill:var(--line);stroke:var(--bg);stroke-width:2}',
        '.bg{fill:var(--bg)}',
        '</style>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="6" class="bg"/>',
        f'<text class="title" x="{LEFT}" y="22">Release downloads</text>',
        f'<text x="{WIDTH - RIGHT}" y="22" text-anchor="end">'
        f'<tspan class="value">{points[-1]["total"]}</tspan> total</text>',
    ]

    for i in range(5):
        value = top * i // 4
        gy = y(value)
        out.append(f'<line class="grid" x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{gy:.1f}" y2="{gy:.1f}"/>')
        out.append(f'<text x="{LEFT - 8}" y="{gy + 4:.1f}" text-anchor="end">{value}</text>')

    for mark in history.get('releases', []):
        if points[0]['date'] <= mark['date'] <= points[-1]['date'] and len(points) > 1:
            mx = x(mark['date'])
            out.append(f'<line class="mark" x1="{mx:.1f}" x2="{mx:.1f}" y1="{TOP}" y2="{TOP + plot_h}"/>')
            out.append(f'<text x="{mx + 4:.1f}" y="{TOP + 12}">{html.escape(mark["version"])}</text>')

    coords = [(x(p['date']), y(p['total'])) for p in points]
    if len(coords) > 1:
        path = ' '.join(f'{cx:.1f},{cy:.1f}' for cx, cy in coords)
        base = TOP + plot_h
        out.append(
            f'<polygon class="area" points="{coords[0][0]:.1f},{base} {path} {coords[-1][0]:.1f},{base}"/>'
        )
        out.append(f'<polyline class="line" points="{path}"/>')
    cx, cy = coords[-1]
    out.append(f'<circle class="dot" cx="{cx:.1f}" cy="{cy:.1f}" r="4"/>')

    axis_y = HEIGHT - 14
    if len(points) == 1:
        out.append(
            f'<text x="{LEFT + plot_w / 2:.1f}" y="{axis_y}" text-anchor="middle">'
            f'History starts {label(points[0]["date"])}</text>'
        )
    else:
        out.append(f'<text x="{LEFT}" y="{axis_y}">{label(points[0]["date"])}</text>')
        out.append(
            f'<text x="{WIDTH - RIGHT}" y="{axis_y}" text-anchor="end">{label(points[-1]["date"])}</text>'
        )
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    history = load(os.path.join(out, HISTORY))
    if len(sys.argv) == 3:
        total = int(sys.argv[2])
    else:
        total, history['releases'] = summarise(fetch_releases())
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record(history, today, total)

    with open(os.path.join(out, HISTORY), 'w') as f:
        json.dump(history, f, indent=1)
        f.write('\n')
    with open(os.path.join(out, CHART), 'w') as f:
        f.write(render(history))
    print(f'{HISTORY}: {total} downloads on {today} ({len(history["points"])} days)')


if __name__ == '__main__':
    main()
