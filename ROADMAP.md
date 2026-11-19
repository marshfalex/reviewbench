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
- [ ] **Import public CVE cases, batch 1** (reverse the fix commit; pin it; verify license):
      CVE-2018-18074 requests, CVE-2023-43804 urllib3, CVE-2024-22195 Jinja2,
      CVE-2024-23334 aiohttp, CVE-2022-24439 GitPython.
- [ ] **Import public CVE cases, batch 2:** CVE-2023-41040 GitPython, CVE-2021-33203 Django,
      CVE-2022-29217 PyJWT, CVE-2023-32681 requests.
- [ ] **Import public CVE cases, batch 3:** CVE-2024-35195 requests, CVE-2023-45803 urllib3,
      CVE-2024-34064 Jinja2, CVE-2019-10906 Jinja2.
- [ ] [owner] Run the `benchmark` workflow on Groq (k=3, L0/L1/L2) with the full public set, and
      adjudicate pending findings.
- [ ] **Findings report v0.1** (needs results committed): `docs/findings/v0.1.md` — headline
      numbers, recall by difficulty and context level, any-of-k vs all-of-k, the L0→L2 effect on
      the cursor case, every miss with a one-line explanation. Honest about n.
- [ ] **Leaderboard charts:** generate SVG charts (recall by category/level with Wilson error bars)
      from results; embed in README and the findings report.
- [ ] **Launch post draft:** `docs/posts/v0.1.md` — a short thread-style write-up (headline
      finding, one chart, one concrete missed bug, link to method). The owner posts it.

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
