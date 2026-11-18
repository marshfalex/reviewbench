"""The one reviewer interface: ReviewRequest (diff + context) -> ReviewResult (findings JSON).

Prompt, output schema and parsing are adapted from fda-device-rag's
tools/ai_review/review.py. They are part of the benchmark definition: change
them and you must bump BENCH_VERSION.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

from reviewbench.context import ReviewRequest

CATEGORIES = ["correctness", "security", "maintainability"]
SEVERITIES = ["critical", "high", "medium", "low"]

SYSTEM_PROMPT = """You are a senior engineer reviewing a pull request.
You get the diff, and you may also get full files from the repository for
context (role="changed": a file the PR modifies, shown after the change;
role="related": another file from the repository).
Report only real, specific problems introduced or exposed by the changed lines:
bugs, security vulnerabilities (injection, secrets, missing authz/authn,
unsafe deserialization, race conditions), and maintainability issues that
would matter to a reviewer. Do not comment on style a linter would catch,
and do not praise. If the PR has no problems, return an empty list.

For each finding give the file path exactly as it appears in the diff, the
line number in the NEW version of the file, a category, a severity, a
one-line title, and a short explanation with a concrete fix.
Severity guide: critical = exploitable or data loss; high = likely bug in
normal use; medium = bug in edge cases or notable risk; low = minor."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "line": {"type": "integer"},
                    "category": {"type": "string", "enum": CATEGORIES},
                    "severity": {"type": "string", "enum": SEVERITIES},
                    "title": {"type": "string"},
                    "explanation": {"type": "string"},
                },
                "required": ["path", "line", "category", "severity", "title", "explanation"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["summary", "findings"],
    "additionalProperties": False,
}


@dataclass
class Finding:
    path: str
    line: int
    category: str
    severity: str
    title: str
    explanation: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReviewResult:
    summary: str
    findings: list[Finding]
    error: str | None = None  # set when the review did not happen (too large, refusal, API error)
    usage: dict = field(default_factory=dict)  # input/output tokens, served model, ...


def parse_review(raw_json: str) -> tuple[str, list[Finding]]:
    """Validates the model's JSON into Findings, dropping malformed items
    rather than failing the whole review."""
    data = json.loads(raw_json)
    findings = []
    for item in data.get("findings", []) or []:
        try:
            category = str(item["category"]).strip().lower()
            severity = str(item["severity"]).strip().lower()
            f = Finding(
                path=str(item["path"]).removeprefix("b/"),
                line=int(item["line"]),
                category=category if category in CATEGORIES else "maintainability",
                severity=severity if severity in SEVERITIES else "low",
                title=str(item["title"]),
                explanation=str(item["explanation"]),
            )
        except (KeyError, TypeError, ValueError):
            continue
        findings.append(f)
    return str(data.get("summary", "")), findings


class Reviewer:
    """Adapter base. Subclasses implement _review(); review() enforces the
    per-provider prompt budget so oversized requests become a recorded error
    instead of a truncation or a crash."""

    provider: str = ""
    default_model: str = ""
    max_prompt_chars: int = 400_000
    # USD per 1M tokens (input, output); (0, 0) = free. Used for the pre-run estimate.
    price_per_mtok: tuple[float, float] = (0.0, 0.0)

    def __init__(self, model: str | None = None):
        self.model = model or self.default_model

    @property
    def is_paid(self) -> bool:
        return self.price_per_mtok != (0.0, 0.0)

    def review(self, request: ReviewRequest) -> ReviewResult:
        prompt = request.render()
        if len(prompt) > self.max_prompt_chars:
            return ReviewResult("", [], error=f"too_large: {len(prompt)} chars > {self.max_prompt_chars}")
        return self._review(prompt)

    def _review(self, prompt: str) -> ReviewResult:  # pragma: no cover - interface
        raise NotImplementedError
