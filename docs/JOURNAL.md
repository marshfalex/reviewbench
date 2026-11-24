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

## 2026-11-23 — design review with the owner (v0.2 decisions)
- A structured grilling of the plan with the owner. The decisions are in SPEC §10 and a new
  "v0.2 redesign" roadmap section; nothing is implemented yet.
- Main finding: the benchmark looks too easy. Cerebras qwen-3.8-27b caught 54/54 per-run at L0
  (Wilson lower bound ~93%) with 0/12 control false alarms, including every author-labeled "hard"
  case. A pre-registered ceiling rule decides it once groq, gemini and nemotron finish.
- Corrected during the review: a noise flag on the control-FPR *upper* bound would flag every
  model (0/12 already gives ~24%), so the flag uses the point estimate, and controls go to ≥36.
- Held-out: `heldout_ok` was set without checking providers' training terms. Held-out runs are
  paused until a dated data-use table exists. No workflow references `REVIEWBENCH_HELDOUT` and no
  committed result mentions held-out cases, so they very likely never left the private repo; the
  owner will confirm from the run logs.
- Next: the ceiling write-up, then the provider data-use table.

## 2026-11-23 — provider errors were being counted as finished runs
- While pulling numbers for the ceiling write-up: gemini and nemotron results are marked `complete`
  but ~200 of their 243 reviews each are `exception: HTTPError: 429` (plus a few 503s). Their
  leaderboard rows (6/6, 100%) rest on the few cases that got through, and the scheduler would
  never rerun them.
- Cause: on the last retry, a 429 fell through to `raise_for_status()`. The runner recorded it as a
  generic exception, which resume treats as done, and the run kept going instead of stopping.
- Fix: a final 429 is `rate_limited`; 5xx is retried, then recorded as `transient`. `retryable()`
  also recognizes the old `HTTPError: 429/5xx` strings, so the existing files are repaired: a file
  holding retryable errors is `partial`, `find_resumable` picks it up, and `lineup.completed` no
  longer counts it. The next scheduled runs will redo only the failed reviews.
- Ceiling check so far (L0, public, per-run recall, Wilson lower bound): cerebras 54/54 (93.4%),
  groq 58/69 (73.7%). gemini and nemotron can't be judged until they rerun. Groq also had control
  false alarms in 3/12 runs (25%), which is over the 20% noise flag.
- Next: the leaderboard should mark partial results. Then the ceiling write-up, once gemini and
  nemotron finish.

## 2026-11-23 — leaderboard marks results with failed reviews
- The leaderboard now marks a row `(partial) (N reviews failed, to retry)` whenever its level holds
  retryable errors, even if the file says `complete` (the pre-#16 files do). Gemini and Nemotron
  no longer read as finished 6/6 results.
- Next: the ceiling write-up, once the scheduled runs have retried gemini and nemotron.

## 2026-11-23 — provider data-use table
- Added `docs/providers.md`. No lineup provider qualifies for held-out cases today: Gemini free and
  Mistral Experiment train on inputs (Mistral by default, with an opt-out); OpenRouter free depends
  on the host; Groq and Cerebras say they don't retain data, but neither public text forbids
  training. Groq's no-training clause reportedly sits in its Services Agreement, which we couldn't read.
- Groq was `heldout_ok: true`; it's now `false`. A held-out run approval now needs a "yes" row.
- Decision: "not stated" counts as no. The point of held-out cases is that nobody can train on
  them, so the burden is on the terms.
- Next: owner checks Groq's agreement and/or switches off Mistral training if they want a held-out
  model; sessions continue with cross-file L2 cases.
## 2026-11-23 — automerge workflow (owner request)
- The owner wants merges automatic. `.github/workflows/automerge.yml` merges a Claude-branch PR
  when `ci` passes on its current head, unless it's gated (.github/, pyproject.toml, prompt/schema,
  matcher, BENCH_VERSION, or adding `heldout_ok: true`). Gated PRs get `needs-owner` and wait.
  The owner can hold any PR by adding that label.
- Uses `workflow_run`, which always runs the copy on `main`, so a PR can't weaken its own gate.
- Merges done with GITHUB_TOKEN don't trigger other workflows; the push-to-main `ci` run won't fire
  for them. That's acceptable: the same commit already passed `ci` on the PR.

## 2026-11-23 — first cross-file (L2-only) cases
- py-0028 (authz bypass: `if not can_edit(...)` where can_edit returns an always-truthy Decision),
  py-0029 (seconds TTL added to a millisecond clock: sessions last 28.8 s), and py-0030 (control:
  f-string ORDER BY whose column is an Enum whitelisted in another file). Checked that the fact
  needed to judge each one appears in the prompt at L2 only, never at L0/L1.
- New case.yaml field `since: "0.2"`. These cases are validated now but not run until
  BENCH_VERSION is 0.2, so v0.1's 27-case set stays frozen while gemini/nemotron finish.
  Bumping BENCH_VERSION is gated (owner).
- Expected signal: a model that "catches" py-0028/29 at L0 is guessing; py-0030 at L0 should tempt
  SQL-injection false alarms that L2 removes. That's the context hypothesis in one table.
- Commits are now authored as the owner (their GitHub noreply address), with Claude as co-author.
- Next: large noisy-diff cases, then more controls toward 36.

