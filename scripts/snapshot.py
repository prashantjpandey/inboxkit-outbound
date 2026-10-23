"""Fetch each company's homepage title, description and outbound keywords.

Feeds the qualify skill (is this really an agency?) and the 'sells_infra' tag.
Usage: python scripts/snapshot.py data/companies.csv [--offline]
"""
import argparse
import html
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from lib import log, read_csv, write_csv

KEYWORDS = ["cold email", "outbound", "lead generation", "appointment setting", "sdr", "pipeline", "deliverability"]
INFRA = ["done-for-you inbox", "done for you inbox", "domains and inboxes", "mailbox setup", "inbox setup",
         "email infrastructure", "we set up your domains", "sending infrastructure", "domains & inboxes"]


def fetch(domain):
    """Try the bare domain, then www. (many small agency sites only serve one of them)."""
    last = None
    for url in (f"https://{domain}", f"https://www.{domain}", f"http://www.{domain}"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (outbound-research)"})
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.read(400_000).decode("utf-8", "ignore")
        except Exception as e:
            last = e
    raise last


RETRY_FAILED = False


def snapshot(row):
    failed = row.get("site_title", "").startswith("ERROR")
    if (row.get("site_title") and not (failed and RETRY_FAILED)) or not row.get("domain"):
        return row  # already captured (sample data or a previous run); --retry-failed re-fetches errors
    try:
        page = fetch(row["domain"])
    except Exception as e:
        row["site_title"] = f"ERROR: {type(e).__name__}"
        return row
    title = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', page, re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", page)).lower()
    row["site_title"] = html.unescape(title.group(1).strip())[:150] if title else ""
    row["site_description"] = html.unescape(desc.group(1).strip())[:250] if desc else ""
    row["site_keywords"] = ";".join(k for k in KEYWORDS if k in text)
    row["sells_infra"] = "yes" if any(k in text for k in INFRA) else "no"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("companies")
    ap.add_argument("--offline", action="store_true", help="skip network, keep existing snapshot fields")
    ap.add_argument("--retry-failed", action="store_true", help="re-fetch sites that errored on a previous run")
    a = ap.parse_args()
    global RETRY_FAILED
    RETRY_FAILED = a.retry_failed
    rows = read_csv(a.companies)
    if not a.offline:
        with ThreadPoolExecutor(12) as ex:
            rows = list(ex.map(snapshot, rows))
    errors = sum(r.get("site_title", "").startswith("ERROR") for r in rows)
    write_csv(a.companies, rows)
    log("snapshot", f"{len(rows)} companies, {errors} sites unreachable, "
                    f"{sum(r.get('sells_infra') == 'yes' for r in rows)} mention selling infrastructure")


if __name__ == "__main__":
    main()
