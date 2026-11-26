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

## 2026-11-20 — CVE batch 2
- Added py-0035..py-0038 (`since: "0.2"`; renumbered from py-0028..31 after main took those ids), the same method as batch 1:
  - GitPython CVE-2023-41040 (64ebb9f, the commit titled "Fix CVE-2023-41040": rejects `..` in
    ref paths)
  - Django CVE-2021-33203 (dfaba12: `safe_join` in admindocs)
  - PyJWT CVE-2022-29217 (9c52867: replaces the incomplete HMAC key blocklist)
  - requests CVE-2023-32681 (74ea7cf: no Proxy-Authorization on HTTPS-tunnelled requests)

  Licenses are BSD-3, BSD-3, MIT and Apache-2.0. The largest prompt is Django at L1/L2 (17,709
  chars).
- Decisions:
  - GitPython: 3.1.37 also has follow-up refname hardening (46d3d05, in #1672). The case pins only
    the commit named for the CVE.
  - PyJWT: the fix also touched OKPAlgorithm.prepare_key (key-type checks). That stays in the diff
    as part of the pinned commit but is not a planted bug.
  - Difficulty: GitPython and Django are `easy` (the diff removes an explicit `..` check /
    safe_join); PyJWT and requests are `hard` (you need to know which key formats or which tunnel
    path the old code missed).
- Ran the private repo's overlap check against these cases: no overlap with the held-out set,
  including the PyJWT and Django held-out cases, which change different files.
- BENCH_VERSION stays 0.1, as for batch 1. The complete cerebras run covers only the 22 synthetic
  cases; re-running finished models on new cases is #12.
- Next: CVE batch 3.

## 2026-11-21 — maintenance only (2 PRs open)
- #13 (findings report) and #14 (CVE batch 2) are open with green CI, no review comments, and
  both still merge cleanly into main. Per the 2-open-PR rule, no new roadmap work this session.
- Scheduled benchmark runs #8–#10 succeeded after #5 and #7 failed; groq keeps adding results.
- Next: once #13/#14 merge, CVE batch 3 (requests CVE-2024-35195, urllib3 CVE-2023-45803, Jinja2
  CVE-2024-34064, CVE-2019-10906). Run the private overlap check on it. The urllib3 case touches
  redirect handling, but the held-out urllib3 case has already been replaced.
- 2026-11-21 (later): still 2 PRs open (#13, #14), unreviewed, green, merge cleanly. No new work.

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

## 2026-11-24 — per-run intervals use the bug as the unit; two pending decisions made
- The other session's finding (cerebras's 3 runs are byte-identical) means per-run Wilson intervals
  over 69 bug × run observations overstated the evidence ~√3-fold. Measured: cerebras identical on
  23/23 L0 bug cases; groq's catch/miss differs across runs on only 4/23.
- Reports and leaderboard now show per-run recall as "58/69 runs (84%; 95% CI 65–94 over 23 bugs)".
  Done in report.py (scoring.py is gated); SPEC §6 documents it.
- **This reversed a published claim.** The findings report said cerebras beats groq because the
  intervals didn't overlap (95–100 vs 74–91). Per-bug intervals overlap at every level (86–100 vs
  65–94 at L0). Report and RISKS corrected: no model ranking is supported yet.
- Owner delegated decisions. Made the two that were waiting:
  - Keep k = 3. Groq varies, so the repeats are cheap insurance.
  - Widen CVE bug ranges in v0.2 only (whole vulnerable hunk, multiple ranges). v0.1 stays frozen.
- Owner also turned off the twice-daily "next roadmap item" scheduled task and archived the
  builder session; this session continues the work directly.
- Next: real-PR controls (7/36), then refuse-to-resume on served-model change.

## 2026-11-24 — five more upstream controls (click)
- py-0039..0043 from click (422e211, 8d7f03d, 3699bcc, c2a5bb0, b964c1e): small single-function
  behavior fixes, 2019–2022, every added line still present on click main today.
- Made the excerpting repeatable: a small ast-based script keeps the file's top-level imports and
  the changed function (with its class header), then checks that the excerpt diff has exactly the
  upstream commit's +/- lines. It caught one problem: click's `main` has typing `@overload` stubs
  with the same name, and matching by name pulled them into the "before" side. Now both sides match
  by changed line numbers.
- Controls: 12 of 36. All 7 upstream ones are click; next batches should use other projects.
- The excerpt script is committed as `scripts/upstream_excerpt.py` for future batches.

## 2026-11-24 — one served model per results file
- `run` now refuses, with an error, to append a review whose `served_model` differs from the ones
  already in the file. The mismatching review isn't written, so the file stays single-model and
  the scheduled job fails visibly instead of silently mixing models (RISKS §6).