## 2026-11-23 — leaderboard: per-run recall first, noise flag, prompt hash
- Leaderboard rows are sorted by per-run recall within each context level, with unfinished
  results last (otherwise gemini's 12/12 on a sliver of cases outranked groq's 58/69).
- Noise flag (SPEC §10): groq is flagged at L0 and L1 (control FPR 3/12 = 25%); nobody exceeds
  3 counted findings per review.
- New results files store `prompt_sha256` (prompt + output schema). Resuming a file made with a
  different prompt is refused, so one result never mixes prompts. Older files have no hash;
  resuming them stamps the current one (the prompt hasn't changed since v0.1 started).
- Split the roadmap item: blind adjudication + κ is still open.
- Next: blind adjudication, then large noisy-diff cases.

## 2026-11-23 — blind adjudication and a second rater
- `reviewbench adjudicate-blind <results...>` pools findings across results files, shuffles them
  (seeded) and shows only the case title and the finding: no model, provider, file name or finding
  id. Verdicts carry `"blind": true` and are saved after each answer, so quitting loses nothing.
- `--rater second` re-judges a fixed 20% sample (hash of the finding id, so it's stable as results
  grow) of the primary *human* verdicts into a separate `.second.json`; `reviewbench agreement`
  prints agreement and Cohen's kappa. The second rater could later be an LLM, labeled as such.
- Caught my own arithmetic error in the kappa test (assumed pe = .5); the code was right.
- Doing the pass is an `[owner]` item (it's human judgment). Next: large noisy-diff cases.

## 2026-11-23 — first noisy-diff cases
- py-0031: a 154-line typing/docstring refactor of 12 views; delete_project alone loses
  @login_required. py-0032: a 116-line typing refactor of a listing module; paginate's offset
  changes from (page - 1) * size to page * size, so page 1 shows the second page.
- Caught a dud before shipping: in my first py-0031 draft the unprotected view read
  `request.user.id`, so an anonymous call crashed with AttributeError before deleting anything. The
  "bug" wasn't exploitable. Now the store relies on the decorator and deletes by project id. Lesson
  for future cases: trace the planted bug to its actual harm, don't stop at "looks wrong".
- Both are `since: "0.2"`.
- Next: ceiling write-up once gemini/nemotron finish; more controls; more noisy diffs.

## 2026-11-23 — first upstream controls (click)
- py-0033 (click 589ca31, help text form-feed truncation) and py-0034 (click 36e3765, dots in the
  completion env var name): real merged PRs, BSD-3-Clause, used as-is. New `source.kind: upstream`.
- "No later fix" check: the changed lines are unchanged on click main today. Dropped b36e3ed
  (multiple flags): its lines were rewritten later, so it may have needed fixing.
- Dead end: `git log -S` on a `--filter=blob:none` clone fetches blobs one by one and timed out.
  Grepping upstream main for the changed lines is a cheap proxy; a full clone would allow a real
  `git log -L` check.
- Next: keep adding upstream controls (requests, urllib3, Jinja2, Flask all permissive) in batches
  of ~5; ceiling write-up once gemini/nemotron finish.

## 2026-11-23 — risk register
- Owner asked for realism. Wrote `docs/RISKS.md`: what could make the numbers wrong, most serious
  first. The headline: **0 of ~750 v0.1 findings have a human verdict**, so every precision figure
  on the leaderboard is meaningless today, and groq's noise flag rests on 6 rule verdicts.
- Other big ones: n = 23 bugs can't rank models; synthetic cases are LLM-written (and Claude
  wrote the recent ones: a self-grading risk); held-out (5) is too small to detect contamination.
- Added four roadmap items that fix the reporting side now, without waiting for the owner.
- Next session: "stop reporting unmeasured precision" first; it's the most misleading number we
  publish.

## 2026-11-23 — precision hidden until it's measured
- Leaderboard and per-run reports now print "not measured (N of M unjudged)" for precision until
  80% of the findings that need a human verdict have one. Every v0.1 row now says "not measured".
- The noise flag's control-FPR reason says "≥" when control findings are unjudged (confirmed
  false positives are only a lower bound).
- Done in report.py on purpose: scoring.py is gated under automerge, and this didn't need it.

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

## 2026-11-24 — maintenance: #13 and #14 brought up to date with main
- Still 2 PRs open, so no new roadmap work. main had moved a lot (#12, #15–#25: v0.1 frozen at 27
  cases, `since: "0.2"`, RISKS.md, 429 retry, precision shown as "not measured"), and both PRs
  conflicted.
- #14: main had taken py-0028..0034, so CVE batch 2 became py-0035..0038 with `since: "0.2"`. Re-ran
  the private overlap check: no overlap with the held-out set.
- #13: rewrote the report for the current results. cerebras was re-run on all 27 cases, so both
  usable runs now share a case set. Headline is per-run recall (SPEC §10): cerebras 69/69 (95–100)
  vs groq 58/69 (74–91) at L0. The intervals don't overlap, but most of groq's CVE misses are
  matcher artifacts. Precision is "not measured"; the RISKS caveats are repeated. Dropped the 429
  idea (done in #16) and the urllib3 held-out idea (resolved).
- Mistake caught: mid-merge I ran `git checkout origin/main -- .`, which would have discarded the
  branch's roadmap edits. I aborted the merge and redid it before committing anything.
