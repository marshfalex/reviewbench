"""Context levels -- a measured variable, reported separately.

L0: the diff only.
L1: L0 + the full post-PR content of every file the diff changes.
L2: L1 + the case's context.related files (post-PR).
"""
from __future__ import annotations

from dataclasses import dataclass

from reviewbench.cases import Case

LEVELS = ("L0", "L1", "L2")


@dataclass(frozen=True)
class ContextFile:
    path: str
    content: str
    role: str  # "changed" or "related"


@dataclass(frozen=True)
class ReviewRequest:
    diff: str
    files: tuple[ContextFile, ...] = ()

    def render(self) -> str:
        """The user message every adapter sends. Identical across adapters."""
        parts = [f"<diff>\n{self.diff}\n</diff>"]
        for f in self.files:
            parts.append(f'<file path="{f.path}" role="{f.role}">\n{f.content}\n</file>')
        return "\n\n".join(parts)


def build_request(case: Case, level: str) -> ReviewRequest:
    if level not in LEVELS:
        raise ValueError(f"unknown context level {level!r}; use one of {LEVELS}")
    if level == "L0":
        return ReviewRequest(diff=case.diff)
    files = case.post_pr_files
    ctx = [ContextFile(p, files[p], "changed") for p in case.changed_files if p in files]
    if level == "L2":
        seen = {f.path for f in ctx}
        ctx += [ContextFile(p, files[p], "related") for p in case.related if p not in seen]
    return ReviewRequest(diff=case.diff, files=tuple(ctx))
