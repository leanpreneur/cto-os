"""Tests for org_shape.py. Expected values were worked out by hand from examples/roster-example.csv.

Run:  python3 -I test_org_shape.py
"""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "org_shape.py")
ROSTER = os.path.join(HERE, "examples", "roster-example.csv")
AS_OF = "2026-11-22"


def run(*args):
    p = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def read_rows():
    with open(ROSTER, newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))


def write_rows(rows):
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    csv.writer(fh).writerows(rows)
    fh.close()
    return fh.name


def analyze(*extra):
    code, out, err = run("--roster", ROSTER, "--as-of", AS_OF, "--format", "json", *extra)
    assert code == 0, err
    return json.loads(out)


class Shape(unittest.TestCase):
    def test_headcount_layers_spans(self):
        d = analyze()
        self.assertEqual(d["headcount"], 29)
        self.assertEqual(d["ic_track"], 23)
        self.assertEqual(d["manager_track"], 6)
        self.assertEqual(d["layers"], 4)                      # cto, dir, managers, ICs
        self.assertEqual(d["managers_with_reports"], 6)
        self.assertEqual(d["span"]["min"], 1)
        self.assertEqual(d["span"]["median"], 4.5)            # spans 1,1,4,5,6,11
        self.assertEqual(d["span"]["max"], 11)
        self.assertEqual(d["span"]["thin_count"], 2)          # cto (1) and mgrC (1)
        self.assertEqual(d["span"]["wide_count"], 1)          # mgrD (11)
        self.assertEqual(d["ics_per_manager"], 3.83)          # 23 / 6

    def test_levels_and_time_in_level(self):
        d = analyze()
        lv = {l["level"]: l for l in d["levels"]}
        self.assertEqual(sorted(lv), ["E2", "E3"])            # all other levels have fewer than 5 people
        self.assertEqual(lv["E2"]["count"], 16)
        self.assertEqual(lv["E2"]["median_months_in_level"], 18.0)   # 549 days / 30.4375
        self.assertEqual(lv["E3"]["count"], 5)
        self.assertEqual(lv["E3"]["median_months_in_level"], 24.0)   # 730 days / 30.4375
        self.assertEqual(lv["E3"]["over_stale_share"], 20.0)         # one of five, 1461 days = 48 months
        self.assertEqual(lv["E2"]["over_stale_share"], 0.0)

    def test_small_groups_are_combined_and_not_broken_out(self):
        d = analyze()
        self.assertEqual(d["levels_under_min_cell"]["count"], 8)     # E1 1, E4 1, M4 1, M3 1, M1 4
        text = json.dumps(d)
        for hidden in ('"E1"', '"E4"', '"M1"', '"M3"', '"M4"'):
            self.assertNotIn(hidden, text)

    def test_ids_are_off_by_default(self):
        self.assertNotIn("ids", analyze())
        ids = analyze("--show-ids")["ids"]
        self.assertEqual(ids["thin_span"], ["cto", "mgrC"])
        self.assertEqual(ids["wide_span"], ["mgrD"])

    def test_thresholds_can_change(self):
        d = analyze("--max-span", "5")
        self.assertEqual(d["span"]["wide_count"], 2)                 # mgrA (6) and mgrD (11)

    def test_track_mismatch(self):
        rows = read_rows()
        for r in rows:
            if r[0] == "mgrC":
                r[2] = "IC"
            if r[0] == "a1":
                r[2] = "M"
        path = write_rows(rows)
        code, out, _ = run("--roster", path, "--as-of", AS_OF, "--format", "json")
        d = json.loads(out)
        self.assertEqual(d["track_mismatch"], {"manager_track_without_reports": 1, "ic_track_with_reports": 1})
        os.unlink(path)

    def test_markdown_report(self):
        code, out, _ = run("--roster", ROSTER, "--as-of", AS_OF)
        self.assertEqual(code, 0)
        self.assertIn("**Headcount:** 29 (23 on the IC track, 6 on the manager track)", out)
        self.assertIn("It is not anonymization.", out)


class BadInput(unittest.TestCase):
    def check(self, rows, text):
        path = write_rows(rows)
        code, _, err = run("--roster", path, "--as-of", AS_OF)
        os.unlink(path)
        self.assertEqual(code, 2)
        self.assertIn(text, err)

    def test_loop(self):
        self.check([["id", "level", "track", "manager_id"], ["a", "E2", "IC", "b"], ["b", "E2", "IC", "a"]], "loop")

    def test_duplicate_id(self):
        self.check([["id", "level", "track", "manager_id"], ["a", "E2", "IC", ""], ["a", "E3", "IC", ""]], "duplicate id")

    def test_bad_track(self):
        self.check([["id", "level", "track", "manager_id"], ["a", "E2", "XX", ""]], "'track' must be IC or M")

    def test_bad_date(self):
        self.check([["id", "level", "track", "manager_id", "start_date"], ["a", "E2", "IC", "", "2024-13-45"]], "YYYY-MM-DD")

    def test_missing_column(self):
        self.check([["id", "level", "track"], ["a", "E2", "IC"]], "'manager_id' column")

    def test_future_date(self):
        self.check([["id", "level", "track", "manager_id", "start_date"], ["a", "E2", "IC", "", "2030-01-01"]], "after the --as-of")


if __name__ == "__main__":
    unittest.main(verbosity=2)
