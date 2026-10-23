"""Check SPF, DMARC and MX on each company's main domain. Free, public DNS only.

Adds: mx_provider (google / microsoft / other / none), dns_gaps (semicolon list), dns_angle.
Usage: python scripts/dns_check.py data/companies.csv [--fixture sample/dns_fixture.json]
"""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from lib import doh, log, read_csv, write_csv
from suppress import dropped_log

HARD_GAPS = {"no_dmarc", "no_spf", "multiple_spf", "spf_plus_all"}


def check(domain):
    txt = doh(domain, "TXT")
    spf = [t for t in txt if t.lower().startswith("v=spf1")]
    dmarc = [t for t in doh(f"_dmarc.{domain}", "TXT") if t.lower().startswith("v=dmarc1")]
    mx = " ".join(doh(domain, "MX")).lower()
    provider = "google" if "google" in mx else "microsoft" if "outlook" in mx else "other" if mx else "none"
    gaps = []
    if not spf:
        gaps.append("no_spf")
    elif len(spf) > 1:
        gaps.append("multiple_spf")
    elif spf[0].rstrip().endswith("+all"):
        gaps.append("spf_plus_all")
    if not dmarc:
        gaps.append("no_dmarc")
    else:
        tags = dict(kv.strip().split("=", 1) for kv in dmarc[0].split(";") if "=" in kv)
        if tags.get("p", "").strip().lower() == "none":
            gaps.append("dmarc_p_none")
    return {"mx_provider": provider, "dns_gaps": ";".join(gaps)}


def angle(gaps):
    g = set(filter(None, gaps.split(";")))
    if g & HARD_GAPS:
        return "domain_gap"
    if "dmarc_p_none" in g:
        return "dmarc_none"
    return "hiring"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("companies")
    ap.add_argument("--fixture", help="JSON {domain: {mx_provider, dns_gaps}} for offline runs")
    a = ap.parse_args()
    rows = read_csv(a.companies)
    fixture = json.load(open(a.fixture, encoding="utf-8")) if a.fixture else None

    def one(row):
        d = row.get("domain", "")
        try:
            res = fixture[d] if fixture is not None else check(d)
        except Exception as e:
            res = {"mx_provider": "error", "dns_gaps": ""}
            log("dns", f"{d}: {type(e).__name__}")
        row.update(res)
        row["dns_angle"] = angle(row["dns_gaps"])
        return row

    with ThreadPoolExecutor(10) as ex:
        rows = list(ex.map(one, rows))
    # Every company needs a reason to write now: an open outbound role or a gap on its domain
    no_signal = [r for r in rows if not r.get("hiring_for") and not r["dns_gaps"]]
    rows = [r for r in rows if r not in no_signal]
    dropped_log(Path(a.companies).parent, [{"stage": "signal", "record": f"{r.get('name')} ({r.get('domain')})",
                                            "reason": "no_signal", "detail": "not hiring, no domain gap"}
                                           for r in no_signal])
    write_csv(a.companies, rows)
    count = {k: sum(r["dns_angle"] == k for r in rows) for k in ("domain_gap", "dmarc_none", "hiring")}
    log("dns", f"{len(rows)} domains checked: {count}")


if __name__ == "__main__":
    main()
