# Provider data-use table

Which providers may receive **held-out cases** (SPEC §10). A provider qualifies only if its
published terms *forbid* training on API inputs for the tier we use. "Doesn't retain" or "not
stated" does not qualify. Re-check each provider before approving it and at least every 3 months;
terms change.

Checked **2026-11-23** from public pages (links below). This is a reading of public text, not
legal advice. Where a provider points to a contract we can't see, the answer is *unverified*.

| provider (tier we use) | trains on API inputs? | retention | held-out? | source |
|---|---|---|---|---|
| Groq (free) | **not stated** in public docs; third parties report the Services Agreement forbids it, but we couldn't read that text | none by default; logs kept for reliability/abuse investigations; ZDR available | **no** (unverified) | [Your data](https://console.groq.com/docs/your-data), [privacy](https://groq.com/privacy-policy) |
| Gemini (free / unpaid quota) | **yes**: unpaid use improves Google products; human reviewers may read inputs | logged | **no** | [Gemini API terms](https://ai.google.dev/gemini-api/terms) |
| OpenRouter (`:free` models) | **depends on the host** serving the request; several free hosts may train | per host; OpenRouter itself doesn't log unless opted in | **no** | [provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging) |
| Cerebras (free) | **not stated**; policy says inference inputs/outputs aren't retained | not retained; operational logs kept as needed | **no** (unverified) | [privacy policy](https://www.cerebras.ai/privacy-policy), [help: retention](https://cerebras-inference.help.usepylon.com/articles/1811589793-does-cerebras-retain-my-data) |
| Mistral (Experiment, free) | **yes by default**; can be switched off in the Admin Console (Privacy → training toggle) | per plan | **no** (owner could opt out) | [Experiment plan](https://help.mistral.ai/en/articles/455206-how-can-i-try-the-api-for-free-with-the-experiment-plan), [opt out](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training) |

## What would change a "no"
- **Groq:** the owner reads the Groq Services Agreement / DPA that applies to their account and
  confirms the no-training clause covers free-tier API use. Enabling Zero Data Retention in Groq's
  Data Controls is a sensible extra.
- **Mistral:** the owner disables training in the Admin Console. That is an opt-out, so record the
  date it was switched off.
- **Cerebras:** a written no-training statement from Cerebras (docs or support reply).
- **Gemini, OpenRouter free:** no free path; paid tiers would be needed (costs money: `[owner]`).

## Consequences
- `lineup.yaml`: every entry is `heldout_ok: false` until a row above says **yes**.
- Held-out results so far: no workflow loads `REVIEWBENCH_HELDOUT` and no committed result
  mentions held-out cases, so they very likely never reached a provider. The owner confirms this
  from the run logs (roadmap item).