- All four current v0.1 files have exactly one served id each, so nothing existing trips it.
- Next: upstream controls from projects other than click.

## 2026-11-24 — five upstream controls from Flask and Jinja2
- py-0044..0046 (Flask 700fc7d9, 5050a18a, b10b6d4a) and py-0047/48 (Jinja2 051df10c, e8da6267).
- Skipped security fixes and anything in the same file as one, so no control sits next to a CVE
  case. Added that rule to the roadmap.
- Fixed `scripts/upstream_excerpt.py`: when a commit touches two methods of one class it emitted
  two class headers, so the diff gained a fake `class` line. Same-class methods now share one
  header; the excerpt check (+/- lines identical to upstream) caught it, and the click cases
  re-excerpt identically.
- Controls: 17 of 36.

## 2026-11-24 — the held-out set is exposed
- An automated check blocked this session from naming a held-out case in the journal. Looking
  further: the roadmap's owner item had named all 5 held-out cases since 2026-11-19. They're in git
  history, so removing the text doesn't un-expose them.
- Removed the names from the current roadmap, recorded the exposure in RISKS §4, and added an
  `[owner]` item to replace the held-out set. Rule for every session: never name held-out cases,
  their CVEs or their projects anywhere in this repository.
- Scanned all current files for the five identifiers: none remain.

## 2026-11-24 — real vs synthetic split on the leaderboard
- New "Per-run recall by case origin" table per version: synthetic vs real (CVE + upstream), per
  bug intervals, unfinished runs marked. Results now store `source_kind`; older files fall back to
  the `cve`/`upstream` tags (checked: tags match `source.kind` for every case).
- First signal: groq catches 94% (74–99) of synthetic bugs vs 47% (15–81) of real ones at L0, and
  13% at L1. Only 5 real bugs, and many misses are the narrow line window, so it's a lead, not a
  finding, but it's the strongest argument yet for more real cases and the v0.2 range fix.
- Gemini and Nemotron re-runs are progressing (41 and 54 of 243 reviews) under daily quotas.
- Next: more real-PR controls from outside Pallets; then real bug cases (CVE batch 3).

## 2026-11-24 — CVE batch 3 (py-0049..0052)
- Jinja2 CVE-2024-34064 (d6550307, xmlattr `/ > =` keys), Jinja2 CVE-2019-10906 (a2a6c930, sandbox
  `format_map`), urllib3 CVE-2023-45803 (4e50fbc5, body kept on 303), requests CVE-2024-35195
  (c0813a2d, `verify=False` pool reuse). Reversed fixes, `since: "0.2"`, upstream LICENSE copied.
- Bug ranges cover the vulnerable hunk (the v0.2 decision), e.g. py-0049 spans the regex constant to
  the check. urllib3's second call site (connectionpool) is a `known_issues` entry until scoring
  supports several ranges per bug.
- Caught before shipping: the roadmap's "CVE-2024-34064" and the commit I first picked (7dd3680e)
  didn't match: 7dd3680e is CVE-2024-22195, already public py-0025. Checked `git tag --contains`
  (3.1.3 vs 3.1.4) to pin the right commit. Also my journal entry earlier today called d6550307
  "py-0025"; it's this batch's CVE.
- `scripts/upstream_excerpt.py` now also keeps touched module-level statements (with their leading
  comments) and emits a class header on both sides when a commit adds or removes a whole method.
  All 10 script-built controls still re-excerpt identically.
- Real bugs now: 13 CVE cases (5 in v0.1, 8 held for v0.2).

## 2026-11-24 — five non-Pallets upstream controls
- py-0053 (attrs 88e2896), py-0054/55 (httpx 6d852d3, 59df819), py-0056/57 (rich 368e8ad7,
  3469674b). Skipped httpx auth, URL-parsing and proxy fixes as security-adjacent.
- Controls: 22 of 36. 17 of them are real upstream PRs from 6 projects.

## 2026-11-24 — five more upstream controls; independent review before each PR
- py-0058 (Starlette 2168e47), py-0059..0061 (pydantic 2b09cf48c, 332eac4be, e1a5c1818), py-0062
  (rich 720800e6). Controls: 27 of 36, 22 of them real upstream PRs from 8 projects.
- Dropped three candidates whose change sits in a class body or class docstring rather than a
  function (Starlette 93074e8, pydantic 28ed33f1b, attrs bfd7bb4): the excerpt script only keeps
  functions, so their diffs couldn't be reproduced exactly.
