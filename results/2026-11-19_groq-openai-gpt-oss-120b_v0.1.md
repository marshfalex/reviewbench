# groq / openai/gpt-oss-120b — ReviewBench v0.1

Created 2026-11-19T07:36:57+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 18/18 (100%, 82–100) | 16/18 (89%, 67–97) | 51/54 (94%, 85–98) | 68/68 (100%, 95–100) | 0/9 (0%, 0–30) | 5 | 0 |
| L0 | easy | 12/12 (100%, 76–100) | 12/12 (100%, 76–100) | 36/36 (100%, 90–100) | 49/49 (100%, 93–100) | 0/9 (0%, 0–30) | 4 | 0 |
| L0 | hard | 6/6 (100%, 61–100) | 4/6 (67%, 30–90) | 15/18 (83%, 61–94) | 19/19 (100%, 83–100) | n/a | 1 | 0 |
| L1 | all | 17/18 (94%, 74–99) | 16/18 (89%, 67–97) | 49/54 (91%, 80–96) | 54/54 (100%, 93–100) | 0/6 (0%, 0–39) | 6 | 0 |
| L1 | easy | 12/12 (100%, 76–100) | 12/12 (100%, 76–100) | 36/36 (100%, 90–100) | 40/40 (100%, 91–100) | 0/6 (0%, 0–39) | 4 | 0 |
| L1 | hard | 5/6 (83%, 44–97) | 4/6 (67%, 30–90) | 13/18 (72%, 49–88) | 14/14 (100%, 78–100) | n/a | 2 | 0 |
| L2 | all | 18/18 (100%, 82–100) | 15/18 (83%, 61–94) | 49/54 (91%, 80–96) | 57/57 (100%, 94–100) | 0/6 (0%, 0–39) | 6 | 0 |
| L2 | easy | 12/12 (100%, 76–100) | 11/12 (92%, 65–98) | 35/36 (97%, 86–100) | 43/43 (100%, 92–100) | 0/6 (0%, 0–39) | 3 | 0 |
| L2 | hard | 6/6 (100%, 61–100) | 4/6 (67%, 30–90) | 14/18 (78%, 55–91) | 14/14 (100%, 78–100) | n/a | 3 | 0 |

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
| py-0016-float-money | L0 | 1/3 | 1 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L2 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0017-cursor-pagination-skips | L0 | 2/3 | 2 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L1 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0017-cursor-pagination-skips | L2 | 1/3 | 1 | 0 | 0 | 0 | 1 | 0 |
| py-0018-naive-local-vs-utc | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L0 | control | 0 | 2 | 0 | 0 | 1 | 0 |
