"""Write the lead sheet, the sequencer import file and a run report.

  <out>/leads.csv             every graded lead (the 100-row sheet), with status and signal
  <out>/sequencer_import.csv  'send' rows only; headers import into Smartlead and Instantly,
                              where first_line and signal map to custom variables
  <out>/linkedin_list.csv     rows that also get HeyReach steps (clear domain gap + LinkedIn profile)
  <out>/leads_redacted.csv    the same sheet with names shortened, emails masked and LinkedIn URLs removed
  <out>/run_report.md         counts in, out and dropped by reason

Files with full contact details are git-ignored; only the redacted sheet is meant to be published.

Usage: python scripts/export.py --workdir data --out output
"""
import argparse
from pathlib import Path

from lib import log, read_csv, write_csv

SHEET = ["name", "title", "company", "domain", "linkedin_url", "email", "verification_status", "qualifying_signal",
         "source", "first_line", "signal_bridge", "signal_short", "signal_tier", "linkedin", "action", "verification_detail", "angle", "first_line_engine"]
IMPORT = ["email", "first_name", "last_name", "company_name", "website", "linkedin_url", "title", "first_line", "signal_bridge", "signal_short", "signal"]


def redact(r):
    """'Jane Doe' / jane@acme.example -> 'Jane D.' / j***@acme.example; LinkedIn URL dropped."""
    out = dict(r)
    out["name"] = f"{r['first_name']} {r['last_name'][:1]}.".strip() if r.get("last_name") else r.get("first_name", "")
    if "@" in (r.get("email") or ""):
        local, domain = r["email"].split("@", 1)
        out["email"] = f"{local[:1]}***@{domain}"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default="data")
    ap.add_argument("--out", default="output")
    a = ap.parse_args()
    wd, out = Path(a.workdir), Path(a.out)
    rows = read_csv(wd / "people_final.csv")
    for r in rows:
        r["name"] = f"{r['first_name']} {r['last_name']}".strip()
        # signal_tier: 1 = hiring outbound roles, 2 = domain gap only (set when the shortlist was built)
        sig = r.get("qualifying_signal", "")
        r["signal_tier"] = r.get("tier") or ("1" if "Hiring" in sig else "2" if sig else "")
        # LinkedIn (HeyReach) steps only for the strongest signal with a named profile, as the JD reserves LinkedIn for top accounts
        r["linkedin"] = "yes" if r.get("angle") == "domain_gap" and r.get("linkedin_url") and r["action"] != "drop" else "no"
    write_csv(out / "leads.csv", rows, SHEET)

    send = [r for r in rows if r["action"] == "send" and r.get("first_line")]
    write_csv(out / "sequencer_import.csv", [{
        "email": r["email"], "first_name": r["first_name"], "last_name": r["last_name"], "company_name": r["company"],
        "website": r["domain"], "linkedin_url": r.get("linkedin_url", ""), "title": r["title"],
        "first_line": r["first_line"], "signal_bridge": r.get("signal_bridge", ""), "signal_short": r.get("signal_short", ""), "signal": r["qualifying_signal"]} for r in send], IMPORT)
    write_csv(out / "linkedin_list.csv", [r for r in rows if r["linkedin"] == "yes"],
              ["name", "title", "company", "linkedin_url", "qualifying_signal", "first_line"])
    # Shareable copy with contact details masked, for public repos and screenshots
    write_csv(out / "leads_redacted.csv", [redact(r) for r in rows], [c for c in SHEET if c != "linkedin_url"])

    dropped = read_csv(wd / "dropped.csv") if (wd / "dropped.csv").exists() else []
    by_reason = {}
    for d in dropped:
        by_reason[d["reason"]] = by_reason.get(d["reason"], 0) + 1
    status = {s: sum(r["verification_status"] == s for r in rows) for s in ("valid", "risky", "invalid")}
    report = [
        "# Run report", "",
        f"- Leads graded: {len(rows)} ({status})",
        f"- Ready to import (valid email + first line): {len(send)}",
        f"- Held for a second verifier (risky): {status['risky']}",
        f"- Signal: {sum(r['signal_tier'] == '1' for r in rows)} hiring (tier 1), {sum(r['signal_tier'] == '2' for r in rows)} domain gap only (tier 2)",
        f"- Also get LinkedIn steps (clear domain gap + profile): {sum(r['linkedin'] == 'yes' for r in rows)}",
        "", "## Removed before export", "",
        "| Reason | Count |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(by_reason.items())],
        "", "Every removed record is listed in dropped.csv.",
    ]
    (out / "run_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    write_csv(out / "dropped.csv", dropped, ["stage", "record", "reason", "detail"])
    log("export", f"{len(rows)} in sheet, {len(send)} ready to import, report at {out / 'run_report.md'}")


if __name__ == "__main__":
    main()
