# What could make ReviewBench's numbers wrong

An honest list, most serious first. Each item says what it breaks, where it stands, and what fixes
it. Sessions should treat these as standing priorities, and the findings report must repeat any
that still apply. Last reviewed 2026-11-24.

## 1. Precision is unmeasured
**Breaks:** every precision number and the noise flag's control-FPR half.
**Status:** 0 of ~750 v0.1 findings have a human verdict. Groq has 6 rule verdicts, and these
produce its "3/12 control runs with FP". The leaderboard's "precision 100%" only counts findings
that hit a planted bug, because unjudged findings are excluded. It is not evidence of low noise.
**Fix:** the owner's blind adjudication pass (roadmap). Meanwhile (done 2026-11-23) reports show
"not measured (N of M unjudged)" until 80% of the findings needing a verdict have one, and the
noise flag marks the control FPR as a lower bound while control findings are unjudged.

## 2. n is far too small to rank models
**Breaks:** any claim that model A beats model B.
**Status:** 23 planted bugs in v0.1. The k = 3 runs per bug are not independent (byte-identical
for cerebras at temperature 0; groq's catch/miss differs across runs on only 4 of 23 bugs), so
intervals use the bug as the unit (since 2026-11-24). They are 15–40 points wide and every model
pair overlaps. 4 controls (12 runs) can't measure a false-positive rate at all.
**Fix:** v0.2 targets: at least 100 planted bugs and 36 controls. Until then, report only
differences whose intervals don't overlap, and say so.

## 3. The cases are written by an LLM and judged on LLMs
**Breaks:** external validity: planted bugs may be "LLM-shaped" (textbook, well-commented,
small) and easier for LLMs than real bugs. Also a conflict of interest: Claude wrote the synthetic
cases since py-0028, so evaluating Claude models on them would be self-grading.
**Status:** of 62 cases, 13 are real CVEs (8 held for v0.2) and 22 are real upstream controls (all v0.2); 27 are synthetic. v0.1 itself is 22 synthetic + 5 CVE.
**Fix:** shift the mix toward real bugs (CVE fixes, upstream postmortems, reverted commits). The
leaderboard reports synthetic and real cases separately (since 2026-11-24). First signal: groq
gpt-oss-120b catches 94% of synthetic bugs but 47% of real ones at L0 (5 real bugs; partly matcher
artifacts), so the concern is live. Never evaluate a model family on cases its own family wrote
without saying so in the table.

## 4. Contamination
**Breaks:** recall on public cases, especially CVEs, whose fixes and write-ups are in training data.
**Status:** the held-out set is 5 cases, too few to detect a public-vs-held-out gap, and no
provider is currently cleared to receive it (docs/providers.md). **The 5 are also exposed:** the
public roadmap named them from 2026-11-19 until 2026-11-24, and git history keeps that text, so
they can't serve as a contamination check any more. Found 2026-11-24 when an automated check stopped
a session from naming one of them in the journal.
**Fix:** replace the held-out set (owner, roadmap) and grow it to ≥30 real cases; clear one
provider; report the gap with intervals. Never name a held-out case anywhere in this repository.

## 5. The matcher is crude
**Breaks:** recall in both directions: a finding at the right line for the wrong reason counts
as a catch, and a correct finding on the caller (not the planted line) counts as a miss.
**Status:** file + line ±2, no check of what the finding says.
**Fix:** the defect-check matcher (roadmap), plus a published hand audit of ~50 matches with the
miss/false-match rate.

## 6. Free-tier models aren't stable objects
**Breaks:** reproducibility and comparisons over time.
**Status:** providers can change quantization, routing (OpenRouter) or the model behind a name
without notice; `auto:` lineup entries pick "the newest" model, so a resumed run could switch
models. Results record the served model id, and since 2026-11-24 a run refuses to add a review from a
different served model to an existing file (the review is not written; the job fails loudly).
**Fix:** refuse to resume a results file when the served model id changes; pin exact ids for any
run that goes into a published comparison.

## 7. One prompt
**Breaks:** "model X is better" may really mean "the prompt suits model X".
**Fix:** the prompt-sensitivity check (roadmap): 2–3 paraphrased prompts on one model.

## 8. Unreviewed automation
**Breaks:** case quality. Since 2026-11-23, non-gated PRs merge without human review. That day's
work had two errors caught before merging (an unexploitable planted bug, a wrong expected value in
a test); others may get through.
**Fix:** every new case states its harm in one sentence that a reviewer could verify; the owner
spot-checks a few cases per batch; anything found wrong becomes a regression test or a validator
rule.

## What this means for claims today
The defensible statement right now is narrow: on 23 small, mostly synthetic Python bugs, the free
models tested catch most of them from the diff alone (L0 per-run recall: qwen-3.8-27b 100%, 86–100;
gpt-oss-120b 84%, 65–94; 95% CIs with the bug as the unit). The intervals overlap, so **no model
ranking is supported**. Nothing about precision, noise, real-world bug finding, or commercial
reviewers is supported yet.
