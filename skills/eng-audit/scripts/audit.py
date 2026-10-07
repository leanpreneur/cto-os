#!/usr/bin/env python3
"""eng-audit: engineering baseline metrics from git history.

Standard library only. Reads one or more local git repositories and, optionally,
GitHub pull request data. Prints a Markdown report, JSON, or both.

Rules this tool follows:
  * No estimates. Anything git cannot show is reported as Unknown, with the source
    that would answer it.
  * Every number is labeled Measured (git states it directly), Proxy (git suggests it
    but the definition differs) or Unknown.
  * No model is involved. The same repository and window give the same numbers.
"""
import argparse
import json
import math
import os
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

VERSION = "0.1.0"

# Paths excluded from change-size math: lockfiles, minified or generated output.
EXCLUDE_RE = re.compile(
    r"(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|poetry\.lock|uv\.lock|"
    r"Pipfile\.lock|Cargo\.lock|go\.sum|Gemfile\.lock|composer\.lock)$"
    r"|\.lock$|\.min\.(js|css)$|\.snap$|(^|/)(dist|build|vendor|node_modules)/"
)
BOT_NAME_RE = re.compile(r"\[bot\]|\bbot$|dependabot|renovate|github-actions|semantic-release", re.I)
AI_TRAILER_RE = re.compile(
    r"co-authored-by:[^\n]*(claude|copilot|cursor|codex|gemini|devin|aider|openai|anthropic)"
    r"|generated with \[?claude code", re.I)
REVERT_SUBJECT_RE = re.compile(r"^revert\b", re.I)
REVERT_BODY_RE = re.compile(r"This reverts commit ([0-9a-f]{7,40})", re.I)
HOTFIX_RE = re.compile(r"\bhot-?fix", re.I)
SQUASH_PR_RE = re.compile(r"\(#\d+\)\s*$")
MERGE_PR_RE = re.compile(r"^Merge pull request #\d+")

CONTEXT_PATTERNS = {
    "instruction_files": re.compile(
        r"(^|/)(agents\.md|claude\.md|gemini\.md|conventions\.md|\.cursorrules|\.windsurfrules)$"
        r"|(^|/)\.cursor/rules/|(^|/)\.github/copilot-instructions\.md$|(^|/)\.claude/", re.I),
    "codeowners": re.compile(r"(^|/)codeowners$", re.I),
    "pr_template": re.compile(r"pull_request_template(\.md|/)", re.I),
    "contributing": re.compile(r"(^|/)contributing(\.(md|rst|txt))?$", re.I),
    "security_policy": re.compile(r"(^|/)security(\.(md|rst|txt))?$", re.I),
    "decision_records": re.compile(r"(^|/)(adrs?|decisions|architecture-decisions?)/", re.I),
    "runbooks": re.compile(r"(^|/)(runbooks?|playbooks?|on-?call)/", re.I),
    "ci_config": re.compile(
        r"^\.github/workflows/|^\.gitlab-ci\.yml$|^jenkinsfile$|^\.circleci/"
        r"|^azure-pipelines\.yml$|^bitbucket-pipelines\.yml$", re.I),
    "ai_policy": re.compile(r"(^|/)ai[-_ ]?(policy|usage|guidelines|use)[^/]*\.md$", re.I),
}
CONTEXT_LABELS = {
    "instruction_files": "AI instruction files (AGENTS.md, CLAUDE.md, editor rules)",
    "codeowners": "CODEOWNERS",
    "pr_template": "Pull request template",
    "contributing": "CONTRIBUTING guide",
    "security_policy": "Security policy",
    "decision_records": "Decision records (adr, decisions)",
    "runbooks": "Runbooks",
    "ci_config": "CI configuration",
    "ai_policy": "AI usage policy file",
}


def run(cmd, cwd, check=True):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace")
    if check and p.returncode != 0:
        raise RuntimeError("%s failed: %s" % (" ".join(cmd[:3]), p.stderr.strip()[:300]))
    return p.stdout


def git(repo, *args, check=True):
    return run(["git"] + list(args), repo, check)


