"""Groq (free tier) and Ollama (local) via their OpenAI-compatible chat endpoints."""
from __future__ import annotations

import json
import os
import time

from reviewbench.adapters.base import OUTPUT_SCHEMA, SYSTEM_PROMPT, Reviewer, ReviewResult, parse_review

# Groq's per-minute token limit routinely asks for 3-7 min waits on large prompts; those are
# normal and must be slept. Only a wait longer than this signals a daily quota, which a run
# can't outlast: the review is recorded as rate_limited and the runner stops (status partial).
MAX_RETRY_WAIT_S = 1200


class OpenAICompatReviewer(Reviewer):
    url: str = ""
    key_env: str | None = None
    retries: int = 6

    def _headers(self) -> dict:
        if not self.key_env:
            return {}
        key = os.environ.get(self.key_env, "").strip()
        if not key:
            raise RuntimeError(f"{self.key_env} is not set; it is required for provider {self.provider!r}")
        return {"Authorization": f"Bearer {key}"}

    def _review(self, prompt: str) -> ReviewResult:
        import requests

        # JSON mode guarantees valid JSON but not our schema, so the schema goes
        # in the prompt and parse_review() drops anything malformed.
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT + "\n\nRespond with ONLY a JSON object matching "
                 "this JSON Schema:\n" + json.dumps(OUTPUT_SCHEMA)},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        }
        headers = self._headers()
        for attempt in range(self.retries):
            r = requests.post(self.url, headers=headers, json=payload, timeout=300)
            if r.status_code == 429:  # free-tier rate limit
                wait = float(r.headers.get("retry-after", 10 * (attempt + 1)))
                # A long retry-after means a daily quota, not a per-minute burst: waiting it out
                # would burn the job's time limit and lose the run. Record it and move on.
                if wait > MAX_RETRY_WAIT_S:
                    return ReviewResult("", [], error=f"rate_limited: retry-after {wait:.0f}s (quota)")
                if attempt < self.retries - 1:
                    time.sleep(wait)
                    continue
            if r.status_code == 413:  # bigger than this tier allows, despite our budget
                return ReviewResult("", [], error="too_large: HTTP 413")
            r.raise_for_status()
            body = r.json()
            try:
                summary, findings = parse_review(body["choices"][0]["message"]["content"])
            except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
                return ReviewResult("", [], error=f"unparseable_output: {e!r}")
            u = body.get("usage") or {}
            return ReviewResult(summary, findings, usage={
                "input_tokens": u.get("prompt_tokens"), "output_tokens": u.get("completion_tokens"),
                "served_model": body.get("model", self.model)})
        return ReviewResult("", [], error="rate_limited: retries exhausted")


class GroqReviewer(OpenAICompatReviewer):
    provider = "groq"
    default_model = "openai/gpt-oss-120b"
    url = "https://api.groq.com/openai/v1/chat/completions"
    key_env = "GROQ_API_KEY"
    # Groq's free tier caps request size far below large-model context windows.
    max_prompt_chars = 24_000


class OllamaReviewer(OpenAICompatReviewer):
    provider = "ollama"
    default_model = "qwen2.5-coder:7b"
    key_env = None
    max_prompt_chars = 100_000

    def __init__(self, model: str | None = None):
        super().__init__(model)
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.url = f"{host}/v1/chat/completions"
