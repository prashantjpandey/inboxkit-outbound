"""Merge qualify decisions (written by Claude following skills/qualify.md) into a companies file.

Decisions file columns: domain, qualified (yes/no/unsure), qualify_reason. Companies not listed are 'unsure'.
Usage: python scripts/apply_qualify.py data/qualify_decisions.csv data/companies.csv
"""
import sys
from collections import Counter

from lib import log, norm_domain, read_csv, write_csv


def main(decisions_path, companies_path):
    decisions = {norm_domain(d["domain"]): d for d in read_csv(decisions_path)}
    rows = read_csv(companies_path)
    for r in rows:
        d = decisions.get(norm_domain(r["domain"]))
        r["qualified"] = d["qualified"] if d else "unsure"
        r["qualify_reason"] = d["qualify_reason"] if d else "not reviewed"
    write_csv(companies_path, rows)
    log("qualify", f"{len(rows)} companies: {dict(Counter(r['qualified'] for r in rows))}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
