"""Human adjudication of findings that are neither a planted-bug hit nor a known issue.

Verdicts live next to the results they judge: results/<stem>.adjudications.json,
keyed by finding id. Reusable rules (adjudications/rules.yaml: case id ->
[{match, verdict, note}]) pre-fill verdicts for findings the same model, or
another one, has raised before; those are recorded with by="rule".
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from reviewbench.scoring import norm, score


def verdicts_path(results_path: Path) -> Path:
    return results_path.with_name(results_path.stem + ".adjudications.json")


def load_verdicts(results_path: Path) -> dict:
    p = verdicts_path(results_path)
    return json.loads(p.read_text())["verdicts"] if p.exists() else {}


def save_verdicts(results_path: Path, verdicts: dict) -> None:
    verdicts_path(results_path).write_text(json.dumps({"verdicts": dict(sorted(verdicts.items()))}, indent=1))


def load_rules(path: Path) -> dict:
    return (yaml.safe_load(path.read_text()) or {}) if path.exists() else {}


def apply_rules(results: dict, verdicts: dict, rules: dict) -> int:
    """Fills verdicts for unadjudicated findings from rules. Returns how many were added."""
    labels = score(results, verdicts)["labels"]
    added = 0
    for rec in results["records"]:
        for f in rec["findings"]:
            if labels.get(f["id"]) != "unadjudicated":
                continue
            text = norm(f["title"] + " " + f["explanation"])
            for rule in rules.get(rec["case"], []):
                if norm(rule["match"]) in text:
                    verdicts[f["id"]] = {"verdict": rule["verdict"], "by": "rule",
                                         "note": rule.get("note", "")}
                    added += 1
                    break
    return added


def interactive(results: dict, verdicts: dict, ask=input, show=print) -> int:
    """Prompts for each remaining unadjudicated finding. Returns how many were judged."""
    labels = score(results, verdicts)["labels"]
    judged = 0
    for rec in results["records"]:
        truth = results["cases"][rec["case"]]
        for f in rec["findings"]:
            if labels.get(f["id"]) != "unadjudicated":
                continue
            show(f"\n=== {f['id']}  ({truth['title']})")
            show(f"{f['severity']} {f['category']} {f['path']}:{f['line']} -- {f['title']}\n{f['explanation']}")
            ans = ask("[v]alid / [i]nvalid / [s]kip / [q]uit > ").strip().lower()
            if ans.startswith("q"):
                return judged
            if ans[:1] in ("v", "i"):
                note = ask("note (optional) > ").strip()
                verdicts[f["id"]] = {"verdict": "valid" if ans[0] == "v" else "invalid",
                                     "by": "human", "note": note}
                judged += 1
    return judged
