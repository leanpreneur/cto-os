#!/usr/bin/env python3
"""incident_check: check a postmortem written from templates/postmortem.md, and summarize a file of incidents.

Python standard library only. No model. The same input always gives the same output.

  python3 incident_check.py postmortem --file postmortem.md [--format md|json]
  python3 incident_check.py summary --incidents incidents.csv --as-of 2026-11-22 [--actions actions.csv]

postmortem: checks structure, times, action items and blame phrases, and measures time to detect, mitigate and resolve.
  Lines that start with ">" and fenced code blocks are ignored. Times are UTC, YYYY-MM-DD HH:MM.

summary: reads a CSV with a header row.
  required columns: id, severity, started, detected, mitigated, resolved, detected_by
  optional columns: factor (tags separated by ";"), postmortem_required (yes or no), postmortem_published (YYYY-MM-DD)
  The optional actions file has columns: incident_id, due, status (open or done).
  If postmortem_required is missing, SEV1 and SEV2 are owed a postmortem.
  Use opaque ids. Keep the files private. Do not put real incident data in a public repository.

Every threshold is a default of the cto-os repository, not a standard. Change it with a flag.
The blame-phrase check is a Proxy: it finds the phrases it lists and cannot judge whether a document is blameless.
Exit codes: 0 ok (warnings allowed), 1 failures found in a postmortem, 2 bad input.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, OrderedDict
from datetime import date, datetime, time, timedelta

SEVERITIES = ("SEV1", "SEV2", "SEV3", "SEV4")
DETECTED_BY = ("monitoring", "customer", "employee")
ACTION_TYPES = ("prevent", "detect", "mitigate", "process")
ACTION_STATUS = ("open", "done")
REQUIRED_SECTIONS = ("summary", "impact", "timeline", "contributing factors",
                     "what went well", "what went badly", "where we got lucky", "action items")
BLAME_PHRASES = ("human error", "operator error", "user error", "careless", "carelessness",
                 "negligent", "negligence", "incompetent", "incompetence", "lazy", "sloppy",
                 "should have known", "should have caught", "should have been more careful",
                 "stupid", "their fault", "his fault", "her fault")

TS = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[ T](\d{1,2}):(\d{2})\s*(?:UTC|Z)?$", re.I)
TIME_ONLY = re.compile(r"^(\d{1,2}):(\d{2})\s*(?:UTC|Z)?$", re.I)
SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")
LIST_ITEM = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*(.*)$")


class InputError(Exception):
    pass


# ---------------------------------------------------------------- shared helpers

def parse_ts(text):
    m = TS.match((text or "").strip())
    if not m:
        return None
    y, mo, d, h, mi = (int(g) for g in m.groups())
    try:
        return datetime(y, mo, d, h, mi)
    except ValueError:
        return None


def parse_date(text):
    try:
        return date.fromisoformat((text or "").strip())
    except ValueError:
        return None


def fmt_minutes(minutes):
    minutes = int(round(minutes))
    if minutes < 60:
        return f"{minutes} min"
    h, m = divmod(minutes, 60)
    return f"{h} h {m:02d} min" if m else f"{h} h"


def minutes_between(a, b):
    return (b - a).total_seconds() / 60.0


# ---------------------------------------------------------------- postmortem: parsing

def read_lines(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except FileNotFoundError:
        raise InputError(f"File not found: {path}")
    except UnicodeDecodeError:
        raise InputError(f"{path} is not UTF-8 text.")


def clean(lines):
    """Return [(line_number, text)] without guidance lines and fenced code blocks."""
    out, in_fence = [], False
    for i, raw in enumerate(lines, start=1):
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or s.startswith(">"):
            continue
        out.append((i, raw))
    return out


def split_sections(cleaned):
    """Return (title, preamble, sections) where sections maps a lowercase heading to [(n, text)]."""
    title, preamble, sections, current = "", [], OrderedDict(), None
    for n, text in cleaned:
        s = text.strip()
        if s.startswith("## "):
            current = s[3:].strip().lower()
            sections[current] = []
        elif s.startswith("# ") and not title:
            title = s[2:].strip()
        elif current is None:
            preamble.append((n, text))
        else:
            sections[current].append((n, text))
    return title, preamble, sections


def split_row(text):
    s = text.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def first_table(lines):
    """Return (header, rows) for the first markdown table in [(n, text)]. rows are [(n, [cells])]."""
    header, rows, started = None, [], False
    items = list(lines)
    for idx, (n, text) in enumerate(items):
        s = text.strip()
        if not s.startswith("|"):
            if started:
                break
            continue
        if header is None:
            nxt = items[idx + 1][1].strip() if idx + 1 < len(items) else ""
            if SEPARATOR.match(nxt):
                header, started = [c.lower() for c in split_row(s)], True
            continue
        if SEPARATOR.match(s):
            continue
        rows.append((n, split_row(s)))
    return header, rows


def column(header, *names):
    for i, h in enumerate(header or []):
        for name in names:
            if h == name or h.startswith(name):
                return i
    return None


def cell(cells, idx):
    if idx is None or idx >= len(cells):
        return ""
    return cells[idx].strip()


def field_table(preamble):
    header, rows = first_table(preamble)
    fields = {}
    if header is None:
        return fields
    for _, cells in rows:
        if len(cells) >= 2:
            key = re.sub(r"\s*\(utc\)", "", cells[0].lower()).strip()
            fields[key] = cells[1].strip()
    return fields


def text_items(lines):
    """Content lines of a text section: not tables, with list markers removed. Returns [(n, text)]."""
    out = []
    for n, text in lines:
        s = text.strip()
        if not s or s.startswith("|") or SEPARATOR.match(s):
            continue
        m = LIST_ITEM.match(s)
        body = (m.group(1) if m else s).strip()
        body = re.sub(r"^\[[ xX]\]\s*", "", body).strip()
        if body:
            out.append((n, body, bool(m)))
    return out


# ---------------------------------------------------------------- postmortem: checks

def check_postmortem(lines, args):
    cleaned = clean(lines)
    title, preamble, sections = split_sections(cleaned)
    fields = field_table(preamble)
    findings = []

    def add(level, code, msg):
        findings.append({"level": level, "code": code, "message": msg})

    title = re.sub(r"^postmortem:\s*", "", title, flags=re.I).strip()
    if not title or title.startswith("["):
        add("WARN", "title", "The title is empty or still the template placeholder. Say what customers experienced.")

    # severity
    sev = fields.get("severity", "").strip().upper()
    if sev not in SEVERITIES:
        add("FAIL", "severity", f"Severity must be one of {', '.join(SEVERITIES)}. Found: '{fields.get('severity', '')}'.")
        sev = ""

    # the four times
    keys = (("impact started", "Impact started (UTC)"), ("detected", "Detected (UTC)"),
            ("mitigated", "Mitigated (UTC)"), ("resolved", "Resolved (UTC)"))
    times = {}
    for key, label in keys:
        dt = parse_ts(fields.get(key, ""))
        if dt is None:
            add("FAIL", "timestamp", f"'{label}' must be a time like 2026-11-22 14:05. Found: '{fields.get(key, '')}'.")
        else:
            times[key] = dt
    names = [k for k, _ in keys]
    if all(k in times for k in names):
        for a, b in zip(names, names[1:]):
            if times[b] < times[a]:
                add("FAIL", "time-order", f"'{b}' is earlier than '{a}'. The four times must not go backwards.")

    # detected by
    det = fields.get("detected by", "").strip().lower()
    if det not in DETECTED_BY:
        add("FAIL", "detected-by", f"'Detected by' must be one of {', '.join(DETECTED_BY)}. Found: '{fields.get('detected by', '')}'.")
        det = ""

    # required sections
    for name in REQUIRED_SECTIONS:
        if name not in sections:
            add("FAIL", "missing-section", f"The section '## {name.capitalize()}' is missing.")

    # impact
    if "impact" in sections:
        body = text_items(sections["impact"])
        if not body:
            add("FAIL", "empty-section", "The section 'Impact' is empty.")
        elif not any(re.search(r"\d", t) for _, t, _ in body):
            add("WARN", "impact-no-number", "Impact has no number. Give customers affected, minutes, failed requests or money, or say what you could not measure.")

    for name in ("summary", "what went well", "what went badly", "where we got lucky"):
        if name in sections and not text_items(sections[name]):
            add("FAIL", "empty-section", f"The section '{name.capitalize()}' is empty.")

    # contributing factors
    if "contributing factors" in sections:
        items = text_items(sections["contributing factors"])
        listed = [i for i in items if i[2]]
        count = len(listed) if listed else len(items)
        if count == 0:
            add("FAIL", "empty-section", "The section 'Contributing factors' is empty.")
        elif count == 1:
            add("WARN", "one-factor", "Only one contributing factor. Most incidents have several. Check detection, the change process, design, tooling and gaps between teams.")

    # timeline
    timeline_rows = []
    if "timeline" in sections:
        header, rows = first_table(sections["timeline"])
        ti, ei, si = column(header, "time"), column(header, "event"), column(header, "source")
        data = [(n, c) for n, c in rows if cell(c, ti) or cell(c, ei)]
        if header is None or ti is None or ei is None:
            add("FAIL", "timeline-columns", "The timeline needs a table with Time (UTC), Event and Source columns.")
        elif not data:
            add("FAIL", "empty-section", "The section 'Timeline' has no rows.")
        else:
            cursor = times["impact started"].date() if "impact started" in times else None
            prev, no_source, bad = None, 0, False
            for n, c in data:
                raw = cell(c, ti)
                dt = parse_ts(raw)
                if dt is None and TIME_ONLY.match(raw) and cursor is not None:
                    m = TIME_ONLY.match(raw)
                    try:
                        dt = datetime.combine(cursor, time(int(m.group(1)), int(m.group(2))))
                    except ValueError:
                        dt = None
                    if dt is not None and prev is not None and dt < prev:
                        dt += timedelta(days=1)
                        if "resolved" in times and dt > times["resolved"]:
                            add("WARN", "timeline-order", f"Line {n}: the time is earlier than the row before it, so it was read as the next day, "
                                "which is after the incident was resolved. Check the order, or write the full date.")
                if dt is None:
                    add("FAIL", "timeline-time", f"Line {n}: the time '{raw}' cannot be read. Use YYYY-MM-DD HH:MM, or HH:MM after a full time.")
                    bad = True
                    continue
                if prev is not None and dt < prev:
                    add("WARN", "timeline-order", f"Line {n}: this row is earlier than the row before it. Put the timeline in order.")
                cursor, prev = dt.date(), max(dt, prev) if prev else dt
                timeline_rows.append(dt)
                if not cell(c, ei):
                    add("WARN", "timeline-event", f"Line {n}: the row has a time and no event.")
                if not cell(c, si):
                    no_source += 1
            if no_source:
                add("WARN", "timeline-source", f"{no_source} timeline row(s) have no source. Name the graph, log or message.")
            if not bad and len(data) < args.min_timeline:
                add("WARN", "short-timeline", f"The timeline has {len(data)} row(s). It should show at least detection, mitigation and resolution ({args.min_timeline} or more rows).")

    # action items
    actions = []
    if "action items" in sections:
        header, rows = first_table(sections["action items"])
        ai = column(header, "action")
        ty, ow, du = column(header, "type"), column(header, "owner"), column(header, "due")
        dw, st = column(header, "done when"), column(header, "status")
        if header is None or None in (ai, ow, du):
            add("FAIL", "action-columns", "The action items need a table with at least Action, Owner and Due columns.")
        else:
            for n, c in rows:
                if not cell(c, ai):
                    continue
                actions.append((n, c))
            if not actions:
                level = "FAIL" if sev in ("SEV1", "SEV2") else "WARN"
                add(level, "no-actions", "There are no action items. A SEV1 or SEV2 always has some. For lower severities, say in the Summary why none are needed.")
            started_date = times["impact started"].date() if "impact started" in times else None
            for n, c in actions:
                if not cell(c, ow):
                    add("FAIL", "action-owner", f"Line {n}: the action has no owner.")
                due = parse_date(cell(c, du))
                if due is None:
                    add("FAIL", "action-due", f"Line {n}: the action has no due date in the form YYYY-MM-DD. Found: '{cell(c, du)}'.")
                else:
                    if started_date and due < started_date:
                        add("FAIL", "action-due", f"Line {n}: the due date is before the incident started.")
                    if "resolved" in times and (due - times["resolved"].date()).days > args.max_days:
                        add("WARN", "action-far", f"Line {n}: the due date is more than {args.max_days} days after resolution. Split the item.")
                if ty is not None and cell(c, ty).lower() not in ACTION_TYPES:
                    add("WARN", "action-type", f"Line {n}: type must be one of {', '.join(ACTION_TYPES)}. Found: '{cell(c, ty)}'.")
                if dw is not None and not cell(c, dw):
                    add("WARN", "action-done-when", f"Line {n}: the action has no 'done when' test.")
                if st is not None and cell(c, st).lower() not in ACTION_STATUS:
                    add("WARN", "action-status", f"Line {n}: status must be open or done. Found: '{cell(c, st)}'.")
            if len(actions) > args.max_actions:
                add("WARN", "too-many-actions", f"{len(actions)} action items. More than {args.max_actions} rarely get finished. Rank them and keep the ones that matter.")
            if det in ("customer", "employee") and ty is not None and \
                    not any(cell(c, ty).lower() == "detect" for _, c in actions):
                add("WARN", "no-detect-action", f"Detected by {det}, not monitoring, and no action has type 'detect'. Add one that would have found it sooner.")

    # blame phrases, in the sections that tell the story
    story = ("summary", "impact", "timeline", "contributing factors", "what went well", "what went badly", "where we got lucky")
    hits = []
    for name in story:
        for n, text in sections.get(name, []):
            low = text.lower()
            for phrase in BLAME_PHRASES:
                if re.search(r"\b" + re.escape(phrase) + r"\b", low):
                    hits.append((n, phrase))
    for n, phrase in sorted(set(hits)):
        add("WARN", "blame-phrase", f"Line {n}: '{phrase}'. Describe the conditions that made the action reasonable at the time.")

    measures = OrderedDict()
    if all(k in times for k in names) and not any(f["code"] == "time-order" for f in findings):
        measures["to_detect"] = minutes_between(times["impact started"], times["detected"])
        measures["to_mitigate"] = minutes_between(times["impact started"], times["mitigated"])
        measures["to_resolve"] = minutes_between(times["impact started"], times["resolved"])

    order = {"FAIL": 0, "WARN": 1}
    findings.sort(key=lambda f: (order[f["level"]], f["code"], f["message"]))
    return {"title": title, "severity": sev, "detected_by": det, "measures": measures,
            "findings": findings, "actions": len(actions)}


def render_postmortem_md(res, args):
    fails = [f for f in res["findings"] if f["level"] == "FAIL"]
    warns = [f for f in res["findings"] if f["level"] == "WARN"]
    out = [f"# Postmortem check: {res['title'] or '(untitled)'}", ""]
    out.append(f"**Result: {'FAIL' if fails else 'PASS'}** ({len(fails)} failure{'s' if len(fails) != 1 else ''}, "
               f"{len(warns)} warning{'s' if len(warns) != 1 else ''}). "
               f"Severity: {res['severity'] or 'unknown'}. Detected by: {res['detected_by'] or 'unknown'}. "
               f"Action items: {res['actions']}.")
    out.append("")
    m = res["measures"]
    if m:
        out += ["| Measure | From impact start | Label |", "| --- | --- | --- |",
                f"| Time to detect | {fmt_minutes(m['to_detect'])} | Measured from the times in the document |",
                f"| Time to mitigate | {fmt_minutes(m['to_mitigate'])} | Measured from the times in the document |",
                f"| Time to resolve | {fmt_minutes(m['to_resolve'])} | Measured from the times in the document |", ""]
        out += ["Time to detect is only as good as the impact start time. If someone estimated it afterwards, read it as a Proxy.", ""]
    else:
        out += ["Times could not be measured. Fix the time findings first.", ""]
    if res["findings"]:
        out.append("## Findings")
        out.append("")
        for f in res["findings"]:
            out.append(f"- **{f['level']}** ({f['code']}): {f['message']}")
    else:
        out.append("No findings.")
    out += ["", f"Thresholds are defaults of this repository, not standards: at most {args.max_actions} action items, "
            f"due within {args.max_days} days of resolution, at least {args.min_timeline} timeline rows.",
            "The blame-phrase check is a Proxy. It finds the phrases it lists and cannot judge whether a postmortem is blameless. A person must read it."]
    return "\n".join(out) + "\n"


def cmd_postmortem(args):
    lines = read_lines(args.file)
    res = check_postmortem(lines, args)
    if args.format == "json":
        print(json.dumps(res, indent=2))
    else:
        sys.stdout.write(render_postmortem_md(res, args))
    return 1 if any(f["level"] == "FAIL" for f in res["findings"]) else 0


# ---------------------------------------------------------------- summary

def load_csv(path, required):
    try:
        fh = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        raise InputError(f"File not found: {path}")
    with fh:
        reader = csv.DictReader(fh)
        cols = [c.strip() for c in (reader.fieldnames or [])]
        for req in required:
            if req not in cols:
                raise InputError(f"{path} needs a '{req}' column. Found: {', '.join(cols) or 'none'}.")
        rows = []
        for i, raw in enumerate(reader, start=2):
            rows.append((i, {k.strip(): (v or "").strip() for k, v in raw.items() if k}))
    return rows


def load_incidents(path, as_of):
    rows = load_csv(path, ("id", "severity", "started", "detected", "mitigated", "resolved", "detected_by"))
    incidents, seen = [], set()
    for i, r in rows:
        if not r["id"]:
            raise InputError(f"Row {i}: 'id' is empty.")
        if r["id"] in seen:
            raise InputError(f"Row {i}: duplicate id '{r['id']}'.")
        seen.add(r["id"])
        sev = r["severity"].upper()
        if sev not in SEVERITIES:
            raise InputError(f"Row {i}: 'severity' must be one of {', '.join(SEVERITIES)}.")
        t = {}
        for key in ("started", "detected", "mitigated", "resolved"):
            dt = parse_ts(r[key])
            if dt is None:
                raise InputError(f"Row {i}: '{key}' must be YYYY-MM-DD HH:MM.")
            t[key] = dt
        if not (t["started"] <= t["detected"] <= t["mitigated"] <= t["resolved"]):
            raise InputError(f"Row {i}: the times must not go backwards (started, detected, mitigated, resolved).")
        if t["started"].date() > as_of:
            raise InputError(f"Row {i}: the incident starts after --as-of.")
        det = r["detected_by"].lower()
        if det not in DETECTED_BY:
            raise InputError(f"Row {i}: 'detected_by' must be one of {', '.join(DETECTED_BY)}.")
        req = r.get("postmortem_required", "").lower()
        if req not in ("", "yes", "no"):
            raise InputError(f"Row {i}: 'postmortem_required' must be yes or no.")
        owed = (req == "yes") if req else sev in ("SEV1", "SEV2")
        pub = None
        if r.get("postmortem_published"):
            pub = parse_date(r["postmortem_published"])
            if pub is None:
                raise InputError(f"Row {i}: 'postmortem_published' must be YYYY-MM-DD.")
        factors = sorted({f.strip().lower() for f in r.get("factor", "").split(";") if f.strip()})
        incidents.append({"id": r["id"], "severity": sev, "times": t, "detected_by": det, "owed": owed,
                          "published": pub, "factors": factors})
    if not incidents:
        raise InputError(f"{path} has no incidents.")
    return incidents


def load_actions(path, ids):
    rows = load_csv(path, ("incident_id", "due", "status"))
    actions = []
    for i, r in rows:
        if r["incident_id"] not in ids:
            raise InputError(f"Actions row {i}: incident_id '{r['incident_id']}' is not in the incidents file.")
        due = parse_date(r["due"])
        if due is None:
            raise InputError(f"Actions row {i}: 'due' must be YYYY-MM-DD.")
        status = r["status"].lower()
        if status not in ACTION_STATUS:
            raise InputError(f"Actions row {i}: 'status' must be open or done.")
        actions.append({"incident_id": r["incident_id"], "due": due, "status": status})
    return actions


def stats(values):
    return {"median": statistics.median(values), "longest": max(values)} if values else None


def summarize(incidents, actions, as_of, args):
    n = len(incidents)
    by_sev = OrderedDict((s, [i for i in incidents if i["severity"] == s]) for s in SEVERITIES)
    table = []
    for s, group in by_sev.items():
        if not group:
            continue
        row = {"severity": s, "n": len(group)}
        for key, a, b in (("detect", "started", "detected"), ("mitigate", "started", "mitigated"), ("resolve", "started", "resolved")):
            row[key] = stats([minutes_between(i["times"][a], i["times"][b]) for i in group])
        table.append(row)
    overall = {}
    for key, a, b in (("detect", "started", "detected"), ("mitigate", "started", "mitigated"), ("resolve", "started", "resolved")):
        overall[key] = stats([minutes_between(i["times"][a], i["times"][b]) for i in incidents])
    found = Counter(i["detected_by"] for i in incidents)
    tags = Counter(f for i in incidents for f in i["factors"])
    repeats = sorted(((t, c) for t, c in tags.items() if c >= 2), key=lambda x: (-x[1], x[0]))
    owed = [i for i in incidents if i["owed"]]
    published = [i for i in owed if i["published"]]
    on_time = [i for i in published if (i["published"] - i["times"]["resolved"].date()).days <= args.pm_days]
    overdue = sorted(i["id"] for i in owed if not i["published"]
                     and (as_of - i["times"]["resolved"].date()).days > args.pm_days)
    out = {"as_of": as_of.isoformat(), "incidents": n, "by_severity": table, "overall": overall,
           "found_by": {k: found.get(k, 0) for k in DETECTED_BY}, "repeat_factors": repeats,
           "postmortems": {"owed": len(owed), "published": len(published), "on_time": len(on_time),
                           "overdue_ids": overdue, "target_days": args.pm_days}}
    if actions is not None:
        open_items = [a for a in actions if a["status"] == "open"]
        late = [a for a in open_items if a["due"] < as_of]
        out["actions"] = {"total": len(actions), "done": len(actions) - len(open_items), "open": len(open_items),
                          "overdue": len(late), "oldest_overdue_days": max(((as_of - a["due"]).days for a in late), default=0)}
    return out


def pct(part, whole):
    return f"{part} of {whole} ({round(100.0 * part / whole)}%)" if whole else "none"


def render_summary_md(s, args):
    n = s["incidents"]
    out = ["# Incident summary", "", f"**{n} incident{'s' if n != 1 else ''}**, as of {s['as_of']}.", ""]
    out += ["| Severity | Incidents | Detect median | Detect longest | Mitigate median | Mitigate longest | Resolve median | Resolve longest |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in s["by_severity"]:
        out.append(f"| {r['severity']} | {r['n']} | " + " | ".join(
            f"{fmt_minutes(r[k][f])}" for k in ("detect", "mitigate", "resolve") for f in ("median", "longest")) + " |")
    o = s["overall"]
    out.append(f"| All | {n} | " + " | ".join(
        f"{fmt_minutes(o[k][f])}" for k in ("detect", "mitigate", "resolve") for f in ("median", "longest")) + " |")
    out += ["", "Times run from impact start. They are Measured from the file you gave, and only as good as its start times.", ""]
    f = s["found_by"]
    out += ["## Detection", "",
            f"- Found by monitoring: {pct(f['monitoring'], n)}",
            f"- Found by customers: {pct(f['customer'], n)}",
            f"- Found by employees: {pct(f['employee'], n)}", ""]
    out.append("## Repeat contributing factors")
    out.append("")
    if s["repeat_factors"]:
        out += [f"- {t}: {c} incidents" for t, c in s["repeat_factors"]]
        out += ["", "This is a Proxy. It depends on how consistently the factor tags were written."]
    else:
        out.append("None appear in two or more incidents. If the file has no factor column, this tells you nothing.")
    p = s["postmortems"]
    out += ["", "## Postmortems", "",
            f"- Owed: {p['owed']}",
            f"- Published: {pct(p['published'], p['owed'])}",
            f"- Published within {p['target_days']} days of resolution: {pct(p['on_time'], p['owed'])}",
            f"- Overdue and unpublished: {', '.join(p['overdue_ids']) if p['overdue_ids'] else 'none'}"]
    if "actions" in s:
        a = s["actions"]
        out += ["", "## Action items", "",
                f"- Total: {a['total']}, done: {a['done']}, open: {a['open']}",
                f"- Open and overdue: {a['overdue']}" + (f", the oldest by {a['oldest_overdue_days']} days" if a["overdue"] else "")]
    out += ["", "Read the median and the longest value, not a mean. With fewer than 20 incidents, read each case. "
            "Do not compare teams by these numbers: a team that reports every incident will look worse than one that hides them.",
            f"Thresholds are defaults of this repository, not standards: a postmortem is published within {p['target_days']} days of resolution."]
    return "\n".join(out) + "\n"


def cmd_summary(args):
    as_of = parse_date(args.as_of)
    if as_of is None:
        raise InputError("--as-of must be YYYY-MM-DD.")
    incidents = load_incidents(args.incidents, as_of)
    for flag, name in ((args.since, "--since"), (args.until, "--until")):
        if flag and parse_date(flag) is None:
            raise InputError(f"{name} must be YYYY-MM-DD.")
    if args.since:
        incidents = [i for i in incidents if i["times"]["started"].date() >= parse_date(args.since)]
    if args.until:
        incidents = [i for i in incidents if i["times"]["started"].date() <= parse_date(args.until)]
    if not incidents:
        raise InputError("No incidents in the chosen window.")
    actions = load_actions(args.actions, {i["id"] for i in incidents}) if args.actions else None
    res = summarize(incidents, actions, as_of, args)
    if args.format == "json":
        print(json.dumps(res, indent=2))
    else:
        sys.stdout.write(render_summary_md(res, args))
    return 0


# ---------------------------------------------------------------- cli

def build_parser():
    p = argparse.ArgumentParser(description="Postmortem check and incident summary.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("postmortem", help="check a postmortem written from templates/postmortem.md")
    c.add_argument("--file", required=True)
    c.add_argument("--format", choices=("md", "json"), default="md")
    c.add_argument("--max-actions", type=int, default=8, help="warn above this many action items (default 8)")
    c.add_argument("--max-days", type=int, default=90, help="warn when an action is due this many days after resolution (default 90)")
    c.add_argument("--min-timeline", type=int, default=4, help="warn below this many timeline rows (default 4)")
    s = sub.add_parser("summary", help="summarize a CSV of incidents")
    s.add_argument("--incidents", required=True)
    s.add_argument("--actions")
    s.add_argument("--as-of", required=True, help="YYYY-MM-DD")
    s.add_argument("--since", help="only incidents that started on or after this date")
    s.add_argument("--until", help="only incidents that started on or before this date")
    s.add_argument("--pm-days", type=int, default=7, help="postmortem publishing target in days after resolution (default 7)")
    s.add_argument("--format", choices=("md", "json"), default="md")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return cmd_postmortem(args) if args.cmd == "postmortem" else cmd_summary(args)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
