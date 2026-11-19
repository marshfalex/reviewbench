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
