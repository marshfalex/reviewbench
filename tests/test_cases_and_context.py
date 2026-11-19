from pathlib import Path

import pytest

from reviewbench.cases import discover, load_case, validate_case
from reviewbench.context import build_request

CASES = Path(__file__).resolve().parents[1] / "cases"
ALL = discover((CASES, "public"))


def test_case_counts():
    assert len(ALL) == 27
    assert sum(c.is_control for c in ALL) == 4
    bugs = [c for c in ALL if not c.is_control]
    assert sum(c.difficulty == "easy" for c in bugs) == 15
    assert sum(c.difficulty == "hard" for c in bugs) == 8
    cves = [c for c in ALL if c.source["kind"] == "cve"]
    assert len(cves) == 5 and all(c.source.get("cve", "").startswith("CVE-") for c in cves)


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