- Process change (owner asked whether this is a proper senior-engineer process; honest answer: not
  without independent review). From now on every PR is reviewed by a separate reviewer agent before
  it opens. This batch: all 5 PASS (diff applies, excerpt coherent, no defect introduced). A full
  audit of the PRs merged on 2026-11-23/24 is running; its findings get fixed in follow-up PRs.

## 2026-11-24 — fixes from the independent audit
- Audited today's merged PRs with a separate reviewer agent. Confirmed and fixed here:
  - Network failures (timeouts, resets, dropped mid-body, garbled 2xx bodies) were recorded as
    generic exceptions, which resume treats as done, so n shrank silently. They're now retried, then
    recorded as `transient:` (retryable). Retry-After as an HTTP date no longer crashes.
  - The per-run recall cell put run counts next to the per-bug mean ("51/68 runs (74%)", but
    51/68 = 75%). Now labelled "per-bug mean"; the findings report explains it.
  - Stale RISKS §3 counts and a findings line saying gemini/nemotron weren't re-running.
- The pre-PR review of this very fix found a gap (ChunkedEncodingError and bad JSON bodies still
  escaped). Fixed before opening the PR. That's the case for keeping the second reviewer.
- Not fixed here (needs the owner): the automerge gate only protects .github/, pyproject,
  BENCH_VERSION, the prompt/schema and scoring.py; report.py, stats.py, runner.py, adapters,
  cases/ and docs merge unreviewed, and CLAUDE.md still says the owner merges. Proposed a wider gate
  in a separate `needs-owner` PR.
- Suspected, not acted on: OpenRouter may report varying `model` ids across routes, which would trip
  the served-model check. Current files show one id each; watch the next runs.

## 2026-11-24 — proposed: wider automerge gate (needs owner)
- The audit found the gate protected only .github/, pyproject, BENCH_VERSION, the prompt/schema
  and scoring.py, while report.py, stats.py, runner.py, the adapters and the findings docs (all of
  which change published numbers or claims) merged on green CI. This PR widens it to those plus
  CLAUDE.md. Cases, the roadmap, the journal and tooling still merge automatically, since each case
  batch now gets an independent reviewer pass.
- It touches .github/, so it waits for the owner. The PR description also proposes CLAUDE.md wording
  that matches how merging actually works; only the owner can make that edit.

## 2026-11-24 — lessons file
- Owner asked that mistakes be written down so they don't repeat. Added `docs/LESSONS.md`: every
  mistake so far with the rule or check that now prevents it, plus a pre-PR checklist (tests
  proven to fail on old code, independent reviewer agent, no held-out names, regenerated numbers).
  CLAUDE.md now points sessions at it.
- Turned one lesson into a test: two cases may not share an upstream commit (the near-duplicate
  CVE import).
- Owner's direction: keep working autonomously; bring major direction choices to them.

## 2026-11-24 — controls batch 6 (py-0063..0067)
- rich daf6e38f and f540b003, Flask 1af8f957 and e679a85b, click 46b78bc. Controls: 32 of 36.
- Independent reviewer: all 5 PASS. Acted on two notes: py-0063's title undersold the change (it
  also fixes the xterm colour-cube mapping), and py-0067's `params.extend` mutates the caller's
  list. That's a real latent quirk, so it's now a `known_issues` entry: a reviewer who flags it
  earns a valid finding instead of a false positive on a control.
- Lesson for controls (added to LESSONS): "no known defect" isn't "no issue a reviewer could fairly
  raise". Record such quirks as known_issues.

## 2026-11-24 — controls reach 36 (py-0068..0071)
- Jinja2 a150ff74 and ac3ac6c9, click 0435112, attrs 4b1d869. Independent reviewer: 4/4 PASS;
  py-0071's None-vs-False return recorded as a known issue. Roadmap item done: 36 controls, 31 of
  them real upstream PRs from 8 projects. At 0 false alarms the Wilson upper bound on control FPR
  is now ~9% (vs 24% at n = 12), so the noise flag becomes meaningful in v0.2.
- v0.2 now holds 44 cases beyond v0.1's 27. The next major step (a version bump and full re-run)
  is a direction call for the owner.

## 2026-11-24 — owner decisions: freeze slow models; scoring before v0.2
- Found that gemini and nemotron gain only a few reviews per 6-hour run (free daily quotas): 40 and
  54 of 243 after five days. Asked the owner; decision: freeze them (`frozen: true`, a new lineup
  flag; their partial files stay on the leaderboard) and add fast free models: groq
  `auto:versatile` and `auto:qwen3`, cerebras `auto:llama` and `auto:gpt-oss`. `auto:` skips the
  entry if the provider lists no match, and guard/moderation models were already excluded.