def parse_dt(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def median(xs):
    return statistics.median(xs) if xs else None


def pctl(xs, q):
    if not xs:
        return None
    s = sorted(xs)
    return s[max(0, math.ceil(q * len(s)) - 1)]


def norm_path(path):
    if "{" in path and "=>" in path:
        path = re.sub(r"\{[^}]* => ([^}]*)\}", r"\1", path).replace("//", "/")
    elif " => " in path:
        path = path.split(" => ")[-1]
    return path


def parse_numstat(block):
    lines, files = 0, []
    for ln in block.split("\n"):
        parts = ln.split("\t")
        if len(parts) != 3:
            continue
        added, deleted, path = parts
        path = norm_path(path)
        if EXCLUDE_RE.search(path):
            continue
        files.append(path)
        if added.isdigit() and deleted.isdigit():
            lines += int(added) + int(deleted)
    return lines, files


def resolve_ref(repo, override):
    if override:
        return override
    p = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD", check=False).strip()
    if p:
        return p
    cur = git(repo, "rev-parse", "--abbrev-ref", "HEAD", check=False).strip()
    if cur and cur != "HEAD":
        return cur
    for c in ("main", "master"):
        if git(repo, "rev-parse", "--verify", "--quiet", c, check=False).strip():
            return c
    raise RuntimeError("Could not determine the default branch. Pass --branch.")


def shallow_boundary(repo):
    """SHAs at the edge of a shallow clone. Git shows them as adding every file."""
    p = git(repo, "rev-parse", "--git-path", "shallow", check=False).strip()
    if not p:
        return set()
    full = p if os.path.isabs(p) else os.path.join(repo, p)
    try:
        with open(full, encoding="utf-8") as fh:
            return set(x.strip() for x in fh if x.strip())
    except OSError:
        return set()


def collect_commits(repo, ref, since, boundary=frozenset()):
    fmt = "%x1e%H%x1f%aE%x1f%aN%x1f%aI%x1f%P%x1f%s%x1f%b%x1f"
    out = git(repo, "log", ref, "--since=" + since, "--no-merges", "--numstat", "--format=" + fmt)
    commits, skipped = [], 0
    for rec in out.split("\x1e")[1:]:
        parts = rec.split("\x1f", 7)
        if len(parts) < 8:
            continue
        sha, email, name, date, parents, subject, body, rest = parts
        if sha in boundary:
            skipped += 1
            continue
        lines, files = parse_numstat(rest)
        commits.append({
            "sha": sha, "email": email.strip().lower(), "name": name.strip(),
            "date": parse_dt(date), "subject": subject.strip(), "body": body,
            "lines": lines, "files": files,
            "bot": bool(BOT_NAME_RE.search(name) or "[bot]" in email.lower() or "dependabot" in email.lower()),
        })
    return commits, skipped


def collect_merges(repo, ref, since):
    fmt = "%x1e%H%x1f%aI%x1f%P%x1f%s%x1f%b"
    out = git(repo, "log", ref, "--since=" + since, "--merges", "--format=" + fmt)
    merges = []
    for rec in out.split("\x1e")[1:]:
        parts = rec.split("\x1f", 4)
        if len(parts) < 5:
            continue
        sha, date, parents, subject, body = parts
        merges.append({"sha": sha, "date": parse_dt(date), "parents": parents.split(),
                       "subject": subject.strip(), "body": body})
    return merges


def pr_units_from_merges(repo, merges, cap=300):
    units = []
    prs = [m for m in merges if len(m["parents"]) == 2 and
           (MERGE_PR_RE.match(m["subject"]) or "See merge request" in m["body"])]
    for m in prs[:cap]:
        p1, p2 = m["parents"]
        lines, _ = parse_numstat(git(repo, "diff", "--numstat", p1, m["sha"], check=False))
        dates = [parse_dt(x) for x in git(repo, "log", "--format=%aI", "%s..%s" % (p1, p2), check=False).split()]
        life = None
        if dates:
            hours = (m["date"] - min(dates)).total_seconds() / 3600.0
            if hours >= 0:
                life = hours
        who = git(repo, "show", "-s", "--format=%aN%x1f%aE", p2, check=False).strip().split("\x1f")
        bot = bool(len(who) == 2 and (BOT_NAME_RE.search(who[0]) or "[bot]" in who[1].lower()))
        units.append({"lines": lines, "lifetime_hours": life, "bot": bot})
    return units, len(prs), len(merges) - len(prs)


def tag_info(repo, since_dt):
    out = git(repo, "for-each-ref", "--sort=creatordate",
              "--format=%(refname:short)\t%(creatordate:iso-strict)", "refs/tags", check=False)
    tags = []
    for ln in out.split("\n"):
        if "\t" in ln:
            name, d = ln.split("\t", 1)
            try:
                tags.append((name, parse_dt(d)))
            except ValueError:
                continue
    in_window = [t for t in tags if t[1] >= since_dt]
    gaps = [(b[1] - a[1]).total_seconds() / 86400.0 for a, b in zip(in_window, in_window[1:])]
    last = tags[-1] if tags else None
    return {"total": len(tags), "in_window": len(in_window),
            "median_gap_days": median(gaps) if len(in_window) >= 3 else None,
            "last_tag": last[0] if last else None,
            "last_tag_date": last[1].date().isoformat() if last else None}


def ref_files(repo, ref):
    return [p for p in git(repo, "ls-tree", "-r", "--name-only", ref, check=False).split("\n") if p]


def newest_commit_date(repo, ref, paths, boundary=frozenset()):
    paths = paths[:200]
    if not paths:
        return None
    out = git(repo, "log", "-1", "--format=%H%x1f%aI", ref, "--", *paths, check=False).strip()
    if not out or "\x1f" not in out:
        return None
    sha, date = out.split("\x1f", 1)
    return None if sha in boundary else parse_dt(date)


def context_scan(repo, ref, files, now, boundary=frozenset()):
    result = {}
    for key, rx in CONTEXT_PATTERNS.items():
        matched = [p for p in files if rx.search(p)]
        newest = newest_commit_date(repo, ref, matched, boundary) if matched else None
        result[key] = {
            "found": bool(matched), "count": len(matched), "examples": matched[:5],
            "last_changed": newest.date().isoformat() if newest else None,
            "age_days": (now - newest).days if newest else None,
        }
    instr = [p for p in files if CONTEXT_PATTERNS["instruction_files"].search(p)]
    root_level = [p for p in instr if "/" not in p or p.startswith((".github/", ".cursor/", ".claude/"))]
    result["instruction_files"]["root_level"] = bool(root_level)
    return result


def doc_freshness(repo, ref, files, now):
    docs = [p for p in files if p.lower().endswith((".md", ".mdx", ".rst"))
            and not EXCLUDE_RE.search(p)
            and not re.search(r"(^|/)(changelog|license|licence|code_of_conduct|third[-_]party)[^/]*$", p, re.I)]
    if not docs:
        return None
    since = (now - timedelta(days=365)).isoformat()
    touched = set(norm_path(x) for x in git(repo, "log", ref, "--since=" + since,
                                          "--name-only", "--format=", check=False).split("\n") if x)
    fresh = sum(1 for p in docs if p in touched)
    return {"docs": len(docs), "touched_last_12_months": fresh, "share": fresh / len(docs)}


def github_prs(args, repo, since_dt):
    data = None
    note = None
    if args.prs:
        with open(args.prs, encoding="utf-8") as fh:
            data = json.load(fh)
    elif args.gh:
        try:
            out = run(["gh", "pr", "list", "--state", "merged", "--limit", "300", "--json",
                       "number,createdAt,mergedAt,additions,deletions,reviews"], repo)
            data = json.loads(out)
        except (RuntimeError, FileNotFoundError, json.JSONDecodeError) as exc:
            return {"available": False, "reason": "GitHub data not available (%s)." % str(exc)[:200]}
    else:
        return None
    rows = [p for p in data if p.get("mergedAt") and parse_dt(p["mergedAt"]) >= since_dt]
    sizes = [(p.get("additions") or 0) + (p.get("deletions") or 0) for p in rows]
    cycle = [(parse_dt(p["mergedAt"]) - parse_dt(p["createdAt"])).total_seconds() / 3600.0
             for p in rows if p.get("createdAt")]
    first_review, no_review = [], 0
    for p in rows:
        subs = [parse_dt(r["submittedAt"]) for r in (p.get("reviews") or []) if r.get("submittedAt")]
        if subs and p.get("createdAt"):
            first_review.append((min(subs) - parse_dt(p["createdAt"])).total_seconds() / 3600.0)
        else:
            no_review += 1
    return {"available": True, "count": len(rows), "limit_reached": len(data) >= 300,
            "median_size": median(sizes), "p90_size": pctl(sizes, 0.9),
            "median_cycle_hours": median(cycle), "median_first_review_hours": median(first_review),
            "share_without_review": (no_review / len(rows)) if rows else None}


def audit_repo(repo, args, now):
    repo = os.path.abspath(repo)
    if not os.path.isdir(os.path.join(repo, ".git")) and \
            git(repo, "rev-parse", "--git-dir", check=False).strip() == "":
        raise RuntimeError("%s is not a git repository." % repo)
    ref = resolve_ref(repo, args.branch)
    since_dt = now - timedelta(days=args.days)
    since = since_dt.isoformat()
    head = git(repo, "log", "-1", "--format=%H%x1f%aI", ref).strip()
    head_sha, head_date = head.split("\x1f")
    head_dt = parse_dt(head_date)
    shallow = git(repo, "rev-parse", "--is-shallow-repository", check=False).strip() == "true"
    roots = [parse_dt(x) for x in git(repo, "log", ref, "--max-parents=0", "--format=%aI", check=False).split()]
    oldest = min(roots) if roots else None

    warnings = []
    if shallow:
        warnings.append("This is a shallow clone. History before the clone depth is missing, so counts may be truncated.")
    if oldest and oldest > since_dt:
        warnings.append("History starts %s, after the window start %s. Numbers cover only the available history."
                        % (oldest.date().isoformat(), since_dt.date().isoformat()))
    stale_days = (now - head_dt).days
    if stale_days > 14:
        warnings.append("The newest commit on %s is %d days old. Run git fetch if this is not expected." % (ref, stale_days))

    boundary = shallow_boundary(repo) if shallow else frozenset()
    commits, skipped = collect_commits(repo, ref, since, boundary)
    if skipped:
        warnings.append("%d commit(s) at the edge of the shallow clone were excluded, because git shows them as adding every file. Run git fetch --unshallow for full history." % skipped)
    merges = collect_merges(repo, ref, since)
    human = [c for c in commits if not c["bot"]]
    bots = len(commits) - len(human)
    if not commits:
        warnings.append("No commits on %s in the last %d days. Check --branch and --days." % (ref, args.days))

    weeks = max(args.days / 7.0, 1e-9)
    metrics = []

    def add(mid, label, value, kind, note="", unit=""):
        if value is None:
            kind = "Unknown"
        metrics.append({"id": mid, "label": label, "value": value, "unit": unit, "kind": kind, "note": note})

    add("commits", "Commits to %s (excluding merges and bots)" % ref, len(human), "Measured",
        "%.1f per week. Bot commits excluded: %d." % (len(human) / weeks, bots), "commits")
    contributors = len(set(c["email"] for c in human))
    add("contributors", "Active human contributors", contributors, "Measured",
        "Distinct author emails with at least one commit in the window.", "people")

    # Pull-request units and change size
    squash = [c for c in commits if SQUASH_PR_RE.search(c["subject"])]
    merge_units, merge_pr_count, other_merges = pr_units_from_merges(repo, merges)
    all_units = [{"lines": c["lines"], "lifetime_hours": None, "bot": c["bot"]} for c in squash] + merge_units
    units = [u for u in all_units if not u["bot"]]
    bot_units = len(all_units) - len(units)
    if len(units) >= 10:
        basis = "human pull requests (%d found, %d bot pull requests excluded)" % (len(units), bot_units)
        sizes = [u["lines"] for u in units]
        size_kind = "Measured"
    else:
        basis = "human commits, used as a proxy because fewer than 10 human pull request changes were found"
        sizes = [c["lines"] for c in human]
        size_kind = "Proxy"
    add("integration", "Pull request changes per week", (len(units) / weeks) if units else None,
        "Measured" if units else "Unknown",
        "%d human pull request changes found, %d bot excluded. Merge commits that are not pull requests: %d." % (len(units), bot_units, other_merges) if units
        else "No human squash or merge-commit pull requests found in the window. Bot pull requests: %d. Merge commits that are not pull requests: %d." % (bot_units, other_merges), "per week")
    add("size_median", "Median change size", median(sizes), size_kind,
        "Lines added plus deleted, excluding lockfiles and generated output. Basis: %s." % basis, "lines")
    add("size_p90", "90th percentile change size", pctl(sizes, 0.9), size_kind, "Same basis as the median.", "lines")
    over = (sum(1 for s in sizes if s > args.threshold) / len(sizes)) if sizes else None
    add("size_over", "Share of changes above %d lines" % args.threshold, over, size_kind,
        "The threshold is a default you should set with the team before reading the data.")
    lifetimes = [u["lifetime_hours"] for u in merge_units if u["lifetime_hours"] is not None and not u["bot"]]
    add("branch_life", "Median branch lifetime (first commit to merge)",
        median(lifetimes) if len(lifetimes) >= 5 else None, "Proxy" if len(lifetimes) >= 5 else "Unknown",
        "From merge-commit pull requests only (%d found). Squash merges hide the branch, so use GitHub data for those." % len(lifetimes),
        "hours")

    gh = github_prs(args, repo, since_dt)
    if gh is None:
        add("pr_cycle", "Median pull request cycle time (opened to merged)", None, "Unknown",
            "Needs GitHub data. Re-run with --gh or --prs FILE.", "hours")
        add("pr_review", "Median time to first review", None, "Unknown", "Needs GitHub data. Re-run with --gh or --prs FILE.", "hours")
    elif not gh["available"]:
        add("pr_cycle", "Median pull request cycle time (opened to merged)", None, "Unknown", gh["reason"], "hours")
        add("pr_review", "Median time to first review", None, "Unknown", gh["reason"], "hours")
    else:
        cap = " The 300 pull request limit was reached, so older pull requests in the window are missing." if gh["limit_reached"] else ""
        add("pr_cycle", "Median pull request cycle time (opened to merged)", gh["median_cycle_hours"], "Measured",
            "%d merged pull requests in the window.%s" % (gh["count"], cap), "hours")
        add("pr_review", "Median time to first review", gh["median_first_review_hours"], "Measured",
            "%s of pull requests had no recorded review." % (("%.0f%%" % (100 * gh["share_without_review"])) if gh["share_without_review"] is not None else "Unknown"),
            "hours")
        add("pr_size_gh", "Median pull request size (GitHub)", gh["median_size"], "Measured",
            "Includes lockfiles and generated files, so it runs higher than the git figure.", "lines")

    # Releases
    tg = tag_info(repo, since_dt)
    if tg["total"] == 0:
        add("tags", "Tags in the window", None, "Unknown",
            "No tags found. Releases are not visible in git. Use CI/CD or deployment tool data for deployment frequency."
            + (" This is a shallow clone, so run git fetch --tags first." if shallow else ""))
    else:
        add("tags", "Tags in the window", tg["in_window"], "Proxy",
            "A tag is not a deployment. Last tag: %s (%s)." % (tg["last_tag"], tg["last_tag_date"]), "tags")
        add("tag_gap", "Median days between tags", tg["median_gap_days"], "Proxy" if tg["median_gap_days"] is not None else "Unknown",
            "Needs at least 3 tags in the window." if tg["median_gap_days"] is None else "Proxy for release cadence.", "days")

    # Reverts and hotfixes
    reverts, revert_hours = 0, []
    for c in commits:
        m = REVERT_BODY_RE.search(c["body"])
        if REVERT_SUBJECT_RE.match(c["subject"]) or m:
            reverts += 1
            if m:
                tdate = git(repo, "show", "-s", "--format=%aI", m.group(1), check=False).strip()
                if tdate:
                    h = (c["date"] - parse_dt(tdate)).total_seconds() / 3600.0
                    if h >= 0:
                        revert_hours.append(h)
    hotfixes = sum(1 for c in commits if HOTFIX_RE.search(c["subject"]))
    add("reverts", "Revert commits", reverts, "Measured",
        ("%.1f%% of commits. " % (100.0 * reverts / len(commits)) if commits else "No commits in the window. ") +
        "A real change failure rate needs incident or rollback records.", "commits")
    add("revert_time", "Median time from change to its revert",
        median(revert_hours) if len(revert_hours) >= 3 else None, "Proxy" if len(revert_hours) >= 3 else "Unknown",
        "Needs at least 3 reverts that name the reverted commit. This is not time to restore service.", "hours")
    add("hotfixes", "Commits with hotfix in the subject", hotfixes, "Proxy",
        "Keyword match. Undercounts teams that do not use the word.", "commits")

    # Contributor concentration
    counts = Counter(c["email"] for c in human)
    total = sum(counts.values())
    rank = {e: i + 1 for i, (e, _) in enumerate(counts.most_common())}
    names = {c["email"]: c["name"] for c in human}

    def label(email):
        return names.get(email, email) if args.names else "Contributor %d" % rank[email]

    k, cum = 0, 0
    for email, n in counts.most_common():
        cum += n
        k += 1
        if total and cum / total >= 0.5:
            break
    add("bus_factor", "Contributors who account for half of all commits", k if total else None,
        "Measured" if total else "Unknown", "A simple concentration measure. It does not capture who knows what.", "people")
    dir_commits, dir_authors = Counter(), defaultdict(Counter)
    for c in human:
        for d in set((p.split("/")[0] if "/" in p else "(root)") for p in c["files"]):
            dir_commits[d] += 1
            dir_authors[d][c["email"]] += 1
    concentration = []
    for d, n in dir_commits.most_common(8):
        if n < 10:
            continue
        top_email, top_n = dir_authors[d].most_common(1)[0]
        concentration.append({"dir": d, "commits": n, "top_contributor": label(top_email),
                              "share": top_n / n, "flag": (top_n / n) >= 0.8})

    # AI traceability
    ai = sum(1 for c in commits if AI_TRAILER_RE.search(c["subject"] + "\n" + c["body"]))
    add("ai_trace", "Commits that name an AI tool in a trailer or message", ai, "Measured",
        ("%.1f%% of commits. " % (100.0 * ai / len(commits)) if commits else "No commits in the window. ") +
        "Absence does not mean AI was not used. It means the use is not traceable here.", "commits")

    # Context and knowledge
    files = ref_files(repo, ref)
    ctx = context_scan(repo, ref, files, now, boundary)
    fresh = None if shallow else doc_freshness(repo, ref, files, now)
    if fresh:
        add("doc_fresh", "Markdown and doc files changed in the last 12 months", fresh["share"], "Measured",
            "%d of %d files." % (fresh["touched_last_12_months"], fresh["docs"]))
    else:
        add("doc_fresh", "Markdown and doc files changed in the last 12 months", None, "Unknown",
            "Needs full history. Run git fetch --unshallow." if shallow else "No documentation files found.")

    return {
        "repo": os.path.basename(repo), "path": repo, "ref": ref, "head_sha": head_sha[:7],
        "head_date": head_dt.date().isoformat(), "window_days": args.days,
        "window_start": since_dt.date().isoformat(), "generated": now.date().isoformat(),
        "tool_version": VERSION, "warnings": warnings, "metrics": metrics,
        "concentration": concentration, "context": ctx, "threshold": args.threshold,
        "change_basis": basis, "branch_protection": "Unknown",
    }


def fmt_value(m):
    v = m["value"]
    if v is None:
        return "Unknown"
    if isinstance(v, float):
        if m["id"] in ("size_over", "doc_fresh"):
            return "%.0f%%" % (100 * v)
        v = round(v, 1)
        if v == int(v):
            v = int(v)
    unit = m["unit"]
    if v == 1:
        unit = {"commits": "commit", "people": "person", "tags": "tag"}.get(unit, unit)
    return ("%s %s" % (v, unit)).strip()


def esc(s):
    return str(s).replace("|", "\\|")


def render_repo(r):
    L = []
    L.append("# Engineering baseline: %s" % r["repo"])
    L.append("")
    L.append("Ref `%s` at `%s` (%s). Window: last %d days from %s. Generated %s by eng-audit %s."
             % (r["ref"], r["head_sha"], r["head_date"], r["window_days"], r["window_start"], r["generated"], r["tool_version"]))
    L.append("")
    for w in r["warnings"]:
        L.append("> Warning: %s" % w)
    if r["warnings"]:
        L.append("")
    L.append("Types: **Measured** means git states it directly. **Proxy** means git suggests it, but the definition differs from the standard one. **Unknown** means git cannot show it, and the note names the source that can.")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Metric | Value | Type | Note |")
    L.append("| --- | --- | --- | --- |")
    for m in r["metrics"]:
        L.append("| %s | %s | %s | %s |" % (esc(m["label"]), esc(fmt_value(m)), m["kind"], esc(m["note"])))
    L.append("")
    if r["concentration"]:
        L.append("## Where work concentrates")
        L.append("")
        L.append("| Top-level folder | Commits | Top contributor | Share | Flag |")
        L.append("| --- | --- | --- | --- | --- |")
        for c in r["concentration"]:
            L.append("| %s | %d | %s | %.0f%% | %s |" % (esc(c["dir"]), c["commits"], esc(c["top_contributor"]),
                                                       100 * c["share"], "One contributor holds 80% or more" if c["flag"] else ""))
        L.append("")
        L.append("Use this to ask who else can change the flagged areas. Do not use it to evaluate people.")
        L.append("")
    L.append("## Context and knowledge files at `%s`" % r["ref"])
    L.append("")
    L.append("| Item | Found | Count | Last changed |")
    L.append("| --- | --- | --- | --- |")
    for key, label in CONTEXT_LABELS.items():
        c = r["context"][key]
        L.append("| %s | %s | %d | %s |" % (label, "Yes" if c["found"] else "No", c["count"],
                                           c["last_changed"] or "n/a"))
    L.append("")
    ins = r["context"]["instruction_files"]
    L.append("Instruction file at the repository root level: **%s**." % ("Yes" if ins.get("root_level") else "No"))
    L.append("")
    L.append("## Baseline rows for the First 90 Days table")
    L.append("")
    L.append("These are git-derived stand-ins. Replace them with CI/CD and incident data when you have it.")
    L.append("")
    L.append("| Metric | Value | Source | Date |")
    L.append("| --- | --- | --- | --- |")
    mm = {m["id"]: m for m in r["metrics"]}

    def row(name, ids, source):
        vals = []
        for i in ids:
            if i in mm and mm[i]["value"] is not None:
                vals.append("%s: %s" % (mm[i]["label"], fmt_value(mm[i])))
        L.append("| %s | %s | %s | %s |" % (name, esc("; ".join(vals)) if vals else "Unknown", source if vals else "Needs CI/CD or deployment data", r["generated"]))

    row("Deployment frequency", ["tags", "tag_gap", "integration"], "git tags and pull request merges, proxy")
    row("Lead time for changes", ["pr_cycle", "branch_life"], "GitHub or git branch history, proxy")
    row("Change failure rate", ["reverts"], "git reverts, proxy")
    row("Time to restore service", ["revert_time"], "git reverts, proxy")
    L.append("")
    L.append("## Evidence for the ADOPT assessment")
    L.append("")
    L.append("This is evidence, not a rating. You make the Present, Partial or Absent call with the playbook.")
    L.append("")
    sm = mm["size_median"]
    L.append("- **Small batches (capability 5):** median change size %s, %s of changes above %d lines (basis: %s)."
             % (fmt_value(sm), fmt_value(mm["size_over"]), r["threshold"], r["change_basis"]))
    L.append("- **Version control (capability 4):** revert commits in the window: %s. Branch protection is **Unknown** from git. Check the repository settings (Branches and Rules)." % fmt_value(mm["reverts"]))
    dm = mm["doc_fresh"]
    L.append("- **Healthy data (capability 2):** documentation changed in the last 12 months: %s. Decision records found: %s. Runbooks found: %s."
             % (fmt_value(dm), "yes" if r["context"]["decision_records"]["found"] else "no", "yes" if r["context"]["runbooks"]["found"] else "no"))
    L.append("- **AI-accessible data (capability 3):** not visible in git. Check how the approved AI tools connect to repositories, docs and tickets.")
    L.append("- **AI stance (capability 1):** an AI usage policy file was %s. Whether engineers can describe the stance comes from interviews, not git."
             % ("found" if r["context"]["ai_policy"]["found"] else "not found"))
    L.append("- **Context practice (dimension D):** instruction files found: %d, at root level: %s, last changed: %s."
             % (ins["count"], "yes" if ins.get("root_level") else "no", ins["last_changed"] or "n/a"))
    L.append("- **Traceability (dimension P):** commits that name an AI tool: %s. Absence does not mean AI was not used." % fmt_value(mm["ai_trace"]))
    L.append("")
    L.append("## Not visible in git")
    L.append("")
    L.append("| Item | Where to get it |")
    L.append("| --- | --- |")
    for item, src in (("Deployment frequency and lead time to production", "CI/CD and deployment tool"),
                      ("Change failure rate and time to restore", "Incident tracker, rollback records, on-call history"),
                      ("Branch protection and required reviews", "Repository settings"),
                      ("Review quality", "Interviews and sampled pull requests"),
                      ("Unplanned work, attrition, cloud cost, open roles", "Ticketing, HR and billing systems")):
        L.append("| %s | %s |" % (item, src))
    L.append("")
    return "\n".join(L)


def render_all(results):
    if len(results) == 1:
        return render_repo(results[0])
    L = ["# Engineering baseline: %d repositories" % len(results), "", "## Context files across repositories", "",
         "| Repository | Instruction file | CODEOWNERS | PR template | Decision records | Runbooks | CI |",
         "| --- | --- | --- | --- | --- | --- | --- |"]

    def yn(r, k):
        return "Yes" if r["context"][k]["found"] else "No"
    for r in results:
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (esc(r["repo"]), yn(r, "instruction_files"), yn(r, "codeowners"),
                 yn(r, "pr_template"), yn(r, "decision_records"), yn(r, "runbooks"), yn(r, "ci_config")))
    have = sum(1 for r in results if r["context"]["instruction_files"]["found"])
    L += ["", "Repositories with an AI instruction file: %d of %d." % (have, len(results)), ""]
    for r in results:
        L.append(render_repo(r).replace("# Engineering baseline:", "## Repository:", 1))
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Engineering baseline metrics from git history.")
    ap.add_argument("--repo", action="append", help="Path to a git repository. Repeat for several. Default: current directory.")
    ap.add_argument("--days", type=int, default=90, help="Window in days. Default 90.")
    ap.add_argument("--branch", help="Branch or ref to analyze. Default: the remote default branch.")
    ap.add_argument("--threshold", type=int, default=400, help="Change size threshold in lines. Default 400.")
    ap.add_argument("--gh", action="store_true", help="Also read merged pull requests with the GitHub CLI.")
    ap.add_argument("--prs", help="JSON file from: gh pr list --state merged --limit 300 --json number,createdAt,mergedAt,additions,deletions,reviews")
    ap.add_argument("--names", action="store_true", help="Show contributor names instead of Contributor N.")
    ap.add_argument("--format", choices=["md", "json", "both"], default="md")
    ap.add_argument("--out", help="Directory to write eng-audit.md and eng-audit.json. Default: print to stdout.")
    args = ap.parse_args()
    repos = args.repo or ["."]
    if args.prs and len(repos) > 1:
        ap.error("--prs works with a single --repo.")
    now = datetime.now(timezone.utc)
    results, failed = [], []
    for r in repos:
        try:
            results.append(audit_repo(r, args, now))
        except (RuntimeError, ValueError) as exc:
            failed.append((r, str(exc)))
    for r, msg in failed:
        sys.stderr.write("eng-audit: skipped %s: %s\n" % (r, msg))
    if not results:
        sys.exit(1)
    md, js = render_all(results), json.dumps(results if len(results) > 1 else results[0], indent=2)
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        if args.format in ("md", "both"):
            with open(os.path.join(args.out, "eng-audit.md"), "w", encoding="utf-8") as fh:
                fh.write(md + "\n")
        if args.format in ("json", "both"):
            with open(os.path.join(args.out, "eng-audit.json"), "w", encoding="utf-8") as fh:
                fh.write(js + "\n")
        sys.stderr.write("eng-audit: wrote report to %s\n" % args.out)
    else:
        if args.format in ("md", "both"):
            print(md)
        if args.format in ("json", "both"):
            print(js)


if __name__ == "__main__":
    main()
