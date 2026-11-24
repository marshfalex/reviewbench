# ReviewBench roadmap

Sessions take the **first unchecked item** whose prerequisites are met (see `CLAUDE.md`).
`[owner]` items need the owner; skip them. Tick items in the PR that completes them.

## v0.1 — finish and publish
- [x] **Held-out loader.** Load extra cases from the directory in `REVIEWBENCH_HELDOUT` (if set),
      tag them `split: heldout`, report them separately, and make sure nothing about them is ever
      written into committed results (only aggregate numbers). Tests with a temp dir.
- [x] [owner] Create private repo `marshfalex/reviewbench-heldout` and add the 5 held-out CVE cases
      (PyJWT iss CVE-2024-53861, urllib3 Proxy-Authorization CVE-2024-37891, Flask Vary: Cookie
      CVE-2023-30861, Django Trunc/Extract CVE-2022-34265, python-multipart ReDoS CVE-2024-24762).
- [ ] [owner] **Let the `benchmark` workflow read held-out cases** (no cost; prerequisite: the
      held-out cases exist). The owner needs to:
      1. Create a fine-grained personal access token scoped to `marshfalex/reviewbench-heldout`
         only, with *Contents: read-only* and an expiry. Add it to `reviewbench` as the Actions
         secret `HELDOUT_READ_TOKEN`.
      2. Add an opt-in `heldout` boolean input to `benchmark.yml`, plus a step guarded by it:
         `actions/checkout` with `repository: marshfalex/reviewbench-heldout`,
         `token: ${{ secrets.HELDOUT_READ_TOKEN }}` and `path: .heldout`. Then set
         `REVIEWBENCH_HELDOUT: .heldout` on the run step. Add `.heldout/` to `.gitignore`.
         The workflow's own `permissions:` don't change: the token is used only by that checkout.
      3. Know the limits. Held-out raw results stay in the git-ignored `results/raw/` on the
         ephemeral runner, so only the aggregate in the committed results file survives the job.
         That means held-out findings can't be adjudicated later, and `--resume` can't continue a
         held-out part that ran out of time. Keeping the raw file would need a private store, such
         as pushing it to `reviewbench-heldout`, which would need a write token. Run logs alias
         held-out ids (`heldout-NN`), but they are public, so never add a step that prints case
         contents.
      Sessions may draft the workflow change as a PR once the owner has added the secret. The
      owner decides whether it merges, because it is a workflow change.
- [ ] [owner] **Free API keys for parallel model runs** (all free, no card needed). Create each key
      and add it as a repo secret (Settings → Secrets and variables → Actions):
      `GEMINI_API_KEY` (aistudio.google.com → Get API key), `OPENROUTER_API_KEY` (openrouter.ai →
      Keys; use models ending in `:free`), `CEREBRAS_API_KEY` (cloud.cerebras.ai),
      `MISTRAL_API_KEY` (console.mistral.ai → Experiment plan). Each provider has its own rate limit,
      so models run in parallel.
- [x] **Run the free-model lineup in parallel**, automated: the `benchmark` workflow runs every 6 h
      and works through `lineup.yaml`, running each model whose key secret is set until its result is
      complete. Add or change models by editing `lineup.yaml`.
- [x] **Findings report v0.1, first cut**, as soon as ONE full run completes (don't wait for the CVE
      cases): `docs/findings/v0.1.md`. Headline numbers with n and CIs, recall by difficulty and
      context level, any-of-k vs all-of-k, the L0→L2 effect on the cursor case, and every miss with a
      one-line explanation. Update it as more models finish.
- [x] **Import public CVE cases, batch 1** (reverse the fix commit; pin it; verify license):
      CVE-2018-18074 requests, CVE-2023-43804 urllib3, CVE-2024-22195 Jinja2,
      CVE-2024-23334 aiohttp, CVE-2022-24439 GitPython.
- [x] **Import public CVE cases, batch 2:** CVE-2023-41040 GitPython, CVE-2021-33203 Django,
      CVE-2022-29217 PyJWT, CVE-2023-32681 requests.
- [ ] **Import public CVE cases, batch 3:** CVE-2024-35195 requests, CVE-2023-45803 urllib3,
      CVE-2024-34064 Jinja2, CVE-2019-10906 Jinja2.
- [ ] [owner] Adjudicate pending findings after each completed run (`python -m reviewbench adjudicate`).
- [ ] **Leaderboard charts:** generate SVG charts (recall by category/level with Wilson error bars)
      from results; embed in README and the findings report.
- [ ] **Launch post draft:** `docs/posts/v0.1.md` — a short thread-style write-up (headline
      finding, one chart, one concrete missed bug, link to method). The owner posts it.

## v0.2 redesign — make the benchmark discriminate (decided 2026-11-23, see SPEC §10)
Do these before the v0.2 items below. They come before remaining v0.1 items except the owner ones.
- [ ] **Write up the ceiling finding and the redesign plan** (`docs/findings/ceiling.md`): the
      Cerebras result (54/54 per-run at L0, lower bound ~93%; 0/12 control FPs), why it can't rank
      models, and the SPEC §10 plan. Apply the ceiling rule once groq, gemini and nemotron finish.
