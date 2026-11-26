"""SVG charts of per-run recall, with 95% intervals, from results files. No plotting dependency.

One chart per benchmark version: a row per (provider, model), a dot per context level with its
per-bug Wilson interval (the same numbers as the leaderboard). Only complete results are drawn,
so a half-finished run can't look like a result. Versions are never mixed in one chart.
"""
from __future__ import annotations

import json
from collections import defaultdict
from html import escape
from pathlib import Path

from reviewbench.adjudicate import load_verdicts
from reviewbench.heldout import all_slices
from reviewbench.report import noise_reasons, per_run_by_bug
from reviewbench.runner import retryable

LEVELS = ("L0", "L1", "L2")
COLORS = {"L0": "#1f77b4", "L1": "#ff7f0e", "L2": "#2ca02c"}  # colour-blind-safe trio
ROW_H, LEFT, PLOT_W, TOP = 34, 330, 420, 64


def chart_rows(results_dir: Path) -> dict[str, list[tuple[str, dict]]]:
    """version -> [(label, {level: (rate, lo, hi, n)})] for complete public results."""
    by_version: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for p in sorted(results_dir.glob("*.json")):
        if p.name.endswith(".adjudications.json"):
            continue
        doc = json.loads(p.read_text())
        if doc.get("status") != "complete" or any(retryable(r.get("error")) for r in doc["records"]):
            continue
        cells = {lv: per_run_by_bug(doc, lv) for lv in doc["levels"] if lv in LEVELS}
        cells = {lv: c for lv, c in cells.items() if c is not None}
        if cells:
            label = f"{doc['provider']} / {doc['model']}"
            ctrl = all_slices(doc, load_verdicts(p)).get("public/L0/all", {}).get("control_runs_with_confirmed_fp")
            if ctrl and noise_reasons(doc, "L0", ctrl):
                label += " ⚠ noisy"
            by_version[doc["bench_version"]].append((label, cells))
    return by_version


def svg(version: str, rows: list[tuple[str, dict]]) -> str:
    rows = sorted(rows, key=lambda r: -(r[1].get("L0") or (0,))[0])
    h = TOP + ROW_H * len(rows) + 46

    def x(pct: float) -> float:
        return LEFT + PLOT_W * pct / 100

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{LEFT + PLOT_W + 30}" height="{h}" '
           f'font-family="sans-serif" font-size="12">',
           '<rect width="100%" height="100%" fill="white"/>',
           f'<text x="10" y="22" font-size="15" font-weight="bold">ReviewBench v{escape(version)}: '
           f'per-run recall (public cases)</text>',
           '<text x="10" y="42" fill="#555">Dot = per-bug mean catch rate; bar = 95% Wilson interval '
           'with the bug as the unit. Complete runs only. Ordered by L0 for readability, not a ranking: '
           'compare models bug by bug.</text>']
    for pct in (0, 25, 50, 75, 100):
        out.append(f'<line x1="{x(pct)}" y1="{TOP - 6}" x2="{x(pct)}" y2="{h - 40}" stroke="#ddd"/>')
        out.append(f'<text x="{x(pct)}" y="{h - 26}" text-anchor="middle" fill="#555">{pct}%</text>')
    for i, (label, cells) in enumerate(rows):
        y0 = TOP + ROW_H * i + ROW_H / 2
        out.append(f'<text x="{LEFT - 8}" y="{y0 + 4}" text-anchor="end">{escape(label)}</text>')
        for j, lv in enumerate(LEVELS):
            if lv not in cells:
                continue
            rate, lo, hi, n = cells[lv]
            y = y0 + (j - 1) * 8
            c = COLORS[lv]
            out.append(f'<line x1="{x(lo)}" y1="{y}" x2="{x(hi)}" y2="{y}" stroke="{c}" stroke-width="2"/>')
            out.append(f'<circle cx="{x(rate * 100)}" cy="{y}" r="3.5" fill="{c}">'
                       f'<title>{escape(label)} {lv}: {rate:.0%} ({lo:.0f}–{hi:.0f}), {n} bugs</title></circle>')
    lx = LEFT
    for lv in LEVELS:
        out.append(f'<circle cx="{lx}" cy="{h - 10}" r="4" fill="{COLORS[lv]}"/>'
                   f'<text x="{lx + 8}" y="{h - 6}">{lv}</text>')
        lx += 60
    out.append("</svg>")
    return "\n".join(out) + "\n"


def write_charts(results_dir: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for version, rows in sorted(chart_rows(results_dir).items()):
        p = out_dir / f"recall_v{version}.svg"
        p.write_text(svg(version, rows))
        written.append(p)
    return written
