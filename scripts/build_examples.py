#!/usr/bin/env python3
"""build_examples: keep the script output shown in examples/ identical to what the scripts print.

Python standard library only.

  python3 scripts/build_examples.py            rewrite every generated block
  python3 scripts/build_examples.py --check    exit 1 if any generated block is stale

A generated block in an example file looks like this:

  <!-- output:loop-draft -->
  > ...script output, as a block quote...
  <!-- end output -->

The key names a command in OUTPUTS below. Everything outside the markers is written by hand.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HP = "skills/hiring-plan/scripts"
LL = "skills/leveling-ladder/scripts"
IR = "skills/incident-response/scripts"

OUTPUTS = {
    "loop-draft": [f"{HP}/loop_check.py", "coverage", "--plan", f"{HP}/examples/loop-draft.json"],
    "loop-fixed": [f"{HP}/loop_check.py", "coverage", "--plan", f"{HP}/examples/loop-example.json"],
    "debrief": [f"{HP}/loop_check.py", "debrief", "--feedback", f"{HP}/examples/feedback-example.json",
                "--plan", f"{HP}/examples/loop-example.json"],
    "postmortem-draft": [f"{IR}/incident_check.py", "postmortem", "--file", f"{IR}/examples/postmortem-draft.md"],
    "postmortem-fixed": [f"{IR}/incident_check.py", "postmortem", "--file", f"{IR}/examples/postmortem-example.md"],
    "incident-summary": [f"{IR}/incident_check.py", "summary", "--incidents", f"{IR}/examples/incidents-example.csv",
                         "--actions", f"{IR}/examples/actions-example.csv", "--as-of", "2026-11-22"],
    "org-shape": [f"{LL}/org_shape.py", "--roster", f"{LL}/examples/roster-example.csv",
                  "--as-of", "2026-11-22", "--show-ids"],
}

BLOCK = re.compile(r"(<!-- output:(?P<key>[a-z0-9-]+) -->\n)(?P<body>.*?)(<!-- end output -->)", re.S)


def run(key):
    cmd = [sys.executable, "-I"] + [os.path.join(ROOT, c) if i == 0 or c.startswith(("skills/",)) else c
                                    for i, c in enumerate(OUTPUTS[key])]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if p.returncode not in (0, 1):          # loop_check exits 1 when it reports failures, which is the point of the draft
        raise SystemExit(f"{key}: the command failed with exit code {p.returncode}\n{p.stderr}")
    return p.stdout


def as_quote(text):
    return "".join(("> " + line if line.strip() else ">") + "\n" for line in text.rstrip("\n").split("\n"))


def example_files():
    base = os.path.join(ROOT, "examples")
    for dirpath, _, names in os.walk(base):
        for n in sorted(names):
            if n.endswith(".md"):
                yield os.path.join(dirpath, n)


def main(argv):
    check = "--check" in argv
    stale, blocks = [], 0
    for path in sorted(example_files()):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        def repl(m):
            nonlocal blocks
            key = m.group("key")
            if key not in OUTPUTS:
                raise SystemExit(f"{path}: unknown output key '{key}'")
            blocks += 1
            return m.group(1) + as_quote(run(key)) + m.group(4)

        new = BLOCK.sub(repl, text)
        if new != text:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
    if check:
        if stale:
            print("Stale example output in: " + ", ".join(stale) + ". Run: python3 scripts/build_examples.py")
            return 1
        print(f"Examples OK: {blocks} generated block(s) match the scripts.")
        return 0
    print(f"Refreshed {blocks} generated block(s); {len(stale)} file(s) changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
