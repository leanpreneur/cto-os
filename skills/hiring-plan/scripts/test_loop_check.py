"""Tests for loop_check.py. Expected values were worked out by hand from the fixtures.

Run:  python3 -I test_loop_check.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "loop_check.py")
GOOD_PLAN = os.path.join(HERE, "examples", "loop-example.json")
FEEDBACK = os.path.join(HERE, "examples", "feedback-example.json")


def run(*args):
    p = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(obj):
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(obj, fh)
    fh.close()
    return fh.name


class Coverage(unittest.TestCase):
    def test_good_plan_passes_with_no_findings(self):
        code, out, _ = run("coverage", "--plan", GOOD_PLAN, "--format", "json")
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data["findings"], [])
        self.assertEqual(data["candidate_minutes"], 300)
        # interviewer counts worked out by hand
        self.assertEqual(data["coverage"]["judgment"], ["engineer-a", "engineer-b"])
        self.assertEqual(data["coverage"]["ai"], ["engineer-a", "hiring-manager"])
        self.assertEqual(data["coverage"]["collab"], ["engineer-c", "hiring-manager", "product-partner"])

    def test_flawed_plan_reports_known_findings(self):
        plan = {
            "role": "X", "level": "E3",
            "competencies": [
                {"id": "judgment", "name": "Judgment", "must": True},
                {"id": "design", "name": "Design", "must": True},
                {"id": "ai", "name": "AI", "must": True},
            ],
            "interviews": [
                {"id": "a", "minutes": 90, "interviewer": "eng-a", "type": "work_sample",
                 "competencies": ["judgment", "design", "ai", "delivery_typo"]},
                {"id": "b", "minutes": 60, "interviewer": "eng-a", "competencies": ["judgment"]},
                {"id": "c", "minutes": 200, "interviewer": "eng-a", "competencies": ["design"]},
            ],
        }
        path = write_json(plan)
        code, out, _ = run("coverage", "--plan", path, "--format", "json")
        data = json.loads(out)
        self.assertEqual(code, 1)
        codes = sorted(f["code"] for f in data["findings"])
        fails = sorted(f["code"] for f in data["findings"] if f["level"] == "FAIL")
        warns = sorted(f["code"] for f in data["findings"] if f["level"] == "WARN")
        self.assertEqual(fails, ["no-decision-owner", "thin-coverage", "thin-coverage", "thin-coverage",
                                 "unknown-competency"])
        self.assertEqual(warns, ["candidate-time", "competency-count", "interviewer-load",
                                 "no-ai-policy", "no-debrief", "too-many-competencies"])
        self.assertEqual(len(codes), 11)
        os.unlink(path)

    def test_same_interviewer_twice_is_not_two_signals(self):
        plan = load(GOOD_PLAN)
        for iv in plan["interviews"]:
            if iv["id"] == "design":
                iv["interviewer"] = "engineer-a"   # judgment now has only engineer-a
        for iv in plan["interviews"]:
            if iv["id"] == "manager":
                iv["interviewer"] = "engineer-a"
        path = write_json(plan)
        code, out, _ = run("coverage", "--plan", path, "--format", "json")
        data = json.loads(out)
        self.assertEqual(code, 1)
        msgs = " ".join(f["message"] for f in data["findings"] if f["code"] == "thin-coverage")
        self.assertIn("Technical judgment", msgs)
        os.unlink(path)

    def test_markdown_has_matrix_and_result(self):
        code, out, _ = run("coverage", "--plan", GOOD_PLAN)
        self.assertEqual(code, 0)
        self.assertIn("**Result: PASS**", out)
        self.assertIn("| Technical judgment* |", out)

    def test_bad_input(self):
        code, _, err = run("coverage", "--plan", "/nonexistent.json")
        self.assertEqual(code, 2)
        self.assertIn("File not found", err)


class Debrief(unittest.TestCase):
    def setUp(self):
        code, out, _ = run("debrief", "--feedback", FEEDBACK, "--plan", GOOD_PLAN, "--format", "json")
        self.assertEqual(code, 0)
        self.data = json.loads(out)
        self.rows = {r["id"]: r for r in self.data["rows"]}

    def test_means_and_spread(self):
        self.assertEqual(self.rows["judgment"]["mean"], 3.0)
        self.assertEqual(self.rows["design"]["mean"], 3.0)
        self.assertEqual(self.rows["design"]["spread"], 2)
        self.assertEqual(self.rows["ai"]["mean"], 4.0)   # only the score with evidence counts

    def test_flags(self):
        self.assertEqual(self.rows["judgment"]["flags"], [])
        self.assertEqual(self.rows["delivery"]["flags"], [])
        self.assertEqual(self.rows["design"]["flags"], ["DISCUSS: scores differ by 2"])
        self.assertEqual(self.rows["ai"]["flags"],
                         ["NO EVIDENCE: hiring-manager", "INSUFFICIENT: fewer than 2 interviewers with evidence"])

    def test_signal_and_tally(self):
        self.assertEqual(self.data["signal"], "Not established on: Engineering with AI.")
        self.assertEqual(self.data["recommendations"], {"hire": 4, "hire_other_level": 0, "no_hire": 1})
        self.assertIn("Feedback not marked as submitted before the debrief: hiring-manager.", self.data["process"])

    def test_below_bar_and_score_of_one(self):
        fb = load(FEEDBACK)
        for item in fb["feedback"]:
            if item["interviewer"] == "engineer-b":
                item["scores"]["judgment"] = 1
                item["evidence"]["judgment"] = "Picked the newest framework with no reason"
        path = write_json(fb)
        code, out, _ = run("debrief", "--feedback", path, "--plan", GOOD_PLAN, "--format", "json")
        rows = {r["id"]: r for r in json.loads(out)["rows"]}
        self.assertEqual(rows["judgment"]["mean"], 2.0)
        self.assertIn("BELOW BAR", rows["judgment"]["flags"])
        self.assertIn("DISCUSS: scores differ by 2", rows["judgment"]["flags"])
        os.unlink(path)

    def test_invalid_score_is_rejected(self):
        fb = load(FEEDBACK)
        fb["feedback"][0]["scores"]["judgment"] = 5
        path = write_json(fb)
        code, _, err = run("debrief", "--feedback", path)
        self.assertEqual(code, 2)
        self.assertIn("1 to 4", err)
        os.unlink(path)

    def test_without_plan_every_competency_is_must(self):
        code, out, _ = run("debrief", "--feedback", FEEDBACK, "--format", "json")
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertTrue(all(r["must"] for r in data["rows"]))

    def test_markdown_shows_evidence_behind_gap(self):
        code, out, _ = run("debrief", "--feedback", FEEDBACK, "--plan", GOOD_PLAN)
        self.assertIn("## Evidence behind the gaps", out)
        self.assertIn("Drew the happy path only", out)
        self.assertIn("This is a summary. The decision owner decides.", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
