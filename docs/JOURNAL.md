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
