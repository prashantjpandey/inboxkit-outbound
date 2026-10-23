"""End-to-end check on the planted sample data: every bad record must be caught for the right reason.

Run: python -m unittest discover tests
"""
import csv
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "output" / "sample_run"


def rows(name):
    with open(RUN / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class SampleRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "run.py"), "sample"], cwd=ROOT, check=True,
                       capture_output=True)

    def test_every_planted_problem_is_caught(self):
        reasons = Counter(r["reason"] for r in rows("dropped.csv"))
        self.assertEqual(reasons, Counter({
            "duplicate_company": 1, "duplicate_person": 2, "invalid_bad_syntax": 1, "invalid_no_mx": 1,
            "not_qualified": 1, "suppressed_competitor": 1, "suppressed_customer": 2,
            "suppressed_do_not_contact": 1, "suppressed_in_conversation": 1}))

    def test_import_file_only_has_valid_unique_unsuppressed_emails(self):
        emails = [r["email"] for r in rows("sequencer_import.csv")]
        self.assertEqual(sorted(emails), ["dana@acmeoutbound.example", "maria@meridianappts.example"])

    def test_risky_emails_are_held_not_sent(self):
        held = {r["email"] for r in rows("leads.csv") if r["action"] == "hold"}
        self.assertEqual(held, {"lee@signalleads.example", "info@meridianappts.example", "omar@signalleads.example"})

    def test_first_lines_use_the_strongest_signal(self):
        angle = {r["email"]: r["angle"] for r in rows("leads.csv")}
        self.assertEqual(angle["dana@acmeoutbound.example"], "domain_gap")
        self.assertEqual(angle["lee@signalleads.example"], "hiring")


if __name__ == "__main__":
    unittest.main()
