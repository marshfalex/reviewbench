# cerebras / qwen-3.8-27b — ReviewBench v0.1

Created 2026-11-19T17:36:18+00:00, k=3 runs per case and level, status `complete`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 23/23 (100%, 86–100) | 23/23 (100%, 86–100) | 69/69 runs (100%; 95% CI 86–100 over 23 bugs) | not measured (15 of 15 unjudged) | 0/12 (0%, 0–24) | 15 | 0 |
| L0 | easy | 15/15 (100%, 80–100) | 15/15 (100%, 80–100) | 45/45 runs (100%; 95% CI 80–100 over 15 bugs) | not measured (15 of 15 unjudged) | 0/12 (0%, 0–24) | 12 | 0 |
| L0 | hard | 8/8 (100%, 68–100) | 8/8 (100%, 68–100) | 24/24 runs (100%; 95% CI 68–100 over 8 bugs) | not measured (15 of 15 unjudged) | n/a | 3 | 0 |
| L1 | all | 22/23 (96%, 79–99) | 22/23 (96%, 79–99) | 66/69 runs (96%; 95% CI 79–99 over 23 bugs) | not measured (15 of 15 unjudged) | 0/12 (0%, 0–24) | 15 | 0 |
| L1 | easy | 14/15 (93%, 70–99) | 14/15 (93%, 70–99) | 42/45 runs (93%; 95% CI 70–99 over 15 bugs) | not measured (15 of 15 unjudged) | 0/12 (0%, 0–24) | 12 | 0 |
| L1 | hard | 8/8 (100%, 68–100) | 8/8 (100%, 68–100) | 24/24 runs (100%; 95% CI 68–100 over 8 bugs) | not measured (15 of 15 unjudged) | n/a | 3 | 0 |
| L2 | all | 23/23 (100%, 86–100) | 23/23 (100%, 86–100) | 69/69 runs (100%; 95% CI 86–100 over 23 bugs) | not measured (12 of 12 unjudged) | 0/12 (0%, 0–24) | 12 | 0 |
| L2 | easy | 15/15 (100%, 80–100) | 15/15 (100%, 80–100) | 45/45 runs (100%; 95% CI 80–100 over 15 bugs) | not measured (12 of 12 unjudged) | 0/12 (0%, 0–24) | 9 | 0 |
| L2 | hard | 8/8 (100%, 68–100) | 8/8 (100%, 68–100) | 24/24 runs (100%; 95% CI 68–100 over 8 bugs) | not measured (12 of 12 unjudged) | n/a | 3 | 0 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 3/3 | 3 | 3 | 0 | 0 | 3 | 0 |
| py-0002-hardcoded-secret | L1 | 3/3 | 3 | 3 | 0 | 0 | 3 | 0 |
| py-0002-hardcoded-secret | L2 | 3/3 | 3 | 3 | 0 | 0 | 3 | 0 |
| py-0003-off-by-one-page | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L1 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0010-timing-unsafe-compare | L1 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L2 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L0 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L0 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L1 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L2 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L0 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0021-clean-locked-reserve | L1 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0022-clean-compare-digest | L2 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0023-requests-auth-https-downgrade | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L0 | 3/3 | 3 | 3 | 0 | 0 | 3 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
