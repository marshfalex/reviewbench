import json
from pathlib import Path

from reviewbench.adapters import ReplayReviewer, get_adapter
from reviewbench.adapters.base import Finding, parse_review
from reviewbench.adjudicate import apply_rules, interactive
from reviewbench.cases import discover
from reviewbench.cli import main
from reviewbench.context import ReviewRequest
from reviewbench.report import leaderboard, run_report
from reviewbench.runner import estimate_cost, run
from reviewbench.scoring import score

CASES = Path(__file__).resolve().parents[1] / "cases"


def _oracle(prompt: str) -> list[Finding]:
    """Flags SQL injection only when it can see it; plus one spurious finding."""
    out = [Finding("app/users.py", 6, "security", "critical", "SQL injection", "f-string")] \
        if "SELECT id, email FROM users WHERE name = '{username}'" in prompt else []
    return out + [Finding("app/whatever.py", 1, "maintainability", "medium", "KeyError at import", "x")]


def test_end_to_end_replay(tmp_path):
    cases = [c for c in discover((CASES, "public")) if c.id in
             ("py-0001-sql-injection", "py-0022-clean-compare-digest")]
    out = tmp_path / "r.json"
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0", "L2"], 2, out, log=lambda m: None)
    assert json.loads(out.read_text())["status"] == "complete"
    assert len(doc["records"]) == 2 * 2 * 2
    verdicts = {}
    rules = {"py-0022-clean-compare-digest": [{"match": "keyerror", "verdict": "invalid"}]}
    assert apply_rules(doc, verdicts, rules) == 4  # only the control's spurious findings match a rule
    s = score(doc, verdicts)["slices"]["public/L0/all"]
    assert s["all_of_k"]["hits"] == 1 and s["control_runs_with_confirmed_fp"]["hits"] == 2
    assert s["unadjudicated_findings"] == 2
    answers = iter(["i", "", "v", "a note", "q"])
    assert interactive(doc, verdicts, ask=lambda _: next(answers), show=lambda *_: None) == 2
    assert "py-0001-sql-injection" in run_report(doc, verdicts)


def test_parse_review_drops_malformed():
    raw = json.dumps({"summary": "s", "findings": [
        {"path": "b/a.py", "line": "3", "category": "Security", "severity": "HIGH", "title": "t",
         "explanation": "e"},
        {"path": "a.py"},
        {"path": "a.py", "line": 1, "category": "style", "severity": "urgent", "title": "t", "explanation": "e"}]})
    summary, fs = parse_review(raw)
    assert len(fs) == 2 and fs[0].path == "a.py" and fs[0].line == 3 and fs[0].severity == "high"
    assert fs[1].category == "maintainability" and fs[1].severity == "low"


def test_prompt_budget_records_error():
    r = get_adapter("groq")
    res = r.review(ReviewRequest(diff="x" * 30_000))
    assert res.error.startswith("too_large") and res.findings == []


def test_cost_estimate_free_vs_paid():
    cases = discover((CASES, "public"))
    assert estimate_cost(cases, ["L0"], 1, get_adapter("groq"))["usd"] == 0
    est = estimate_cost(cases, ["L0", "L1", "L2"], 3, get_adapter("anthropic", "claude-haiku-5-5"))
    assert est["requests"] == len(cases) * 3 * 3 and est["usd"] > 0


