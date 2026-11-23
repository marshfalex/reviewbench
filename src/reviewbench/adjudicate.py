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


# --- Blind adjudication and a second rater (SPEC §10) ---------------------------------------
# Pooling findings from several results files and shuffling them hides which model wrote each
# one, so a verdict can't lean on who produced it. A second rater re-judges a fixed 20% sample
# of the primary human verdicts, blind to them too, and Cohen's kappa reports the agreement.

SECOND_RATER_SHARE = 5  # 1 in 5 findings (by a hash of the finding id) goes to the second rater


def second_path(results_path: Path) -> Path:
    return results_path.with_name(results_path.stem + ".adjudications.second.json")


def load_second(results_path: Path) -> dict:
    p = second_path(results_path)
    return json.loads(p.read_text())["verdicts"] if p.exists() else {}


def save_second(results_path: Path, verdicts: dict) -> None:
    second_path(results_path).write_text(json.dumps({"verdicts": dict(sorted(verdicts.items()))}, indent=1))


def in_second_sample(finding_id: str) -> bool:
    import hashlib
    return int(hashlib.sha256(finding_id.encode()).hexdigest(), 16) % SECOND_RATER_SHARE == 0


def blind_queue(paths: list[Path], rater: str = "primary", seed: int = 0) -> list[tuple]:
    """(results path, case truth, finding) for every finding this rater still has to judge,
    pooled across files and shuffled. Primary: unadjudicated findings. Second: findings in the
    20% sample that have a primary human verdict and no second verdict yet."""
    import random
    queue = []
    for p in paths:
        doc = json.loads(p.read_text())
        primary = load_verdicts(p)
        labels = score(doc, primary)["labels"]
        second = load_second(p)
        for rec in doc["records"]:
            for f in rec["findings"]:
                if rater == "primary":
                    todo = labels.get(f["id"]) == "unadjudicated"
                else:
                    todo = (primary.get(f["id"], {}).get("by") == "human" and f["id"] not in second
                            and in_second_sample(f["id"]))
                if todo:
                    queue.append((p, doc["cases"][rec["case"]], f))
    random.Random(seed).shuffle(queue)
    return queue


def interactive_blind(paths: list[Path], rater: str = "primary", seed: int = 0,
                      ask=input, show=print) -> int:
    """Judge pooled findings without showing the model, provider, file or finding id. Verdicts
    are saved after each answer (primary into the usual file, second into .second.json)."""
    queue = blind_queue(paths, rater, seed)
    show(f"{len(queue)} finding(s) to judge as the {rater} rater; the model is hidden.")
    judged = 0
    for i, (p, truth, f) in enumerate(queue, 1):
        show(f"\n=== {i}/{len(queue)}  case: {truth['title']}")
        show(f"{f['severity']} {f['category']} {f['path']}:{f['line']} -- {f['title']}\n{f['explanation']}")
        ans = ask("[v]alid / [i]nvalid / [s]kip / [q]uit > ").strip().lower()
        if ans.startswith("q"):
            break
        if ans[:1] not in ("v", "i"):
            continue
        note = ask("note (optional) > ").strip()
        v = {"verdict": "valid" if ans[0] == "v" else "invalid", "by": "human", "blind": True, "note": note}
        if rater == "primary":
            store = load_verdicts(p)
            store[f["id"]] = v
            save_verdicts(p, store)
        else:
            store = load_second(p)
            store[f["id"]] = v
            save_second(p, store)
        judged += 1
    return judged


def cohen_kappa(pairs: list[tuple[str, str]]) -> float | None:
    """Cohen's kappa for two raters' valid/invalid verdicts on the same findings."""
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    pa = sum(a == "valid" for a, _ in pairs) / n
    pb = sum(b == "valid" for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def agreement(paths: list[Path]) -> dict:
    """Primary-vs-second agreement over every finding both raters judged."""
    pairs = []
    for p in paths:
        primary, second = load_verdicts(p), load_second(p)
        pairs += [(primary[k]["verdict"], v["verdict"]) for k, v in second.items()
                  if primary.get(k, {}).get("by") == "human"]
    agree = sum(a == b for a, b in pairs)
    return {"n": len(pairs), "agree": agree, "kappa": cohen_kappa(pairs)}
