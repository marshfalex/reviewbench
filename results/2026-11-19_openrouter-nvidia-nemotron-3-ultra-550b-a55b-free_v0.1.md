# openrouter / nvidia/nemotron-3-ultra-550b-a55b:free — ReviewBench v0.1

Created 2026-11-19T17:36:19+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 (100%, 82–100) | 25/25 (100%, 87–100) | n/a | 1 | 36 |
| L0 | easy | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 (100%, 82–100) | 25/25 (100%, 87–100) | n/a | 1 | 18 |
| L0 | hard | n/a | n/a | n/a | n/a | n/a | 0 | 18 |
| L1 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 (100%, 82–100) | 23/23 (100%, 86–100) | n/a | 3 | 33 |
| L1 | easy | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 18/18 (100%, 82–100) | 23/23 (100%, 86–100) | n/a | 3 | 18 |
| L1 | hard | n/a | n/a | n/a | n/a | n/a | 0 | 15 |
| L2 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 17/17 (100%, 82–100) | 22/22 (100%, 85–100) | n/a | 7 | 34 |
| L2 | easy | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 17/17 (100%, 82–100) | 22/22 (100%, 85–100) | n/a | 7 | 19 |
| L2 | hard | n/a | n/a | n/a | n/a | n/a | 0 | 15 |

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
| py-0015-retry-double-charge | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0015-retry-double-charge | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0016-float-money | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0016-float-money | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0016-float-money | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0017-cursor-pagination-skips | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0017-cursor-pagination-skips | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0017-cursor-pagination-skips | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0018-naive-local-vs-utc | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
