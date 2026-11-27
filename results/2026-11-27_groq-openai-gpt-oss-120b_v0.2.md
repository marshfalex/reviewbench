# groq / openai/gpt-oss-120b — ReviewBench v0.2

Created 2026-11-27T00:42:12+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 22/26 (85%, 66–94) | 20/26 (77%, 58–89) | 64/78 runs; per-bug mean 82% (95% CI 64–92, 26 bugs) | not measured (31 of 34 unjudged) | 3/15 (20%, 7–45) | 31 | 0 |
| L0 | easy | 15/15 (100%, 80–100) | 14/15 (93%, 70–99) | 44/45 runs; per-bug mean 98% (95% CI 76–100, 15 bugs) | not measured (31 of 34 unjudged) | 3/12 (25%, 9–53) | 9 | 0 |
| L0 | hard | 7/11 (64%, 35–85) | 6/11 (55%, 28–79) | 20/33 runs; per-bug mean 61% (95% CI 33–83, 11 bugs) | not measured (31 of 34 unjudged) | 0/3 (0%, 0–56) | 22 | 0 |
| L1 | all | 22/26 (85%, 66–94) | 17/26 (65%, 46–81) | 56/78 runs; per-bug mean 72% (95% CI 53–85, 26 bugs) | not measured (25 of 28 unjudged) | 3/15 (20%, 7–45) | 25 | 0 |
| L1 | easy | 15/15 (100%, 80–100) | 12/15 (80%, 55–93) | 39/45 runs; per-bug mean 87% (95% CI 62–96, 15 bugs) | not measured (25 of 28 unjudged) | 3/12 (25%, 9–53) | 8 | 0 |
| L1 | hard | 7/11 (64%, 35–85) | 5/11 (45%, 21–72) | 17/33 runs; per-bug mean 52% (95% CI 26–77, 11 bugs) | not measured (25 of 28 unjudged) | 0/3 (0%, 0–56) | 17 | 0 |
| L2 | all | 24/26 (92%, 76–98) | 19/26 (73%, 54–86) | 62/77 runs; per-bug mean 81% (95% CI 62–91, 26 bugs) | not measured (28 of 28 unjudged) | 0/15 (0%, 0–20) | 28 | 0 |
| L2 | easy | 15/15 (100%, 80–100) | 13/15 (87%, 62–96) | 41/45 runs; per-bug mean 91% (95% CI 67–98, 15 bugs) | not measured (28 of 28 unjudged) | 0/12 (0%, 0–24) | 8 | 0 |
| L2 | hard | 9/11 (82%, 52–95) | 6/11 (55%, 28–79) | 21/32 runs; per-bug mean 67% (95% CI 38–87, 11 bugs) | not measured (28 of 28 unjudged) | 0/3 (0%, 0–56) | 20 | 0 |

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
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 1/3 | 1 | 2 | 0 | 0 | 3 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L2 | 1/3 | 1 | 2 | 0 | 0 | 3 | 0 |
| py-0028-truthy-permission-decision | L0 | 0/3 | 0 | 0 | 0 | 0 | 1 | 0 |
| py-0028-truthy-permission-decision | L1 | 0/3 | 0 | 0 | 0 | 0 | 1 | 0 |
| py-0028-truthy-permission-decision | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0029-ttl-seconds-vs-ms-clock | L0 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0029-ttl-seconds-vs-ms-clock | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0029-ttl-seconds-vs-ms-clock | L2 | 3/3 | 3 | 0 | 0 | 0 | 2 | 0 |
| py-0030-clean-sort-column-whitelist | L0 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0030-clean-sort-column-whitelist | L1 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0030-clean-sort-column-whitelist | L2 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0031-refactor-drops-login-required | L0 | 2/3 | 2 | 0 | 0 | 0 | 6 | 0 |
| py-0031-refactor-drops-login-required | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0031-refactor-drops-login-required | L2 | 2/2 | 2 | 0 | 0 | 0 | 4 | 0 |
