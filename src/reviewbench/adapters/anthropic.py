"""Claude via the Anthropic SDK. PAID: the CLI prints a cost estimate and
requires --yes before running it."""
from __future__ import annotations

import json
import os

from reviewbench.adapters.base import OUTPUT_SCHEMA, SYSTEM_PROMPT, Reviewer, ReviewResult, parse_review

# USD per 1M tokens (input, output), Anthropic first-party API, checked 2026-11.
PRICES = {
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-fable-5-2": (8.00, 40.00),
}


class AnthropicReviewer(Reviewer):
    provider = "anthropic"
    default_model = "claude-opus-5-5"
    max_prompt_chars = 400_000

    def __init__(self, model: str | None = None):
        super().__init__(model)
        # Unknown model: assume the most expensive listed price so the estimate errs high.
        self.price_per_mtok = PRICES.get(self.model, max(PRICES.values()))

    def _review(self, prompt: str) -> ReviewResult:
        import anthropic  # lazy: keeps the SDK out of the core/test deps

        if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
            raise RuntimeError("ANTHROPIC_API_KEY is not set; it is required for provider 'anthropic'")
        client = anthropic.Anthropic()
        with client.beta.messages.stream(
            model=self.model,
            max_tokens=32000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=SYSTEM_PROMPT,
            output_config={"effort": "high", "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            response = stream.get_final_message()
        usage = {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens,
                 "served_model": response.model}
        if response.stop_reason == "refusal":
            return ReviewResult("", [], error="refusal", usage=usage)
        text = next((b.text for b in response.content if b.type == "text"), "")
        try:
            summary, findings = parse_review(text)
        except json.JSONDecodeError as e:
            return ReviewResult("", [], error=f"unparseable_output: {e!r}", usage=usage)
        return ReviewResult(summary, findings, usage=usage)
