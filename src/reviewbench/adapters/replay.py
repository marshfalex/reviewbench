"""Offline adapter for tests and dry runs: returns canned findings, makes no API calls."""
from __future__ import annotations

from collections.abc import Callable

from reviewbench.adapters.base import Finding, Reviewer, ReviewResult


class ReplayReviewer(Reviewer):
    provider = "replay"
    default_model = "none"

    def __init__(self, model: str | None = None, fn: Callable[[str], list[Finding]] | None = None):
        super().__init__(model)
        self.fn = fn or (lambda prompt: [])

    def _review(self, prompt: str) -> ReviewResult:
        return ReviewResult("replay", list(self.fn(prompt)), usage={"served_model": self.model})
