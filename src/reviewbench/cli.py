"""reviewbench CLI: validate | estimate | run | adjudicate | report | leaderboard | lineup."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from reviewbench import BENCH_VERSION
from reviewbench.adapters import ADAPTERS, get_adapter
from reviewbench.adjudicate import apply_rules, interactive, load_rules, load_verdicts, save_verdicts
from reviewbench.cases import active, discover, validate_case
from reviewbench.context import LEVELS
from reviewbench.heldout import attach_summary, heldout_allowed, heldout_dir, leaks, raw_path, redacting_log
from reviewbench.report import leaderboard, run_report
from reviewbench.runner import estimate_cost, find_resumable, results_path, run

ROOT = Path.cwd()


def _cases(args):
    dirs = [(Path(args.cases), "public")]
    held = heldout_dir(args.heldout)
    if held:
        dirs.append((held, "heldout"))
    cases = discover(*dirs)
    if getattr(args, "cmd", None) != "validate":  # validate checks every case, future ones too
        cases = active(cases)
    if args.only:
        wanted = set(args.only.split(","))
        cases = [c for c in cases if c.id in wanted]
    return cases


def _levels(s: str) -> list[str]:
    levels = [x.strip() for x in s.split(",") if x.strip()]
    bad = [x for x in levels if x not in LEVELS]
    if bad:
        raise SystemExit(f"unknown level(s) {bad}; use {LEVELS}")
    return levels


def cmd_validate(args) -> int:
    bad = 0
    for c in _cases(args):
        errs = validate_case(c)
        if errs:
            bad += 1
            print(f"FAIL {c.id}: " + "; ".join(errs))
    print(f"{'all valid' if not bad else f'{bad} invalid case(s)'}")
    return 1 if bad else 0


def _estimate(args, reviewer, cases, levels) -> dict:
    est = estimate_cost(cases, levels, args.k, reviewer)
    price = "free" if not reviewer.is_paid else f"${est['usd']:.2f} (upper estimate)"
    print(f"{reviewer.provider}/{reviewer.model}: {est['requests']} requests, ~{est['input_tokens']:,} input "
          f"tokens, <= {est['output_tokens_upper']:,} output tokens -> {price}", file=sys.stderr)
    return est


def _guard_heldout(args, reviewer, cases):
    """Drops held-out cases unless lineup.yaml marks this provider/model heldout_ok: true
    (or --allow-heldout is given). They are never sent to an unapproved endpoint."""
    held = [c for c in cases if c.split != "public"]
    if not held or args.allow_heldout or heldout_allowed(reviewer.provider, reviewer.model, Path(args.lineup)):
        return cases
    print(f"skipping {len(held)} held-out case(s): {reviewer.provider}/{reviewer.model} is not marked "
          f"heldout_ok: true in {args.lineup}; held-out cases are never sent to it", file=sys.stderr)
    return [c for c in cases if c.split == "public"]


def cmd_estimate(args) -> int:
    reviewer = get_adapter(args.provider, args.model)
    _estimate(args, reviewer, _guard_heldout(args, reviewer, _cases(args)), _levels(args.levels))
    return 0


def cmd_run(args) -> int:
    reviewer = get_adapter(args.provider, args.model)
    cases, levels = _guard_heldout(args, reviewer, _cases(args)), _levels(args.levels)
    est = _estimate(args, reviewer, cases, levels)
    approved = args.yes or (args.max_usd is not None and est["usd"] <= args.max_usd)
    if reviewer.is_paid and not approved:
        print(f"Refusing to spend money: estimated ${est['usd']:.2f}. Pass --yes, or --max-usd at or above "
              "the estimate.", file=sys.stderr)
        return 2
    out = Path(args.out) if args.out else None
    if out is None and args.resume:
        out = find_resumable(Path(args.results_dir), reviewer.provider, reviewer.model, args.k, levels,
                             {c.id for c in cases if c.split == "public"})
    if out is None:
        out = results_path(Path(args.results_dir), reviewer.provider, reviewer.model)
    public = [c for c in cases if c.split == "public"]
    held = [c for c in cases if c.split != "public"]
    rules = load_rules(Path(args.rules))
    started = time.monotonic()
    doc = run(public, reviewer, levels, args.k, out, max_minutes=args.max_minutes)
    verdicts = load_verdicts(out)  # a resumed run keeps earlier verdicts
    added = apply_rules(doc, verdicts, rules)
    if verdicts:
        save_verdicts(out, verdicts)
    if held and doc["status"] != "complete":
        print("held-out cases not started: public run is partial (continue with --resume)", file=sys.stderr)
    elif held:
        # reviewed into git-ignored results/raw/; only aggregates reach the committed file
        raw = raw_path(out)
        log = redacting_log(held, lambda msg: print(msg, file=sys.stderr))
        left = None if args.max_minutes is None else max(args.max_minutes - (time.monotonic() - started) / 60, 0)
        raw_doc = run(held, reviewer, levels, args.k, raw, log=log, max_minutes=left)
        raw_verdicts = load_verdicts(raw)
        if apply_rules(raw_doc, raw_verdicts, rules):
            save_verdicts(raw, raw_verdicts)
        attach_summary(out)
        doc = json.loads(out.read_text())
        print(f"held-out: {len(held)} case(s), raw results in {raw.parent} (never commit)", file=sys.stderr)
    problems = leaks(doc)
    if problems:  # cannot happen by construction; fail loudly (the file is kept: it may hold hours of runs)
        raise SystemExit("held-out leak check failed: " + "; ".join(problems))
    out.with_suffix(".md").write_text(run_report(doc, verdicts))
    print(f"wrote {out} ({added} findings pre-adjudicated by rules)", file=sys.stderr)
    return 0


def cmd_adjudicate(args) -> int:
    path = Path(args.results)
    doc = json.loads(path.read_text())
    verdicts = load_verdicts(path)
    added = apply_rules(doc, verdicts, load_rules(Path(args.rules)))
    judged = 0 if args.rules_only else interactive(doc, verdicts)
    save_verdicts(path, verdicts)
    raw = raw_path(path)
    if raw.exists():  # held-out raw results are local only; adjudicate them too, then re-aggregate
        raw_doc, raw_verdicts = json.loads(raw.read_text()), load_verdicts(raw)
        added += apply_rules(raw_doc, raw_verdicts, load_rules(Path(args.rules)))
        judged += 0 if args.rules_only else interactive(raw_doc, raw_verdicts)
        save_verdicts(raw, raw_verdicts)
        attach_summary(path)
        doc = json.loads(path.read_text())
    path.with_suffix(".md").write_text(run_report(doc, verdicts))
    print(f"{added} by rule, {judged} by hand; saved {path.stem}.adjudications.json", file=sys.stderr)
    return 0


def cmd_adjudicate_blind(args) -> int:
    from reviewbench.adjudicate import interactive_blind
    paths = [Path(p) for p in args.results]
    judged = interactive_blind(paths, rater=args.rater, seed=args.seed)
    if args.rater == "primary":
        for p in paths:
            p.with_suffix(".md").write_text(run_report(json.loads(p.read_text()), load_verdicts(p)))
    print(f"{judged} judged blind as the {args.rater} rater", file=sys.stderr)
    return 0


def cmd_agreement(args) -> int:
    from reviewbench.adjudicate import agreement
    a = agreement([Path(p) for p in args.results])
    if not a["n"]:
        print("no findings judged by both raters yet")
        return 0
    print(f"second rater agreed on {a['agree']}/{a['n']} findings; Cohen's kappa = {a['kappa']:.2f}")
    return 0


def cmd_report(args) -> int:
    path = Path(args.results)
    print(run_report(json.loads(path.read_text()), load_verdicts(path)))
    return 0


def cmd_leaderboard(args) -> int:
    d = Path(args.results_dir)
    (d / "LEADERBOARD.md").write_text(leaderboard(d))
    print(f"wrote {d / 'LEADERBOARD.md'}", file=sys.stderr)
    return 0


def cmd_lineup(args) -> int:
    from reviewbench.lineup import plan

    public = {c.id for c in active(discover((Path(args.cases), "public")))}
    entries = plan(Path(args.lineup), Path(args.results_dir), log=lambda m: print(m, file=sys.stderr),
                   case_ids=public)
    print(json.dumps(entries))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="reviewbench", description=f"ReviewBench v{BENCH_VERSION}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def case_args(p):
        p.add_argument("--cases", default="cases")
        p.add_argument("--heldout", help="private held-out cases dir (never committed); "
                       "default: $REVIEWBENCH_HELDOUT, else heldout/ if it exists")
        p.add_argument("--only", help="comma-separated case ids")

    def run_args(p):
        case_args(p)
        p.add_argument("--provider", required=True, choices=sorted(ADAPTERS))
        p.add_argument("--model", help="defaults to the adapter's default model")
        p.add_argument("--levels", default="L0,L1,L2")
        p.add_argument("-k", type=int, default=3, help="runs per case and level")
        p.add_argument("--lineup", default="lineup.yaml",
                       help="held-out cases go only to provider/models marked heldout_ok: true here")
        p.add_argument("--allow-heldout", action="store_true",
                       help="send held-out cases even if the lineup does not approve this model "
                            "(only for endpoints that neither log nor train, e.g. a local ollama)")

    p = sub.add_parser("validate", help="check every case's format and that pr.diff applies")
    case_args(p)
    p.set_defaults(fn=cmd_validate)
    p = sub.add_parser("estimate", help="print request count, tokens and estimated cost; calls no API")
    run_args(p)
    p.set_defaults(fn=cmd_estimate)
    p = sub.add_parser("run", help="run the benchmark")
    run_args(p)
    p.add_argument("--yes", action="store_true", help="confirm spending money on a paid provider")
    p.add_argument("--max-usd", type=float, help="confirm a paid run only if the estimate is at most this")
    p.add_argument("--results-dir", default="results")
    p.add_argument("--out")
    p.add_argument("--resume", action="store_true",
                   help="continue the newest partial results file for this reviewer and settings")
    p.add_argument("--max-minutes", type=float,
                   help="stop cleanly (status partial) after this long; resume later with --resume")
    p.add_argument("--rules", default="adjudications/rules.yaml")
    p.set_defaults(fn=cmd_run)
    p = sub.add_parser("adjudicate", help="judge unadjudicated findings in a results file")
    p.add_argument("results")
    p.add_argument("--rules", default="adjudications/rules.yaml")
    p.add_argument("--rules-only", action="store_true", help="apply rules, ask nothing (for CI)")
    p.set_defaults(fn=cmd_adjudicate)
    p = sub.add_parser("adjudicate-blind",
                       help="judge findings pooled from several results files with the model hidden")
    p.add_argument("results", nargs="+")
    p.add_argument("--rater", choices=["primary", "second"], default="primary",
                   help="second: re-judge a fixed 20%% sample of primary verdicts for agreement")
    p.add_argument("--seed", type=int, default=0, help="shuffle seed")
    p.set_defaults(fn=cmd_adjudicate_blind)
    p = sub.add_parser("agreement", help="Cohen's kappa between the primary and second rater")
    p.add_argument("results", nargs="+")
    p.set_defaults(fn=cmd_agreement)
    p = sub.add_parser("report", help="print the markdown report for one results file")
    p.add_argument("results")
    p.set_defaults(fn=cmd_report)
    p = sub.add_parser("lineup", help="print (JSON) the lineup entries to run now: key set, not complete")
    p.add_argument("--lineup", default="lineup.yaml")
    p.add_argument("--cases", default="cases")
    p.add_argument("--results-dir", default="results")
    p.set_defaults(fn=cmd_lineup)
    p = sub.add_parser("leaderboard", help="regenerate results/LEADERBOARD.md")
    p.add_argument("--results-dir", default="results")
    p.set_defaults(fn=cmd_leaderboard)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
