# groq / qwen/qwen3.8-27b — ReviewBench v0.2

Created 2026-11-27T00:42:15+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 26/31 (84%, 67–93) | 26/31 (84%, 67–93) | 78/93 runs; per-bug mean 84% (95% CI 67–93, 31 bugs) | not measured (35 of 38 unjudged) | 3/30 (10%, 4–26) | 35 | 0 |
| L0 | easy | 17/17 (100%, 82–100) | 17/17 (100%, 82–100) | 51/51 runs; per-bug mean 100% (95% CI 82–100, 17 bugs) | not measured (35 of 38 unjudged) | 3/12 (25%, 9–53) | 10 | 0 |
| L0 | hard | 9/14 (64%, 39–84) | 9/14 (64%, 39–84) | 27/42 runs; per-bug mean 64% (95% CI 39–84, 14 bugs) | not measured (35 of 38 unjudged) | 0/18 (0%, 0–18) | 25 | 0 |
| L1 | all | 25/31 (81%, 64–91) | 25/31 (81%, 64–91) | 73/91 runs; per-bug mean 81% (95% CI 64–91, 31 bugs) | not measured (43 of 45 unjudged) | 2/29 (7%, 2–22) | 43 | 3 |
| L1 | easy | 16/17 (94%, 73–99) | 16/17 (94%, 73–99) | 48/51 runs; per-bug mean 94% (95% CI 73–99, 17 bugs) | not measured (43 of 45 unjudged) | 2/11 (18%, 5–48) | 4 | 1 |
| L1 | hard | 9/14 (64%, 39–84) | 9/14 (64%, 39–84) | 25/40 runs; per-bug mean 64% (95% CI 39–84, 14 bugs) | not measured (43 of 45 unjudged) | 0/18 (0%, 0–18) | 39 | 2 |
| L2 | all | 29/31 (94%, 79–98) | 28/31 (90%, 75–97) | 84/92 runs; per-bug mean 91% (95% CI 76–97, 31 bugs) | not measured (35 of 35 unjudged) | 0/28 (0%, 0–12) | 35 | 2 |
| L2 | easy | 17/17 (100%, 82–100) | 16/17 (94%, 73–99) | 49/51 runs; per-bug mean 96% (95% CI 76–99, 17 bugs) | not measured (35 of 35 unjudged) | 0/12 (0%, 0–24) | 6 | 0 |
| L2 | hard | 12/14 (86%, 60–96) | 12/14 (86%, 60–96) | 35/41 runs; per-bug mean 86% (95% CI 60–96, 14 bugs) | not measured (35 of 35 unjudged) | 0/16 (0%, 0–19) | 29 | 2 |

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
| py-0004-missing-admin-check | L1 | 3/3 | 3 | 0 | 0 | 0 | 1 | 0 |
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
| py-0012-ssrf-preview | L0 | 3/3 | 3 | 1 | 0 | 0 | 4 | 0 |
| py-0012-ssrf-preview | L1 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0012-ssrf-preview | L2 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0013-idor-invoice | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0013-idor-invoice | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0014-cache-leaks-across-users | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0015-retry-double-charge | L0 | 0/3 | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0015-retry-double-charge | L1 | 0/3 | 0 | 0 | 0 | 0 | 7 | 0 |
| py-0015-retry-double-charge | L2 | 0/3 | 0 | 0 | 0 | 0 | 7 | 0 |
| py-0016-float-money | L0 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0016-float-money | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
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
| py-0021-clean-locked-reserve | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0021-clean-locked-reserve | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0022-clean-compare-digest | L0 | control | 0 | 0 | 0 | 3 | 0 | 0 |
| py-0022-clean-compare-digest | L1 | control | 0 | 0 | 0 | 2 | 0 | 1 |
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
| py-0026-aiohttp-static-symlink-traversal | L0 | 3/3 | 6 | 0 | 0 | 0 | 0 | 0 |
| py-0026-aiohttp-static-symlink-traversal | L1 | 1/1 | 2 | 0 | 0 | 0 | 0 | 2 |
| py-0026-aiohttp-static-symlink-traversal | L2 | 2/2 | 4 | 0 | 0 | 0 | 1 | 1 |
| py-0027-gitpython-clone-ext-protocol-rce | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L1 | 0/3 | 0 | 3 | 0 | 0 | 0 | 0 |
| py-0027-gitpython-clone-ext-protocol-rce | L2 | 1/3 | 1 | 2 | 0 | 0 | 0 | 0 |
| py-0028-truthy-permission-decision | L0 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0028-truthy-permission-decision | L1 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0028-truthy-permission-decision | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0029-ttl-seconds-vs-ms-clock | L0 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0029-ttl-seconds-vs-ms-clock | L1 | 0/3 | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0029-ttl-seconds-vs-ms-clock | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0030-clean-sort-column-whitelist | L0 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0030-clean-sort-column-whitelist | L1 | control | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0030-clean-sort-column-whitelist | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0031-refactor-drops-login-required | L0 | 0/3 | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0031-refactor-drops-login-required | L1 | 0/3 | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0031-refactor-drops-login-required | L2 | 0/3 | 0 | 0 | 0 | 0 | 6 | 0 |
| py-0032-refactor-pagination-off-by-one | L0 | 3/3 | 3 | 0 | 0 | 0 | 1 | 0 |
| py-0032-refactor-pagination-off-by-one | L1 | 3/3 | 3 | 0 | 0 | 0 | 5 | 0 |
| py-0032-refactor-pagination-off-by-one | L2 | 3/3 | 3 | 0 | 0 | 0 | 6 | 0 |
| py-0033-clean-click-help-formfeed | L0 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0033-clean-click-help-formfeed | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0033-clean-click-help-formfeed | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0034-clean-click-completion-var-dots | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0034-clean-click-completion-var-dots | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0034-clean-click-completion-var-dots | L2 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0035-gitpython-ref-path-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0035-gitpython-ref-path-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0035-gitpython-ref-path-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0036-django-admindocs-template-traversal | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0036-django-admindocs-template-traversal | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0036-django-admindocs-template-traversal | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0037-pyjwt-hmac-key-confusion | L0 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0037-pyjwt-hmac-key-confusion | L1 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0037-pyjwt-hmac-key-confusion | L2 | 3/3 | 3 | 0 | 0 | 0 | 3 | 0 |
| py-0038-requests-proxy-auth-https-leak | L0 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0038-requests-proxy-auth-https-leak | L1 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0038-requests-proxy-auth-https-leak | L2 | 3/3 | 3 | 0 | 0 | 0 | 0 | 0 |
| py-0039-clean-click-abort-chains-cause | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0039-clean-click-abort-chains-cause | L1 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0039-clean-click-abort-chains-cause | L2 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0040-clean-click-empty-envvar-is-none | L0 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0040-clean-click-empty-envvar-is-none | L1 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0040-clean-click-empty-envvar-is-none | L2 | control | 0 | 0 | 0 | 0 | 3 | 0 |
| py-0041-clean-click-invalid-glob-pattern | L0 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0041-clean-click-invalid-glob-pattern | L1 | control | 0 | 0 | 0 | 0 | 0 | 0 |
| py-0041-clean-click-invalid-glob-pattern | L2 | control | 0 | 0 | 0 | 0 | 0 | 1 |
