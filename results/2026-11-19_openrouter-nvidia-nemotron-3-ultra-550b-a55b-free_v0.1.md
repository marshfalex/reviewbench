# openrouter / nvidia/nemotron-3-ultra-550b-a55b:free — ReviewBench v0.1

Created 2026-11-19T17:36:19+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (1 of 1 unjudged) | n/a | 1 | 0 |
| L0 | easy | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (1 of 1 unjudged) | n/a | 1 | 0 |
| L1 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (3 of 3 unjudged) | n/a | 3 | 0 |
| L1 | easy | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (3 of 3 unjudged) | n/a | 3 | 0 |
| L2 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 17/17 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (7 of 7 unjudged) | n/a | 7 | 1 |
| L2 | easy | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 17/17 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (7 of 7 unjudged) | n/a | 7 | 1 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 3/3 | 7 | 2 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L1 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L2 | 3/3 | 3 | 3 | 0 | 0 | 2 | 0 |
| py-0003-off-by-one-page | L0 | 3/3 | 4 | 0 | 0 | 0 | 1 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L2 | 3/3 | 4 | 0 | 0 | 0 | 2 | 0 |
| py-0004-missing-admin-check | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L1 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0004-missing-admin-check | L2 | 3/3 | 4 | 0 | 0 | 0 | 3 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L2 | 2/2 | 2 | 0 | 0 | 0 | 0 | 1 |
