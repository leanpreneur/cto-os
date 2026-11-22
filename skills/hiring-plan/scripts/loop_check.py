#!/usr/bin/env python3
"""loop_check: coverage check for an interview loop, and a summary of interview feedback for a debrief.

Python standard library only. No model. The same input always gives the same output.

  python3 loop_check.py coverage --plan loop.json
  python3 loop_check.py debrief  --feedback feedback.json [--plan loop.json]

Every threshold is a default of the cto-os repository, not a standard. Change it with a flag.
Exit codes: 0 ok (warnings allowed), 1 coverage failures found, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict

AI_POLICIES = {"allowed", "allowed_with_disclosure", "not_allowed"}
RECOMMENDATIONS = {"hire", "hire_other_level", "no_hire"}


class InputError(Exception):
    pass


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise InputError(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise InputError(f"{path} is not valid JSON: {exc}")


def need(cond, msg):
    if not cond:
        raise InputError(msg)


# ---------------------------------------------------------------- coverage

def check_plan(plan, args):
    """Return (findings, matrix_info). Findings are dicts with level FAIL or WARN."""
    need(isinstance(plan, dict), "The plan must be a JSON object.")
    comps = plan.get("competencies")
    ivs = plan.get("interviews")
    need(isinstance(comps, list) and comps, "The plan needs a non-empty 'competencies' list.")
    need(isinstance(ivs, list) and ivs, "The plan needs a non-empty 'interviews' list.")

    findings = []

    def add(level, code, msg):
        findings.append({"level": level, "code": code, "message": msg})

    comp_ids = []
    for c in comps:
        need(isinstance(c, dict) and c.get("id"), "Each competency needs an 'id'.")
        comp_ids.append(str(c["id"]))
    for cid in sorted({c for c in comp_ids if comp_ids.count(c) > 1}):
        add("FAIL", "duplicate-competency", f"Competency id '{cid}' appears more than once.")
    comp_by_id = OrderedDict((str(c["id"]), c) for c in comps)

    iv_ids = []
    for iv in ivs:
        need(isinstance(iv, dict) and iv.get("id"), "Each interview needs an 'id'.")
        iv_ids.append(str(iv["id"]))
        need(isinstance(iv.get("competencies", []), list),
             f"Interview '{iv['id']}': 'competencies' must be a list.")
    for iid in sorted({i for i in iv_ids if iv_ids.count(i) > 1}):
        add("FAIL", "duplicate-interview", f"Interview id '{iid}' appears more than once.")

    # coverage per competency
    covered_by = OrderedDict((cid, []) for cid in comp_by_id)  # cid -> list of (interview id, interviewer)
    for iv in ivs:
        who = str(iv.get("interviewer", "")).strip()
        if not who:
            add("FAIL", "no-interviewer", f"Interview '{iv['id']}' has no interviewer.")
        for cid in iv.get("competencies", []):
            cid = str(cid)
            if cid not in comp_by_id:
                add("FAIL", "unknown-competency",
                    f"Interview '{iv['id']}' tests '{cid}', which is not in the competency list.")
                continue
            covered_by[cid].append((str(iv["id"]), who))

    for cid, c in comp_by_id.items():
        pairs = covered_by[cid]
        interviewers = {w for _, w in pairs if w}
        tag = "must-have" if c.get("must") else "trainable"
        name = c.get("name", cid)
        if not pairs:
            add("FAIL", "no-coverage", f"Competency '{name}' ({tag}) is not tested in any interview.")
        elif len(interviewers) < args.min_signals:
            lvl = "FAIL" if c.get("must") else "WARN"
            add(lvl, "thin-coverage",
                f"Competency '{name}' ({tag}) has {len(interviewers)} interviewer"
                f"{'' if len(interviewers) == 1 else 's'} across {len(pairs)} interview"
                f"{'' if len(pairs) == 1 else 's'}. It needs {args.min_signals} different interviewers.")

    # interview shape
    total_minutes = 0
    for iv in ivs:
        minutes = iv.get("minutes")
        if not isinstance(minutes, (int, float)) or minutes <= 0:
            add("WARN", "no-minutes", f"Interview '{iv['id']}' has no valid 'minutes'.")
        else:
            total_minutes += minutes
        n = len(iv.get("competencies", []))
        is_screen = str(iv.get("type", "")).lower() == "screen" or str(iv["id"]).lower() == "screen"
        if n > args.max_competencies:
            add("WARN", "too-many-competencies",
                f"Interview '{iv['id']}' scores {n} competencies. More than {args.max_competencies} "
                f"cannot be probed in one interview.")
        if n == 0 and not is_screen:
            add("WARN", "empty-interview", f"Interview '{iv['id']}' tests no competency.")

    # interviewer load
    loads = {}
    for iv in ivs:
        who = str(iv.get("interviewer", "")).strip()
        if who:
            loads.setdefault(who, []).append(str(iv["id"]))
    for who in sorted(loads):
        if len(loads[who]) > args.max_per_person:
            add("WARN", "interviewer-load",
                f"'{who}' runs {len(loads[who])} interviews ({', '.join(loads[who])}). "
                f"More than {args.max_per_person} gives one person too much weight.")

    # candidate time
    if total_minutes > args.max_hours * 60:
        add("WARN", "candidate-time",
            f"Candidate time is {total_minutes / 60:.1f} hours. The default cap is {args.max_hours:g} hours.")

    # structure
    if not any(str(iv.get("type", "")).lower() == "work_sample" for iv in ivs):
        add("WARN", "no-work-sample", "No interview has type 'work_sample'. Test the work, not only conversation.")
    if not str(plan.get("decision_owner", "")).strip():
        add("FAIL", "no-decision-owner", "The plan names no decision owner.")
    if plan.get("debrief") is not True:
        add("WARN", "no-debrief", "The plan does not schedule a debrief ('debrief': true).")
    if plan.get("ai_policy") not in AI_POLICIES:
        add("WARN", "no-ai-policy",
            "No valid 'ai_policy'. Use one of: " + ", ".join(sorted(AI_POLICIES)) + ". Candidates must be told in advance.")
    n_comp = len(comp_by_id)
    if n_comp < 5 or n_comp > 7:
        add("WARN", "competency-count", f"The scorecard has {n_comp} competencies. 5 to 7 is the guide.")
    if not any(c.get("must") for c in comps):
        add("WARN", "no-must-have", "No competency is marked must-have.")

    info = {
        "role": plan.get("role", ""),
        "level": plan.get("level", ""),
        "total_minutes": total_minutes,
        "competencies": comp_by_id,
        "interviews": ivs,
        "covered_by": covered_by,
    }
    return findings, info


def render_coverage_md(findings, info, args):
    fails = [f for f in findings if f["level"] == "FAIL"]
    warns = [f for f in findings if f["level"] == "WARN"]
    result = "FAIL" if fails else ("PASS with warnings" if warns else "PASS")
    out = []
    title = " ".join(x for x in [str(info["role"]), str(info["level"])] if x) or "Interview loop"
    out.append(f"# Loop coverage: {title}")
    out.append("")
    out.append(f"**Result: {result}** ({len(fails)} failure{'' if len(fails) == 1 else 's'}, "
               f"{len(warns)} warning{'' if len(warns) == 1 else 's'}). "
               f"Candidate time: {info['total_minutes'] / 60:.1f} hours.")
    out.append("")
    ivs = info["interviews"]
    header = "| Competency | " + " | ".join(str(iv["id"]) for iv in ivs) + " | Interviewers |"
    out.append(header)
    out.append("| --- | " + " | ".join("---" for _ in ivs) + " | --- |")
    for cid, c in info["competencies"].items():
        mark = "*" if c.get("must") else ""
        row = []
        for iv in ivs:
            row.append("X" if cid in [str(x) for x in iv.get("competencies", [])] else "")
        who = {w for _, w in info["covered_by"][cid] if w}
        out.append(f"| {c.get('name', cid)}{mark} | " + " | ".join(row) + f" | {len(who)} |")
    out.append("")
    out.append("`*` marks a must-have competency.")
    out.append("")
    if findings:
        out.append("## Findings")
        out.append("")
        for f in sorted(findings, key=lambda x: (x["level"] != "FAIL", x["code"], x["message"])):
            out.append(f"- **{f['level']}** ({f['code']}): {f['message']}")
        out.append("")
    else:
        out.append("No findings.")
        out.append("")
    out.append(f"Thresholds are defaults of this repository, not standards: {args.min_signals} different interviewers per "
               f"competency, at most {args.max_competencies} competencies per interview, at most {args.max_per_person} "
               f"interviews per person, at most {args.max_hours:g} candidate hours.")
    return "\n".join(out) + "\n"


def cmd_coverage(args):
    plan = load_json(args.plan)
    findings, info = check_plan(plan, args)
    if args.format == "json":
        payload = {
            "role": info["role"], "level": info["level"],
            "candidate_minutes": info["total_minutes"],
            "result": "FAIL" if any(f["level"] == "FAIL" for f in findings) else "PASS",
            "findings": findings,
            "coverage": {cid: sorted({w for _, w in pairs if w}) for cid, pairs in info["covered_by"].items()},
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        sys.stdout.write(render_coverage_md(findings, info, args))
    return 1 if any(f["level"] == "FAIL" for f in findings) else 0


# ------------------------------------------------------------------ debrief

def summarize_feedback(data, plan, args):
    need(isinstance(data, dict), "The feedback file must be a JSON object.")
    fb = data.get("feedback")
    need(isinstance(fb, list) and fb, "The feedback file needs a non-empty 'feedback' list.")

    names, must = OrderedDict(), {}
    if plan is not None:
        for c in plan.get("competencies", []):
            cid = str(c["id"])
            names[cid] = c.get("name", cid)
            must[cid] = bool(c.get("must"))

    entries = OrderedDict()  # cid -> list of dicts
    for cid in names:
        entries[cid] = []
    seen = set()
    process = []
    recs = {"hire": 0, "hire_other_level": 0, "no_hire": 0}
    late = []

    for item in fb:
        need(isinstance(item, dict) and str(item.get("interviewer", "")).strip(),
             "Each feedback item needs an 'interviewer'.")
        who = str(item["interviewer"]).strip()
        iv = str(item.get("interview", "")).strip()
        key = (who, iv)
        if key in seen:
            process.append(f"Duplicate feedback from '{who}' for interview '{iv or '?'}'.")
        seen.add(key)
        if item.get("submitted_before_debrief") is not True:
            late.append(who)
        rec = item.get("recommendation")
        if rec in RECOMMENDATIONS:
            recs[rec] += 1
        else:
            process.append(f"'{who}' gave no valid recommendation (use hire, hire_other_level or no_hire).")
        scores = item.get("scores", {})
        evidence = item.get("evidence", {})
        need(isinstance(scores, dict), f"Feedback from '{who}': 'scores' must be an object.")
        for cid, sc in scores.items():
            need(isinstance(sc, int) and not isinstance(sc, bool) and 1 <= sc <= 4,
                 f"Feedback from '{who}': score for '{cid}' must be a whole number from 1 to 4, got {sc!r}.")
            text = str(evidence.get(cid, "")).strip() if isinstance(evidence, dict) else ""
            has_ev = len(text.split()) >= args.min_evidence_words
            if cid not in entries:
                entries[cid] = []
                names.setdefault(cid, cid)
            entries[cid].append({"who": who, "interview": iv, "score": sc, "evidence": text, "has_evidence": has_ev})

    rows = []
    attention = []
    for cid, lst in entries.items():
        counted = [e for e in lst if e["has_evidence"]]
        bare = [e for e in lst if not e["has_evidence"]]
        scores = [e["score"] for e in counted]
        mean = round(sum(scores) / len(scores), 2) if scores else None
        spread = (max(scores) - min(scores)) if scores else None
        distinct = {e["who"] for e in counted}
        is_must = must.get(cid, True)  # without a plan, treat every competency as must-have
        flags = []
        if not lst:
            flags.append("NO SIGNAL")
        if bare:
            flags.append("NO EVIDENCE: " + ", ".join(sorted({e["who"] for e in bare})))
        if lst and len(distinct) < 2:
            flags.append("INSUFFICIENT: fewer than 2 interviewers with evidence")
        if spread is not None and spread >= args.spread:
            flags.append(f"DISCUSS: scores differ by {spread}")
        if is_must and scores and (mean < args.bar or min(scores) == 1):
            flags.append("BELOW BAR")
        rows.append({
            "id": cid, "name": names.get(cid, cid), "must": is_must, "mean": mean, "spread": spread,
            "counted": [{"who": e["who"], "score": e["score"]} for e in counted],
            "uncounted": [{"who": e["who"], "score": e["score"]} for e in bare],
            "flags": flags,
            "detail": lst,
        })
    blockers = []
    for r in rows:
        if not r["must"]:
            continue
        if any(f.startswith(("NO SIGNAL", "INSUFFICIENT", "BELOW BAR")) for f in r["flags"]):
            blockers.append(r["name"])
    signal = ("Not established on: " + ", ".join(blockers) + "." if blockers
              else f"Met on every must-have competency (mean of {args.bar:g} or more and no score of 1).")
    if late:
        process.append("Feedback not marked as submitted before the debrief: " + ", ".join(sorted(set(late))) + ".")
    return {
        "candidate": data.get("candidate", ""), "role": data.get("role", plan.get("role", "") if plan else ""),
        "level": data.get("level", plan.get("level", "") if plan else ""),
        "plan_given": plan is not None, "rows": rows, "recommendations": recs,
        "process": process, "signal": signal,
    }


def render_debrief_md(s, args):
    out = []
    title = " ".join(x for x in [str(s["candidate"]), str(s["role"]), str(s["level"])] if x) or "Candidate"
    out.append(f"# Debrief summary: {title}")
    out.append("")
    out.append(f"**Signal:** {s['signal']} This is a summary. The decision owner decides.")
    out.append("")
    if not s["plan_given"]:
        out.append("No plan file was given, so every competency is treated as must-have.")
        out.append("")
    out.append("| Competency | Must | Scores counted | Mean | Spread | Flags |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for r in s["rows"]:
        counted = ", ".join(f"{c['who']}: {c['score']}" for c in r["counted"]) or "none"
        mean = "n/a" if r["mean"] is None else f"{r['mean']:.2f}"
        spread = "n/a" if r["spread"] is None else str(r["spread"])
        flags = "; ".join(r["flags"]) or ""
        out.append(f"| {r['name']} | {'yes' if r['must'] else 'no'} | {counted} | {mean} | {spread} | {flags} |")
    out.append("")
    r_ = s["recommendations"]
    out.append(f"Recommendations: hire {r_['hire']}, hire at another level {r_['hire_other_level']}, no hire {r_['no_hire']}.")
    out.append("")
    disc = [r for r in s["rows"] if any(f.startswith("DISCUSS") for f in r["flags"])]
    if disc:
        out.append("## Evidence behind the gaps")
        out.append("")
        for r in disc:
            out.append(f"**{r['name']}**")
            for e in sorted(r["detail"], key=lambda e: (e["score"], e["who"])):
                tail = "" if e["has_evidence"] else " (no evidence, not counted)"
                out.append(f"- {e['who']}, score {e['score']}{tail}: {e['evidence'] or 'none given'}")
            out.append("")
    if s["process"]:
        out.append("## Process notes")
        out.append("")
        for p in s["process"]:
            out.append(f"- {p}")
        out.append("")
    out.append(f"Rules: a score counts only with at least {args.min_evidence_words} words of written evidence. "
               f"The bar is a mean of {args.bar:g} on a 1 to 4 scale with no score of 1. "
               f"A gap of {args.spread} points or more goes to discussion. These are defaults of this repository, not standards.")
    return "\n".join(out) + "\n"


def cmd_debrief(args):
    data = load_json(args.feedback)
    plan = load_json(args.plan) if args.plan else None
    if plan is not None:
        need(isinstance(plan, dict), "The plan must be a JSON object.")
    s = summarize_feedback(data, plan, args)
    if args.format == "json":
        for r in s["rows"]:
            r.pop("detail", None)
        print(json.dumps(s, indent=2, sort_keys=True))
    else:
        sys.stdout.write(render_debrief_md(s, args))
    return 0


# --------------------------------------------------------------------- main

def build_parser():
    p = argparse.ArgumentParser(description="Interview loop coverage check and debrief summary.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("coverage", help="check an interview loop plan")
    c.add_argument("--plan", required=True)
    c.add_argument("--min-signals", type=int, default=2, help="different interviewers per competency (default 2)")
    c.add_argument("--max-competencies", type=int, default=3, help="per interview (default 3)")
    c.add_argument("--max-per-person", type=int, default=2, help="interviews per interviewer (default 2)")
    c.add_argument("--max-hours", type=float, default=5.0, help="candidate hours (default 5)")
    c.add_argument("--format", choices=["md", "json"], default="md")
    c.set_defaults(func=cmd_coverage)

    d = sub.add_parser("debrief", help="summarize interview feedback")
    d.add_argument("--feedback", required=True)
    d.add_argument("--plan")
    d.add_argument("--bar", type=float, default=3.0, help="mean score a must-have needs (default 3.0)")
    d.add_argument("--spread", type=int, default=2, help="score gap that triggers discussion (default 2)")
    d.add_argument("--min-evidence-words", type=int, default=4, help="words of evidence a score needs (default 4)")
    d.add_argument("--format", choices=["md", "json"], default="md")
    d.set_defaults(func=cmd_debrief)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except InputError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
