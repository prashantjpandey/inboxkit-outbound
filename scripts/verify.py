"""Grade every email before it can reach a sequencer.

  valid   -> send   (syntax ok, domain has MX, source says verified, not catch-all, company domain)
  risky   -> hold   (role or free-mail address, unverified by the source, catch-all domain,
                     or an email domain that differs from the company's)
  invalid -> drop   (no email, bad syntax, or the domain cannot receive mail)

Only 'send' rows are exported for import. That is how the list stays under a 3% bounce rate.
Production upgrade: run 'risky' rows through a paid verifier (BounceBan) instead of holding them.

Usage: python scripts/verify.py data/people_clean.csv data/people_verified.csv [--mx-fixture sample/mx_fixture.json]
"""
import argparse
import json
import re
from pathlib import Path

from lib import doh, log, norm_domain, read_csv, write_csv
from suppress import dropped_log

EMAIL_RE = re.compile(r"^[a-z0-9._%+'-]+@[a-z0-9.-]+\.[a-z]{2,}$")
ROLE = {"info", "sales", "hello", "contact", "admin", "support", "team", "office", "hi", "marketing"}
FREE = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com", "proton.me", "protonmail.com"}
SOURCE_OK = {"verified"}


def grade(row, has_mx):
    email = (row.get("email") or "").strip().lower()
    if not email:
        return "invalid", "no_email"
    if not EMAIL_RE.match(email):
        return "invalid", "bad_syntax"
    local, domain = email.split("@")
    if not has_mx(domain):
        return "invalid", "no_mx"
    if local in ROLE:
        return "risky", "role_address"
    if domain in FREE:
        return "risky", "free_mail"
    if (row.get("email_status") or "").lower() not in SOURCE_OK:
        return "risky", f"source_status_{row.get('email_status') or 'blank'}".replace(" ", "_")
    if row.get("email_catchall") == "yes":
        return "risky", "catch_all_domain"  # the server accepts any address, so 'verified' proves little
    company = norm_domain(row.get("domain"))
    if company and domain != company and not domain.endswith("." + company):
        return "risky", "email_domain_differs_from_company"  # often an old job or a mismatched record
    return "valid", "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--mx-fixture", help="JSON {domain: true/false} for offline runs")
    a = ap.parse_args()
    fixture = json.load(open(a.mx_fixture, encoding="utf-8")) if a.mx_fixture else None
    cache = {}

    def has_mx(domain):
        if fixture is not None:
            return fixture.get(domain, True)
        if domain not in cache:
            try:
                cache[domain] = bool(doh(domain, "MX"))
            except Exception:
                cache[domain] = True  # network error: do not drop, the source status still applies
        return cache[domain]

    rows, drop = read_csv(a.src), []
    for r in rows:
        status, why = grade(r, has_mx)
        r["verification_status"], r["verification_detail"] = status, why
        r["action"] = {"valid": "send", "risky": "hold", "invalid": "drop"}[status]
        if status == "invalid":
            drop.append({"stage": "verify", "record": f"{r.get('first_name')} {r.get('last_name')} <{r.get('email')}>",
                         "reason": f"invalid_{why}", "detail": r.get("company", "")})
    # Every graded row is kept in the file (the lead sheet shows the status); 'action' decides what is exported.
    write_csv(a.dst, rows)
    dropped_log(Path(a.dst).parent, drop)
    counts = {s: sum(r["verification_status"] == s for r in rows) for s in ("valid", "risky", "invalid")}
    log("verify", f"{len(rows)} emails: {counts}")


if __name__ == "__main__":
    main()
