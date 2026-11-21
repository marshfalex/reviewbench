# groq / openai/gpt-oss-120b — ReviewBench v0.1

Created 2026-11-19T07:36:57+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 21/23 (91%, 73–98) | 17/23 (74%, 54–88) | 58/69 (84%, 74–91) | 83/86 (97%, 90–99) | 3/12 (25%, 9–53) | 12 | 0 |
| L0 | easy | 15/15 (100%, 80–100) | 13/15 (87%, 62–96) | 43/45 (96%, 85–99) | 59/62 (95%, 87–98) | 3/12 (25%, 9–53) | 7 | 0 |
| L0 | hard | 6/8 (75%, 41–93) | 4/8 (50%, 22–78) | 15/24 (62%, 43–79) | 24/24 (100%, 86–100) | n/a | 5 | 0 |
| L1 | all | 18/22 (82%, 62–93) | 16/22 (73%, 52–87) | 51/65 (78%, 67–87) | 59/62 (95%, 87–98) | 3/12 (25%, 9–53) | 17 | 2 |
| L1 | easy | 12/14 (86%, 60–96) | 12/14 (86%, 60–96) | 36/41 (88%, 74–95) | 40/43 (93%, 81–98) | 3/12 (25%, 9–53) | 13 | 2 |
| L1 | hard | 6/8 (75%, 41–93) | 4/8 (50%, 22–78) | 15/24 (62%, 43–79) | 19/19 (100%, 83–100) | n/a | 4 | 0 |
| L2 | all | 21/22 (95%, 78–99) | 15/22 (68%, 47–84) | 53/66 (80%, 69–88) | 66/66 (100%, 94–100) | 0/12 (0%, 0–24) | 14 | 0 |
| L2 | easy | 13/14 (93%, 68–99) | 11/14 (79%, 52–92) | 36/42 (86%, 72–93) | 46/46 (100%, 92–100) | 0/12 (0%, 0–24) | 9 | 0 |
| L2 | hard | 8/8 (100%, 68–100) | 4/8 (50%, 22–78) | 17/24 (71%, 51–85) | 20/20 (100%, 84–100) | n/a | 5 | 0 |

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
| py-0021-clean-locked-reserve | L1 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 2 | 0 | 0 | 1 | 0 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 3 | 0 | 0 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 3 | 1 | 0 |
| py-0022-clean-compare-digest | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L1 | 0/2 | 0 | 0 | 0 | 0 | 2 | 1 |
| py-0023-requests-auth-https-downgrade | L2 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0024-urllib3-cookie-redirect | L0 | 2/3 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0024-urllib3-cookie-redirect | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0024-urllib3-cookie-redirect | L2 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L0 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L1 | 2/3 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L2 | 2/3 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L0 | 0/3 | 0 | 5 | 0 | 0 | 1 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 0/3 | 0 | 3 | 0 | 0 | 1 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 1/3 | 1 | 3 | 0 | 0 | 1 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 2/3 | 2 | 3 | 0 | 0 | 2 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 1 |
