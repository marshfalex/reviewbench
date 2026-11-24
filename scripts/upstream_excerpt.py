"""Excerpt one upstream commit into a ReviewBench case: top-level imports + the changed function(s).

Usage: python scripts/upstream_excerpt.py <git clone> <sha> <path in repo> <out dir>

Writes <out>/before/<path> (at sha^) and <out>/after/<path> (at sha). Diff them with
`git diff --no-index` to get pr.diff, then compare its +/- lines with the upstream commit's: they
must be identical. Functions are matched by changed line numbers on each side, so same-named
`@overload` stubs are not pulled in.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys


def show(repo: str, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def changed_lines(repo: str, sha: str, path: str) -> tuple[list[int], list[int]]:
    d = subprocess.run(["git", "-C", repo, "diff", "-U0", f"{sha}^", sha, "--", path],
                       capture_output=True, text=True, check=True).stdout
    old: list[int] = []
    new: list[int] = []
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", d, re.M):
        a, b, c, e = int(m[1]), int(m[2] or 1), int(m[3]), int(m[4] or 1)
        old += list(range(a, a + max(b, 1)))
        new += list(range(c, c + max(e, 1)))
    return old, new


def functions(tree: ast.AST) -> list[tuple[int, int, str | None]]:
    """(first line incl. decorators, last line, enclosing class name) of every function."""
    out = []

    def walk(node: ast.AST, cls: str | None) -> None:
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.ClassDef):
                walk(ch, ch.name)
            elif isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = min([ch.lineno] + [d.lineno for d in ch.decorator_list])
                out.append((start, ch.end_lineno or ch.lineno, cls))

    walk(tree, None)
    return out


def touched_classes(text: str, lines: list[int]) -> set[str]:
    tree = ast.parse(text)
    return {c for s, e, c in functions(tree) if c and any(s <= x <= e for x in lines)}


def excerpt(text: str, lines: list[int], path: str, classes: set[str] = frozenset()) -> str:
    """classes: class headers to emit even if none of their methods changed on this side (a
    method added or removed by the commit exists on one side only, but the header must not)."""
    tree = ast.parse(text)
    src = text.splitlines()
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    body = [f"# Excerpt of {path} from an upstream project; code outside the functions below is omitted."]
    body += [line for n in imports for line in src[n.lineno - 1:n.end_lineno]] + [""]
    # Module-level statements the commit touches (e.g. a new compiled regex constant).
    for n in tree.body:
        if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        end = n.end_lineno or n.lineno
        start = n.lineno
        while start > 1 and src[start - 2].lstrip().startswith("#"):  # its leading comment block
            start -= 1
        if any(start - 1 <= x <= end + 1 for x in lines):
            body += ["", *src[start - 1:end]]
    prev_cls = None
    picked = {f for f in functions(tree) if any(f[0] <= x <= f[1] for x in lines)}
    class_lines = {n.name: n.lineno for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
    for cls in sorted(set(classes) - {c for _, _, c in picked}):
        if cls in class_lines:  # header only, at the class's position
            picked.add((class_lines[cls], class_lines[cls] - 1, cls))
    for start, end, cls in sorted(picked):
        if cls and cls == prev_cls:  # another method of the same class: one header for all of them
            body += [""]
        else:
            body += ["", ""]
            if cls:
                body += [f"class {cls}:", "    # [... omitted ...]", ""]
        body += src[start - 1:end]
        prev_cls = cls
    return "\n".join(body) + "\n"


def main(repo: str, sha: str, path: str, out: str) -> None:
    old, new = changed_lines(repo, sha, path)
    texts = {"before": show(repo, f"{sha}^", path), "after": show(repo, sha, path)}
    classes = touched_classes(texts["before"], old) | touched_classes(texts["after"], new)
    for tag, lines in (("before", old), ("after", new)):
        dest = os.path.join(out, tag, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w") as fh:
            fh.write(excerpt(texts[tag], lines, path, classes))


if __name__ == "__main__":
    main(*sys.argv[1:5])
