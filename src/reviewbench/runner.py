"""Runs a reviewer over cases x context levels x k runs and writes a versioned results file."""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path

from reviewbench import BENCH_VERSION
from reviewbench.adapters.base import OUTPUT_SCHEMA, SYSTEM_PROMPT, Reviewer
from reviewbench.cases import Case
from reviewbench.context import build_request

CHARS_PER_TOKEN = 4
# Conservative output allowance per review, including any hidden reasoning tokens.
EST_OUTPUT_TOKENS = 4000


def case_truth(case: Case) -> dict:
    """Snapshot of the ground truth used, stored inside every results file."""
    return {"title": case.title, "difficulty": case.difficulty, "split": case.split, "tags": case.tags,
            "source_kind": case.source.get("kind"),
            "bugs": [{"file": b.file, "lines": list(b.lines), "class": b.cls, "cwe": b.cwe,
                      "severity": b.severity} for b in case.bugs],
            "known_issues": [asdict(k) for k in case.known_issues]}


def estimate_cost(cases: list[Case], levels: list[str], k: int, reviewer: Reviewer) -> dict:
    in_tokens = 0
    for case in cases:
        for level in levels:
            in_tokens += (len(SYSTEM_PROMPT) + len(build_request(case, level).render())) // CHARS_PER_TOKEN
    in_tokens *= k
    n_requests = len(cases) * len(levels) * k
    out_tokens = n_requests * EST_OUTPUT_TOKENS
    pin, pout = reviewer.price_per_mtok
    return {"requests": n_requests, "input_tokens": in_tokens, "output_tokens_upper": out_tokens,
            "usd": round(in_tokens / 1e6 * pin + out_tokens / 1e6 * pout, 2)}


def results_path(out_dir: Path, provider: str, model: str, today: dt.date | None = None) -> Path:
    today = today or dt.date.today()
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", model).strip("-")
    base = f"{today.isoformat()}_{provider}-{slug}_v{BENCH_VERSION}"
    path, n = out_dir / f"{base}.json", 2
    while path.exists():
        path, n = out_dir / f"{base}-{n}.json", n + 1
    return path


# Errors that say nothing about the model, only that the provider didn't answer: resume
# re-runs these records. The HTTPError forms are what older adapter versions recorded.
_RETRYABLE = re.compile(r"^(rate_limited|transient)|HTTPError: (429|5\d\d) ")


def prompt_hash() -> str:
    """Fingerprint of the reviewer prompt and output schema (SPEC §10: frozen per version)."""
    import hashlib
    blob = SYSTEM_PROMPT + "\n" + json.dumps(OUTPUT_SCHEMA, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def retryable(error: str | None) -> bool:
    return bool(error) and bool(_RETRYABLE.search(error))


def has_retryable(doc: dict) -> bool:
    return any(retryable(r.get("error")) for r in doc.get("records") or [])


def find_resumable(out_dir: Path, provider: str, model: str, k: int, levels: list[str],
                   case_ids: set[str] | None = None) -> Path | None:
    """Newest partial results file for the same reviewer and settings, if any. A complete file
    that lacks some of case_ids (cases added since it ran) also counts, so only new cases run."""
    for path in sorted(out_dir.glob("*.json"), reverse=True):
        if path.name.endswith(".adjudications.json"):
            continue
        try:
            doc = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        partial = doc.get("status") == "partial" or (doc.get("heldout") or {}).get("status") == "partial"
        partial = partial or bool((case_ids or set()) - set(doc.get("cases") or {})) or has_retryable(doc)
        if (partial and doc.get("bench_version") == BENCH_VERSION
                and doc.get("provider") == provider and doc.get("model") == model
                and doc.get("k") == k and doc.get("levels") == levels):
            return path
    return None


def run(cases: list[Case], reviewer: Reviewer, levels: list[str], k: int, out_path: Path,
        log=lambda msg: print(msg, file=sys.stderr), max_minutes: float | None = None,
        clock=None) -> dict:
    """Run every (case, level, run) not already recorded in out_path (resume), checkpointing
    after each review. Stops early, leaving status "partial", once max_minutes is used up."""
    import time as _time
    clock = clock or _time.monotonic
    started = clock()
    if out_path.exists():
        doc = json.loads(out_path.read_text())
        done = {(r["case"], r["level"], r["run"]) for r in doc["records"]
                if not retryable(r.get("error"))}
        doc["records"] = [r for r in doc["records"] if (r["case"], r["level"], r["run"]) in done]
        old = doc.get("prompt_sha256")
        if old and old != prompt_hash():
            raise ValueError(f"{out_path.name} was run with a different prompt ({old}); "
                             f"resuming it with {prompt_hash()} would mix prompts in one result")
        doc.setdefault("prompt_sha256", prompt_hash())
        doc["cases"].update({c.id: case_truth(c) for c in cases})
        log(f"resuming {out_path.name}: {len(done)} reviews already done")
    else:
        doc = {
            "bench_version": BENCH_VERSION,
            "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "provider": reviewer.provider, "model": reviewer.model, "k": k, "levels": levels,
            "status": "partial",
            "prompt_sha256": prompt_hash(),
            "cases": {c.id: case_truth(c) for c in cases},
            "records": [],
        }
        done = set()
    # RISKS §6: a provider can swap what runs behind a model name. Every record in one results file
    # must come from the same served model, or the file silently mixes two models.
    served = {(r.get("usage") or {}).get("served_model") for r in doc["records"] if not r.get("error")}
    served.discard(None)
    doc["status"] = "partial"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for case in cases:
        for level in levels:
            request = None
            for r in range(k):
                if (case.id, level, r) in done:
                    continue
                if max_minutes is not None and (clock() - started) / 60 >= max_minutes:
                    log(f"time budget of {max_minutes} min used; stopping with status partial")
                    out_path.write_text(json.dumps(doc, indent=1))
                    return doc
                request = request or build_request(case, level)
                try:
                    result = reviewer.review(request)
                except Exception as e:  # recorded, not fatal: one flaky call must not lose the run
                    from reviewbench.adapters.base import ReviewResult
                    result = ReviewResult("", [], error=f"exception: {type(e).__name__}: {e}")
                now_serving = (result.usage or {}).get("served_model") if not result.error else None
                if now_serving and served and now_serving not in served:
                    out_path.write_text(json.dumps(doc, indent=1))
                    raise ValueError(
                        f"{out_path.name}: provider now serves {now_serving!r}, but earlier reviews in this file "
                        f"came from {sorted(served)}; refusing to mix models in one result. Start a new "
                        "results file for the new model.")
                if now_serving:
                    served.add(now_serving)
                findings = []
                for i, f in enumerate(result.findings):
                    findings.append({"id": f"{case.id}/{level}/r{r}/f{i}", **f.to_dict()})
                doc["records"].append({"case": case.id, "level": level, "run": r, "error": result.error,
                                       "summary": result.summary, "usage": result.usage,
                                       "findings": findings})
                log(f"{case.id} {level} run{r}: {len(findings)} findings"
                    + (f" ERROR {result.error}" if result.error else ""))
                out_path.write_text(json.dumps(doc, indent=1))  # checkpoint after every review
                if (result.error or "").startswith("rate_limited"):
                    # Every later call would hit the same quota; stop and let --resume retry it.
                    log("rate limited (quota); stopping with status partial. Resume later.")
                    return doc
    doc["status"] = "partial" if has_retryable(doc) else "complete"
    out_path.write_text(json.dumps(doc, indent=1))
    return doc
