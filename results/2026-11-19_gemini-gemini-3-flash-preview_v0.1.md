# gemini / gemini-3-flash-preview — ReviewBench v0.1

Created 2026-11-19T17:36:19+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 9/9 (100%, 70–100) | 10/10 (100%, 72–100) | n/a | 3 | 36 |
| L0 | easy | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 9/9 (100%, 70–100) | 10/10 (100%, 72–100) | n/a | 3 | 27 |
| L0 | hard | n/a | n/a | n/a | n/a | n/a | 0 | 9 |
| L1 | all | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 7/7 (100%, 65–100) | 7/7 (100%, 65–100) | n/a | 2 | 37 |
| L1 | easy | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 7/7 (100%, 65–100) | 7/7 (100%, 65–100) | n/a | 2 | 29 |
| L1 | hard | n/a | n/a | n/a | n/a | n/a | 0 | 8 |
| L2 | all | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 6/6 (100%, 61–100) | 7/7 (100%, 65–100) | n/a | 1 | 36 |
| L2 | easy | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 6/6 (100%, 61–100) | 7/7 (100%, 65–100) | n/a | 1 | 30 |
| L2 | hard | n/a | n/a | n/a | n/a | n/a | 0 | 6 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 1/1 | 1 | 0 | 0 | 0 | 0 | 2 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 1/1 | 1 | 0 | 0 | 0 | 1 | 2 |
| py-0002-hardcoded-secret | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0002-hardcoded-secret | L2 | 1/1 | 1 | 1 | 0 | 0 | 0 | 2 |
| py-0003-off-by-one-page | L0 | 3/3 | 3 | 0 | 0 | 0 | 2 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 3 | 0 | 0 | 0 | 2 | 0 |
| py-0003-off-by-one-page | L2 | 2/2 | 2 | 0 | 0 | 0 | 1 | 1 |
| py-0004-missing-admin-check | L0 | 1/1 | 2 | 0 | 0 | 0 | 0 | 2 |
| py-0004-missing-admin-check | L1 | 1/1 | 1 | 0 | 0 | 0 | 0 | 2 |
| py-0004-missing-admin-check | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0005-check-then-act-race | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0005-check-then-act-race | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0006-path-traversal | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0006-path-traversal | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0006-path-traversal | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0007-pickle-cookie | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0007-pickle-cookie | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0007-pickle-cookie | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0008-mutable-default | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0008-mutable-default | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0008-mutable-default | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0009-swallowed-exception | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0009-swallowed-exception | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0009-swallowed-exception | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0010-timing-unsafe-compare | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0010-timing-unsafe-compare | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0010-timing-unsafe-compare | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0011-trial-boundary | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0011-trial-boundary | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0011-trial-boundary | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0012-ssrf-preview | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0012-ssrf-preview | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0012-ssrf-preview | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0013-idor-invoice | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0013-idor-invoice | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0013-idor-invoice | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0014-cache-leaks-across-users | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0014-cache-leaks-across-users | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0014-cache-leaks-across-users | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0015-retry-double-charge | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0015-retry-double-charge | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 2 |
