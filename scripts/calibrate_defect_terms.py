"""Measure how a set of defect_terms would change scoring, before adding them to ground truth.

Usage: python scripts/calibrate_defect_terms.py <terms.yaml> [results/*.json ...]

terms.yaml maps a case-id prefix (e.g. "py-0001") to a list of terms. For every finding that
catches a bug by location today, it reports whether the finding also names the defect, and lists
the ones that don't, so a human can check they really are right-line-wrong-reason findings and not
terms that are too narrow. Read-only: nothing in cases/ or results/ is changed.
"""
from __future__ import annotations

import glob
import json
import sys

import yaml

from reviewbench.scoring import COUNTED, bug_matches, norm


def calibrate(terms: dict[str, list[str]], paths: list[str]) -> tuple[int, int, list[tuple]]:
    total = named = 0
    misses = []
    for path in paths:
        doc = json.load(open(path))
        for rec in doc["records"]:
            if rec.get("error"):
                continue
            case_terms = next((v for k, v in terms.items() if rec["case"].startswith(k)), None)
            if not case_terms:
                continue
            for bug in doc["cases"][rec["case"]]["bugs"]:
                location_only = {**bug, "defect_terms": None}
                hits = [f for f in rec["findings"] if f["severity"] in COUNTED and bug_matches(f, location_only)]
                if not hits:
                    continue
                total += 1
                ok = any(any(norm(t) in norm(f["title"] + " " + f["explanation"]) for t in case_terms)
                         for f in hits)
                named += ok
                if not ok:
                    misses.append((doc["model"], rec["case"], rec["level"], hits[0]["title"]))
    return total, named, misses


if __name__ == "__main__":
    terms = yaml.safe_load(open(sys.argv[1]))
    paths = sys.argv[2:] or [p for p in sorted(glob.glob("results/*.json")) if not p.endswith(".adjudications.json")]
    total, named, misses = calibrate(terms, paths)
    print(f"location catches: {total}; also name the defect: {named} ({named / max(total, 1):.1%})")
    for m in misses:
        print("  would no longer count:", *m)
