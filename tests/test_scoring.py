from pathlib import Path

import pytest

from reviewbench.cases import discover, validate_case
from reviewbench.scoring import classify, norm, score
from reviewbench.stats import fmt_rate, wilson_interval

CASES = Path(__file__).resolve().parents[1] / "cases"

BUG = {"file": "app/x.py", "lines": [10, 12], "class": "c", "cwe": None, "severity": "high"}


def f(fid, path="app/x.py", line=10, sev="high", title="t", expl="e"):
    return {"id": fid, "path": path, "line": line, "category": "correctness", "severity": sev,
            "title": title, "explanation": expl}


def doc(records, bugs=(BUG,), known=(), difficulty="hard", split="public", case="c1"):
    return {"cases": {case: {"title": "x", "difficulty": difficulty, "split": split,
                             "bugs": list(bugs), "known_issues": list(known)}},
            "records": records}


def rec(run, findings, level="L0", case="c1", error=None):
    return {"case": case, "level": level, "run": run, "error": error, "findings": findings}


def test_wilson_matches_known_values():
    assert wilson_interval(0, 0) == (0.0, 0.0)
    lo, hi = wilson_interval(13, 18)
    assert round(lo) == 49 and round(hi) == 88  # the seed EVALUATION.md figure
    lo, hi = wilson_interval(36, 36)
    assert round(lo) == 90 and hi == 100
    assert fmt_rate(1, 3).startswith("1/3 (33%, CI")


@pytest.mark.parametrize("line,expected", [(7, None), (8, "hit"), (12, "hit"), (14, "hit"), (15, None)])
def test_line_tolerance(line, expected):
    lab = classify(f("a", line=line), doc([])["cases"]["c1"], {})
    assert (lab == "hit") == (expected == "hit")


def test_wrong_path_and_low_severity():
    t = doc([])["cases"]["c1"]
    assert classify(f("a", path="app/y.py"), t, {}) == "unadjudicated"
    assert classify(f("a", sev="low"), t, {}) is None


def test_known_issue_normalizes_unicode_hyphens():
    t = doc([], known=[{"match": "hard-coded to empty", "file": "app/x.py"}])["cases"]["c1"]
    assert classify(f("a", line=1, title="Secret hard‑coded to EMPTY"), t, {}) == "known"
    assert norm("A–B") == "a-b"


def test_known_issue_respects_file():
    t = doc([], known=[{"match": "negative", "file": "app/other.py"}])["cases"]["c1"]
    assert classify(f("a", line=1, title="negative qty"), t, {}) == "unadjudicated"


def test_any_and_all_of_k():
    # caught in runs 0 and 2 but not 1 -> any-of-k yes, all-of-k no, per-run 2/3
    d = doc([rec(0, [f("r0")]), rec(1, [f("r1", line=40)]), rec(2, [f("r2")])])
    s = score(d)["slices"]["public/L0/all"]
    assert (s["any_of_k"]["hits"], s["any_of_k"]["n"]) == (1, 1)
    assert (s["all_of_k"]["hits"], s["all_of_k"]["n"]) == (0, 1)
    assert (s["per_run_recall"]["hits"], s["per_run_recall"]["n"]) == (2, 3)


def test_multiple_bugs_counted_separately():
    bug2 = {**BUG, "lines": [30, 30]}
    d = doc([rec(0, [f("a")]), rec(1, [f("b"), f("c", line=30)])], bugs=[BUG, bug2])
    s = score(d)["slices"]["public/L0/all"]
    assert s["any_of_k"]["hits"] == 2 and s["all_of_k"]["hits"] == 1 and s["per_run_recall"]["n"] == 4


def test_precision_uses_only_adjudicated_findings():
    d = doc([rec(0, [f("hit"), f("x1", line=50), f("x2", line=60), f("x3", line=70)])])
    verdicts = {"c1/x1": {}, "x1": {"verdict": "valid"}, "x2": {"verdict": "invalid"}}
    s = score(d, verdicts)["slices"]["public/L0/all"]
    # hit + valid good, invalid bad; x3 unadjudicated and excluded from precision
    assert (s["precision_adjudicated"]["hits"], s["precision_adjudicated"]["n"]) == (2, 3)
    assert s["unadjudicated_findings"] == 1


def test_control_fp_rate_and_known_issue_not_fp():
    known = [{"match": "negative quantity", "file": "app/x.py"}]
    d = doc([rec(0, [f("a", title="Negative quantity increases stock")]),
             rec(1, [f("b", title="KeyError at import")]),
             rec(2, [])], bugs=[], known=known, difficulty="easy")
    s = score(d, {"b": {"verdict": "invalid"}})["slices"]["public/L0/all"]
    assert (s["control_runs_with_confirmed_fp"]["hits"], s["control_runs_with_confirmed_fp"]["n"]) == (1, 3)
    assert s["any_of_k"]["n"] == 0  # controls never enter recall
    assert (s["precision_adjudicated"]["hits"], s["precision_adjudicated"]["n"]) == (1, 2)


