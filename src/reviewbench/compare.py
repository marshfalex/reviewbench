"""Paired, bug-by-bug comparison of reviewers (docs/LESSONS.md: paired tests for paired data).

Every reviewer in a benchmark version sees the same bugs, so the right question is "on the same
bugs, how much more often does A catch them than B?", not "do A's and B's intervals overlap?".
For each pair of complete results at a context level this computes the mean per-bug difference in
catch rate, a descriptive paired bootstrap 95% interval (fixed seed), how many bugs each side
catches more often, and an exact sign-flip permutation p-value, Bonferroni-adjusted for the number
of comparisons. Only the adjusted p-value decides significance: with few bugs and differences all
in one direction, bootstrap intervals are too narrow (found by review, 2026-11-26).
"""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

from reviewbench.runner import retryable
from reviewbench.scoring import COUNTED, bug_matches

RESAMPLES = 10_000
SEED = 20261126


def per_bug_rates(doc: dict, level: str, split: str = "public") -> dict[tuple, float]:
    """(case, bug index) -> fraction of usable runs that caught it."""
    runs: dict[tuple, list[bool]] = {}
    for r in doc["records"]:
        t = doc["cases"].get(r["case"], {})
        if r["level"] != level or r.get("error") or t.get("split", "public") != split:
            continue
        for i, b in enumerate(t.get("bugs") or []):
            caught = any(f["severity"] in COUNTED and bug_matches(f, b) for f in r["findings"])
            runs.setdefault((r["case"], i), []).append(caught)
    return {k: sum(v) / len(v) for k, v in runs.items()}


def _percentile(sorted_vals: list[float], q: float) -> float:
    i = min(len(sorted_vals) - 1, max(0, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[i]


def sign_flip_p(diffs: list[float], resamples: int = RESAMPLES) -> float:
    """Two-sided p-value for mean difference 0 under random sign flips (paired permutation test).
    Exact when there are at most 20 non-zero differences, otherwise Monte Carlo (fixed seed)."""
    nz = [d for d in diffs if d != 0]
    if not nz:
        return 1.0
    obs = abs(sum(nz))
    if len(nz) <= 20:
        hits = 0
        for mask in range(1 << len(nz)):
            t = sum(d if mask >> i & 1 else -d for i, d in enumerate(nz))
            hits += abs(t) >= obs - 1e-12
        return hits / (1 << len(nz))
    rng = random.Random(SEED)
    hits = sum(abs(sum(d if rng.random() < 0.5 else -d for d in nz)) >= obs - 1e-12 for _ in range(resamples))
    return (hits + 1) / (resamples + 1)


def paired(a: dict, b: dict, comparisons: int = 1) -> dict | None:
    """Paired difference a - b over the bugs both have rates for."""
    keys = sorted(set(a) & set(b))
    if len(keys) < 2:
        return None
    diffs = [a[k] - b[k] for k in keys]
    n = len(diffs)
    rng = random.Random(SEED)
    boots = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(RESAMPLES))
    alpha_adj = 0.05 / max(comparisons, 1)
    return {"n": n, "diff": sum(diffs) / n,
            "ci95": (_percentile(boots, 0.025), _percentile(boots, 0.975)),
            "ci_adjusted": (_percentile(boots, alpha_adj / 2), _percentile(boots, 1 - alpha_adj / 2)),
            "a_more": sum(d > 0 for d in diffs), "b_more": sum(d < 0 for d in diffs),
            "p": (p := sign_flip_p(diffs)), "p_adjusted": min(1.0, p * max(comparisons, 1))}


def complete_results(results_dir: Path, version: str) -> list[dict]:
    docs = []
    for p in sorted(results_dir.glob("*.json")):
        if p.name.endswith(".adjudications.json"):
            continue
        doc = json.loads(p.read_text())
        if (doc.get("bench_version") == version and doc.get("status") == "complete"
                and not any(retryable(r.get("error")) for r in doc["records"])):
            docs.append(doc)
    return docs


def compare_table(results_dir: Path, version: str, levels=("L0", "L1", "L2")) -> str:
    docs = complete_results(results_dir, version)
    names = [f"{d['provider']} / {d['model']}" for d in docs]
    pairs = list(itertools.combinations(range(len(docs)), 2))
    m = len(pairs) * len(levels)
    out = [f"## v{version}: paired per-bug comparisons", "",
           f"{len(docs)} complete reviewer(s), {m} comparison(s). Difference = mean over shared bugs of "
           "(A's catch rate - B's), in points, with a descriptive paired-bootstrap 95% CI. Significance "
           "comes only from the exact sign-flip test, Bonferroni-adjusted for all "
           f"{m} comparisons: ✱ marks adjusted p < 0.05. Unstarred differences are not established.", "",
           "| level | A | B | diff (pts) | 95% CI (descriptive) | bugs A>B / B>A | p | adjusted p | n bugs |",
           "|---|---|---|---|---|---|---|---|---|"]
    for lv in levels:
        rates = [per_bug_rates(d, lv) for d in docs]
        for i, j in pairs:
            r = paired(rates[i], rates[j], m)
            if r is None:
                continue
            lo, hi = r["ci95"]
            star = " ✱" if r["p_adjusted"] < 0.05 else ""
            out.append(f"| {lv} | {names[i]} | {names[j]} | {r['diff'] * 100:+.0f}{star} | "
                       f"{lo * 100:.0f} to {hi * 100:.0f} | {r['a_more']} / {r['b_more']} | "
                       f"{r['p']:.3f} | {r['p_adjusted']:.2f} | {r['n']} |")
    out += ["", "✱ = Bonferroni-adjusted sign-flip p < 0.05.", ""]
    return "\n".join(out)
