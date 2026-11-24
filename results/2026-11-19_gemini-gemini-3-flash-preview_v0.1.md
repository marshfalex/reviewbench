# gemini / gemini-3-flash-preview — ReviewBench v0.1

Created 2026-11-19T17:36:19+00:00, k=3 runs per case and level, status `complete`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 12/12 (100%, 76–100) | not measured (3 of 3 unjudged) | n/a | 3 | 69 |
| L0 | easy | 5/5 (100%, 57–100) | 5/5 (100%, 57–100) | 9/9 (100%, 70–100) | not measured (3 of 3 unjudged) | n/a | 3 | 48 |
| L0 | hard | 1/1 (100%, 21–100) | 1/1 (100%, 21–100) | 3/3 (100%, 44–100) | not measured (3 of 3 unjudged) | n/a | 0 | 21 |
| L1 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 10/10 (100%, 72–100) | not measured (2 of 2 unjudged) | n/a | 2 | 71 |
| L1 | easy | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 7/7 (100%, 65–100) | not measured (2 of 2 unjudged) | n/a | 2 | 50 |
| L1 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | not measured (2 of 2 unjudged) | n/a | 0 | 21 |
| L2 | all | 6/6 (100%, 61–100) | 6/6 (100%, 61–100) | 11/11 (100%, 74–100) | not measured (2 of 2 unjudged) | n/a | 2 | 70 |
| L2 | easy | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 6/6 (100%, 61–100) | not measured (2 of 2 unjudged) | n/a | 1 | 51 |
| L2 | hard | 3/3 (100%, 44–100) | 3/3 (100%, 44–100) | 5/5 (100%, 57–100) | not measured (2 of 2 unjudged) | n/a | 1 | 19 |

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
| py-0015-retry-double-charge | L1 | 1/1 | 3 | 0 | 0 | 0 | 0 | 2 |
| py-0015-retry-double-charge | L2 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 1/1 | 1 | 0 | 0 | 0 | 0 | 2 |
| py-0016-float-money | L2 | 1/1 | 2 | 0 | 0 | 0 | 1 | 2 |
| py-0017-cursor-pagination-skips | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0017-cursor-pagination-skips | L1 | 1/1 | 1 | 0 | 0 | 0 | 0 | 2 |
| py-0017-cursor-pagination-skips | L2 | 1/1 | 2 | 0 | 0 | 0 | 0 | 2 |
| py-0018-naive-local-vs-utc | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0018-naive-local-vs-utc | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0018-naive-local-vs-utc | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0019-clean-parameterized-query | L0 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0019-clean-parameterized-query | L1 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0019-clean-parameterized-query | L2 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0020-clean-pagination | L0 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0020-clean-pagination | L1 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0020-clean-pagination | L2 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0021-clean-locked-reserve | L0 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0021-clean-locked-reserve | L1 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0022-clean-compare-digest | L2 | control | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0023-requests-auth-https-downgrade | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0023-requests-auth-https-downgrade | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0023-requests-auth-https-downgrade | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0024-urllib3-cookie-redirect | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0024-urllib3-cookie-redirect | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0024-urllib3-cookie-redirect | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0025-jinja2-xmlattr-key-injection | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0025-jinja2-xmlattr-key-injection | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0025-jinja2-xmlattr-key-injection | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0026-aiohttp-static-symlink-traversal | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0027-gitpython-clone-ext-protocol-rce | L2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
