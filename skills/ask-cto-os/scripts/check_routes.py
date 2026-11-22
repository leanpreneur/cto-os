#!/usr/bin/env python3
"""check_routes: keep the /ask-cto-os routing table honest.

Python standard library only. No model. The same input always gives the same output.

  python3 check_routes.py check  [--repo PATH] [--skip-docs]   fail if an artifact cannot be reached from a situation
  python3 check_routes.py render [--repo PATH]                   print docs/situations.md from the routing table
  python3 check_routes.py match  --text "..." [--format json]    rank situations by keyword signals (candidates only)

The routing table is skills/ask-cto-os/references/routes.json. Add every new playbook, template or skill to it.
Exit codes: 0 ok, 1 problems found, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES = os.path.join(HERE, "..", "references", "routes.json")
SELF_SKILL = "ask-cto-os"


class InputError(Exception):
    pass


def load_routes(path=ROUTES):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        raise InputError(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise InputError(f"{path} is not valid JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("situations"), list) or not data["situations"]:
        raise InputError("The routing table needs a non-empty 'situations' list.")
    return data


def default_repo():
    return os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def list_skills(repo):
    base = os.path.join(repo, "skills")
    if not os.path.isdir(base):
        return []
    return sorted(d for d in os.listdir(base)
                  if d != SELF_SKILL and os.path.isfile(os.path.join(base, d, "SKILL.md")))


def list_docs(repo, folder):
    base = os.path.join(repo, folder)
    if not os.path.isdir(base):
        return []
    return sorted(f"{folder}/{f}" for f in os.listdir(base) if f.endswith(".md"))


# ------------------------------------------------------------------- check

def check(data, repo, skip_docs=False):
    errors = []
    skills = set(list_skills(repo))
    seen_ids = set()
    reached_skills, reached_docs = set(), set()

    for i, s in enumerate(data["situations"], start=1):
        label = f"Situation {i}"
        if not isinstance(s, dict):
            errors.append(f"{label} is not an object.")
            continue
        sid = s.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"[a-z0-9-]+", sid or ""):
            errors.append(f"{label} needs an 'id' made of lowercase letters, digits and hyphens.")
            continue
        label = f"Situation '{sid}'"
        if sid in seen_ids:
            errors.append(f"{label}: duplicate id.")
        seen_ids.add(sid)
        for key in ("situation", "ask_first", "you_get"):
            if not isinstance(s.get(key), str) or not s[key].strip():
                errors.append(f"{label}: '{key}' must be a non-empty string.")
        sig = s.get("signals")
        if not isinstance(sig, list) or len(sig) < 3 or not all(isinstance(x, str) and x.strip() for x in sig):
            errors.append(f"{label}: 'signals' needs at least 3 non-empty strings.")
        start = s.get("start_with")
        then = s.get("then", [])
        read = s.get("read", [])
        if start is not None and not isinstance(start, str):
            errors.append(f"{label}: 'start_with' must be a skill name or null.")
        if not isinstance(then, list) or not isinstance(read, list):
            errors.append(f"{label}: 'then' and 'read' must be lists.")
            continue
        for name in ([start] if start else []) + list(then):
            if name == SELF_SKILL:
                errors.append(f"{label}: a route cannot point to {SELF_SKILL} itself.")
            elif name not in skills:
                errors.append(f"{label}: unknown skill '{name}'.")
            else:
                reached_skills.add(name)
        if start is None and not read:
            errors.append(f"{label}: with no skill to start with, 'read' must name at least one document.")
        for path in read:
            if not os.path.exists(os.path.join(repo, path)):
                errors.append(f"{label}: 'read' path does not exist: {path}")
            else:
                reached_docs.add(path)

    for name in sorted(skills - reached_skills):
        errors.append(f"Skill '{name}' cannot be reached from any situation.")
    for folder in ("playbooks", "templates"):
        for path in list_docs(repo, folder):
            if path not in reached_docs:
                errors.append(f"Document '{path}' cannot be reached from any situation.")

    for g in data.get("gaps", []):
        if not isinstance(g, dict) or not g.get("topic"):
            errors.append("Each gap needs a 'topic'. 'closest' is optional, and null means no close match.")
        elif g.get("closest") and g["closest"] not in skills and not os.path.exists(os.path.join(repo, g["closest"])):
            errors.append(f"Gap '{g['topic']}': closest '{g['closest']}' is not a skill or an existing file.")

    if not skip_docs:
        target = os.path.join(repo, "docs", "situations.md")
        if not os.path.isfile(target):
            errors.append("docs/situations.md is missing. Run: check_routes.py render > docs/situations.md")
        else:
            with open(target, encoding="utf-8") as fh:
                if fh.read() != render(data):
                    errors.append("docs/situations.md is out of date. Run: check_routes.py render > docs/situations.md")
    return errors


# ------------------------------------------------------------------ render

def doc_link(path, rel_prefix="../"):
    name = os.path.basename(path)
    stem = name[:-3] if name.endswith(".md") else name
    return f"[{stem}]({rel_prefix}{path})"


def render(data):
    out = ["# Find your situation", ""]
    out.append("Run `/ask-cto-os` and describe what is happening, or find your situation in the table. "
               "This page is generated from `skills/ask-cto-os/references/routes.json`. Do not edit it by hand.")
    out.append("")
    out.append("| If this is you | Start with | Then | Read |")
    out.append("| --- | --- | --- | --- |")
    for s in data["situations"]:
        start = f"`/{s['start_with']}`" if s.get("start_with") else "Read the documents"
        then = ", ".join(f"`/{n}`" for n in s.get("then", [])) or "none"
        read = ", ".join(doc_link(p) for p in s.get("read", [])) or "none"
        out.append(f"| {s['situation']} | {start} | {then} | {read} |")
    out.append("")
    gaps = data.get("gaps", [])
    if gaps:
        out.append("## Not covered yet")
        out.append("")
        for g in gaps:
            closest = g.get("closest")
            if not closest:
                out.append(f"- {g['topic']}. No close match today.")
            else:
                shown = doc_link(closest) if "/" in closest or closest.endswith(".md") else f"`/{closest}`"
                out.append(f"- {g['topic']}. Closest today: {shown}.")
        out.append("")
    return "\n".join(out)


# ------------------------------------------------------------------- match

def norm(text):
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip() + " "


def match(data, text, top=3):
    t = norm(text)
    scored = []
    for order, s in enumerate(data["situations"]):
        score = 0
        hits = []
        for sig in s.get("signals", []):
            n = norm(sig)
            if n in t:
                words = len(n.split())
                score += words
                hits.append(sig)
        if score:
            scored.append((-score, order, s["id"], s["situation"], hits))
    scored.sort()
    return [{"id": sid, "score": -neg, "situation": sit, "matched": hits}
            for neg, _, sid, sit, hits in scored[:top]]


# -------------------------------------------------------------------- main

def build_parser():
    p = argparse.ArgumentParser(description="Check, render and test the /ask-cto-os routing table.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--repo", default=default_repo())
    c.add_argument("--routes", default=ROUTES)
    c.add_argument("--skip-docs", action="store_true")
    r = sub.add_parser("render")
    r.add_argument("--routes", default=ROUTES)
    m = sub.add_parser("match")
    m.add_argument("--text", required=True)
    m.add_argument("--routes", default=ROUTES)
    m.add_argument("--format", choices=["md", "json"], default="md")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        data = load_routes(args.routes)
        if args.cmd == "check":
            errors = check(data, os.path.abspath(args.repo), args.skip_docs)
            if errors:
                print(f"{len(errors)} problem(s) in the routing table:")
                for e in errors:
                    print(f"- {e}")
                return 1
            print(f"Routing table OK: {len(data['situations'])} situations, every skill, playbook and template reachable.")
            return 0
        if args.cmd == "render":
            sys.stdout.write(render(data))
            return 0
        res = match(data, args.text)
        if args.format == "json":
            print(json.dumps(res, indent=2))
        elif not res:
            print("No situation matched. Ask the user one question about their role and the problem.")
        else:
            for i, r in enumerate(res, start=1):
                print(f"{i}. {r['id']} (score {r['score']}): {r['situation']}. Matched: {', '.join(r['matched'])}")
        return 0
    except InputError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
