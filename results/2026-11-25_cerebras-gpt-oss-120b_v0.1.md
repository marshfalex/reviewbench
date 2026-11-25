# cerebras / gpt-oss-120b — ReviewBench v0.1

Created 2026-11-25T00:43:06+00:00, k=3 runs per case and level, status `complete`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 18/23 (78%, 58–90) | 16/23 (70%, 49–84) | 50/69 runs; per-bug mean 72% (95% CI 52–86, 23 bugs) | not measured (18 of 19 unjudged) | 1/12 (8%, 2–35) | 18 | 0 |
| L0 | easy | 13/15 (87%, 62–96) | 11/15 (73%, 48–89) | 35/45 runs; per-bug mean 78% (95% CI 53–92, 15 bugs) | not measured (18 of 19 unjudged) | 1/12 (8%, 2–35) | 14 | 0 |
| L0 | hard | 5/8 (62%, 31–86) | 5/8 (62%, 31–86) | 15/24 runs; per-bug mean 62% (95% CI 31–86, 8 bugs) | not measured (18 of 19 unjudged) | n/a | 4 | 0 |
| L1 | all | 17/23 (74%, 54–88) | 16/23 (70%, 49–84) | 49/69 runs; per-bug mean 71% (95% CI 51–85, 23 bugs) | not measured (17 of 20 unjudged) | 3/12 (25%, 9–53) | 17 | 0 |
| L1 | easy | 12/15 (80%, 55–93) | 12/15 (80%, 55–93) | 36/45 runs; per-bug mean 80% (95% CI 55–93, 15 bugs) | not measured (17 of 20 unjudged) | 3/12 (25%, 9–53) | 13 | 0 |
| L1 | hard | 5/8 (62%, 31–86) | 4/8 (50%, 22–78) | 13/24 runs; per-bug mean 54% (95% CI 24–81, 8 bugs) | not measured (17 of 20 unjudged) | n/a | 4 | 0 |
| L2 | all | 16/23 (70%, 49–84) | 16/23 (70%, 49–84) | 48/69 runs; per-bug mean 70% (95% CI 49–84, 23 bugs) | not measured (20 of 20 unjudged) | 0/12 (0%, 0–24) | 20 | 0 |
| L2 | easy | 12/15 (80%, 55–93) | 12/15 (80%, 55–93) | 36/45 runs; per-bug mean 80% (95% CI 55–93, 15 bugs) | not measured (20 of 20 unjudged) | 0/12 (0%, 0–24) | 12 | 0 |
| L2 | hard | 4/8 (50%, 22–78) | 4/8 (50%, 22–78) | 12/24 runs; per-bug mean 50% (95% CI 22–78, 8 bugs) | not measured (20 of 20 unjudged) | n/a | 8 | 0 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L1 | 3/3 | 3 | 2 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L2 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L0 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L0 | 0/3 | 0 | 0 | 0 | 0 | 5 | 0 |
| py-0004-missing-admin-check | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L2 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L0 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L1 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L0 | 1/3 | 1 | 1 | 0 | 0 | 2 | 0 |
| py-0010-timing-unsafe-compare | L1 | 3/3 | 3 | 2 | 0 | 0 | 1 | 0 |
| py-0010-timing-unsafe-compare | L2 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L1 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L2 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L0 | 3/3 | 6 | 0 | 0 | 0 | 1 | 0 |
| py-0015-retry-double-charge | L1 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L2 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0017-cursor-pagination-skips | L0 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L1 | 1/3 | 1 | 0 | 0 | 0 | 1 | 0 |
| py-0017-cursor-pagination-skips | L2 | 0/3 | 0 | 0 | 0 | 0 | 2 | 0 |
| py-0018-naive-local-vs-utc | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0018-naive-local-vs-utc | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0019-clean-parameterized-query | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0020-clean-pagination | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L0 | control | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L1 | control | 0 | 2 | 0 | 0 | 1 | 0 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 1 | 2 | 0 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 3 | 0 | 0 |
| py-0022-clean-compare-digest | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0023-requests-auth-https-downgrade | L2 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0024-urllib3-cookie-redirect | L0 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0024-urllib3-cookie-redirect | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0024-urllib3-cookie-redirect | L2 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L0 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L2 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L0 | 0/3 | 0 | 6 | 0 | 0 | 0 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 0/3 | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 0/3 | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 0/3 | 0 | 3 | 0 | 0 | 3 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 0/3 | 0 | 3 | 0 | 0 | 5 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L2 | 0/3 | 0 | 3 | 0 | 0 | 6 | 0 |