- Second decision: land multi-range bugs and the defect-check matcher before bumping to v0.2, so
  v0.2 doesn't need a quick v0.3. All three steps touch gated files and wait for the owner.
- Unknown until the next scheduled run: which ids the auto entries resolve to. Check the
  benchmark job log.
- Independent review caught that `pick_auto` used plain string order, so "newest" meant
  "alphabetically last": `gpt-oss-20b` beat `gpt-oss-120b`, and `llama3.1-8b` beat `llama-3.3-70b`.
  Fixed with a natural sort (digit runs compare as numbers) plus narrow cerebras needles. Added to
  LESSONS.

## 2026-11-24 — bugs can have several locations (`also`)
- `bugs[].also: [{file, lines}]` lists other places the same defect lives; a finding at any of
  them (±2) catches the bug. Old results files, whose truth snapshots lack `also`, score exactly
  as before. py-0051 (v0.2) now lists urllib3's connection-pool call site this way (and keeps a
  known issue for findings elsewhere in that file), so catching only that site counts as a hit.
- Deliberately not applied to v0.1 cases yet (py-0026, py-0027 have the same pattern): new v0.1
  runs from the fast models would otherwise use different truth than the finished ones. Queued
  for the v0.2 bump PR.
- Gated (scoring.py, runner.py): waits for the owner.

## 2026-11-25 — defect check in the matcher; two new fast models finished
- The lineup change worked: cerebras gpt-oss-120b and groq qwen3.8-27b each finished all 243 v0.1
  reviews in under a day. groq `auto:versatile` and cerebras `auto:llama-3.3-70b` produced nothing,
  probably because no model matched; check the job log before relying on them.
- Same model, different provider, different numbers (L0 per-run recall, per-bug 95% CIs): qwen
  3.8-27b 100% (86–100) on cerebras vs 90% (71–97) on groq; gpt-oss-120b 84% (65–94) on groq vs
  72% (52–86) on cerebras. The intervals overlap, so it's not a finding yet, but provider variance
  belongs in RISKS and in how results are labelled (provider + model, never model alone).
- Defect check: `bugs[].defect_terms`. A location hit must also name the defect. Calibrated first
  on the four complete v0.1 runs with draft terms (not applied to v0.1 truth): 781/791 (98.7%)
  location catches name the defect. I read all 10 that don't, and each is right-line-wrong-reason
  (e.g. "unverified HTTP status" on the double-charge bug, "negative limit" on the cursor-skip
  bug). So today's matcher over-credits ~1.3%. All 12 v0.2 bug cases have terms; the v0.1 draft
  terms wait for the bump. Old results score identically (no terms in their snapshots).
- Gated (scoring.py, runner.py): waits for the owner.
- Independent review: code correct, old results identical. But several of my term lists used the
  code's own identifiers (`format`, `path`, `verify`, `pool`, `decision`, `key`) or substrings that
  hit unrelated words (`cert` in "certain", `unit` in "community", `..` in any ellipsis), so they
  filtered nothing. Tightened py-0028/29/35/36/49/50/51/52 to defect-concept terms. Lesson added.

## 2026-11-26 — v0.2 bump
- BENCH_VERSION 0.2: 71 cases (35 bug cases incl. 13 CVEs; 36 controls incl. 31 upstream PRs).
- v0.1 ground truth updated in the same PR, as planned:
  - Every v0.1 bug gets defect_terms, tightened after LESSONS' "terms that filter nothing".
    Independent review flagged more generic terms (`rce` in "source", `tie` in "properties", `cent`
    in "percent", identifiers like `pickle`, `login_required`, `<=`); fixed. Tightening then dropped
    two correct catches ("skip or duplicate rows when timestamps collide"; "up to and including
    trial_days"), found by reading every miss; terms widened for those. Final: 756/791 (95.6%)
    location catches name the defect; the other 35 are right-line-wrong-reason, mostly "missing
    HTTP status check" on the double-charge bug (planted bug: missing idempotency key).
  - Batch-1 CVE ranges are widened to the vulnerable hunk (py-0023..0027).
  - py-0026 and py-0027 get `also` locations for their second call sites.
- Frozen v0.1 results are untouched (scored from their own truth snapshots); the v0.1
  leaderboard table is byte-identical.
- The lineup now re-runs the four active fast models on all 71 cases (639 reviews each).
- Tests that hard-coded "v0.1" now follow BENCH_VERSION; a new test keeps the `since` hold-back
  covered now that every committed case is active (review finding). Draft terms file removed (applied).
