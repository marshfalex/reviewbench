# groq / openai/gpt-oss-120b — ReviewBench v0.2

Created 2026-11-27T00:42:12+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 21/23 (91%, 73–98) | 20/23 (87%, 68–96) | 62/69 runs; per-bug mean 90% (95% CI 71–97, 23 bugs) | not measured (18 of 21 unjudged) | 3/12 (25%, 9–53) | 18 | 0 |
| L0 | easy | 15/15 (100%, 80–100) | 14/15 (93%, 70–99) | 44/45 runs; per-bug mean 98% (95% CI 76–100, 15 bugs) | not measured (18 of 21 unjudged) | 3/12 (25%, 9–53) | 9 | 0 |
| L0 | hard | 6/8 (75%, 41–93) | 6/8 (75%, 41–93) | 18/24 runs; per-bug mean 75% (95% CI 41–93, 8 bugs) | not measured (18 of 21 unjudged) | n/a | 9 | 0 |
| L1 | all | 20/22 (91%, 72–98) | 16/22 (73%, 52–87) | 52/66 runs; per-bug mean 79% (95% CI 58–91, 22 bugs) | not measured (15 of 18 unjudged) | 3/12 (25%, 9–53) | 15 | 1 |
| L1 | easy | 14/14 (100%, 78–100) | 12/14 (86%, 60–96) | 38/42 runs; per-bug mean 90% (95% CI 66–98, 14 bugs) | not measured (15 of 18 unjudged) | 3/12 (25%, 9–53) | 5 | 1 |
| L1 | hard | 6/8 (75%, 41–93) | 4/8 (50%, 22–78) | 14/24 runs; per-bug mean 58% (95% CI 27–84, 8 bugs) | not measured (15 of 18 unjudged) | n/a | 10 | 0 |
| L2 | all | 20/22 (91%, 72–98) | 16/22 (73%, 52–87) | 53/66 runs; per-bug mean 80% (95% CI 60–92, 22 bugs) | not measured (16 of 16 unjudged) | 0/12 (0%, 0–24) | 16 | 0 |
| L2 | easy | 14/14 (100%, 78–100) | 13/14 (93%, 68–99) | 40/42 runs; per-bug mean 95% (95% CI 72–99, 14 bugs) | not measured (16 of 16 unjudged) | 0/12 (0%, 0–24) | 5 | 0 |
| L2 | hard | 6/8 (75%, 41–93) | 3/8 (38%, 14–69) | 13/24 runs; per-bug mean 54% (95% CI 24–81, 8 bugs) | not measured (16 of 16 unjudged) | n/a | 11 | 0 |

## Per case

| case | level | caught (runs) | hit | known | valid | invalid | unadj. | errors |
|---|---|---|---|---|---|---|---|---|
| py-0001-sql-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0001-sql-injection | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0002-hardcoded-secret | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0002-hardcoded-secret | L2 | 3/3 | 3 | 0 | 0 | 0 | 1 | 0 |
| py-0003-off-by-one-page | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0003-off-by-one-page | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L1 | 3/3 | 4 | 0 | 0 | 0 | 0 | 0 |
| py-0004-missing-admin-check | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L0 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L1 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0005-check-then-act-race | L2 | 3/3 | 3 | 2 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0006-path-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0007-pickle-cookie | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L0 | 3/3 | 3 | 1 | 0 | 0 | 1 | 0 |
| py-0008-mutable-default | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0008-mutable-default | L2 | 3/3 | 3 | 1 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L0 | 3/3 | 5 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0009-swallowed-exception | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L0 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L1 | 3/3 | 3 | 3 | 0 | 0 | 0 | 0 |
| py-0010-timing-unsafe-compare | L2 | 3/3 | 3 | 2 | 0 | 0 | 1 | 0 |
| py-0011-trial-boundary | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0011-trial-boundary | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0012-ssrf-preview | L0 | 3/3 | 3 | 1 | 0 | 0 | 2 | 0 |
| py-0012-ssrf-preview | L1 | 3/3 | 3 | 0 | 0 | 0 | 1 | 0 |
| py-0012-ssrf-preview | L2 | 3/3 | 3 | 1 | 0 | 0 | 1 | 0 |
| py-0013-idor-invoice | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L0 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0015-retry-double-charge | L1 | 0/3 | 0 | 0 | 0 | 0 | 5 | 0 |
| py-0015-retry-double-charge | L2 | 0/3 | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0016-float-money | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0016-float-money | L1 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0016-float-money | L2 | 1/3 | 1 | 0 | 0 | 0 | 0 | 0 |
| py-0017-cursor-pagination-skips | L0 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0017-cursor-pagination-skips | L1 | 0/3 | 0 | 0 | 0 | 0 | 2 | 0 |
| py-0017-cursor-pagination-skips | L2 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
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
| py-0021-clean-locked-reserve | L1 | control | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 3 | 0 | 0 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 3 | 0 | 0 |
| py-0022-clean-compare-digest | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0023-requests-auth-https-downgrade | L1 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0023-requests-auth-https-downgrade | L2 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0024-urllib3-cookie-redirect | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0024-urllib3-cookie-redirect | L1 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0024-urllib3-cookie-redirect | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0025-jinja2-xmlattr-key-injection | L2 | 2/3 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L0 | 3/3 | 3 | 2 | 0 | 0 | 0 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 1/3 | 2 | 0 | 0 | 0 | 1 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 1/3 | 1 | 3 | 0 | 0 | 1 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 2/3 | 2 | 2 | 0 | 0 | 2 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 1 |