def test_paid_run_refused_without_yes(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    rc = main(["run", "--provider", "anthropic", "--only", "py-0001-sql-injection", "-k", "1",
               "--results-dir", str(tmp_path)])
    assert rc == 2 and not list(tmp_path.iterdir())


def test_leaderboard_groups_by_version(tmp_path):
    cases = [c for c in discover((CASES, "public")) if c.id == "py-0001-sql-injection"]
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0"], 1, tmp_path / "a.json", log=lambda m: None)
    other = {**doc, "bench_version": "0.0"}
    (tmp_path / "b.json").write_text(json.dumps(other))
    md = leaderboard(tmp_path)
    assert "## v0.1 — public cases" in md and "## v0.0 — public cases" in md
    assert md.index("v0.1") < md.index("v0.0")


def test_groq_long_retry_after_is_recorded_not_slept(monkeypatch):
    import requests

    from reviewbench.adapters import openai_compat

    class Resp:
        status_code, headers = 429, {"retry-after": "7200"}

    slept = []
    monkeypatch.setattr(openai_compat.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setattr(requests, "post", lambda *a, **k: Resp())
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    result = openai_compat.GroqReviewer()._review("prompt")
    assert slept == [] and result.error.startswith("rate_limited")


def test_time_budget_stops_partial_and_resume_finishes(tmp_path):
    from reviewbench.runner import find_resumable

    cases = discover((CASES, "public"))[:2]
    out = tmp_path / "results" / "r.json"
    ticks = iter(range(0, 10_000, 60))  # every clock() call advances one minute
    calls = []

    def counting(request):
        calls.append(request)
        return _oracle(request)

    doc = run(cases, ReplayReviewer(fn=counting), ["L0"], 2, out, log=lambda m: None,
              max_minutes=2, clock=lambda: next(ticks))
    assert doc["status"] == "partial" and 0 < len(doc["records"]) < 4
    first = len(doc["records"])
    assert find_resumable(out.parent, doc["provider"], doc["model"], 2, ["L0"]) == out

    doc2 = run(cases, ReplayReviewer(fn=counting), ["L0"], 2, out, log=lambda m: None)
    assert doc2["status"] == "complete" and len(doc2["records"]) == 4
    assert len(calls) == 4  # resumed reviews were not repeated
    keys = {(r["case"], r["level"], r["run"]) for r in doc2["records"]}
    assert len(keys) == 4 and first < 4
    assert find_resumable(out.parent, doc["provider"], doc["model"], 2, ["L0"]) is None


def test_resume_retries_rate_limited_records(tmp_path):
    cases = discover((CASES, "public"))[:1]
    out = tmp_path / "r.json"
    from reviewbench.adapters.base import ReviewResult

    class Limited(ReplayReviewer):
        def _review(self, prompt):
            return ReviewResult("", [], error="rate_limited: quota")

    run(cases, Limited(), ["L0"], 1, out, log=lambda m: None)
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0"], 1, out, log=lambda m: None)
    assert [r["error"] for r in doc["records"]] == [None]


def test_groq_per_minute_waits_are_slept(monkeypatch):
    import requests

    from reviewbench.adapters import openai_compat

    body = {"choices": [{"message": {"content": '{"summary": "s", "findings": []}'}}], "usage": {}}

    class Limited:
        status_code, headers = 429, {"retry-after": "300"}

    class Ok:
        status_code, headers = 200, {}

        def raise_for_status(self):
            pass

        def json(self):
            return body

    responses = [Limited(), Ok()]
    slept = []
    monkeypatch.setattr(openai_compat.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setattr(requests, "post", lambda *a, **k: responses.pop(0))
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    result = openai_compat.GroqReviewer()._review("prompt")
    assert slept == [300.0] and result.error is None


def test_quota_stops_run_as_partial(tmp_path):
    from reviewbench.adapters.base import ReviewResult

    class Quota(ReplayReviewer):
        calls = 0

        def _review(self, prompt):
            Quota.calls += 1
            return ReviewResult("", [], error="rate_limited: retry-after 7200s (quota)")

    cases = discover((CASES, "public"))[:3]
    doc = run(cases, Quota(), ["L0"], 2, tmp_path / "r.json", log=lambda m: None)
    assert doc["status"] == "partial" and Quota.calls == 1


def test_free_providers_registered_and_require_a_model():
    import pytest

    for name in ("openrouter", "gemini", "cerebras", "mistral"):
        with pytest.raises(ValueError, match="pass --model"):
            get_adapter(name)
        r = get_adapter(name, "some-model")
        assert r.model == "some-model" and not r.is_paid and r.url.startswith("https://")


def test_json_mode_rejected_falls_back_to_plain(monkeypatch):
    import requests


    body = {"choices": [{"message": {"content": '{"summary": "s", "findings": []}'}}], "usage": {}}
    sent = []

    class Bad:
        status_code, headers, text = 400, {}, "response_format is not supported"

    class Ok:
        status_code, headers, text = 200, {}, ""

        def raise_for_status(self):
            pass

        def json(self):
            return body

    responses = [Bad(), Ok()]

    def post(url, headers, json, timeout):
        sent.append(dict(json))
        return responses.pop(0)

    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setenv("MISTRAL_API_KEY", "k")
    result = get_adapter("mistral", "m")._review("prompt")
    assert result.error is None
    assert "response_format" in sent[0] and "response_format" not in sent[1]


def test_pick_auto_prefers_newest_stable():
    from reviewbench.lineup import pick_auto

    ids = ["models/gemini-2.5-flash", "models/gemini-3.0-flash", "models/gemini-3.0-flash-preview",
           "models/gemini-3.0-flash-lite", "models/gemini-3.0-pro"]
    assert pick_auto(ids, "flash") == "gemini-3.0-flash"
    assert pick_auto(ids, "nothing") is None


def test_lineup_plan_skips_missing_keys_and_complete(tmp_path, monkeypatch):
    import json as _json

    from reviewbench import BENCH_VERSION
    from reviewbench.lineup import plan

    (tmp_path / "lineup.yaml").write_text(
        "k: 3\n"
        "levels: L0,L1,L2\n"
        "models:\n"
        "  - {provider: groq, model: openai/gpt-oss-120b}\n"
        "  - {provider: gemini, model: 'auto:flash'}\n"
        "  - {provider: mistral, model: m}\n"
        "  - {provider: anthropic, model: claude}\n")
    res = tmp_path / "results"
    res.mkdir()
    (res / "a.json").write_text(_json.dumps({"status": "complete", "bench_version": BENCH_VERSION,
        "provider": "mistral", "model": "m", "k": 3, "levels": ["L0", "L1", "L2"]}))
    for key in ("GROQ_API_KEY", "GEMINI_API_KEY", "MISTRAL_API_KEY", "OPENROUTER_API_KEY", "CEREBRAS_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    monkeypatch.setenv("MISTRAL_API_KEY", "m")
    entries = plan(tmp_path / "lineup.yaml", res, lister=lambda p: ["models/gemini-3.0-flash"], log=lambda m: None)
    assert entries == [{"provider": "gemini", "model": "gemini-3.0-flash", "k": "3", "levels": "L0,L1,L2"}]


def test_complete_run_missing_new_cases_is_resumed(tmp_path):
    from reviewbench import BENCH_VERSION
    from reviewbench.lineup import completed
    from reviewbench.runner import find_resumable

    doc = {"bench_version": BENCH_VERSION, "status": "complete", "provider": "p", "model": "m",
           "k": 3, "levels": ["L0"], "cases": {"a": {}}, "records": []}
    (tmp_path / "r.json").write_text(json.dumps(doc))
    assert completed(tmp_path, "p", "m", 3, ["L0"], {"a"})
    assert find_resumable(tmp_path, "p", "m", 3, ["L0"], {"a"}) is None
    assert not completed(tmp_path, "p", "m", 3, ["L0"], {"a", "b"})
    assert find_resumable(tmp_path, "p", "m", 3, ["L0"], {"a", "b"}) == tmp_path / "r.json"


def _fake_post(monkeypatch, statuses):
    import requests

    from reviewbench.adapters import openai_compat

    class Resp:
        def __init__(self, code):
            self.status_code, self.headers, self.text = code, {"retry-after": "1"}, ""

        def raise_for_status(self):
            raise requests.HTTPError(f"{self.status_code} Error")

    seq = iter(statuses)
    monkeypatch.setattr(openai_compat.time, "sleep", lambda s: None)
    monkeypatch.setattr(requests, "post", lambda *a, **k: Resp(next(seq)))
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    return openai_compat.GroqReviewer()


def test_last_429_is_rate_limited_not_an_exception(monkeypatch):
    reviewer = _fake_post(monkeypatch, [429] * 6)
    assert reviewer._review("prompt").error == "rate_limited: retries exhausted"


def test_5xx_is_retried_then_recorded_as_transient(monkeypatch):
    reviewer = _fake_post(monkeypatch, [503] * 6)
    assert reviewer._review("prompt").error == "transient: HTTP 503"


def test_retryable_covers_legacy_http_errors():
    from reviewbench.runner import retryable

    assert retryable("exception: HTTPError: 429 Client Error: Too Many Requests for url: x")
    assert retryable("exception: HTTPError: 503 Server Error: Service Unavailable for url: x")
    assert retryable("transient: HTTP 502") and retryable("rate_limited: quota")
    assert not retryable("exception: HTTPError: 400 Client Error: Bad Request for url: x")
    assert not retryable("unparseable_output: x") and not retryable(None)


def test_complete_file_with_provider_errors_is_resumed(tmp_path):
    from reviewbench.lineup import completed
    from reviewbench.runner import find_resumable

    cases = discover((CASES, "public"))[:2]
    out = tmp_path / "r.json"
    calls = []

    def flaky(request):
        calls.append(request)
        if len(calls) == 1:
            raise RuntimeError("HTTPError: 429 Client Error: Too Many Requests")
        return _oracle(request)

    doc = run(cases, ReplayReviewer(fn=flaky), ["L0"], 1, out, log=lambda m: None)
    assert doc["status"] == "partial"  # a provider error left behind is not a finished run
    args = (doc["provider"], doc["model"], 1, ["L0"])
    # Mimic a file written by the old runner, which marked such runs complete.
    out.write_text(json.dumps({**doc, "status": "complete"}))
    assert find_resumable(tmp_path, *args) == out and not completed(tmp_path, *args)
    doc2 = run(cases, ReplayReviewer(fn=flaky), ["L0"], 1, out, log=lambda m: None)
    assert doc2["status"] == "complete" and not any(r["error"] for r in doc2["records"])
    assert len(calls) == 3  # only the errored review was repeated


def test_leaderboard_marks_results_with_failed_reviews(tmp_path):
    cases = discover((CASES, "public"))[:2]
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0"], 2, tmp_path / "a.json", log=lambda m: None)
    assert "(partial)" not in leaderboard(tmp_path)
    doc["records"][0]["error"] = "exception: HTTPError: 429 Client Error: Too Many Requests for url: x"
    (tmp_path / "a.json").write_text(json.dumps(doc))  # still says status "complete", like the old files
    assert "(partial) (1 reviews failed, to retry)" in leaderboard(tmp_path)


def test_results_record_prompt_hash_and_refuse_to_mix(tmp_path, monkeypatch):
    import pytest

    from reviewbench import runner

    cases = discover((CASES, "public"))[:1]
    out = tmp_path / "r.json"
    doc = run(cases, ReplayReviewer(fn=_oracle), ["L0"], 1, out, log=lambda m: None)
    assert doc["prompt_sha256"] == runner.prompt_hash() and len(doc["prompt_sha256"]) == 16
    monkeypatch.setattr(runner, "SYSTEM_PROMPT", runner.SYSTEM_PROMPT + " changed")
    assert runner.prompt_hash() != doc["prompt_sha256"]
    with pytest.raises(ValueError, match="different prompt"):
        run(cases, ReplayReviewer(fn=_oracle), ["L0"], 2, out, log=lambda m: None)


def test_leaderboard_sorts_by_per_run_recall_and_flags_noise(tmp_path):
    cases = [c for c in discover((CASES, "public")) if c.id == "py-0001-sql-injection"]
    hit = Finding("app/users.py", 6, "security", "critical", "SQL injection", "f-string")
    noise = [Finding("app/users.py", 100 + i, "style", "medium", "nit", "x") for i in range(4)]
    run(cases, ReplayReviewer(model="weak", fn=lambda p: []), ["L0"], 1, tmp_path / "a.json",
        log=lambda m: None)
    run(cases, ReplayReviewer(model="strong", fn=lambda p: [hit, *noise]), ["L0"], 1,
        tmp_path / "b.json", log=lambda m: None)
    md = leaderboard(tmp_path)
    assert md.index("`strong`") < md.index("`weak`")
    strong = next(line for line in md.splitlines() if "`strong`" in line)
    weak = next(line for line in md.splitlines() if "`weak`" in line)
    assert "⚠ noisy: 5.0 findings/review" in strong and "noisy" not in weak


def test_blind_adjudication_hides_model_and_second_rater_gives_kappa(tmp_path):
    from reviewbench.adjudicate import (
        agreement,
        in_second_sample,
        interactive_blind,
        load_second,
        load_verdicts,
    )

    cases = [c for c in discover((CASES, "public")) if c.id == "py-0001-sql-injection"]
    noise = [Finding("app/users.py", 100 + i, "style", "medium", f"nit {i}", "x") for i in range(10)]
    paths = []
    for name in ("secret-model-a", "secret-model-b"):
        p = tmp_path / f"{name}.json"
        run(cases, ReplayReviewer(model=name, fn=lambda _: noise), ["L0"], 1, p, log=lambda m: None)
        paths.append(p)
    shown = []
    n = interactive_blind(paths, ask=lambda _: "i", show=shown.append)
    assert n == 20
    text = "\n".join(shown)
    assert "secret-model" not in text and "replay" not in text and "/r0/f" not in text
    v = load_verdicts(paths[0])
    assert len(v) == 10 and all(x["blind"] and x["verdict"] == "invalid" for x in v.values())

    sampled = sum(in_second_sample(k) for p in paths for k in load_verdicts(p))
    assert interactive_blind(paths, rater="second", ask=lambda _: "i", show=lambda _: None) == sampled
    assert sum(len(load_second(p)) for p in paths) == sampled
    a = agreement(paths)
    assert a["n"] == sampled and a["agree"] == sampled


def test_precision_hidden_until_findings_are_judged(tmp_path):
    from reviewbench.adjudicate import save_verdicts

    cases = [c for c in discover((CASES, "public")) if c.id == "py-0001-sql-injection"]
    hit = Finding("app/users.py", 6, "security", "critical", "SQL injection", "f-string")
    extra = [Finding("app/users.py", 100 + i, "style", "medium", f"nit {i}", "x") for i in range(5)]
    p = tmp_path / "a.json"
    doc = run(cases, ReplayReviewer(model="m", fn=lambda _: [hit, *extra]), ["L0"], 1, p, log=lambda m: None)
    row = next(line for line in leaderboard(tmp_path).splitlines() if "`m`" in line)
    assert "| not measured (5 of 5 unjudged) |" in row
    ids = [f["id"] for f in doc["records"][0]["findings"][1:]]
    save_verdicts(p, {i: {"verdict": "invalid", "by": "human", "note": ""} for i in ids})
    row = next(line for line in leaderboard(tmp_path).splitlines() if "`m`" in line)
    assert "1/6 (17%" in row and "not measured" not in row


def test_per_run_interval_counts_bugs_not_runs(tmp_path):
    from reviewbench.report import per_run_by_bug
    from reviewbench.stats import wilson_interval

    cases = [c for c in discover((CASES, "public")) if c.id == "py-0001-sql-injection"]
    hit = Finding("app/users.py", 6, "security", "critical", "SQL injection", "f-string")
    doc = run(cases, ReplayReviewer(model="m", fn=lambda _: [hit]), ["L0"], 3, tmp_path / "a.json",
              log=lambda m: None)
    rate, lo, hi, n = per_run_by_bug(doc, "L0")
    assert (rate, n) == (1.0, 1)  # 3 identical runs of one bug are one observation, not three
    assert (lo, hi) == wilson_interval(1, 1) and lo < wilson_interval(3, 3)[0]
    assert "3/3 runs (100%; 95% CI 21–100 over 1 bugs)" in leaderboard(tmp_path)
