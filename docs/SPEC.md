# ReviewBench specification — v0.1

This document defines the benchmark. Any change to the case set, the
reviewer prompt or output schema, context assembly, or scoring requires a new
`BENCH_VERSION` (`src/reviewbench/__init__.py`). **Results are never compared
across benchmark versions.**

## 1. Cases

A case is a directory under `cases/` named after its id:

```
cases/py-0017-cursor-pagination-skips/
  case.yaml   # metadata + ground truth
  repo/       # minimal codebase BEFORE the PR
  pr.diff     # the PR under review (git diff format; must `git apply` cleanly to repo/)
```

### case.yaml

| field | required | meaning |
|---|---|---|
| `id` | yes | `py-NNNN-short-slug`; equals the directory name |
| `title` | yes | one line |
| `language` | yes | `python` (only language in v0.1) |
| `difficulty` | yes | `easy` (textbook pattern) or `hard` (logic / context-dependent; no "dangerous function" to pattern-match) |
| `tags` | no | free-form |
| `source.kind` | yes | `synthetic`, `cve` or `postmortem` |
| `source.ref` | yes | provenance: commit URL / CVE id / repo@sha path |
| `source.license` | yes | license of the code in `repo/` and `pr.diff` (permissive only) |
| `bugs` | yes | list of planted bugs; **empty list = clean control** |
| `bugs[].file` | yes | post-PR path; must be a file the diff touches |
| `bugs[].lines` | yes | `[start, end]`, **post-PR** line numbers, inclusive |
| `bugs[].class` | yes | short bug-class slug |
| `bugs[].cwe` | no | e.g. `CWE-89`, or null |
| `bugs[].severity` | yes | `critical`/`high`/`medium`/`low` (the bug's real severity; not used for matching) |
| `bugs[].description` | yes | what is wrong |
| `context.related` | no | post-PR paths of other files a careful reviewer would open (used at L2) |
| `known_issues` | no | `[{match, file?, note?}]`: real issues in the PR that were not planted. A finding whose title + explanation contains `match` (case/Unicode-insensitive), on `file` if given, counts as a **valid extra** automatically |

`reviewbench validate` checks all of this, applies the diff, and checks that
every bug range and related file exists in the post-PR tree.

### Splits

* **public** — `cases/`, committed.
* **held-out** — same format, kept outside this repository (the directory in
  `$REVIEWBENCH_HELDOUT`, else a git-ignored `heldout/`) and never committed,
  to limit training-set contamination. Reported in its own table. A large
  public-vs-held-out gap is a contamination signal.

Nothing that identifies a held-out case is ever committed or logged. A run
reviews held-out cases into `results/raw/<stem>.heldout.json` (git-ignored,
with its own `.adjudications.json`); the committed results file gets only a
`heldout` object of aggregate numbers (`cases`, `status`, and the
`heldout/<level>/<difficulty>` metric slices). Run logs replace held-out case
ids with `heldout-NN`. `reviewbench adjudicate` also adjudicates the raw file
when it exists locally and refreshes the aggregate; `reviewbench leaderboard`
refuses any results file that contains held-out cases or records.

Held-out cases are only sent to endpoints trusted not to log or train on
prompts: `run` and `estimate` skip them (with a log line) unless `lineup.yaml`
marks that provider/model `heldout_ok: true`. A model missing from the
lineup, an unreadable lineup, or any value but `true` means refuse.
`--allow-heldout` overrides this for endpoints such as a local Ollama.

## 2. Reviewer interface

Every adapter implements one function: `ReviewRequest -> ReviewResult`.
The request renders to one user message, identical for all adapters:

```
<diff>
...pr.diff...
</diff>

<file path="app/feed.py" role="changed">
...post-PR content...
</file>

<file path="app/schema.sql" role="related">
...
</file>
```

The system prompt and JSON output schema are fixed in
`src/reviewbench/adapters/base.py`. A finding is
`{path, line, category, severity, title, explanation}` with `line` in the new
file, `category ∈ {correctness, security, maintainability}`,
`severity ∈ {critical, high, medium, low}`. Malformed findings are dropped,
not fatal. Adapters in v0.1: `groq` (free tier), `anthropic` (paid), `ollama`
(local), `replay` (tests).

Each adapter has a prompt-size budget (Groq free tier: 24,000 chars). An
over-budget request is recorded as an errored run, never truncated.

## 3. Context levels

Context is a measured variable. Each is run and reported separately.

| level | the reviewer sees |
|---|---|
| L0 | the diff only |
| L1 | L0 + full post-PR content of every changed file |
| L2 | L1 + `context.related` files |

Hypothesis under test: more context fixes misses that depend on facts outside
the diff (e.g. a non-unique sort key) and false positives of the "can't see
the guard in the other file" kind.

Note for v0.1: the 22 ported synthetic cases are new-file PRs, so L1 adds no
information over L0 for them (the whole file is already in the diff). L0 vs
L1 becomes informative with modification PRs such as reversed CVE fixes.

## 4. Runs and consistency

Each (case, level) is reviewed **k** times (default 3) on identical input.
Consistency is first-class: a reviewer that catches a bug in 1 of 3 runs is
reported as such, not rounded up.

## 5. Scoring

Only findings with severity **medium or higher** are counted; low-severity
findings are ignored. Each counted finding gets exactly one label, in order:

1. **hit** — `path == bug.file` and `bug.lines[0] - 2 <= line <= bug.lines[1] + 2`
   (line tolerance ±2) for some planted bug;
2. **known** — matches a `known_issues` entry (valid extra);
3. **valid** / **invalid** — a human verdict in the results' adjudication file;
4. **unadjudicated** — otherwise.

A bug is **caught in a run** if at least one counted finding hits it.

## 6. Metrics

All are computed per split × context level × difficulty (`easy`, `hard`, `all`).
Every rate is published as `hits/n (%, Wilson 95% CI)`.

| metric | unit (n) | definition |
|---|---|---|
| recall any-of-k | planted bugs | caught in at least one of the k runs |
| recall all-of-k | planted bugs | caught in every one of the k runs |
| per-run recall | bug × run | caught in that run |
| precision (adjudicated) | adjudicated findings | (hit + known + valid) / (hit + known + valid + invalid). **Unadjudicated findings are excluded** and their count is always published next to it |
| control runs with confirmed FP | clean-control runs | runs with ≥1 `invalid` finding |
| errored runs | runs | API failure, refusal, over budget, unparseable output; excluded from the rates above and reported |

The gap between any-of-k and all-of-k is the consistency gap: bugs a reviewer
catches only sometimes.

## 7. Adjudication

Automatic scoring cannot tell a real unplanted issue from a false positive
(v1 of the prototype got this wrong). So:

* Verdicts are stored **next to the results they judge**:
  `results/<stem>.adjudications.json`, keyed by finding id
  (`<case>/<level>/r<run>/f<index>`), each `{verdict, by: human|rule, note}`.
* `adjudications/rules.yaml` holds reusable verdicts (`case id -> [{match,
  verdict, note}]`) that pre-fill verdicts for recurring findings; they are
  recorded with `by: rule`.
* `reviewbench adjudicate <results.json>` applies rules, then asks a human
  about each remaining finding.

When a verdict is "this is a real issue in the case", prefer adding it to the
case's `known_issues` (and bumping the benchmark version) so every future
reviewer gets the same ruling.

## 8. Results

`results/<YYYY-MM-DD>_<provider>-<model>_v<bench-version>.json` contains the
benchmark version, provider, model, k, levels, a snapshot of the ground truth
used, and every raw finding of every run (with token usage and the served
model id). Next to it: `<stem>.md` (per-run report) and
`<stem>.adjudications.json`. `reviewbench leaderboard` regenerates
`results/LEADERBOARD.md`, one table per benchmark version and split.

## 9. Cost

`reviewbench estimate` prints request count, input tokens and an upper bound
on output tokens (4,000 per review, including reasoning) without calling any
API. `reviewbench run` on a paid provider refuses to start unless given
`--yes` or `--max-usd` at or above the estimate.
