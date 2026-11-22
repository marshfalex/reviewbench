# Project journal

Append-only. One short entry per working session: what was done, what was learned, what's next.

## 2026-11-18 — v0.1 scaffold + autonomy setup
- Built v0.1: 22 Python cases (ported from the fda-device-rag prototype), runner with L0/L1/L2
  context, k runs, any-of-k/all-of-k, adjudication-aware precision, Wilson CIs, groq/anthropic/
  ollama adapters, cost gate, benchmark workflow, leaderboard generation. 47 tests pass.
- Learned: two seed labels pointed past end-of-file (float-money, cursor); the validator caught
  them. L1 adds nothing for new-file cases, so modify-existing-file cases are needed for L0 vs L1
  to mean anything.
- Prototype results (Groq gpt-oss-120b, 3 runs): textbook 36/36, hard 13/18; cursor-pagination
  missed 0/3; float-money caught 1/3 on identical input.
- Added CLAUDE.md (session rules), ROADMAP.md, this journal. Sessions now run on a schedule.
- Next: held-out loader, then CVE batch 1.

## 2026-11-19 — held-out loader
- Held-out cases load from `$REVIEWBENCH_HELDOUT` (or `--heldout`, else `heldout/` if present); a
  configured dir that doesn't exist is an error rather than a silently public-only run.
- `run` reviews held-out cases into git-ignored `results/raw/<stem>.heldout.json`; the committed
  results file gets only a `heldout` aggregate (slices of hits/n/rate/CI). Logs alias ids to
  `heldout-NN` because CI logs of a public repo are public. `adjudicate` handles the raw file
  and refreshes the aggregate; `leaderboard` refuses files with held-out cases or records.
- Decision: wrapped `runner.run()` (called once for public, once for held-out) instead of changing
  it. PR #3 (resumable runs) merged mid-session; after rebasing, held-out cases start only once the
  public part is complete, share the `--max-minutes` budget, and resume with `--resume` (the raw
  path derives from the public one; `find_resumable` also picks a file whose held-out part is
  partial). Fixed in passing: a resumed `run` overwrote existing verdict files with rules-only ones.
- Learned: earlier sessions' version of this was never pushed (no repo access); rebuilt from
  scratch. Tests use a renamed copy of py-0001 as a fake held-out case and assert its id, title,
  path and finding text appear in no committed file and not in stderr.
- Next: CVE batch 1 (the private held-out repo is `[owner]`).

## 2026-11-19 — held-out repo follow-up (same session)
- PR #4 merged. The owner created the empty private repo `marshfalex/reviewbench-heldout` and asked
  for the 5 held-out CVE cases to be built there. Attaching that repo to this session was denied
  by the session's permission check, so no cases were built. I did not try any workaround.
- Roadmap: marked the `[owner]` private-repo item as partial (repo exists, cases pending). Added an
  `[owner]` item for CI access to held-out cases: a read-only fine-grained token, an opt-in
  checkout step, and the limit that raw held-out results don't survive an ephemeral runner. It
  replaces the matching unapproved idea.
- Later the owner approved attaching the repo. The 5 cases were merged into `reviewbench-heldout`;
  details live there, not here. Method: pin the fix commit with `git log`
  between release tags, reverse its source hunks, and excerpt big files with `# [... omitted ...]`
  markers to stay under Groq's 24,000-char budget (watch L2: Django's related file pushed it over
  until trimmed).
- Learned: an empty GitHub repo has no base branch for a PR. The owner chose to seed `main` with a
  README-only commit.
- Next: CVE batch 1 in the public repo. The same build method should work.

## 2026-11-19 (evening) — CVE batch 1
- Added py-0023..py-0027: requests CVE-2018-18074, urllib3 CVE-2023-43804, Jinja2 CVE-2024-22195,
  aiohttp CVE-2024-23334, GitPython CVE-2022-24439. Each `source.ref` pins the fix commit found
  with `git log` between release tags, the license was checked at that commit, and `pr.diff` is the
  fix's source hunks reversed. Big files are excerpted with `# [... omitted ...]` markers; the
  largest prompt is urllib3 at L2, with 22,285 chars.
