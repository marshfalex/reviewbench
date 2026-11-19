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
- BENCH_VERSION stays 0.1, although SPEC says a case-set change needs a bump. The roadmap puts the
  CVE imports inside v0.1 and no v0.1 run has completed. The partial Groq file resumes with the new
  cases added, so it stays internally consistent. Owner: bump to 0.2 instead if you prefer.
- Couldn't restart the partial Groq run: workflow dispatch returned 403 "Resource not accessible by
  integration" (this session's GitHub access can't run Actions). The owner needs to trigger it.
- Next: CVE batch 2.
