# groq / openai/gpt-oss-120b — ReviewBench v0.1

Created 2026-11-19T07:36:57+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 15/15 (100%, 80–100) | 15/15 (100%, 80–100) | 45/45 (100%, 92–100) | 60/60 (100%, 94–100) | n/a | 4 | 0 |
| L0 | easy | 12/12 (100%, 76–100) | 12/12 (100%, 76–100) | 36/36 (100%, 90–100) | 47/47 (100%, 92–100) | n/a | 3 | 0 |
| L0 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 9/9 (100%, 70–100) | 13/13 (100%, 77–100) | n/a | 1 | 0 |
| L1 | all | 15/15 (100%, 80–100) | 15/15 (100%, 80–100) | 45/45 (100%, 92–100) | 50/50 (100%, 93–100) | n/a | 4 | 0 |
| L1 | easy | 12/12 (100%, 76–100) | 12/12 (100%, 76–100) | 36/36 (100%, 90–100) | 40/40 (100%, 91–100) | n/a | 4 | 0 |
| L1 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 9/9 (100%, 70–100) | 10/10 (100%, 72–100) | n/a | 0 | 0 |
| L2 | all | 15/15 (100%, 80–100) | 14/15 (93%, 70–99) | 44/45 (98%, 88–100) | 52/52 (100%, 93–100) | n/a | 3 | 0 |
| L2 | easy | 12/12 (100%, 76–100) | 11/12 (92%, 65–98) | 35/36 (97%, 86–100) | 43/43 (100%, 92–100) | n/a | 3 | 0 |
| L2 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 9/9 (100%, 70–100) | 9/9 (100%, 70–100) | n/a | 0 | 0 |

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
| py-0005-check-then-act-race | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L0 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L0 | 3/3 | 3 | 1 | 0 | 0 | 1 | 0 |
| py-0010-timing-unsafe-compare | L1 | 3/3 | 3 | 1 | 0 | 0 | 1 | 0 |
| py-0010-timing-unsafe-compare | L2 | 2/3 | 2 | 2 | 0 | 0 | 1 | 0 |
| py-0011-trial-boundary | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L1 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L2 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L0 | 3/3 | 7 | 0 | 0 | 0 | 1 | 0 |
| py-0015-retry-double-charge | L1 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