def test_errored_runs_excluded_and_reported():
    d = doc([rec(0, [f("a")]), rec(1, [], error="rate_limited")])
    s = score(d)["slices"]["public/L0/all"]
    assert s["errored_runs"] == 1 and s["per_run_recall"]["n"] == 1 and s["all_of_k"]["hits"] == 1


def test_levels_and_splits_are_separate_slices():
    d = doc([rec(0, [f("a")], level="L0"), rec(0, [], level="L2")], split="heldout")
    s = score(d)["slices"]
    assert s["heldout/L0/hard"]["any_of_k"]["hits"] == 1
    assert s["heldout/L2/hard"]["any_of_k"]["hits"] == 0
    assert not any(k.startswith("public/") for k in s)


def test_cohen_kappa_known_values():
    from reviewbench.adjudicate import cohen_kappa

    assert cohen_kappa([]) is None
    assert cohen_kappa([("valid", "valid"), ("invalid", "invalid")]) == 1.0
    # 20 findings: agree on 15 (10 valid, 5 invalid), disagree on 5. po = .75;
    # rater A says valid 13/20, B 12/20, so pe = .65*.6 + .35*.4 = .53 and kappa = .22/.47
    pairs = [("valid", "valid")] * 10 + [("invalid", "invalid")] * 5 \
        + [("valid", "invalid")] * 3 + [("invalid", "valid")] * 2
    assert abs(cohen_kappa(pairs) - (0.75 - 0.53) / (1 - 0.53)) < 1e-9


def test_bug_also_locations_count_as_hits():
    from reviewbench.scoring import bug_matches

    bug = {"file": "a.py", "lines": [10, 12], "also": [{"file": "b.py", "lines": [40, 41]}]}
    f = lambda path, line: {"path": path, "line": line}  # noqa: E731
    assert bug_matches(f("a.py", 11), bug) and bug_matches(f("b.py", 43), bug)  # within ±2
    assert not bug_matches(f("b.py", 44), bug) and not bug_matches(f("c.py", 40), bug)
    assert bug_matches(f("a.py", 10), {"file": "a.py", "lines": [10, 12]})  # old truth, no "also"


def test_case_with_also_location_loads_validates_and_snapshots():
    from reviewbench.runner import case_truth

    c = next(c for c in discover((CASES, "public")) if c.id == "py-0051-urllib3-303-body-not-dropped")
    assert c.bugs[0].also == (("src/urllib3/connectionpool.py", (356, 358)),)
    assert validate_case(c) == []
    assert case_truth(c)["bugs"][0]["also"] == [{"file": "src/urllib3/connectionpool.py", "lines": [356, 358]}]


def test_defect_terms_require_the_finding_to_name_the_defect():
    from reviewbench.scoring import bug_matches

    bug = {"file": "a.py", "lines": [10, 12], "defect_terms": ["idempoten", "double charge"]}
    on_topic = {"path": "a.py", "line": 11, "title": "Retry can double charge", "explanation": "x"}
    off_topic = {"path": "a.py", "line": 11, "title": "Unchecked HTTP status", "explanation": "r.json()"}
    unicode_hit = {"path": "a.py", "line": 11, "title": "No IDEMPOTENCY key", "explanation": ""}
    assert bug_matches(on_topic, bug) and bug_matches(unicode_hit, bug)
    assert not bug_matches(off_topic, bug)
    assert not bug_matches({**on_topic, "line": 40}, bug)  # still needs the location
    assert bug_matches(off_topic, {"file": "a.py", "lines": [10, 12]})  # no terms: location only


def test_v02_bug_cases_all_have_defect_terms_and_snapshot_them():
    from reviewbench.runner import case_truth

    bugs = [c for c in discover((CASES, "public")) if c.since == "0.2" and c.bugs]
    assert bugs and all(c.bugs[0].defect_terms for c in bugs)
    assert all(validate_case(c) == [] for c in bugs)
    assert case_truth(bugs[0])["bugs"][0]["defect_terms"] == list(bugs[0].bugs[0].defect_terms)
    v01 = [c for c in discover((CASES, "public")) if c.since == "0.1" and c.bugs]
    assert not any(c.bugs[0].defect_terms for c in v01)  # v0.1 truth stays frozen until the bump


def test_calibration_script_reports_right_line_wrong_reason():
    import importlib.util
    import json

    spec = importlib.util.spec_from_file_location("cal", CASES.parent / "scripts" / "calibrate_defect_terms.py")
    cal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cal)
    import tempfile
    doc = {"model": "m", "cases": {"py-9999-x": {"bugs": [{"file": "a.py", "lines": [1, 2]}]}},
           "records": [{"case": "py-9999-x", "level": "L0", "error": None, "findings": [
               {"path": "a.py", "line": 1, "severity": "high", "title": "SQL injection", "explanation": ""}]},
                       {"case": "py-9999-x", "level": "L1", "error": None, "findings": [
               {"path": "a.py", "line": 1, "severity": "high", "title": "Style nit", "explanation": ""}]}]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(doc, fh)
    total, named, misses = cal.calibrate({"py-9999": ["sql"]}, [fh.name])
    assert (total, named) == (2, 1) and misses == [("m", "py-9999-x", "L1", "Style nit")]
