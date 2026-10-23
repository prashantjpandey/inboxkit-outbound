"""Remove suppressed and duplicate records. Every removal is logged to <workdir>/dropped.csv with a reason.

  companies: drop non-qualified, suppressed (domain or company name), duplicate domains/names.
  people:    drop suppressed emails/domains/companies, duplicate emails, LinkedIn URLs and names.

Usage:
  python scripts/suppress.py companies data/companies.csv data/companies_clean.csv
  python scripts/suppress.py people data/people_enriched.csv data/people_clean.csv
"""
import argparse
from pathlib import Path

from lib import ROOT, company_tokens, log, norm_company, norm_domain, read_csv, write_csv


class Suppression:
    def __init__(self, *paths):
        rows = [r for p in paths for r in read_csv(p)]
        self.domains = {norm_domain(r["domain"]): r["reason"] for r in rows if r["domain"]}
        self.emails = {r["email"].strip().lower(): r["reason"] for r in rows if r.get("email")}
        self.names = [(company_tokens(r["company"]), r["reason"]) for r in rows if r["company"]]

    def company(self, name, domain):
        """Return the suppression reason for a company, or None.

        Names match on whole words from the start: 'Hypergen' suppresses 'Hypergen - B2B Cold-Email',
        but 'Expandi' does not suppress 'Expand In Asia' and 'InboxNavigator' does not suppress 'INBOX Agency'.
        """
        d = norm_domain(domain)
        if d in self.domains:
            return self.domains[d]
        tokens = company_tokens(name)
        if not tokens:
            return None
        for s, reason in self.names:
            if s and tokens[:len(s)] == s:
                return reason
        return None


def dropped_log(workdir, entries):
    path = Path(workdir) / "dropped.csv"
    old = read_csv(path) if path.exists() else []
    write_csv(path, old + entries, ["stage", "record", "reason", "detail"])


def companies(rows, sup):
    keep, drop, seen = [], [], set()
    for r in rows:
        label = f"{r.get('name')} ({r.get('domain')})"
        reason = sup.company(r.get("name"), r.get("domain"))
        if reason:  # checked first so customers and competitors are always logged as such
            drop.append({"stage": "companies", "record": label, "reason": f"suppressed_{reason}", "detail": ""})
            continue
        if r.get("qualified") and r["qualified"] != "yes":
            drop.append({"stage": "companies", "record": label, "reason": "not_qualified",
                         "detail": r.get("qualify_reason", r["qualified"])})
            continue
        keys = {("d", norm_domain(r.get("domain"))), ("n", norm_company(r.get("name")))} - {("d", ""), ("n", "")}
        if keys & seen:
            drop.append({"stage": "companies", "record": label, "reason": "duplicate_company", "detail": ""})
            continue
        seen |= keys
        keep.append(r)
    return keep, drop


def people(rows, sup, qualified_domains=None):
    keep, drop, seen = [], [], set()
    for r in rows:
        email = (r.get("email") or "").strip().lower()
        label = f"{r.get('first_name')} {r.get('last_name')} <{email}>"
        reason = sup.emails.get(email) or sup.domains.get(email.split("@")[-1]) if email else None
        reason = reason or sup.company(r.get("company"), r.get("domain"))
        if reason:  # checked first so customers and competitors are always logged as such
            drop.append({"stage": "people", "record": label, "reason": f"suppressed_{reason}", "detail": r.get("company", "")})
            continue
        if qualified_domains is not None and norm_domain(r.get("domain")) not in qualified_domains:
            # the company was re-checked after enrichment and no longer qualifies (e.g. turned out phone-only)
            drop.append({"stage": "people", "record": label, "reason": "company_no_longer_qualified",
                         "detail": r.get("company", "")})
            continue
        name_key = ("p", norm_company(f"{r.get('first_name')}{r.get('last_name')}{r.get('company')}"))
        keys = {name_key}
        if email:
            keys.add(("e", email))
        if r.get("linkedin_url"):
            keys.add(("l", r["linkedin_url"].rstrip("/").lower().split("?")[0]))
        if keys & seen:
            drop.append({"stage": "people", "record": label, "reason": "duplicate_person", "detail": ""})
            continue
        seen |= keys
        keep.append(r)
    return keep, drop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["companies", "people"])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--suppression", default=str(ROOT / "config" / "suppression.csv"))
    ap.add_argument("--extra-suppression", action="append", default=[],
                    help="more suppression files, e.g. a CRM export of open deals or a do-not-contact list")
    ap.add_argument("--companies", help="people only: drop anyone whose company is not in this qualified companies file")
    a = ap.parse_args()
    sup = Suppression(a.suppression, *a.extra_suppression)
    rows = read_csv(a.src)
    if a.kind == "companies":
        keep, drop = companies(rows, sup)
    else:
        qualified = {norm_domain(c["domain"]) for c in read_csv(a.companies)} if a.companies else None
        keep, drop = people(rows, sup, qualified)
    write_csv(a.dst, keep)
    dropped_log(Path(a.dst).parent, drop)
    reasons = {}
    for d in drop:
        reasons[d["reason"]] = reasons.get(d["reason"], 0) + 1
    log(f"suppress:{a.kind}", f"{len(rows)} in, {len(keep)} kept, dropped {reasons or 'none'}")


if __name__ == "__main__":
    main()
