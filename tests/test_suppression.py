"""Suppression name matching: catch real customers, never block look-alike names.

Run: python -m unittest discover tests
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from suppress import Suppression  # noqa: E402


class Matching(unittest.TestCase):
    sup = Suppression(ROOT / "config" / "suppression.csv")

    def test_partner_with_longer_name_is_suppressed(self):
        self.assertEqual(self.sup.company("Hypergen - B2B Cold-Email", "hypergen.io"), "customer")

    def test_competitor_is_suppressed(self):
        self.assertEqual(self.sup.company("Mission Inbox", "missioninbox.com"), "competitor")

    def test_own_group_domain_is_suppressed(self):
        self.assertEqual(self.sup.company("Anything", "https://www.enrich.so/pricing"), "competitor")

    def test_lookalike_names_are_not_suppressed(self):
        self.assertIsNone(self.sup.company("Expand In Asia", "expandin.asia"))   # vs Expandi
        self.assertIsNone(self.sup.company("INBOX Agency", "inboxagency.com"))   # vs InboxNavigator / InboxKit
        self.assertIsNone(self.sup.company("Growth Co", "growthcomarketing.com"))


if __name__ == "__main__":
    unittest.main()
