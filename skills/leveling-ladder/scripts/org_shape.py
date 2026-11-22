#!/usr/bin/env python3
"""org_shape: measure the shape of an engineering organization from a roster file.

Python standard library only. No model. The same roster and --as-of date always give the same output.

  python3 org_shape.py --roster roster.csv --as-of 2026-11-22

Roster columns (CSV with a header row):
  id                   required. An opaque id. Do not use names.
  level                required. For example E3 or M1.
  track                required. IC or M.
  manager_id           required column. Empty for the top person.
  start_date           optional. YYYY-MM-DD.
  last_promotion_date  optional. YYYY-MM-DD. Empty if never promoted.

Every number is Measured from the roster you give, and is only as good as the roster.
Groups smaller than --min-cell people are combined and not broken out. This stops casual reading.
It is not anonymization. Keep the report private. Do not put a roster or a report in a public repository.
Thresholds are defaults of the cto-os repository, not standards.
Exit codes: 0 ok, 2 bad input.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, OrderedDict, defaultdict
from datetime import date

DAYS_PER_MONTH = 30.4375


class InputError(Exception):
    pass


def level_key(level):
    m = re.match(r"^([A-Za-z]+)(\d+)$", level)
    return (m.group(1).upper(), int(m.group(2))) if m else (level.upper(), 0)


def parse_date(text, row_no, column):
    text = (text or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise InputError(f"Row {row_no}: '{column}' must be YYYY-MM-DD.")


def load_roster(path):
    try:
        fh = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        raise InputError(f"File not found: {path}")
    with fh:
        reader = csv.DictReader(fh)
        cols = [c.strip() for c in (reader.fieldnames or [])]
        for req in ("id", "level", "track", "manager_id"):
            if req not in cols:
                raise InputError(f"The roster needs a '{req}' column. Found: {', '.join(cols) or 'none'}.")
        rows, seen = [], set()
        for i, raw in enumerate(reader, start=2):
            r = {k.strip(): (v or "").strip() for k, v in raw.items() if k}
            if not r.get("id"):
                raise InputError(f"Row {i}: 'id' is empty.")
            if r["id"] in seen:
                raise InputError(f"Row {i}: duplicate id.")
            seen.add(r["id"])
            if not r.get("level"):
                raise InputError(f"Row {i}: 'level' is empty.")
            track = r.get("track", "").upper()
            if track not in ("IC", "M"):
                raise InputError(f"Row {i}: 'track' must be IC or M.")
            r["track"] = track
            r["start"] = parse_date(r.get("start_date"), i, "start_date")
            r["promo"] = parse_date(r.get("last_promotion_date"), i, "last_promotion_date")
            rows.append(r)
    if not rows:
        raise InputError("The roster has no rows.")
    return rows


def months_between(d, as_of):
    return (as_of - d).days / DAYS_PER_MONTH


def analyze(rows, as_of, args):
    by_id = {r["id"]: r for r in rows}
    warnings = []

    # reports and depth
    reports = defaultdict(list)
    unknown_mgr = 0
    for r in rows:
        mid = r.get("manager_id", "")
        if mid:
            if mid in by_id:
                reports[mid].append(r["id"])
            else:
                unknown_mgr += 1
    if unknown_mgr:
        warnings.append(f"{unknown_mgr} row(s) name a manager_id that is not in the roster. They are treated as top of a tree.")

    depth = {}

    def get_depth(rid, trail):
        if rid in depth:
            return depth[rid]
        if rid in trail:
            raise InputError("The manager chain contains a loop.")
        mid = by_id[rid].get("manager_id", "")
        if not mid or mid not in by_id:
            depth[rid] = 1
        else:
            depth[rid] = 1 + get_depth(mid, trail | {rid})
        return depth[rid]

    for r in rows:
        get_depth(r["id"], frozenset())

    n = len(rows)
    n_ic = sum(1 for r in rows if r["track"] == "IC")
    n_m = n - n_ic
    managers = sorted(rid for rid in reports if reports[rid])
    spans = {m: len(reports[m]) for m in managers}
    span_vals = sorted(spans.values())

    # time in level
    def time_in_level(r):
        anchor = r["promo"] or r["start"]
        return None if anchor is None else months_between(anchor, as_of)

    missing_dates = sum(1 for r in rows if time_in_level(r) is None)
    if missing_dates:
        warnings.append(f"{missing_dates} person(s) have no start_date or last_promotion_date and are left out of time-in-level.")
    future = sum(1 for r in rows if (r["promo"] or r["start"]) and (r["promo"] or r["start"]) > as_of)
    if future:
        raise InputError(f"{future} date(s) are after the --as-of date.")

    # levels
    by_level = defaultdict(list)
    for r in rows:
        by_level[r["level"]].append(r)
    shown, hidden_people = [], 0
    for lvl in sorted(by_level, key=level_key):
        people = by_level[lvl]
        if len(people) < args.min_cell:
            hidden_people += len(people)
            continue
        t = [time_in_level(p) for p in people if time_in_level(p) is not None]
        shown.append({
            "level": lvl, "count": len(people), "share": round(100 * len(people) / n, 1),
            "median_months_in_level": round(statistics.median(t), 1) if len(t) >= args.min_cell else None,
            "over_stale_share": round(100 * sum(1 for x in t if x > args.stale_months) / len(t), 1) if len(t) >= args.min_cell else None,
            "with_dates": len(t),
        })
    other = None
    if hidden_people:
        other = {"count": hidden_people if hidden_people >= args.min_cell else None,
                 "share": round(100 * hidden_people / n, 1) if hidden_people >= args.min_cell else None}

    # layers
    layer_counts = Counter(depth.values())
    layers = []
    hidden_layer_people = 0
    for d in sorted(layer_counts):
        if layer_counts[d] < args.min_cell:
            hidden_layer_people += layer_counts[d]
        else:
            layers.append({"layer": d, "count": layer_counts[d]})

    thin = [m for m in managers if spans[m] < args.min_span]
    wide = [m for m in managers if spans[m] > args.max_span]
    m_no_reports = sorted(r["id"] for r in rows if r["track"] == "M" and r["id"] not in spans)
    ic_with_reports = sorted(r["id"] for r in rows if r["track"] == "IC" and r["id"] in spans)

    result = OrderedDict()
    result["as_of"] = as_of.isoformat()
    result["headcount"] = n
    result["ic_track"] = n_ic
    result["manager_track"] = n_m
    result["layers"] = max(depth.values())
    result["managers_with_reports"] = len(managers)
    result["span"] = {
        "min": span_vals[0] if span_vals else None,
        "median": statistics.median(span_vals) if span_vals else None,
        "max": span_vals[-1] if span_vals else None,
        "thin_below": args.min_span, "thin_count": len(thin),
        "wide_above": args.max_span, "wide_count": len(wide),
    }
    result["ics_per_manager"] = round(n_ic / len(managers), 2) if managers else None
    result["track_mismatch"] = {"manager_track_without_reports": len(m_no_reports),
                                "ic_track_with_reports": len(ic_with_reports)}
    result["levels"] = shown
    result["levels_under_min_cell"] = other
    result["layer_sizes"] = layers
    result["layer_people_under_min_cell"] = hidden_layer_people
    result["warnings"] = warnings
    if args.show_ids:
        result["ids"] = {"thin_span": thin, "wide_span": wide,
                         "manager_track_without_reports": m_no_reports,
                         "ic_track_with_reports": ic_with_reports}
    return result


def fmt(v, suffix=""):
    return "hidden" if v is None else f"{v}{suffix}"


def render_md(res, args):
    o = []
    o.append(f"# Org shape, as of {res['as_of']}")
    o.append("")
    o.append(f"**Headcount:** {res['headcount']} ({res['ic_track']} on the IC track, {res['manager_track']} on the manager track). "
             f"**Layers:** {res['layers']}. **Managers with reports:** {res['managers_with_reports']}. "
             f"**ICs per manager:** {fmt(res['ics_per_manager'])}.")
    o.append("")
    o.append("All numbers are Measured from the roster you gave, and are only as good as the roster.")
    o.append("")
    if res["warnings"]:
        o.append("## Data warnings")
        o.append("")
        for w in res["warnings"]:
            o.append(f"- {w}")
        o.append("")
    o.append("## Levels")
    o.append("")
    o.append(f"| Level | People | Share | Median months in level | Share over {args.stale_months:g} months in level |")
    o.append("| --- | --- | --- | --- | --- |")
    for l in res["levels"]:
        o.append(f"| {l['level']} | {l['count']} | {l['share']}% | {fmt(l['median_months_in_level'])} | "
                 f"{fmt(l['over_stale_share'], '%')} |")
    u = res["levels_under_min_cell"]
    if u:
        cnt = "fewer than %d" % args.min_cell if u["count"] is None else u["count"]
        shr = "hidden" if u["share"] is None else f"{u['share']}%"
        o.append(f"| Levels with fewer than {args.min_cell} people each, combined | {cnt} | {shr} | hidden | hidden |")
    o.append("")
    o.append("Time in level counts from the last promotion, or the start date if the person was never promoted.")
    o.append("")
    s = res["span"]
    o.append("## Spans and layers")
    o.append("")
    o.append("| Measure | Value |")
    o.append("| --- | --- |")
    o.append(f"| Direct reports per manager, min / median / max | {fmt(s['min'])} / {fmt(s['median'])} / {fmt(s['max'])} |")
    o.append(f"| Managers with fewer than {s['thin_below']} reports | {s['thin_count']} |")
    o.append(f"| Managers with more than {s['wide_above']} reports | {s['wide_count']} |")
    o.append(f"| Manager track, no reports | {res['track_mismatch']['manager_track_without_reports']} |")
    o.append(f"| IC track, with reports | {res['track_mismatch']['ic_track_with_reports']} |")
    o.append("")
    if res["layer_sizes"]:
        o.append("Layer sizes, top to bottom: " + ", ".join(f"layer {l['layer']}: {l['count']}" for l in res["layer_sizes"]) +
                 (f". Layers with fewer than {args.min_cell} people are not shown." if res["layer_people_under_min_cell"] else "."))
        o.append("")
    if "ids" in res:
        o.append("## Ids to look at")
        o.append("")
        for k, v in res["ids"].items():
            o.append(f"- {k.replace('_', ' ')}: {', '.join(v) if v else 'none'}")
        o.append("")
    o.append("## How to read this")
    o.append("")
    o.append("These are questions, not verdicts. Examples: a manager with one report may be a lead who needs a different role; "
             "a manager with more than ten reports may have no time for feedback; many people over the time-in-level threshold at one level "
             "may mean promotions stall there. Ask the managers before you conclude anything.")
    o.append("")
    o.append(f"Defaults of this repository, not standards: thin span under {args.min_span}, wide span over {args.max_span}, "
             f"time in level over {args.stale_months:g} months, and groups under {args.min_cell} people are not broken out. "
             "Hiding small groups stops casual reading. It is not anonymization. Keep this report private.")
    return "\n".join(o) + "\n"


def build_parser():
    p = argparse.ArgumentParser(description="Measure the shape of an engineering organization from a roster.")
    p.add_argument("--roster", required=True)
    p.add_argument("--as-of", required=True, help="YYYY-MM-DD, so results can be reproduced")
    p.add_argument("--min-span", type=int, default=3, help="direct reports below this count as thin (default 3)")
    p.add_argument("--max-span", type=int, default=10, help="direct reports above this count as wide (default 10)")
    p.add_argument("--stale-months", type=float, default=36, help="months in level that count as long (default 36)")
    p.add_argument("--min-cell", type=int, default=5, help="groups smaller than this are not broken out (default 5)")
    p.add_argument("--show-ids", action="store_true", help="list opaque ids for flagged managers. Off by default")
    p.add_argument("--format", choices=["md", "json"], default="md")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        as_of = date.fromisoformat(args.as_of)
    except ValueError:
        print("Input error: --as-of must be YYYY-MM-DD.", file=sys.stderr)
        return 2
    try:
        res = analyze(load_roster(args.roster), as_of, args)
    except InputError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(res, indent=2))
    else:
        sys.stdout.write(render_md(res, args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
