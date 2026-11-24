"""Tests for check_routes.py.

Run:  python3 -I test_check_routes.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_routes.py")
REAL_ROUTES = os.path.join(HERE, "..", "references", "routes.json")
REAL_REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def run(*args):
    p = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def touch(path):
    with open(path, "w") as fh:
        fh.write("x")


def situation(sid, start=None, then=(), read=(), signals=("one thing", "two things", "three things")):
    return {"id": sid, "situation": f"Situation {sid}", "signals": list(signals), "start_with": start,
            "then": list(then), "read": list(read), "ask_first": "A question?", "you_get": "Something."}


def make_repo(skills=("a", "b"), playbooks=("p1.md",), templates=("t1.md",)):
    root = tempfile.mkdtemp()
    for s in skills:
        os.makedirs(os.path.join(root, "skills", s))
        touch(os.path.join(root, "skills", s, "SKILL.md"))
    os.makedirs(os.path.join(root, "skills", "ask-cto-os"))
    touch(os.path.join(root, "skills", "ask-cto-os", "SKILL.md"))
    for folder, names in (("playbooks", playbooks), ("templates", templates)):
        os.makedirs(os.path.join(root, folder))
        for n in names:
            touch(os.path.join(root, folder, n))
    os.makedirs(os.path.join(root, "docs"))
    return root


def check(root, situations, gaps=(), skip_docs=True):
    routes = os.path.join(root, "routes.json")
    with open(routes, "w") as fh:
        json.dump({"version": 1, "situations": situations, "gaps": list(gaps)}, fh)
    args = ["check", "--repo", root, "--routes", routes] + (["--skip-docs"] if skip_docs else [])
    return run(*args)


class Synthetic(unittest.TestCase):
    def good(self):
        return [situation("s1", start="a", read=["playbooks/p1.md"]),
                situation("s2", start="b", read=["templates/t1.md"])]

    def test_good_table_passes(self):
        code, out, _ = check(make_repo(), self.good())
        self.assertEqual(code, 0, out)
        self.assertIn("Routing table OK: 2 situations", out)

    def test_unreachable_skill(self):
        root = make_repo(skills=("a", "b", "c"))
        code, out, _ = check(root, self.good())
        self.assertEqual(code, 1)
        self.assertIn("Skill 'c' cannot be reached", out)

    def test_unreachable_playbook_and_template(self):
        root = make_repo(playbooks=("p1.md", "p2.md"), templates=("t1.md", "t2.md"))
        code, out, _ = check(root, self.good())
        self.assertEqual(code, 1)
        self.assertIn("Document 'playbooks/p2.md' cannot be reached", out)
        self.assertIn("Document 'templates/t2.md' cannot be reached", out)

    def test_then_counts_as_reaching_a_skill(self):
        root = make_repo(skills=("a", "b", "c"))
        s = self.good()
        s[0]["then"] = ["c"]
        code, out, _ = check(root, s)
        self.assertEqual(code, 0, out)

    def test_missing_read_path(self):
        s = self.good()
        s[0]["read"].append("playbooks/nope.md")
        code, out, _ = check(make_repo(), s)
        self.assertEqual(code, 1)
        self.assertIn("'read' path does not exist: playbooks/nope.md", out)

    def test_unknown_skill_and_self_route(self):
        s = self.good()
        s[0]["then"] = ["ghost"]
        s[1]["then"] = ["ask-cto-os"]
        code, out, _ = check(make_repo(), s)
        self.assertEqual(code, 1)
        self.assertIn("unknown skill 'ghost'", out)
        self.assertIn("cannot point to ask-cto-os itself", out)

    def test_duplicate_id_few_signals_and_no_skill_no_read(self):
        s = self.good()
        s.append(situation("s1", start=None, read=[], signals=("only", "two")))
        code, out, _ = check(make_repo(), s)
        self.assertEqual(code, 1)
        self.assertIn("duplicate id", out)
        self.assertIn("at least 3 non-empty strings", out)
        self.assertIn("'read' must name at least one document", out)

    def test_gaps(self):
        code, out, _ = check(make_repo(), self.good(), gaps=[{"topic": "X", "closest": None},
                                                             {"topic": "Y", "closest": "nothing/here.md"}])
        self.assertEqual(code, 1)
        self.assertIn("Gap 'Y'", out)
        self.assertNotIn("Gap 'X'", out)

    def test_docs_page_must_match_render(self):
        root = make_repo()
        routes = os.path.join(root, "routes.json")
        with open(routes, "w") as fh:
            json.dump({"version": 1, "situations": self.good(), "gaps": []}, fh)
        code, out, _ = run("check", "--repo", root, "--routes", routes)
        self.assertEqual(code, 1)
        self.assertIn("docs/situations.md is missing", out)
        _, rendered, _ = run("render", "--routes", routes)
        with open(os.path.join(root, "docs", "situations.md"), "w") as fh:
            fh.write(rendered)
        code, out, _ = run("check", "--repo", root, "--routes", routes)
        self.assertEqual(code, 0, out)
        with open(os.path.join(root, "docs", "situations.md"), "a") as fh:
            fh.write("edited by hand\n")
        code, out, _ = run("check", "--repo", root, "--routes", routes)
        self.assertEqual(code, 1)
        self.assertIn("out of date", out)

    def test_bad_input(self):
        code, _, err = run("check", "--routes", "/nonexistent.json")
        self.assertEqual(code, 2)
        self.assertIn("File not found", err)


@unittest.skipUnless(os.path.isdir(os.path.join(REAL_REPO, "playbooks")), "not running inside the cto-os repository")
class RealRepo(unittest.TestCase):
    def test_every_artifact_is_reachable_and_docs_are_current(self):
        code, out, _ = run("check", "--repo", REAL_REPO)
        self.assertEqual(code, 0, out)


class Matching(unittest.TestCase):
    CASES = [
        ("I am starting as CTO next week and need a 30 60 90 plan", "new-role"),
        ("The CEO and I are not aligned on what the CEO expects", "ceo-alignment"),
        ("I have to give the CEO bad news about a deadline", "hard-conversation-ceo"),
        ("I have a board meeting next month and need a board update", "board"),
        ("Leadership asks about our AI strategy and how mature we are with copilot", "ai-maturity"),
        ("I need delivery metrics and want to know how fast do we ship", "measure-delivery"),
        ("I need to hire an engineer and write the job description", "hire"),
        ("The interviews are done and I need to decide on a candidate", "debrief"),
        ("We have no career ladder and titles are all over the place", "ladder"),
        ("Someone is up for promotion and it is calibration time", "promotion"),
        ("What level should this candidate be offered", "candidate-level"),
        ("Are my spans of control too wide, how many direct reports is too many", "org-shape"),
        ("We need an architecture decision record because the team keeps revisiting a choice", "record-decision"),
        ("I am not sure where to start, what is in this repo", "unsure"),
        ("We are having an incident and production is down, customers cannot check out", "incident-now"),
        ("We have no incident process and the same incident keeps coming back, who is incident commander", "incident-process"),
        ("I need to write a blameless postmortem and measure time to restore", "postmortem"),
    ]

    def test_each_phrase_routes_to_its_situation(self):
        for text, expected in self.CASES:
            code, out, _ = run("match", "--text", text, "--format", "json")
            self.assertEqual(code, 0)
            top = json.loads(out)[0]["id"]
            self.assertEqual(top, expected, f"{text!r} routed to {top}")

    def test_every_situation_has_a_regression_phrase(self):
        with open(REAL_ROUTES, encoding="utf-8") as fh:
            ids = {s["id"] for s in json.load(fh)["situations"]}
        self.assertEqual(ids, {e for _, e in self.CASES})

    def test_no_match(self):
        code, out, _ = run("match", "--text", "What is the weather in Lisbon")
        self.assertEqual(code, 0)
        self.assertIn("No situation matched", out)

    def test_scores_are_word_counts(self):
        code, out, _ = run("match", "--text", "I need to give bad news", "--format", "json")
        res = json.loads(out)
        self.assertEqual(res[0]["id"], "hard-conversation-ceo")
        self.assertEqual(res[0]["score"], 2)   # "bad news" is two words


if __name__ == "__main__":
    unittest.main(verbosity=2)
