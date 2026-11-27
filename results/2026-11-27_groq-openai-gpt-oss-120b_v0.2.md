# groq / openai/gpt-oss-120b — ReviewBench v0.2

Created 2026-11-27T00:42:12+00:00, k=3 runs per case and level, status `partial`. Rates are hits/n (%, Wilson 95% CI).

## public

| level | difficulty | any-of-k recall | all-of-k recall | per-run recall | precision (adjudicated) | control runs w/ FP | unadjudicated | errors |
|---|---|---|---|---|---|---|---|---|
| L0 | all | 18/20 (90%, 70–97) | 18/20 (90%, 70–97) | 54/60 runs; per-bug mean 90% (95% CI 70–97, 20 bugs) | not measured (16 of 19 unjudged) | 3/12 (25%, 9–53) | 16 | 0 |
| L0 | easy | 14/14 (100%, 78–100) | 14/14 (100%, 78–100) | 42/42 runs; per-bug mean 100% (95% CI 78–100, 14 bugs) | not measured (16 of 19 unjudged) | 3/12 (25%, 9–53) | 7 | 0 |
| L0 | hard | 4/6 (67%, 30–90) | 4/6 (67%, 30–90) | 12/18 runs; per-bug mean 67% (95% CI 30–90, 6 bugs) | not measured (16 of 19 unjudged) | n/a | 9 | 0 |
| L1 | all | 17/19 (89%, 69–97) | 15/19 (79%, 57–92) | 47/57 runs; per-bug mean 82% (95% CI 60–94, 19 bugs) | not measured (12 of 15 unjudged) | 3/12 (25%, 9–53) | 12 | 1 |
| L1 | easy | 13/13 (100%, 77–100) | 12/13 (92%, 67–99) | 37/39 runs; per-bug mean 95% (95% CI 70–99, 13 bugs) | not measured (12 of 15 unjudged) | 3/12 (25%, 9–53) | 3 | 1 |
| L1 | hard | 4/6 (67%, 30–90) | 3/6 (50%, 19–81) | 10/18 runs; per-bug mean 56% (95% CI 22–85, 6 bugs) | not measured (12 of 15 unjudged) | n/a | 9 | 0 |
| L2 | all | 17/19 (89%, 69–97) | 15/19 (79%, 57–92) | 47/57 runs; per-bug mean 82% (95% CI 60–94, 19 bugs) | not measured (14 of 14 unjudged) | 0/12 (0%, 0–24) | 14 | 0 |
| L2 | easy | 13/13 (100%, 77–100) | 12/13 (92%, 67–99) | 37/39 runs; per-bug mean 95% (95% CI 70–99, 13 bugs) | not measured (14 of 14 unjudged) | 0/12 (0%, 0–24) | 5 | 0 |
| L2 | hard | 4/6 (67%, 30–90) | 3/6 (50%, 19–81) | 10/18 runs; per-bug mean 56% (95% CI 22–85, 6 bugs) | not measured (14 of 14 unjudged) | n/a | 9 | 0 |

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
| py-0024-urllib3-cookie-redirect | L1 | 0/0 | 0 | 0 | 0 | 0 | 0 | 1 |
