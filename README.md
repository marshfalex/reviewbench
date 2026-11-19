# ReviewBench

An open benchmark for **AI pull-request reviewers**. Give a reviewer a PR
with a known bug (or a known-clean PR), see whether it finds the bug, and
whether the other things it says are true. Re-run it when a new model ships
and publish the numbers.

ReviewBench v0.1: 27 Python cases: 22 synthetic (12 textbook bugs, 6 hard
logic/context bugs, 4 clean controls) and 5 reversed fixes of real CVEs. Spec: [docs/SPEC.md](docs/SPEC.md). Results:
[results/LEADERBOARD.md](results/LEADERBOARD.md).

## Why

Vendor demos of AI code review show the hits. What you need to know before
relying on one is different:

* **Hard bugs, not just textbook ones.** Reviewers reliably catch SQL
  injection and pickle. They miss bugs that only exist because of the data
  (a cursor over a non-unique timestamp) or the surrounding code.
* **Consistency.** In the prototype, a model caught a float-money bug in 1 of
  3 runs on identical input. ReviewBench reports both *any-of-k* and
  *all-of-k* recall.
* **Context.** Reviewers that see only the diff raise confident false
  positives about code they can't see. Context is a measured variable:
  L0 (diff), L1 (+ changed files), L2 (+ related files).
* **Honest precision.** Extra findings are often real issues, not noise.
  Precision is computed only over human-adjudicated findings, and the number
  still pending is always shown.
* **Small n, stated.** Every number carries its n and a Wilson 95% interval.

## Quick start

```bash
pip install -e '.[dev]'
```

```bash
python -m reviewbench validate
```

```bash
python -m reviewbench estimate --provider groq
```

Run on Groq's free tier (`openai/gpt-oss-120b` by default; get a key at console.groq.com):

```bash
GROQ_API_KEY=... python -m reviewbench run --provider groq -k 3 --levels L0,L1,L2
```

Run against a local model with Ollama (free):

```bash
python -m reviewbench run --provider ollama --model qwen2.5-coder:7b
```

Claude is **paid**. The run prints an estimate and refuses to start without
`--yes` or a `--max-usd` cap:

```bash
ANTHROPIC_API_KEY=... python -m reviewbench run --provider anthropic --model claude-haiku-5-5 --max-usd 1
```

Then judge the findings that aren't planted bugs, and rebuild the leaderboard:

```bash
python -m reviewbench adjudicate results/<file>.json
```

```bash
python -m reviewbench leaderboard
```

### From GitHub Actions

`Actions → benchmark → Run workflow` takes a provider, model, k, levels and,
for paid providers, `max_usd`. It runs the benchmark and commits the results
and leaderboard. Needs the repository secret `GROQ_API_KEY` (and
`ANTHROPIC_API_KEY` for Claude). Findings not covered by
`adjudications/rules.yaml` stay unadjudicated until you run `adjudicate`
locally and commit the verdicts.

## Contributing a case

1. Create `cases/py-NNNN-short-slug/` (next free number).
2. `repo/`: the smallest codebase *before* the PR that makes the bug
   meaningful. Include the files a careful reviewer would open.
3. `pr.diff`: the PR, as `git diff` output. It must `git apply` to `repo/`.
4. `case.yaml`: see the [spec](docs/SPEC.md#caseyaml). Bug line numbers are
   in the post-PR file. A clean control has `bugs: []`. List real but
   unplanted issues under `known_issues`. Record provenance and a permissive
   license under `source`.
5. `python -m reviewbench validate && pytest`, then open a PR.

Real bugs are preferred over synthetic ones: reversed CVE fix commits and
public postmortems, with provenance. Code under `cases/` is buggy on purpose
and is excluded from linting.

Want a case kept out of training data? Don't open a PR. Keep it in a private
directory and point `REVIEWBENCH_HELDOUT` at it (or use the git-ignored
`heldout/`). Held-out results are reported separately and only as aggregate
numbers; per-case details stay in the git-ignored `results/raw/`.

## Layout

```
cases/                     public cases
heldout/                   private held-out cases (git-ignored)
adjudications/rules.yaml   reusable human verdicts
results/                   versioned results, adjudications, LEADERBOARD.md
src/reviewbench/           runner, adapters, scoring
docs/SPEC.md               the benchmark definition
```

## Provenance

The prompt, adapters, scoring idea, Wilson interval and the 22 initial cases
were copied and adapted from the AI-review prototype in
[marshfalex/fda-device-rag](https://github.com/marshfalex/fda-device-rag).
ReviewBench does not depend on that repository.

## License

MIT. Imported cases keep their upstream license, recorded in each `case.yaml`.
