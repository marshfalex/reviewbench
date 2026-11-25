# groq / qwen/qwen3.8-27b — ReviewBench v0.1

Created 2026-11-25T00:43:06+00:00, k=3 runs per case and level, status `complete`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 21/23 (91%, 73–98) | 20/23 (87%, 68–96) | 62/69 runs; per-bug mean 90% (95% CI 71–97, 23 bugs) | not measured (8 of 12 unjudged) | 3/12 (25%, 9–53) | 8 | 0 |
| L0 | easy | 14/15 (93%, 70–99) | 14/15 (93%, 70–99) | 42/45 runs; per-bug mean 93% (95% CI 70–99, 15 bugs) | not measured (8 of 12 unjudged) | 3/12 (25%, 9–53) | 6 | 0 |
| L0 | hard | 7/8 (88%, 53–98) | 6/8 (75%, 41–93) | 20/24 runs; per-bug mean 83% (95% CI 49–96, 8 bugs) | not measured (8 of 12 unjudged) | n/a | 2 | 0 |
| L1 | all | 21/22 (95%, 78–99) | 21/22 (95%, 78–99) | 63/66 runs; per-bug mean 95% (95% CI 78–99, 22 bugs) | not measured (1 of 4 unjudged) | 3/12 (25%, 9–53) | 1 | 3 |
| L1 | easy | 14/15 (93%, 70–99) | 14/15 (93%, 70–99) | 42/45 runs; per-bug mean 93% (95% CI 70–99, 15 bugs) | not measured (1 of 4 unjudged) | 3/12 (25%, 9–53) | 1 | 0 |
| L1 | hard | 7/7 (100%, 65–100) | 7/7 (100%, 65–100) | 21/21 runs; per-bug mean 100% (95% CI 65–100, 7 bugs) | not measured (1 of 4 unjudged) | n/a | 0 | 3 |
| L2 | all | 22/23 (96%, 79–99) | 22/23 (96%, 79–99) | 65/68 runs; per-bug mean 96% (95% CI 79–99, 23 bugs) | not measured (3 of 3 unjudged) | 0/12 (0%, 0–24) | 3 | 1 |
| L2 | easy | 14/15 (93%, 70–99) | 14/15 (93%, 70–99) | 42/45 runs; per-bug mean 93% (95% CI 70–99, 15 bugs) | not measured (3 of 3 unjudged) | 0/12 (0%, 0–24) | 3 | 0 |
| L2 | hard | 8/8 (100%, 68–100) | 8/8 (100%, 68–100) | 23/23 runs; per-bug mean 100% (95% CI 68–100, 8 bugs) | not measured (3 of 3 unjudged) | n/a | 0 | 1 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0002-hardcoded-secret | L1 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L2 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L2 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L0 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L1 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L2 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L0 | 3/3 | 8 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L1 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L2 | 3/3 | 9 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L0 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L1 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
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
| py-0021-clean-locked-reserve | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 4 | 0 | 0 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 3 | 1 | 0 |
| py-0022-clean-compare-digest | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L0 | 2/3 | 4 | 3 | 0 | 0 | 2 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 3 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 2/2 | 2 | 2 | 0 | 0 | 0 | 1 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 0/3 | 0 | 3 | 0 | 0 | 3 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 0/3 | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L2 | 0/3 | 0 | 3 | 0 | 0 | 0 | 0 |
