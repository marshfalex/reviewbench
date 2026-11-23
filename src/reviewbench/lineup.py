"""The model lineup the scheduled benchmark works through (lineup.yaml)."""
from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from reviewbench import BENCH_VERSION
from reviewbench.adapters import ADAPTERS

EXCLUDE = ("preview", "exp", "lite", "tts", "image", "audio", "live", "embed", "vision", "guard")


def pick_auto(model_ids: list[str], needle: str) -> str | None:
    """Newest-looking id containing `needle`, skipping preview/experimental variants."""
    ids = [m.removeprefix("models/") for m in model_ids]
    ok = [m for m in ids if needle.lower() in m.lower() and not any(x in m.lower() for x in EXCLUDE)]
    return max(ok) if ok else None


def list_models(provider: str) -> list[str]:
    import requests

    cls = ADAPTERS[provider]
    url = cls.url.replace("/chat/completions", "/models")
    headers = {"Authorization": f"Bearer {os.environ[cls.key_env]}"} if cls.key_env else {}
    r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    return [m["id"] for m in r.json().get("data", [])]


def completed(results_dir: Path, provider: str, model: str, k: int, levels: list[str],
              case_ids: set[str] | None = None) -> bool:
    """A complete results file exists for these settings and covers every case in case_ids."""
    for path in results_dir.glob("*.json"):
        if path.name.endswith(".adjudications.json"):
            continue
        try:
            doc = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if (doc.get("status") == "complete" and doc.get("bench_version") == BENCH_VERSION
                and doc.get("provider") == provider and doc.get("model") == model
                and doc.get("k") == k and doc.get("levels") == levels
                and not (case_ids or set()) - set(doc.get("cases") or {})):
            return True
    return False


def plan(lineup_path: Path, results_dir: Path, lister=list_models, log=print,
         case_ids: set[str] | None = None) -> list[dict]:
    """Entries to run now: provider key present, model resolved, not yet complete."""
    cfg = yaml.safe_load(lineup_path.read_text())
    k, levels = int(cfg.get("k", 3)), [x.strip() for x in str(cfg.get("levels", "L0,L1,L2")).split(",")]
    out = []
    for entry in cfg["models"]:
        provider, model = entry["provider"], str(entry.get("model") or "")
        cls = ADAPTERS.get(provider)
        if cls is None or getattr(cls, "is_paid_provider", False) or provider == "anthropic":
            log(f"skip {provider}: not a free provider")
            continue
        key_env = getattr(cls, "key_env", None)
        if key_env and not os.environ.get(key_env, "").strip():
            log(f"skip {provider}: {key_env} not set")
            continue
        if model.startswith("auto:"):
            try:
                resolved = pick_auto(lister(provider), model[5:])
            except Exception as e:  # a listing failure must not stop the other providers
                log(f"skip {provider}: could not list models ({type(e).__name__}: {e})")
                continue
            if not resolved:
                log(f"skip {provider}: no model matches {model!r}")
                continue
            log(f"{provider}: {model} -> {resolved}")
            model = resolved
        if completed(results_dir, provider, model, k, levels, case_ids):
            log(f"skip {provider}/{model}: already complete")
            continue
        out.append({"provider": provider, "model": model, "k": str(k), "levels": ",".join(levels)})
    return out
