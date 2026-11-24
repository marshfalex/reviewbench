"""Markdown reports: one per results file, and the leaderboard over all of them."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from reviewbench.adjudicate import load_verdicts
from reviewbench.heldout import all_slices, leaks
from reviewbench.runner import retryable
from reviewbench.scoring import COUNTED, bug_matches, per_case_table, score
from reviewbench.stats import wilson_interval

# SPEC §10 noise flag: control FPR point estimate above this, or more counted findings per review.
NOISE_FPR = 0.20
NOISE_FINDINGS_PER_REVIEW = 3.0


# RISKS §1: a precision rate is only shown once this share of the findings that need a human
# verdict (everything that isn't a planted-bug hit or a known issue) actually has one.
MIN_JUDGED_SHARE = 0.80


def judged_counts(doc: dict, verdicts: dict, level: str, split: str = "public",
                  controls_only: bool = False) -> tuple[int, int]:
    """(judged, unjudged) counted findings that needed a verdict, for one level and split."""
    labels = score(doc, verdicts)["labels"]
    judged = unjudged = 0
    for r in doc["records"]:
        t = doc["cases"].get(r["case"], {})
        if r["level"] != level or r.get("error") or t.get("split", "public") != split:
            continue
        if controls_only and t.get("bugs"):
            continue
        for f in r["findings"]:
            lab = labels.get(f["id"])
            judged += lab in ("valid", "invalid")
            unjudged += lab == "unadjudicated"
    return judged, unjudged


def precision_cell(prec: dict, judged: int, unjudged: int) -> str:
    need = judged + unjudged
    if need and judged / need < MIN_JUDGED_SHARE:
        return f"not measured ({unjudged} of {need} unjudged)"
    return _r(prec)


def noise_reasons(doc: dict, level: str, ctrl: dict, ctrl_unjudged: int = 0) -> list[str]:
    """Why a reviewer is flagged noisy at this level (empty = not flagged). With unjudged
    control findings the confirmed FPR is only a lower bound, so it is shown as one."""
    reasons = []
    if ctrl["n"] and ctrl["hits"] / ctrl["n"] > NOISE_FPR:
        bound = f" (≥; {ctrl_unjudged} control findings unjudged)" if ctrl_unjudged else ""
        reasons.append(f"control FPR {ctrl['hits'] / ctrl['n']:.0%}{bound}")
    runs = [r for r in doc["records"] if r["level"] == level and not r.get("error")
            and doc["cases"].get(r["case"], {}).get("split", "public") == "public"]
    if runs:
        per = sum(1 for r in runs for f in r["findings"] if f["severity"] in COUNTED) / len(runs)
        if per > NOISE_FINDINGS_PER_REVIEW:
            reasons.append(f"{per:.1f} findings/review")
    return reasons


def per_run_by_bug(doc: dict, level: str, split: str = "public", difficulty: str | None = None):
    """Per-run recall with the bug, not the run, as the unit of the interval (RISKS §2).

    The k runs of one bug are highly correlated (at temperature 0 they are often byte-identical),
    so a Wilson interval over bug x run pretends to have k times more data than it does. Here each
    bug contributes its catch fraction over its runs, and the interval uses n = number of bugs.
    Returns (rate, lo, hi, n_bugs) or None."""
    fracs = {}
    for r in doc["records"]:
        t = doc["cases"].get(r["case"], {})
        if (r["level"] != level or r.get("error") or t.get("split", "public") != split
                or (difficulty and t.get("difficulty") != difficulty)):
            continue
        for i, b in enumerate(t.get("bugs") or []):
            caught = any(f["severity"] in COUNTED and bug_matches(f, b) for f in r["findings"])
            fracs.setdefault((r["case"], i), []).append(caught)
    if not fracs:
        return None
    hits = sum(sum(v) / len(v) for v in fracs.values())
    n = len(fracs)
    lo, hi = wilson_interval(hits, n)
    return hits / n, lo, hi, n


def _pr(d: dict, by_bug) -> str:
    """Per-run recall cell: run counts, then the interval computed per bug."""
    if not d["n"] or by_bug is None:
        return _r(d)
    rate, lo, hi, n = by_bug
    return f"{d['hits']}/{d['n']} runs ({rate:.0%}; 95% CI {lo:.0f}–{hi:.0f} over {n} bugs)"


def _r(d: dict) -> str:
    if not d["n"]:
        return "n/a"
    lo, hi = d["ci95"]
    return f"{d['hits']}/{d['n']} ({d['rate']:.0%}, {lo:.0f}–{hi:.0f})"


def run_report(results: dict, verdicts: dict) -> str:
    s = all_slices(results, verdicts)
    out = [f"# {results['provider']} / {results['model']} — ReviewBench v{results['bench_version']}", "",
           f"Created {results['created']}, k={results['k']} runs per case and level, status "
           f"`{results['status']}`. Rates are hits/n (%, Wilson 95% CI).", ""]
    for split in ("public", "heldout"):
        keys = [k for k in s if k.startswith(split + "/")]
        if not keys:
            continue
        held = results.get("heldout") or {}
        note = [f"Aggregates only over {held['cases']} private case(s); per-case details are never "
                "published.", ""] if split == "heldout" else []
        out += [f"## {split}", "", *note,
                "| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | "
                "precision (adjudicated) | control runs w/ FP | unadjudicated | errors |",
                "|---|---|---|---|---|---|---|---|---|"]
        for k in keys:
            _, level, diff = k.split("/")
            m = s[k]
            j, u = judged_counts(results, verdicts, level, split) if split == "public" \
                else (0, m["unadjudicated_findings"])
            prec = precision_cell(m["precision_adjudicated"], j, u)
            by_bug = per_run_by_bug(results, level, split, None if diff == "all" else diff) \
                if split == "public" else None
            out.append(f"| {level} | {diff} | {_r(m['any_of_k'])} | {_r(m['all_of_k'])} | "
                       f"{_pr(m['per_run_recall'], by_bug)} | {prec} | "
                       f"{_r(m['control_runs_with_confirmed_fp'])} | {m['unadjudicated_findings']} | "
                       f"{m['errored_runs']} |")
        out.append("")
    out += ["## Per case", "", "| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |",
            "|---|---|---|---|---|---|---|---|---|"]
    for r in per_case_table(results, verdicts):
        caught = "control" if r["control"] else f"{r['caught']}/{r['runs']}"
        out.append(f"| {r['case']} | {r['level']} | {caught} | {r['hit']} | {r['known']} | {r['valid']} | "
                   f"{r['invalid']} | {r['unadjudicated']} | {r['errors']} |")
    return "\n".join(out) + "\n"


def leaderboard(results_dir: Path) -> str:
    by_version: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for p in sorted(results_dir.glob("*.json")):
        if p.name.endswith(".adjudications.json"):
            continue
        doc = json.loads(p.read_text())
        problems = leaks(doc)
        if problems:
            raise ValueError(f"{p.name} would reveal held-out cases: {'; '.join(problems)}")
        by_version[doc["bench_version"]].append((p, doc))
    out = ["# ReviewBench leaderboard", "",
           "Generated by `reviewbench leaderboard`. Every rate is hits/n (%, Wilson 95% CI). "
           "Results from different benchmark versions are never compared; each version has its own table. "
           "Precision counts only adjudicated findings; the unadjudicated column says how many are pending.", ""]
    if not by_version:
        out.append("_No results yet._")
    for version in sorted(by_version, reverse=True):
        for split in ("public", "heldout"):
            rows = []
            for p, doc in by_version[version]:
                s = all_slices(doc, load_verdicts(p))
                for level in doc["levels"]:
                    a, h = s.get(f"{split}/{level}/all"), s.get(f"{split}/{level}/hard")
                    if not a:
                        continue
                    hard = (_r(h["any_of_k"]) + " / " + _r(h["all_of_k"])) if h else "n/a"
                    # Status alone isn't enough: files written before retryable errors were tracked
                    # say "complete" while most reviews failed. Name the gap so 6/6 can't pass as done.
                    failed = sum(1 for r in doc["records"] if r["level"] == level and retryable(r.get("error")))
                    status = "" if doc["status"] == "complete" and not failed else " (partial)"
                    if failed:
                        status += f" ({failed} reviews failed, to retry)"
                    verdicts = load_verdicts(p)
                    j, u = judged_counts(doc, verdicts, level, split) if split == "public" else (0, 1)
                    prec = precision_cell(a["precision_adjudicated"], j, u)
                    _, cu = judged_counts(doc, verdicts, level, split, controls_only=True) \
                        if split == "public" else (0, 0)
                    noisy = noise_reasons(doc, level, a["control_runs_with_confirmed_fp"], cu) \
                        if split == "public" else []
                    flag = f" ⚠ noisy: {', '.join(noisy)}" if noisy else ""
                    pr = a["per_run_recall"]
                    by_bug = per_run_by_bug(doc, level, split) if split == "public" else None
                    # Unfinished results go last: 12/12 on a sliver of the cases must not outrank a full run.
                    sort_key = (level, bool(status), -(pr["rate"] if pr["n"] else -1), doc["provider"], doc["model"])
                    rows.append((sort_key,
                                 f"| {doc['provider']} / `{doc['model']}`{status}{flag} | {level} | {doc['k']} | "
                                 f"**{_pr(pr, by_bug)}** | {_r(a['any_of_k'])} | {_r(a['all_of_k'])} | {hard} | "
                                 f"{prec} | {_r(a['control_runs_with_confirmed_fp'])} | "
                                 f"{a['unadjudicated_findings']} | [{p.stem}]({p.name}) |"))
            if not rows:
                continue
            out += [f"## v{version} — {split} cases", "",
                    f"Precision is shown only once {MIN_JUDGED_SHARE:.0%} of the findings needing a human verdict "
                    "have one; control runs w/ FP counts confirmed false positives only (a lower bound "
                    "while control findings are unjudged). "
                    "Per-run recall's interval treats each bug as one observation (its k runs are "
                    "correlated, often identical at temperature 0), so it is wider than a per-run one. "
                    "Sorted by per-run recall within each context level, unfinished results last. "
                    "⚠ noisy = control false-positive "
                    f"rate over {NOISE_FPR:.0%} or more than {NOISE_FINDINGS_PER_REVIEW:g} findings per review.", "",
                    "| reviewer | context | k | **per-run recall** | recall any-of-k | recall all-of-k | "
                    "hard: any / all | precision | control runs w/ FP | unadj. | results |",
                    "|---|---|---|---|---|---|---|---|---|---|---|", *[r for _, r in sorted(rows)], ""]
    return "\n".join(out) + "\n"
