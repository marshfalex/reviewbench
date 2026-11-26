# Lessons: what went wrong and the check that prevents it

Every mistake a session made (or nearly made) on this project, with the rule or automated check
that now prevents it. Read this before starting work; add to it whenever something goes wrong.
Prefer turning a lesson into a test or validator rule over leaving it as advice.

## Pre-PR checklist (do all of these)
1. `ruff check .`, `python -m reviewbench validate`, `pytest` pass.
2. Every new test was run against the old code and **failed** there (`git stash push -- src`,
   run the test, `git stash pop`). Afterwards, confirm the intended change is still in the tree.
3. An **independent reviewer agent** (fresh context) reviewed the diff and its findings are fixed
   or explained in the PR description.
4. No held-out case, CVE or project is named anywhere in the diff, commit message or PR text.
5. Any number or claim in docs is regenerated from the current results, not edited by hand.

## Statistics and claims
- **Correlated runs counted as independent** (2026-11-24). Per-run recall intervals over
  bug × run treated k = 3 near-identical runs as 3 observations, overstating evidence ~√3-fold,
  and a published "model A beats model B" claim rested on it. Rule: the unit of an interval is
  the thing that varies independently (the bug). Check: `per_run_by_bug` in `report.py`.
- **A metric shown while its inputs were missing** (2026-11-23). "Precision 100%" was computed
  with every unjudged finding left out. Rule: never show a rate when most of its denominator is
  unmeasured; say "not measured (N unjudged)". Check: `precision_cell` in `report.py`.
- **Two estimators in one cell** (2026-11-24). "51/68 runs (74%)" put run counts next to a
  per-bug mean. Rule: label which estimator a number is.
- **Ranking claims.** Never claim one model beats another unless the per-bug intervals don't
  overlap, and have an independent reviewer check the claim before it is published.

## Benchmark runs
- **Provider failures counted as finished reviews** (2026-11-23, again 2026-11-24). 429s, then
  timeouts/connection drops/garbled bodies, were recorded as generic exceptions, so resume skipped
  them and n shrank silently while the file said "complete". Rule: anything that says nothing
  about the model is `rate_limited:` or `transient:` and therefore retryable; a file with
  retryable errors is never "complete". Check: `retryable()` in `runner.py` and the network-error
  tests in `tests/test_runner.py`.
- **"Newest" model by string order** (2026-11-24). `pick_auto` used `max()` on ids, which picks
  the alphabetically last (gpt-oss-20b over gpt-oss-120b). Rule: compare versions naturally, and
  use narrow `auto:` needles. Check: `test_pick_auto_prefers_the_bigger_number_not_the_later_string`.
- **A model can change behind its name.** Check: `run` refuses to mix served models in one file.

## Cases
- **A planted bug that did no harm** (2026-11-23). The unprotected view crashed before deleting
  anything. Rule: trace every planted bug to its concrete harm, not "looks wrong".
- **Duplicate CVE / wrong fix commit** (2026-11-24). The commit first picked for CVE-2024-34064
  was the fix for a different CVE that was already a public case. Rule: pin the fix commit with
  `git tag --contains` against the advisory's fixed version. Check: a test fails if two cases
  share a `source.ref`.
- **Upstream excerpts that don't reproduce the commit** (2026-11-24): same-named `@overload`
  stubs, two class headers for one class, module-level constants and their comments, methods that
  exist on one side only. Rule: a case's `pr.diff` +/- lines must equal the upstream commit's
  (reversed for CVE cases). Check: run `scripts/upstream_excerpt.py` and compare; skip commits
  whose change sits in a class body rather than a function.
- **Fair findings on controls** (2026-11-24). A control can contain a real latent quirk (py-0067's
  in-place list mutation). Rule: when the reviewer agent spots one, add it to `known_issues` so a
  model that flags it isn't charged a false positive.
- **Defect terms that filter nothing** (2026-11-25). Terms copied from the code's own identifiers
  (`format`, `path`, `verify`) appear in every finding on that line, and short substrings match
  unrelated words (`cert` in "certain", `..` in an ellipsis). Rule: a term names the defect
  concept, not the code; avoid substrings under 4 characters unless distinctive (`303`, `../`).
- **Tightening terms creates false misses** (2026-11-26). Stricter defect_terms dropped two correct
  catches. Rule: after changing terms, read every finding the calibration script reports as "would
  no longer count", not just the count.
- **Controls next to security fixes.** Never take a control from a security fix or from the same
  file as one.

## Held-out secrecy
- **Held-out cases named in the public roadmap** (2026-11-19 to 2026-11-24), and a session nearly
  named one in the journal. Rule: never name held-out cases, their CVEs or their projects in this
  repository, even to explain why something was skipped. Say "a held-out case" or "a security
  fix". The automated safety check caught the near-miss; don't rely on it.

## Tooling and process
- **Hand arithmetic in tests** (2026-11-23): an expected Cohen's kappa was worked out wrongly.
  Rule: compute expected values independently (by code or a second derivation).
- **Verification that undid the change** (2026-11-23): `git checkout <file>` after a "does the
  test fail without the fix?" step reverted the fix itself. Rule: after any revert-to-test step,
  re-check the intended change is present before committing.
- **`rm -rf` on a shell variable** (2026-11-24) was blocked as potentially destructive. Rule:
  delete only through code that asserts the path is inside the scratch directory.
- **Editing your own oversight rules** (2026-11-23) was blocked. Rule: never loosen review or
  merge rules yourself; propose the change to the owner in a PR description.
- **Mixed PRs.** One branch per session means unrelated work can land in one PR. Wait for the
  previous PR to merge before starting the next commit.
