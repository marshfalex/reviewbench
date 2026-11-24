from pathlib import Path

import pytest

from reviewbench.cases import discover, load_case, validate_case
from reviewbench.context import build_request

CASES = Path(__file__).resolve().parents[1] / "cases"
ALL = discover((CASES, "public"))


def test_case_counts():
    from reviewbench.cases import active

    assert len(ALL) == 62 and len(active(ALL, "0.1")) == 27  # v0.1 stays frozen at 27
    assert {c.id for c in ALL if c.since == "0.2"} == {
        "py-0028-truthy-permission-decision", "py-0029-ttl-seconds-vs-ms-clock",
        "py-0030-clean-sort-column-whitelist", "py-0031-refactor-drops-login-required",
        "py-0032-refactor-pagination-off-by-one", "py-0033-clean-click-help-formfeed",
        "py-0034-clean-click-completion-var-dots", "py-0035-gitpython-ref-path-traversal",
        "py-0036-django-admindocs-template-traversal", "py-0037-pyjwt-hmac-key-confusion",
        "py-0038-requests-proxy-auth-https-leak", "py-0039-clean-click-abort-chains-cause",
        "py-0040-clean-click-empty-envvar-is-none", "py-0041-clean-click-invalid-glob-pattern",
        "py-0042-clean-click-confirm-default-none", "py-0043-clean-click-choice-complete-case",
        "py-0044-clean-flask-untag-without-object-hook", "py-0045-clean-flask-cert-option-eager",
        "py-0046-clean-flask-config-from-file-text", "py-0047-clean-jinja-required-block-check",
        "py-0048-clean-jinja-get-template-separator", "py-0049-jinja-xmlattr-invalid-key-chars",
        "py-0050-jinja-sandbox-format-map", "py-0051-urllib3-303-body-not-dropped",
        "py-0052-requests-verify-false-pool-reuse", "py-0053-clean-attrs-cached-property-attributeerror",
        "py-0054-clean-httpx-send-timeout", "py-0055-clean-httpx-encoding-after-text",
        "py-0056-clean-rich-progress-negative-time", "py-0057-clean-rich-traceback-missing-file",
        "py-0058-clean-starlette-exception-str-kwargs", "py-0059-clean-pydantic-model-construct-private",
        "py-0060-clean-pydantic-fieldinfo-repr-default", "py-0061-clean-pydantic-json-schema-usage-error",
        "py-0062-clean-rich-text-tab-size"}
    assert sum(c.is_control for c in ALL) == 27  # toward the SPEC §10 target of 36
    ALL_V01 = active(ALL, "0.1")
    assert sum(c.is_control for c in ALL_V01) == 4
    bugs = [c for c in ALL_V01 if not c.is_control]
    assert sum(c.difficulty == "easy" for c in bugs) == 15
    assert sum(c.difficulty == "hard" for c in bugs) == 8
    cves = [c for c in ALL if c.source["kind"] == "cve"]
    assert len(cves) == 13 and all(c.source.get("cve", "").startswith("CVE-") for c in cves)


@pytest.mark.parametrize("case", ALL, ids=lambda c: c.id)
def test_every_case_valid(case):
    assert validate_case(case) == []


def test_context_levels():
    case = load_case(CASES / "py-0017-cursor-pagination-skips")
    l0, l1, l2 = (build_request(case, lv) for lv in ("L0", "L1", "L2"))
    assert l0.files == ()
    assert [f.path for f in l1.files] == ["app/feed.py"]
    assert [(f.path, f.role) for f in l2.files] == [
        ("app/feed.py", "changed"), ("app/schema.sql", "related"), ("app/importer.py", "related")]
    assert "created_at < ?" in l1.files[0].content  # post-PR content
    assert '<file path="app/schema.sql" role="related">' in l2.render()
    assert l0.render().startswith("<diff>")


def test_bad_level():
    with pytest.raises(ValueError):
        build_request(ALL[0], "L9")


def test_validate_catches_out_of_range_lines(tmp_path):
    import shutil

    d = tmp_path / "py-0001-sql-injection"
    shutil.copytree(CASES / "py-0001-sql-injection", d)
    text = (d / "case.yaml").read_text().replace("- 6\n  - 6", "- 6\n  - 60")
    (d / "case.yaml").write_text(text)
    assert any("out of range" in e for e in validate_case(load_case(d)))


def test_cases_for_a_later_version_are_held_back():
    from reviewbench import BENCH_VERSION
    from reviewbench.cases import active

    cases = discover((CASES, "public"))
    later = [c for c in cases if c.since != "0.1"]
    assert later, "expected some cases marked since: 0.2"
    now = {c.id for c in active(cases)}
    assert BENCH_VERSION != "0.1" or not any(c.id in now for c in later)
    assert {c.id for c in active(cases, "0.2")} == {c.id for c in cases}


def test_lineup_case_ids_exclude_later_cases(tmp_path, monkeypatch, capsys):
    from reviewbench import cli

    seen = {}
    monkeypatch.setattr("reviewbench.lineup.plan", lambda *a, **k: seen.setdefault("ids", k["case_ids"]) and [])
    cli.main(["lineup", "--results-dir", str(tmp_path)])
    assert "py-0028-truthy-permission-decision" not in seen["ids"]
    assert "py-0001" not in seen["ids"] and len(seen["ids"]) == 27


def test_no_two_cases_share_an_upstream_commit():
    """A duplicate source.ref means the same real change was imported twice (docs/LESSONS.md)."""
    import collections

    refs = collections.Counter(c.source["ref"] for c in ALL if c.source["kind"] in ("cve", "upstream"))
    dupes = {r: n for r, n in refs.items() if n > 1}
    assert not dupes, f"cases share an upstream commit: {dupes}"
