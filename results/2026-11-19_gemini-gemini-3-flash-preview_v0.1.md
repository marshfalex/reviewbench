# gemini / gemini-3-flash-preview — ReviewBench v0.1

Created 2026-11-19T17:36:19+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 12/12 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (3 of 3 unjudged) | n/a | 3 | 4 |
| L0 | easy | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 9/9 runs; per-bug mean 100% (95% CI 57–100, 5 bugs) | not measured (3 of 3 unjudged) | n/a | 3 | 4 |
| L0 | hard | 1/1 (100%, 21–100) | 1/1 (100%, 21–100) | 3/3 runs; per-bug mean 100% (95% CI 21–100, 1 bugs) | not measured (3 of 3 unjudged) | n/a | 0 | 0 |
| L1 | all | 7/7 (100%, 65–100) | 7/7 (100%, 65–100) | 12/12 runs; per-bug mean 100% (95% CI 65–100, 7 bugs) | not measured (2 of 2 unjudged) | n/a | 2 | 1 |
| L1 | easy | 4/4 (100%, 51–100) | 4/4 (100%, 51–100) | 9/9 runs; per-bug mean 100% (95% CI 51–100, 4 bugs) | not measured (2 of 2 unjudged) | n/a | 2 | 1 |
| L1 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 3/3 runs; per-bug mean 100% (95% CI 44–100, 3 bugs) | not measured (2 of 2 unjudged) | n/a | 0 | 0 |
| L2 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 11/11 runs; per-bug mean 100% (95% CI 61–100, 6 bugs) | not measured (2 of 2 unjudged) | n/a | 2 | 1 |
| L2 | easy | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 6/6 runs; per-bug mean 100% (95% CI 44–100, 3 bugs) | not measured (2 of 2 unjudged) | n/a | 1 | 1 |
| L2 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 5/5 runs; per-bug mean 100% (95% CI 44–100, 3 bugs) | not measured (2 of 2 unjudged) | n/a | 1 | 0 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 1/1 | 1 | 0 | 0 | 0 | 0 | 2 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 1/1 | 1 | 0 | 0 | 0 | 1 | 2 |
| py-0002-hardcoded-secret | L1 | 2/2 | 2 | 2 | 0 | 0 | 0 | 1 |
| py-0002-hardcoded-secret | L2 | 1/1 | 1 | 1 | 0 | 0 | 0 | 1 |
| py-0003-off-by-one-page | L0 | 3/3 | 3 | 0 | 0 | 0 | 2 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 3 | 0 | 0 | 0 | 2 | 0 |
| py-0003-off-by-one-page | L2 | 2/2 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0004-missing-admin-check | L0 | 1/1 | 2 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L1 | 1/1 | 1 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L1 | 1/1 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L2 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 1/1 | 1 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L2 | 1/1 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0017-cursor-pagination-skips | L1 | 1/1 | 1 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L2 | 1/1 | 2 | 0 | 0 | 0 | 0 | 0 |
