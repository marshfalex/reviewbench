# ReviewBench roadmap

Sessions take the **first unchecked item** whose prerequisites are met (see `CLAUDE.md`).
`[owner]` items need the owner; skip them. Tick items in the PR that completes them.

## v0.1 — finish and publish
- [x] **Held-out loader.** Load extra cases from the directory in `REVIEWBENCH_HELDOUT` (if set),
      tag them `split: heldout`, report them separately, and make sure nothing about them is ever
      written into committed results (only aggregate numbers). Tests with a temp dir.
- [ ] [owner] Create private repo `marshfalex/reviewbench-heldout` and add the 5 held-out CVE cases
      (PyJWT iss CVE-2024-53861, urllib3 Proxy-Authorization CVE-2024-37891, Flask Vary: Cookie
      CVE-2023-30861, Django Trunc/Extract CVE-2022-34265, python-multipart ReDoS CVE-2024-24762).
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
- Held-out results can only reach the leaderboard from a local run (the `benchmark` workflow has
  no access to the private repo). A workflow input that checks out `reviewbench-heldout` with a
  read-only deploy key would let CI run them; needs an owner-created secret.