- Decisions:
  - requests: pinned 3331e2a (scheme/port/host check), not the later 857e9b7 rework that allows
    http->https upgrades.
  - GitPython: pinned 2625ed9, whose message names the CVE (block `ext::` and unsafe clone
    options). The sibling commits in that PR (`--` separators, broader option blocking) are out
    of scope.
  - aiohttp and GitPython also have the same bug at a second call site (url_for; Repo.clone).
    Those are `known_issues`, not extra planted bugs.
  - Difficulty: requests, urllib3 and GitPython are `easy` (the diff visibly removes a security
    check); Jinja2 and aiohttp are `hard`.
- BENCH_VERSION stays 0.1 (confirmed), although SPEC says a case-set change needs a bump. The
  roadmap puts the CVE imports inside v0.1 and no v0.1 run has completed. The partial Groq file
  resumes with the new cases added, so it stays internally consistent.
- Couldn't restart the partial Groq run: workflow dispatch returned 403 "Resource not accessible by
  integration" (this session's GitHub access can't run Actions). Since then #10 added a 6-hourly
  scheduled lineup run, which continues partial results without a session triggering it.
- Merged main (with #10) into this branch: the ROADMAP conflict was resolved by keeping #10's new
  items and ticking batch 1.
- Next: CVE batch 2.

## 2026-11-19 — held-out never goes to logging providers
- The owner asked for the held-out set to be protected. `run` and `estimate` now send held-out
  cases only to a provider/model that `lineup.yaml` marks `heldout_ok: true` (today: groq's
  gpt-oss-120b). Anything else skips them with a log line that names no case. An `auto:<text>`
  entry covers that provider's matching models. `--allow-heldout` is the explicit override for
  local endpoints.
- Decision: default to refuse. A missing lineup, a missing entry, or `heldout_ok: 'true'` (a
  string) all count as "no", so a typo can't leak the set.
- Tests: refusal cases record every prompt sent and assert the held-out code never appears in
  one. With the guard disabled, 6 of them fail.
- Next: CVE batch 2 (batch 1 merged in #9).

## 2026-11-20 — findings report v0.1, first cut
- Wrote `docs/findings/v0.1.md` from the only complete run, cerebras qwen-3.8-27b, on the 22
  synthetic cases. The CVE cases were added after it ran. The groq, gemini and openrouter runs are
  still partial and are left out.
- Results: recall 18/18 (100%, 82–100) at L0 and L2, 17/18 at L1; hard bugs 6/6 everywhere.
  That's a ceiling, so the synthetic set doesn't discriminate.
- Learned:
  - (1) All 66 (case, level) groups are byte-identical across the 3 runs (temperature 0 on a
    deterministic provider), so any-of-k = all-of-k says nothing here.
  - (2) The only miss (py-0004 at L1, 0/3) has a summary naming the bug but no findings, which
    points to `parse_review` dropping malformed findings. The raw output isn't stored, so it can't
    be proven.
  - (3) Precision reads 100% only because nothing is adjudicated. Two controls have plausible-real
    unadjudicated findings.

  Ideas for (1) and (2) are added under "Ideas (unapproved)".
- Next: CVE batch 2. Update the report when another run completes.

## 2026-11-22 — findings report: Groq added (maintenance on #13)
- Still 2 PRs open, so no new roadmap work. Groq's run completed on 27 cases, which made #13's
  "only complete run" wrong, so I updated the report in #13.
- Learned: most Groq CVE "misses" are the right bug flagged just outside the ±2 window, or at the
  second call site (scored `known`). The batch 1 bug ranges I wrote are too narrow. Also, Gemini and
  OpenRouter are `complete` with ~80% HTTP 429 errors, because 429 isn't classed as `rate_limited`.
  Both are added as ideas and both need the owner.
