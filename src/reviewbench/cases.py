"""Loading and validating benchmark cases (see docs/SPEC.md)."""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import yaml

DIFFICULTIES = {"easy", "hard"}
SOURCE_KINDS = {"synthetic", "cve", "postmortem"}
SEVERITIES = ["critical", "high", "medium", "low"]
ID_RE = re.compile(r"^py-\d{4}-[a-z0-9-]+$")


class CaseError(ValueError):
    pass


@dataclass(frozen=True)
class Bug:
    file: str
    lines: tuple[int, int]
    cls: str
    cwe: str | None
    severity: str
    description: str


@dataclass(frozen=True)
class KnownIssue:
    match: str
    file: str | None = None
    note: str = ""


@dataclass
class Case:
    id: str
    title: str
    language: str
    difficulty: str
    tags: list[str]
    source: dict
    bugs: list[Bug]
    related: list[str]
    known_issues: list[KnownIssue]
    dir: Path
    split: str = "public"  # "public" or "heldout"
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def is_control(self) -> bool:
        return not self.bugs

    @property
    def diff(self) -> str:
        return (self.dir / "pr.diff").read_text(encoding="utf-8")

    @cached_property
    def changed_files(self) -> list[str]:
        """Post-PR paths touched by the diff (deleted files excluded)."""
        out = []
        for line in self.diff.splitlines():
            if line.startswith("+++ "):
                target = line[4:].strip()
                if target != "/dev/null":
                    out.append(target.removeprefix("b/"))
        return out

    @cached_property
    def post_pr_files(self) -> dict[str, str]:
        """Every text file of repo/ after applying pr.diff, keyed by relative path."""
        return apply_diff(self.dir / "repo", self.dir / "pr.diff")


def apply_diff(repo_dir: Path, diff_path: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        if repo_dir.exists():
            shutil.copytree(repo_dir, work)
        else:
            work.mkdir()
        proc = subprocess.run(["git", "apply", "--whitespace=nowarn", str(diff_path.resolve())],
                              cwd=work, capture_output=True, text=True)
        if proc.returncode != 0:
            raise CaseError(f"pr.diff does not apply to repo/: {proc.stderr.strip()}")
        files = {}
        for p in sorted(work.rglob("*")):
            if p.is_file():
                try:
                    files[p.relative_to(work).as_posix()] = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
        return files


def load_case(case_dir: Path, split: str = "public") -> Case:
    meta_path = case_dir / "case.yaml"
    if not meta_path.exists():
        raise CaseError(f"{case_dir}: missing case.yaml")
    m = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    try:
        bugs = [Bug(file=b["file"], lines=(int(b["lines"][0]), int(b["lines"][-1])), cls=b["class"],
                    cwe=b.get("cwe"), severity=b["severity"], description=b["description"])
                for b in (m.get("bugs") or [])]
        known = [KnownIssue(match=k["match"], file=k.get("file"), note=k.get("note", ""))
                 for k in (m.get("known_issues") or [])]
        case = Case(id=m["id"], title=m["title"], language=m["language"], difficulty=m["difficulty"],
                    tags=list(m.get("tags") or []), source=dict(m["source"]), bugs=bugs,
                    related=list((m.get("context") or {}).get("related") or []),
                    known_issues=known, dir=case_dir, split=split, raw=m)
    except (KeyError, TypeError, IndexError, ValueError) as e:
        raise CaseError(f"{case_dir}: malformed case.yaml ({e!r})") from e
    return case


def validate_case(case: Case) -> list[str]:
    """Returns a list of problems (empty = valid). Applies the diff, so needs git."""
    errs = []
    if not ID_RE.match(case.id):
        errs.append(f"id {case.id!r} must look like py-0042-short-slug")
    if case.dir.name != case.id:
        errs.append(f"directory name {case.dir.name!r} != id {case.id!r}")
    if case.language != "python":
        errs.append("language must be 'python' in v0.1")
    if case.difficulty not in DIFFICULTIES:
        errs.append(f"difficulty must be one of {sorted(DIFFICULTIES)}")
    if case.source.get("kind") not in SOURCE_KINDS:
        errs.append(f"source.kind must be one of {sorted(SOURCE_KINDS)}")
    for key in ("ref", "license"):
        if not case.source.get(key):
            errs.append(f"source.{key} is required")
    if not (case.dir / "pr.diff").exists():
        return errs + ["missing pr.diff"]
    try:
        files = case.post_pr_files
    except CaseError as e:
        return errs + [str(e)]
    for b in case.bugs:
        if b.severity not in SEVERITIES:
            errs.append(f"bug severity {b.severity!r} invalid")
        if b.file not in files:
            errs.append(f"bug file {b.file} not in post-PR tree")
            continue
        n = len(files[b.file].splitlines())
        if not 1 <= b.lines[0] <= b.lines[1] <= n:
            errs.append(f"bug lines {b.lines} out of range for {b.file} ({n} lines)")
        if b.file not in case.changed_files:
            errs.append(f"bug file {b.file} is not touched by pr.diff")
    for r in case.related:
        if r not in files:
            errs.append(f"context.related file {r} not in post-PR tree")
    for k in case.known_issues:
        if not k.match.strip():
            errs.append("known_issues entries need a non-empty match")
    return errs


def discover(*dirs: tuple[Path, str]) -> list[Case]:
    """Loads every case under the given (directory, split) pairs, sorted by id."""
    cases = []
    for d, split in dirs:
        if not d.exists():
            continue
        for sub in sorted(p for p in d.iterdir() if p.is_dir() and (p / "case.yaml").exists()):
            cases.append(load_case(sub, split))
    ids = [c.id for c in cases]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise CaseError(f"duplicate case ids: {sorted(dupes)}")
    return sorted(cases, key=lambda c: c.id)