- [x] **Provider data-use table** (`docs/providers.md`): for every lineup provider, whether API
      inputs may be used for training, a link to the terms and the date checked. Until it exists,
      no held-out runs; then set `heldout_ok` in `lineup.yaml` only for providers that forbid
      training (that change goes to the owner).
- [ ] [owner] **Confirm from the benchmark run logs that no held-out case was ever sent** to a
      provider (no workflow loads `REVIEWBENCH_HELDOUT` today). Retire any case that was.
- [x] **Cross-file L2 cases, proof of concept (2–3):** bugs visible only with the related files
      (L2), not from the diff or changed files alone.
- [x] **Score/report changes, part 1:** per-run recall as the leaderboard sort key; the noise
      flag; a prompt hash in results.
- [x] **Blind adjudication:** hide the model while adjudicating; a second-rater sample and κ.
- [ ] [owner] **Do a blind adjudication pass** over all v0.1 results:
      `python -m reviewbench adjudicate-blind results/*_v0.1.json` (skip the `.adjudications`
      files), then `--rater second` (by a second person, or the owner a few days later), then
      `python -m reviewbench agreement results/*_v0.1.json`.
- [ ] **Controls to ≥36,** labeled "no known defect" (real merged PRs, provenance recorded).
      Progress: 7 of 36 (4 v0.1 synthetic, py-0030 synthetic, py-0033/34 from click). Method that
      works: pick small single-file behavior changes ≥2 years old whose lines are unchanged on
      upstream main today; excerpt just the enclosing method so the upstream diff applies as-is.
- [x] **Large noisy-diff cases, first 2:** planted bugs buried in big, realistic diffs (py-0031, py-0032).
- [ ] **More noisy-diff cases (3+),** including one noisy-diff *control* and one real-world refactor
      PR (reversed CVE fix inside a larger change).
- [ ] **Data-driven hardness labels** from v0.1 results, after the v0.1 lineup completes.
- [ ] **Matching-rule defect check** plus a hand-audited sample of matches.
- [ ] **Prompt sensitivity check:** 2–3 paraphrased prompts × 1 free model.
- [ ] **Rewrite the README problem statement** to say ReviewBench compares models behind a
      standard prompt; review products are a later, paid phase.

- [x] **Stop reporting unmeasured precision** (RISKS §1): when fewer than ~80% of a slice's
      non-hit findings are adjudicated, the leaderboard and reports show "not measured (N
      unjudged)" instead of a precision rate, and the noise flag says which half it rests on.
- [ ] **Refuse to resume across a served-model change** (RISKS §6): `run --resume` stops if the
      provider reports a different served model id than the file's earlier records.
- [ ] **Report real and synthetic cases separately** (RISKS §3), and note in each table which
      model family wrote the synthetic cases.
- [ ] **Shift the case mix toward real bugs:** CVE batches 2–3, plus upstream reverted or
      later-fixed commits (the "bug introduced by PR X, fixed by PR Y" pattern), aiming for
      at least half real cases in v0.2. Progress: CVE batch 2 (py-0035..0038, `since: "0.2"`).

- [ ] **Widen CVE bug ranges for v0.2** (decided 2026-11-24): each CVE bug's range covers the whole
      vulnerable hunk, and a bug may list several ranges (e.g. the second call site) instead of a
      `known_issues` entry. Ships with the v0.2 bump; v0.1 keeps its narrow ranges, documented as a
      matcher artifact in the findings report. Needs a SPEC + scoring change (gated: `needs-owner`).
- Decision 2026-11-24: **keep k = 3 at temperature 0.** Groq's catch/miss varies across runs on
  4 of 23 bugs, so repeats aren't wasted; the cost of correlated runs is handled by computing
  per-run recall intervals with the bug as the unit (done). Revisit if every lineup provider
  turns out deterministic.

## v0.2 — breadth and contributors
- [ ] **Modify-existing-file synthetic cases (8):** PRs that edit existing code so L1 differs from
      L0 (e.g. a refactor that drops an authz check, a changed default, a removed lock).
- [ ] **More hard classes (10 synthetic):** migrations that lock tables, cache invalidation,
      timezone/DST, idempotency keys, N+1 queries, unsafe defaults in config, TOCTOU on files,
      integer overflow in pagination math, retry storms, partial-failure in batch jobs.
- [ ] **Contributing guide + case template** and a CI check that validates contributed cases.
- [ ] **Ollama adapter docs** and a tiny smoke test path for running a local model.
- [ ] **Cost/latency per review** in results and leaderboard.
- [ ] **Run the same cases against an existing GitHub-Action reviewer** (adapter design first;
      flag anything paid as `[owner]`).

## v0.3 — beyond Python
- [ ] TypeScript/JavaScript cases (case format already language-tagged).

## Ideas (unapproved)
<!-- Sessions add ideas here; the owner promotes them above. -->
- Store each review's raw model response, or at least count findings `parse_review` drops. The only
  miss in the first complete run (py-0004 at L1) looks like dropped findings: the summary names the
  bug but the findings list is empty. Today that can't be confirmed.
