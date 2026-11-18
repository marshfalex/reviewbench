import json
from pathlib import Path

from reviewbench.adapters import ReplayReviewer, get_adapter
from reviewbench.adapters.base import Finding, parse_review
from reviewbench.adjudicate import apply_rules, interactive
from reviewbench.cases import discover
from reviewbench.cli import main
from reviewbench.context import ReviewRequest
from reviewbench.report import leaderboard, run_report
from reviewbench.runner import estimate_cost, run
from reviewbench.scoring import score

CASES = Path(__file__).resolve().parents[1] / "cases"


def _oracle(prompt: str) -> list[Finding]:
    """Flags SQL injection only when it can see it; plus one spurious finding."""
    out = [Finding("app/users.py", 6, "security", "critical", "SQL injection", "f-string")] \
        if "SELECT id, email FROM users WHERE name = '{username}'" in prompt else []
    return out + [Finding("app/whatever.py", 1, "maintainability", "medium", "KeyError at import", "x")]


def test_end_to_end_replay(tmp_path):
    cases = [c for c in discover((CASES, "public")) if c.id in
             ("py-0001-sql-injection", "py-0022-clean-compare-digest")]
    out = tmp_path / "r.json"
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0", "L2"], 2, out, log=lambda m: None)
    assert json.loads(out.read_text())["status"] == "complete"
    assert len(doc["records"]) == 2 * 2 * 2
    verdicts = {}
    rules = {"py-0022-clean-compare-digest": [{"match": "keyerror", "verdict": "invalid"}]}
    assert apply_rules(doc, verdicts, rules) == 4  # only the control's spurious findings match a rule
    s = score(doc, verdicts)["slices"]["public/L0/all"]
    assert s["all_of_k"]["hits"] == 1 and s["control_runs_with_confirmed_fp"]["hits"] == 2
    assert s["unadjudicated_findings"] == 2
    answers = iter(["i", "", "v", "a note", "q"])
    assert interactive(doc, verdicts, ask=lambda _: next(answers), show=lambda *_: None) == 2
    assert "py-0001-sql-injection" in run_report(doc, verdicts)


def test_parse_review_drops_malformed():
    raw = json.dumps({"summary": "s", "findings": [
        {"path": "b/a.py", "line": "3", "category": "Security", "severity": "HIGH", "title": "t",
         "explanation": "e"},
        {"path": "a.py"},
        {"path": "a.py", "line": 1, "category": "style", "severity": "urgent", "title": "t", "explanation": "e"}]})
    summary, fs = parse_review(raw)
    assert len(fs) == 2 and fs[0].path == "a.py" and fs[0].line == 3 and fs[0].severity == "high"
    assert fs[1].category == "maintainability" and fs[1].severity == "low"


def test_prompt_budget_records_error():
    r = get_adapter("groq")
    res = r.review(ReviewRequest(diff="x" * 30_000))
    assert res.error.startswith("too_large") and res.findings == []


def test_cost_estimate_free_vs_paid():
    cases = discover((CASES, "public"))
    assert estimate_cost(cases, ["L0"], 1, get_adapter("groq"))["usd"] == 0
    est = estimate_cost(cases, ["L0", "L1", "L2"], 3, get_adapter("anthropic", "claude-haiku-5-5"))
    assert est["requests"] == 22 * 3 * 3 and est["usd"] > 0


def test_paid_run_refused_without_yes(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    rc = main(["run", "--provider", "anthropic", "--only", "py-0001-sql-injection", "-k", "1",
               "--results-dir", str(tmp_path)])
    assert rc == 2 and not list(tmp_path.iterdir())


def test_leaderboard_groups_by_version(tmp_path):
    cases = [c for c in discover((CASES, "public")) if c.id == "py-0001-sql-injection"]
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0"], 1, tmp_path / "a.json", log=lambda m: None)
    other = {**doc, "bench_version": "0.0"}
    (tmp_path / "b.json").write_text(json.dumps(other))
    md = leaderboard(tmp_path)
    assert "## v0.1 — public cases" in md and "## v0.0 — public cases" in md
    assert md.index("v0.1") < md.index("v0.0")
