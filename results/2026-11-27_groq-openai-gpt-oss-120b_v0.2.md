# groq / openai/gpt-oss-120b — ReviewBench v0.2

Created 2026-11-27T00:42:12+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 24/29 (83%, 66–92) | 22/29 (76%, 58–88) | 70/87 runs; per-bug mean 80% (95% CI 63–91, 29 bugs) | not measured (37 of 40 unjudged) | 3/21 (14%, 5–35) | 37 | 0 |
| L0 | easy | 16/17 (94%, 73–99) | 15/17 (88%, 66–97) | 47/51 runs; per-bug mean 92% (95% CI 70–98, 17 bugs) | not measured (37 of 40 unjudged) | 3/12 (25%, 9–53) | 12 | 0 |
| L0 | hard | 8/12 (67%, 39–86) | 7/12 (58%, 32–81) | 23/36 runs; per-bug mean 64% (95% CI 37–84, 12 bugs) | not measured (37 of 40 unjudged) | 0/9 (0%, 0–30) | 25 | 0 |
| L1 | all | 24/28 (86%, 68–94) | 18/28 (64%, 46–79) | 60/84 runs; per-bug mean 71% (95% CI 53–85, 28 bugs) | not measured (27 of 30 unjudged) | 3/21 (14%, 5–35) | 27 | 1 |
| L1 | easy | 16/16 (100%, 81–100) | 12/16 (75%, 50–90) | 40/48 runs; per-bug mean 83% (95% CI 59–95, 16 bugs) | not measured (27 of 30 unjudged) | 3/12 (25%, 9–53) | 10 | 1 |
| L1 | hard | 8/12 (67%, 39–86) | 6/12 (50%, 25–75) | 20/36 runs; per-bug mean 56% (95% CI 30–79, 12 bugs) | not measured (27 of 30 unjudged) | 0/9 (0%, 0–30) | 17 | 0 |
| L2 | all | 26/28 (93%, 77–98) | 20/28 (71%, 53–85) | 67/84 runs; per-bug mean 80% (95% CI 62–91, 28 bugs) | not measured (32 of 32 unjudged) | 0/21 (0%, 0–16) | 32 | 0 |
| L2 | easy | 16/16 (100%, 81–100) | 13/16 (81%, 57–93) | 42/48 runs; per-bug mean 88% (95% CI 64–97, 16 bugs) | not measured (32 of 32 unjudged) | 0/12 (0%, 0–24) | 10 | 0 |
| L2 | hard | 10/12 (83%, 55–95) | 7/12 (58%, 32–81) | 25/36 runs; per-bug mean 69% (95% CI 42–88, 12 bugs) | not measured (32 of 32 unjudged) | 0/9 (0%, 0–30) | 22 | 0 |

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
| py-0031-refactor-drops-login-required | L2 | 3/3 | 3 | 0 | 0 | 0 | 4 | 0 |
| py-0032-refactor-pagination-off-by-one | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0032-refactor-pagination-off-by-one | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0032-refactor-pagination-off-by-one | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0033-clean-click-help-formfeed | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0033-clean-click-help-formfeed | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0033-clean-click-help-formfeed | L2 | control | 0 | 0 | 0 | 0 | 2 | 0 |
| py-0034-clean-click-completion-var-dots | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0034-clean-click-completion-var-dots | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0034-clean-click-completion-var-dots | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0035-gitpython-ref-path-traversal | L0 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0035-gitpython-ref-path-traversal | L1 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0035-gitpython-ref-path-traversal | L2 | 1/3 | 1 | 0 | 0 | 0 | 2 | 0 |
| py-0036-django-admindocs-template-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0036-django-admindocs-template-traversal | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 1 |
