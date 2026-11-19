"""Held-out split: loading from $REVIEWBENCH_HELDOUT and keeping its details out of committed results."""
import argparse
import json
import shutil
from pathlib import Path

import pytest
import yaml

from reviewbench import cli
from reviewbench.adapters import ReplayReviewer
from reviewbench.adapters.base import Finding
from reviewbench.heldout import ENV_VAR, leaks, raw_path
from reviewbench.report import leaderboard

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "cases"
SECRET_ID = "py-0901-secret-heldout-case"
SECRET_TITLE = "Zebra-quokka held-out title"
SECRET_TEXT = "MARKER-7f3a explanation only the held-out finding has"


@pytest.fixture
def heldout(tmp_path, monkeypatch):
    """A held-out dir with one case (a renamed copy of py-0001) and a public dir with py-0022."""
    held = tmp_path / "private"
    case = held / SECRET_ID
    shutil.copytree(CASES / "py-0001-sql-injection", case)
    meta = yaml.safe_load((case / "case.yaml").read_text())
    meta.update(id=SECRET_ID, title=SECRET_TITLE)
    (case / "case.yaml").write_text(yaml.safe_dump(meta))
    public = tmp_path / "cases"
    shutil.copytree(CASES / "py-0022-clean-compare-digest", public / "py-0022-clean-compare-digest")
    monkeypatch.setenv(ENV_VAR, str(held))
    monkeypatch.chdir(tmp_path)  # no stray heldout/ or results/ from the repo
    return tmp_path


def _reviewer(provider, model=None):
    def fn(prompt):
        if "SELECT id, email FROM users WHERE name" in prompt:
            return [Finding("app/users.py", 6, "security", "critical", "SQL injection", SECRET_TEXT),
                    Finding("app/users.py", 1, "correctness", "high", "Spurious", SECRET_TEXT)]
        return [Finding("app/auth.py", 1, "maintainability", "medium", "Public spurious", "x")]
    return ReplayReviewer(fn=fn)


def test_env_var_loads_heldout_split(heldout):
    cases = cli._cases(argparse.Namespace(cases="cases", heldout=None, only=None))
    assert {c.id: c.split for c in cases} == {SECRET_ID: "heldout", "py-0022-clean-compare-digest": "public"}
    assert cli.main(["validate"]) == 0


def test_configured_but_missing_dir_is_an_error(heldout, monkeypatch):
    monkeypatch.setenv(ENV_VAR, str(heldout / "nope"))
    with pytest.raises(SystemExit, match="does not exist"):
        cli.main(["validate"])


def test_no_heldout_configured_is_fine(tmp_path, monkeypatch):
    monkeypatch.delenv(ENV_VAR, raising=False)
    monkeypatch.chdir(tmp_path)
    assert cli.main(["validate", "--cases", str(CASES), "--only", "py-0001-sql-injection"]) == 0


def test_run_keeps_heldout_details_out_of_committed_results(heldout, monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_adapter", _reviewer)
    out = heldout / "results" / "r.json"
    assert cli.main(["run", "--provider", "replay", "-k", "2", "--levels", "L0,L1",
                     "--out", str(out), "--rules", "none.yaml"]) == 0

    committed = [p for p in (heldout / "results").glob("*") if p.is_file()]
    assert sorted(p.name for p in committed) == ["r.json", "r.md"]
    for p in committed:
        text = p.read_text()
        for secret in (SECRET_ID, SECRET_TITLE, SECRET_TEXT, "app/users.py"):
            assert secret not in text, f"{secret!r} leaked into {p.name}"
    assert SECRET_ID not in capsys.readouterr().err  # CI logs are public too

    doc = json.loads(out.read_text())
    assert leaks(doc) == [] and list(doc["cases"]) == ["py-0022-clean-compare-digest"]
    s = doc["heldout"]["slices"]["heldout/L0/all"]
    assert doc["heldout"]["cases"] == 1
    assert s["any_of_k"] == {"hits": 1, "n": 1, "rate": 1.0, "ci95": s["any_of_k"]["ci95"]}
    assert s["unadjudicated_findings"] == 2  # the spurious finding, once per run

    raw = json.loads(raw_path(out).read_text())  # the private raw file has everything
    assert list(raw["cases"]) == [SECRET_ID] and SECRET_TEXT in json.dumps(raw)

    md = out.with_suffix(".md").read_text()
    assert "## heldout" in md and "1 private case(s)" in md and "## public" in md
    board = leaderboard(heldout / "results")
    assert "## v0.1 — heldout cases" in board and "## v0.1 — public cases" in board


def test_adjudicating_heldout_updates_only_the_aggregate(heldout, monkeypatch):
    monkeypatch.setattr(cli, "get_adapter", _reviewer)
    out = heldout / "results" / "r.json"
    cli.main(["run", "--provider", "replay", "-k", "1", "--levels", "L0", "--out", str(out),
              "--rules", "none.yaml"])
    rules = heldout / "rules.yaml"
    rules.write_text(yaml.safe_dump({SECRET_ID: [{"match": "spurious", "verdict": "invalid"}]}))
    assert cli.main(["adjudicate", str(out), "--rules", str(rules), "--rules-only"]) == 0
    s = json.loads(out.read_text())["heldout"]["slices"]["heldout/L0/all"]
    assert s["precision_adjudicated"]["hits"] == 1 and s["precision_adjudicated"]["n"] == 2
    assert SECRET_ID not in out.with_name("r.adjudications.json").read_text()
    assert SECRET_ID in raw_path(out).with_name("r.heldout.adjudications.json").read_text()


def test_leaderboard_refuses_a_leaking_results_file(tmp_path):
    doc = {"bench_version": "0.1", "cases": {"x": {"split": "heldout"}}, "records": []}
    (tmp_path / "bad.json").write_text(json.dumps(doc))
    with pytest.raises(ValueError, match="held-out"):
        leaderboard(tmp_path)
    assert leaks({"cases": {}, "records": [], "heldout": {"cases": 1, "ids": ["x"]}})


def test_committed_results_reveal_no_heldout_cases():
    for p in (ROOT / "results").glob("*.json"):
        if not p.name.endswith(".adjudications.json"):
            assert leaks(json.loads(p.read_text())) == [], p.name


def test_raw_dir_is_gitignored():
    assert "results/raw/" in (ROOT / ".gitignore").read_text().splitlines()


def test_resume_finishes_heldout_and_keeps_verdicts(heldout, monkeypatch):
    monkeypatch.setattr(cli, "get_adapter", _reviewer)
    args = ["run", "--provider", "replay", "-k", "1", "--levels", "L0", "--rules", "none.yaml",
            "--results-dir", "results"]
    assert cli.main(args + ["--max-minutes", "0"]) == 0  # budget used up before any review
    (out,) = [p for p in (heldout / "results").glob("*.json")]
    assert json.loads(out.read_text())["status"] == "partial" and not raw_path(out).exists()
    out.with_name(out.stem + ".adjudications.json").write_text(json.dumps({"verdicts": {"x": {"verdict": "valid"}}}))

    assert cli.main(args + ["--resume"]) == 0
    doc = json.loads(out.read_text())
    assert doc["status"] == "complete" and doc["heldout"]["status"] == "complete"
    assert doc["heldout"]["slices"]["heldout/L0/all"]["any_of_k"]["hits"] == 1
    assert "x" in json.loads(out.with_name(out.stem + ".adjudications.json").read_text())["verdicts"]
    assert len(list((heldout / "results").glob("*.json"))) == 2  # resumed in place: r + adjudications
