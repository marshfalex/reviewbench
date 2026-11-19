"""Held-out split: private cases whose details never reach committed results (SPEC §1 "Splits").

Held-out cases are loaded from the directory in $REVIEWBENCH_HELDOUT (or --heldout). They are
reviewed into a separate raw results file under results/raw/ (git-ignored); the committed results
file only gets an aggregate summary (hits, n, rate and CI per slice). No case id, title, file
path, line or finding text of a held-out case is written to a committed file or to the run log.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from reviewbench.adjudicate import load_verdicts
from reviewbench.cases import Case
from reviewbench.scoring import score

ENV_VAR = "REVIEWBENCH_HELDOUT"
DEFAULT_DIR = "heldout"


def heldout_dir(cli_value: str | None) -> Path | None:
    """The held-out directory to load, or None. An explicitly configured directory
    (--heldout or $REVIEWBENCH_HELDOUT) that does not exist is an error; the default
    `heldout/` is optional."""
    value = cli_value or os.environ.get(ENV_VAR)
    if not value:
        d = Path(DEFAULT_DIR)
        return d if d.is_dir() else None
    d = Path(value).expanduser()
    if not d.is_dir():
        raise SystemExit(f"held-out directory {d} does not exist (set by --heldout or ${ENV_VAR})")
    return d


def heldout_allowed(provider: str, model: str, lineup_path: Path) -> bool:
    """True only if lineup.yaml marks this provider/model `heldout_ok: true`.

    Free endpoints may log or train on prompts, so held-out cases are refused by default:
    a provider or model missing from the lineup, a missing or unreadable lineup file, or any
    value other than literal true all mean "no". An `auto:<text>` entry covers models of that
    provider whose id contains <text>."""
    try:
        cfg = yaml.safe_load(lineup_path.read_text()) or {}
        entries = list(cfg.get("models") or [])
    except (OSError, yaml.YAMLError, AttributeError, TypeError):
        return False
    for e in entries:
        if not isinstance(e, dict) or e.get("provider") != provider or e.get("heldout_ok") is not True:
            continue
        want = str(e.get("model") or "")
        if want == model or (want.startswith("auto:") and want[5:].lower() in model.lower()):
            return True
    return False


def raw_path(public_path: Path) -> Path:
    """Where held-out raw results for a committed results file go (git-ignored results/raw/)."""
    return public_path.parent / "raw" / f"{public_path.stem}.heldout.json"


def redacting_log(cases: list[Case], log):
    """Wraps a log function so held-out case ids are replaced by stable anonymous aliases.
    CI logs of a public repo are public."""
    aliases = {c.id: f"heldout-{i:02d}" for i, c in enumerate(sorted(cases, key=lambda c: c.id), 1)}

    def _log(msg: str) -> None:
        for cid, alias in aliases.items():
            msg = msg.replace(cid, alias)
        log(msg)
    return _log


def summarize(raw_doc: dict, verdicts: dict) -> dict:
    """Aggregate-only view of a held-out raw results document: safe to commit."""
    slices = {k: v for k, v in score(raw_doc, verdicts)["slices"].items() if k.startswith("heldout/")}
    return {"cases": len(raw_doc["cases"]), "status": raw_doc["status"], "slices": slices}


def attach_summary(public_path: Path) -> bool:
    """Recomputes the held-out summary inside a committed results file from its raw file.
    Returns False (and leaves the file alone) when the raw file is not available locally."""
    raw = raw_path(public_path)
    if not raw.exists():
        return False
    doc = json.loads(public_path.read_text())
    doc["heldout"] = summarize(json.loads(raw.read_text()), load_verdicts(raw))
    public_path.write_text(json.dumps(doc, indent=1))
    return True


def all_slices(doc: dict, verdicts: dict) -> dict:
    """Public slices scored from records, plus held-out slices from the aggregate summary."""
    return {**score(doc, verdicts)["slices"], **(doc.get("heldout") or {}).get("slices", {})}


def leaks(doc: dict) -> list[str]:
    """Problems that would reveal held-out cases if this results document were committed.
    Messages carry counts only, never ids."""
    problems = []
    held = [cid for cid, t in doc.get("cases", {}).items() if t.get("split") != "public"]
    if held:
        problems.append(f"{len(held)} non-public case(s) in 'cases'")
    unknown = [r for r in doc.get("records", []) if r.get("case") not in doc.get("cases", {})
               or r.get("case") in held]
    if unknown:
        problems.append(f"{len(unknown)} record(s) for non-public or unknown cases")
    summary = doc.get("heldout") or {}
    if set(summary) - {"cases", "status", "slices"}:
        problems.append("held-out summary has non-aggregate fields")
    if any(not k.startswith("heldout/") for k in summary.get("slices", {})):
        problems.append("held-out summary has non-held-out slices")
    return problems
