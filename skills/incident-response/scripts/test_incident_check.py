"""Tests for incident_check.py. Expected values were worked out by hand from the fixtures.

Run:  python3 -I test_incident_check.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "incident_check.py")
EX = os.path.join(HERE, "examples")
GOOD = os.path.join(EX, "postmortem-example.md")
DRAFT = os.path.join(EX, "postmortem-draft.md")
INCIDENTS = os.path.join(EX, "incidents-example.csv")
ACTIONS = os.path.join(EX, "actions-example.csv")
TEMPLATE = os.path.join(HERE, "..", "..", "..", "templates", "postmortem.md")
AS_OF = "2026-11-22"


def run(*args):
    p = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write_tmp(text, suffix=".md"):
    fh = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    fh.write(text)
    fh.close()
    return fh.name


def pm(path, *extra):
    code, out, err = run("postmortem", "--file", path, "--format", "json", *extra)
    return code, json.loads(out) if out.strip() else None, err


def pm_text(text, *extra):
    return pm(write_tmp(text), *extra)


def codes(res, level=None):
    return sorted(f["code"] for f in res["findings"] if level is None or f["level"] == level)


class PostmortemCheck(unittest.TestCase):
    def test_example_passes_with_no_findings(self):
        code, res, _ = pm(GOOD)
        self.assertEqual(code, 0)
        self.assertEqual(res["findings"], [])
        self.assertEqual(res["severity"], "SEV2")
        self.assertEqual(res["actions"], 5)

    def test_example_measures(self):
        _, res, _ = pm(GOOD)
        self.assertEqual(res["measures"], {"to_detect": 85.0, "to_mitigate": 130.0, "to_resolve": 210.0})

    def test_draft_fails_in_the_documented_way(self):
        code, res, _ = pm(DRAFT)
        self.assertEqual(code, 1)
        self.assertEqual(codes(res, "FAIL"), ["action-due", "action-owner"])
        self.assertEqual(codes(res, "WARN"), ["action-done-when", "blame-phrase", "impact-no-number",
                                              "no-detect-action", "one-factor"])

    def test_blank_template_fails(self):
        code, res, _ = pm(TEMPLATE)
        self.assertEqual(code, 1)
        fails = codes(res, "FAIL")
        self.assertIn("severity", fails)
        self.assertIn("timestamp", fails)
        self.assertEqual(fails.count("empty-section"), 7)

    def test_markdown_report_has_result_line(self):
        code, out, _ = run("postmortem", "--file", GOOD)
        self.assertEqual(code, 0)
        self.assertIn("**Result: PASS** (0 failures, 0 warnings).", out)
        self.assertIn("Time to detect | 1 h 25 min", out)

    def test_times_going_backwards_fail(self):
        text = read(GOOD).replace("| Detected (UTC) | 2026-10-14 15:05 |", "| Detected (UTC) | 2026-10-14 13:00 |")
        code, res, _ = pm_text(text)
        self.assertEqual(code, 1)
        self.assertIn("time-order", codes(res, "FAIL"))
        self.assertEqual(res["measures"], {})

    def test_invalid_severity_and_detected_by_fail(self):
        text = read(GOOD).replace("| Severity | SEV2 |", "| Severity | high |").replace("| Detected by | customer |", "| Detected by | pager |")
        _, res, _ = pm_text(text)
        self.assertEqual(codes(res, "FAIL"), ["detected-by", "severity"])

    def test_missing_section_fails(self):
        text = read(GOOD).replace("## Where we got lucky", "## Luck")
        _, res, _ = pm_text(text)
        self.assertIn("missing-section", codes(res, "FAIL"))

    def test_action_due_before_incident_fails(self):
        text = read(GOOD).replace("| 2026-11-04 |", "| 2026-10-01 |")
        _, res, _ = pm_text(text)
        self.assertEqual(codes(res, "FAIL"), ["action-due"])

    def test_far_due_date_warns(self):
        text = read(GOOD).replace("| 2026-12-16 |", "| 2027-03-01 |")
        _, res, _ = pm_text(text)
        self.assertEqual(codes(res), ["action-far"])
        _, res, _ = pm_text(text, "--max-days", "200")
        self.assertEqual(codes(res), [])

    def test_too_many_actions_warns(self):
        _, res, _ = pm(GOOD, "--max-actions", "4")
        self.assertEqual(codes(res), ["too-many-actions"])

    def test_no_actions_fails_for_sev2_and_warns_for_sev3(self):
        text = read(GOOD)
        for r in text.splitlines():
            if r.startswith("| ") and r[2:3].isdigit() and r.rstrip().endswith(("| open |", "| done |")) and r.count("|") == 8:
                text = text.replace(r + "\n", "")
        _, res, _ = pm_text(text)
        self.assertIn("no-actions", codes(res, "FAIL"))
        _, res, _ = pm_text(text.replace("| Severity | SEV2 |", "| Severity | SEV3 |"))
        self.assertIn("no-actions", codes(res, "WARN"))
        self.assertNotIn("no-actions", codes(res, "FAIL"))

    def test_detect_action_not_needed_when_monitoring_found_it(self):
        text = read(GOOD).replace("| Detected by | customer |", "| Detected by | monitoring |").replace("| detect |", "| prevent |")
        _, res, _ = pm_text(text)
        self.assertEqual(codes(res), [])
        text = read(GOOD).replace("| detect |", "| prevent |")
        _, res, _ = pm_text(text)
        self.assertEqual(codes(res), ["no-detect-action"])

    def test_guidance_and_code_blocks_are_ignored(self):
        text = read(GOOD) + "\n> Do not write human error here.\n\n```\nhuman error careless\n```\n"
        _, res, _ = pm_text(text)
        self.assertEqual(codes(res), [])

    def test_blame_phrase_is_reported_with_its_line(self):
        text = read(GOOD).replace("Customers found it before we did.", "Customers found it before we did. It was careless.")
        _, res, _ = pm_text(text)
        hits = [f for f in res["findings"] if f["code"] == "blame-phrase"]
        self.assertEqual(len(hits), 1)
        self.assertIn("'careless'", hits[0]["message"])
        self.assertIn("Line 18:", hits[0]["message"])

    def test_time_only_rows_roll_over_midnight(self):
        text = read(GOOD)
        text = text.replace("2026-10-14 13:40 | Release 212", "2026-10-14 23:40 | Release 212")
        text = text.replace("| Impact started (UTC) | 2026-10-14 13:40 |", "| Impact started (UTC) | 2026-10-14 23:40 |")
        for old, new in (("15:05", "00:05"), ("15:50", "00:50"), ("17:10", "02:10")):
            text = text.replace(f"2026-10-14 {old}", f"2026-10-15 {old.replace(old, new)}")
        for old, new in (("| 14:10 |", "| 23:50 |"), ("| 15:05 |", "| 00:05 |"), ("| 15:08 |", "| 00:08 |"),
                         ("| 15:20 |", "| 00:20 |"), ("| 15:30 |", "| 00:30 |"), ("| 15:35 |", "| 00:35 |"),
                         ("| 15:50 |", "| 00:50 |"), ("| 15:55 |", "| 00:55 |"), ("| 17:10 |", "| 02:10 |")):
            text = text.replace(old, new)
        _, res, _ = pm_text(text)
        self.assertNotIn("timeline-order", codes(res))
        self.assertNotIn("timeline-time", codes(res))

    def test_out_of_order_timeline_warns(self):
        text = read(GOOD).replace("| 14:10 |", "| 2026-10-14 12:10 |")
        _, res, _ = pm_text(text)
        self.assertIn("timeline-order", codes(res, "WARN"))

    def test_time_only_row_that_wraps_past_resolution_warns(self):
        text = read(GOOD).replace("| 14:10 |", "| 12:10 |")
        _, res, _ = pm_text(text)
        self.assertIn("timeline-order", codes(res, "WARN"))

    def test_unreadable_timeline_time_fails(self):
        text = read(GOOD).replace("| 14:10 |", "| after lunch |")
        _, res, _ = pm_text(text)
        self.assertIn("timeline-time", codes(res, "FAIL"))

    def test_short_timeline_warns(self):
        _, res, _ = pm(GOOD, "--min-timeline", "20")
        self.assertEqual(codes(res), ["short-timeline"])

    def test_missing_file_exits_2(self):
        code, _, err = run("postmortem", "--file", "/no/such/file.md")
        self.assertEqual(code, 2)
        self.assertIn("File not found", err)

    def test_deterministic(self):
        a = run("postmortem", "--file", DRAFT)[1]
        b = run("postmortem", "--file", DRAFT)[1]
        self.assertEqual(a, b)


def summary(*extra, actions=True, incidents=INCIDENTS):
    args = ["summary", "--incidents", incidents, "--as-of", AS_OF, "--format", "json"]
    if actions:
        args += ["--actions", ACTIONS]
    code, out, err = run(*args, *extra)
    return code, json.loads(out) if out.strip() else None, err


class Summary(unittest.TestCase):
    def test_counts_and_medians(self):
        code, s, _ = summary()
        self.assertEqual(code, 0)
        self.assertEqual(s["incidents"], 8)
        counts = {r["severity"]: r["n"] for r in s["by_severity"]}
        self.assertEqual(counts, {"SEV1": 1, "SEV2": 3, "SEV3": 3, "SEV4": 1})
        self.assertEqual(s["overall"]["detect"], {"median": 19.0, "longest": 85.0})
        self.assertEqual(s["overall"]["mitigate"], {"median": 55.0, "longest": 130.0})
        self.assertEqual(s["overall"]["resolve"], {"median": 125.0, "longest": 210.0})
        sev2 = [r for r in s["by_severity"] if r["severity"] == "SEV2"][0]
        self.assertEqual(sev2["detect"], {"median": 18.0, "longest": 85.0})
        self.assertEqual(sev2["resolve"], {"median": 165.0, "longest": 210.0})

    def test_found_by_and_repeat_factors(self):
        _, s, _ = summary()
        self.assertEqual(s["found_by"], {"monitoring": 5, "customer": 2, "employee": 1})
        self.assertEqual(s["repeat_factors"], [["missing-alert", 3], ["bad-deploy", 2], ["capacity", 2], ["no-rollback-plan", 2]])

    def test_postmortem_coverage(self):
        _, s, _ = summary()
        self.assertEqual(s["postmortems"], {"owed": 4, "published": 3, "on_time": 2,
                                            "overdue_ids": ["INC-0414"], "target_days": 7})

    def test_pm_days_flag(self):
        _, s, _ = summary("--pm-days", "10")
        self.assertEqual(s["postmortems"]["on_time"], 3)

    def test_actions(self):
        _, s, _ = summary()
        self.assertEqual(s["actions"], {"total": 10, "done": 6, "open": 4, "overdue": 2, "oldest_overdue_days": 20})

    def test_actions_are_optional(self):
        _, s, _ = summary(actions=False)
        self.assertNotIn("actions", s)

    def test_since_filter(self):
        _, s, _ = summary("--since", "2026-10-01", actions=False)
        self.assertEqual(s["incidents"], 3)
        _, s, _ = summary("--until", "2026-08-31", actions=False)
        self.assertEqual(s["incidents"], 3)

    def test_markdown_output(self):
        code, out, _ = run("summary", "--incidents", INCIDENTS, "--actions", ACTIONS, "--as-of", AS_OF)
        self.assertEqual(code, 0)
        self.assertIn("**8 incidents**, as of 2026-11-22.", out)
        self.assertIn("- Found by customers: 2 of 8 (25%)", out)
        self.assertIn("- Overdue and unpublished: INC-0414", out)

    def test_backwards_times_exit_2(self):
        text = read(INCIDENTS).replace("2026-07-08 09:40", "2026-07-08 08:00")
        code, _, err = run("summary", "--incidents", write_tmp(text, ".csv"), "--as-of", AS_OF)
        self.assertEqual(code, 2)
        self.assertIn("Row 2", err)

    def test_incident_after_as_of_exits_2(self):
        code, _, err = run("summary", "--incidents", INCIDENTS, "--as-of", "2026-07-01")
        self.assertEqual(code, 2)
        self.assertIn("after --as-of", err)

    def test_unknown_incident_in_actions_exits_2(self):
        bad = write_tmp("incident_id,due,status\nINC-9999,2026-12-01,open\n", ".csv")
        code, _, err = run("summary", "--incidents", INCIDENTS, "--actions", bad, "--as-of", AS_OF)
        self.assertEqual(code, 2)
        self.assertIn("INC-9999", err)

    def test_missing_column_exits_2(self):
        bad = write_tmp("id,severity\nINC-1,SEV1\n", ".csv")
        code, _, err = run("summary", "--incidents", bad, "--as-of", AS_OF)
        self.assertEqual(code, 2)
        self.assertIn("needs a", err)

    def test_default_owed_is_sev1_and_sev2(self):
        text = "id,severity,started,detected,mitigated,resolved,detected_by\n" \
               "A,SEV1,2026-11-01 10:00,2026-11-01 10:05,2026-11-01 10:30,2026-11-01 11:00,monitoring\n" \
               "B,SEV3,2026-11-02 10:00,2026-11-02 10:05,2026-11-02 10:30,2026-11-02 11:00,monitoring\n"
        code, out, _ = run("summary", "--incidents", write_tmp(text, ".csv"), "--as-of", AS_OF, "--format", "json")
        s = json.loads(out)
        self.assertEqual(s["postmortems"]["owed"], 1)
        self.assertEqual(s["postmortems"]["overdue_ids"], ["A"])


if __name__ == "__main__":
    unittest.main()
