"""Scoring. Pure functions over result records -- no API calls (see docs/SPEC.md §Metrics).

Every counted finding (severity medium or higher) in a run is exactly one of:
  hit          -- on a planted bug's file, line within LINE_TOLERANCE of its range
  known        -- matches one of the case's known_issues  (a real, unplanted issue)
  valid        -- a human adjudicated it as a real issue
  invalid      -- a human adjudicated it as a false positive
  unadjudicated
Low-severity findings are ignored.
"""
from __future__ import annotations

import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

from reviewbench.stats import wilson_interval

LINE_TOLERANCE = 2
COUNTED = {"critical", "high", "medium"}
_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−"), "-")


def norm(text: str) -> str:
    """Case/Unicode-insensitive form for substring matching (models emit non-breaking hyphens)."""
    return unicodedata.normalize("NFKC", text).translate(_DASHES).casefold()


def bug_matches(finding: dict, bug: dict, tol: int = LINE_TOLERANCE) -> bool:
    lo, hi = bug["lines"]
    return finding["path"] == bug["file"] and lo - tol <= int(finding["line"]) <= hi + tol


def known_matches(finding: dict, known: dict) -> bool:
    if known.get("file") and finding["path"] != known["file"]:
        return False
    return norm(known["match"]) in norm(finding["title"] + " " + finding["explanation"])


def classify(finding: dict, case_truth: dict, verdicts: dict) -> str | None:
    """Label one finding. Returns None for ignored (low-severity) findings."""
    if finding["severity"] not in COUNTED:
        return None
    if any(bug_matches(finding, b) for b in case_truth["bugs"]):
        return "hit"
    if any(known_matches(finding, k) for k in case_truth.get("known_issues", [])):
        return "known"
    v = verdicts.get(finding["id"], {}).get("verdict")
    return v if v in ("valid", "invalid") else "unadjudicated"


@dataclass
class Rate:
    hits: int = 0
    n: int = 0

    def add(self, ok: bool) -> None:
        self.hits += int(ok)
        self.n += 1

    def as_dict(self) -> dict:
        lo, hi = wilson_interval(self.hits, self.n)
        return {"hits": self.hits, "n": self.n, "rate": self.hits / self.n if self.n else None,
                "ci95": [round(lo, 1), round(hi, 1)]}


@dataclass
class Slice:
    """All metrics for one (split, level, difficulty-or-'all') slice."""
    per_run_recall: Rate = field(default_factory=Rate)
    any_of_k: Rate = field(default_factory=Rate)
    all_of_k: Rate = field(default_factory=Rate)
    precision: Rate = field(default_factory=Rate)  # (hit+known+valid) / (hit+known+valid+invalid)
    control_runs_with_fp: Rate = field(default_factory=Rate)
    unadjudicated: int = 0
    errored_runs: int = 0

    def as_dict(self) -> dict:
        return {"per_run_recall": self.per_run_recall.as_dict(), "any_of_k": self.any_of_k.as_dict(),
                "all_of_k": self.all_of_k.as_dict(), "precision_adjudicated": self.precision.as_dict(),
                "control_runs_with_confirmed_fp": self.control_runs_with_fp.as_dict(),
                "unadjudicated_findings": self.unadjudicated, "errored_runs": self.errored_runs}


def score(results: dict, verdicts: dict | None = None) -> dict:
    """Aggregate a results document into metrics keyed '<split>/<level>/<difficulty|all>'."""
    verdicts = verdicts or {}
    truth = results["cases"]
    slices: dict[str, Slice] = defaultdict(Slice)
    # (split, level, case, bug index) -> [caught in run r, ...]
    bug_runs: dict[tuple, list[bool]] = defaultdict(list)
    labels: dict[str, str | None] = {}

    for rec in results["records"]:
        t = truth[rec["case"]]
        keys = [f"{t['split']}/{rec['level']}/{t['difficulty']}", f"{t['split']}/{rec['level']}/all"]
        if rec.get("error"):
            for k in keys:
                slices[k].errored_runs += 1
            continue
        run_labels = []
        for f in rec["findings"]:
            lab = classify(f, t, verdicts)
            labels[f["id"]] = lab
            run_labels.append(lab)
        for i, bug in enumerate(t["bugs"]):
            caught = any(f["severity"] in COUNTED and bug_matches(f, bug) for f in rec["findings"])
            bug_runs[(t["split"], rec["level"], t["difficulty"], rec["case"], i)].append(caught)
            for k in keys:
                slices[k].per_run_recall.add(caught)
        for k in keys:
            s = slices[k]
            for lab in run_labels:
                if lab in ("hit", "known", "valid"):
                    s.precision.add(True)
                elif lab == "invalid":
                    s.precision.add(False)
                elif lab == "unadjudicated":
                    s.unadjudicated += 1
            if not t["bugs"]:
                s.control_runs_with_fp.add("invalid" in run_labels)

    for (split, level, difficulty, _case, _i), runs in bug_runs.items():
        for k in (f"{split}/{level}/{difficulty}", f"{split}/{level}/all"):
            slices[k].any_of_k.add(any(runs))
            slices[k].all_of_k.add(all(runs))

    return {"slices": {k: s.as_dict() for k, s in sorted(slices.items())}, "labels": labels}


def per_case_table(results: dict, verdicts: dict | None = None) -> list[dict]:
    """Per (case, level): runs, runs that caught every planted bug, and finding-label counts."""
    verdicts = verdicts or {}
    rows: dict[tuple, dict] = {}
    for rec in results["records"]:
        t = truth = results["cases"][rec["case"]]
        row = rows.setdefault((rec["case"], rec["level"]), {
            "case": rec["case"], "level": rec["level"], "difficulty": truth["difficulty"],
            "split": truth["split"], "control": not truth["bugs"], "runs": 0, "caught": 0, "errors": 0,
            "hit": 0, "known": 0, "valid": 0, "invalid": 0, "unadjudicated": 0})
        if rec.get("error"):
            row["errors"] += 1
            continue
        row["runs"] += 1
        if t["bugs"] and all(any(f["severity"] in COUNTED and bug_matches(f, b) for f in rec["findings"])
                             for b in t["bugs"]):
            row["caught"] += 1
        for f in rec["findings"]:
            lab = classify(f, t, verdicts)
            if lab:
                row[lab] += 1
    return sorted(rows.values(), key=lambda r: (r["case"], r["level"]))
