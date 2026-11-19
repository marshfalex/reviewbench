# groq / openai/gpt-oss-120b — ReviewBench v0.1

Created 2026-11-19T07:36:57+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 15/15 (100%, 80–100) | 20/20 (100%, 84–100) | n/a | 2 | 0 |
| L0 | easy | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 15/15 (100%, 80–100) | 20/20 (100%, 84–100) | n/a | 2 | 0 |
| L1 | all | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 15/15 (100%, 80–100) | 16/16 (100%, 81–100) | n/a | 3 | 0 |
| L1 | easy | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 15/15 (100%, 80–100) | 16/16 (100%, 81–100) | n/a | 3 | 0 |
| L2 | all | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 14/14 (100%, 78–100) | 17/17 (100%, 82–100) | n/a | 2 | 0 |
| L2 | easy | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 14/14 (100%, 78–100) | 17/17 (100%, 82–100) | n/a | 2 | 0 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 3/3 | 3 | 1 | 0 | 0 | 2 | 0 |
| py-0002-hardcoded-secret | L1 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0002-hardcoded-secret | L2 | 3/3 | 3 | 1 | 0 | 0 | 2 | 0 |
| py-0003-off-by-one-page | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L0 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L2 | 2/2 | 4 | 0 | 0 | 0 | 0 | 0 |
