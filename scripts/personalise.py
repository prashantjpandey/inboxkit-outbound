"""Build checked facts per lead, then attach first lines.

  prepare   join people + companies, write <workdir>/to_personalise.jsonl (facts + angle per lead)
  template  write first lines from the facts with fixed templates (offline / no-LLM fallback)
  apply     merge <workdir>/first_lines.jsonl into <workdir>/people_final.csv

Claude writes the real first lines between 'prepare' and 'apply' by following skills/first-line.md.
Usage: python scripts/personalise.py prepare|template|apply --workdir data
"""
import argparse
import json
from pathlib import Path

from lib import log, norm_domain, read_csv, write_csv

GAP_TEXT = {
    "no_dmarc": "has no DMARC record",
    "no_spf": "has no SPF record",
    "multiple_spf": "publishes two SPF records, which makes both invalid",
    "spf_plus_all": "has an SPF record ending in +all, which lets anyone send as it",
    "dmarc_p_none": "has DMARC set to p=none, so it only monitors and does not protect",
}
MX_TEXT = {"google": "Google Workspace", "microsoft": "Microsoft 365"}
ROLE_LABEL = {"sdr": "an SDR", "sales development representative": "an SDR", "bdr": "a BDR",
              "cold email": "a cold email specialist",
              "outbound": "for an outbound role", "lead generation": "for a lead generation role",
              "lead generation specialist": "a lead generation specialist",
              "appointment setter": "an appointment setter", "deliverability": "a deliverability specialist",
              "campaign manager": "a campaign manager"}


def roles(hiring_for):
    """'sdr;cold email' -> ['an SDR', 'a cold email specialist'] (deduplicated, in order)."""
    out = []
    for r in filter(None, (hiring_for or "").split(";")):
        label = ROLE_LABEL.get(r.strip().lower(), "a " + r.strip())
        if label not in out:
            out.append(label)
    return out


def facts_for(person, company):
    name, domain = company.get("name", person.get("company", "")), company.get("domain", "")
    facts = []
    if company.get("hiring_for"):
        facts.append(f"{name} is hiring {' and '.join(roles(company['hiring_for']))}")
    for g in filter(None, company.get("dns_gaps", "").split(";")):
        facts.append(f"The main domain {domain} {GAP_TEXT[g]}")
    if company.get("mx_provider") in MX_TEXT:
        facts.append(f"{domain} receives email on {MX_TEXT[company['mx_provider']]}")
    if company.get("sells_infra") == "yes":
        facts.append(f"{name}'s website mentions setting up domains or inboxes for clients")
    return facts


def signal_summary(company):
    parts = []
    if company.get("hiring_for"):
        parts.append("Hiring: " + company["hiring_for"].replace(";", ", "))
    gaps = [g for g in company.get("dns_gaps", "").split(";") if g]
    if gaps:
        parts.append("Domain: " + ", ".join(gaps))
    if company.get("sells_infra") == "yes":
        parts.append("Sells infra to clients")
    return "; ".join(parts)


def template_line(item):
    c, gap = item["company"], item.get("gap")
    if item["angle"] == "domain_gap" and gap:
        return f"I ran a quick check on {item['domain']} and the main domain {GAP_TEXT[gap]}, easy to miss while {c} is growing the team."
    if item["angle"] == "dmarc_none":
        return f"Noticed {item['domain']} has DMARC on p=none, which is often fine for a while but worth a look as {c} adds clients."
    role = (roles(item.get("hiring_for")) or ["outbound help"])[0]
    return f"Saw {c} is hiring {role}, which usually means more clients and more mailboxes to stand up."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["prepare", "template", "apply"])
    ap.add_argument("--workdir", default="data")
    a = ap.parse_args()
    wd = Path(a.workdir)

    if a.step == "prepare":
        companies = {norm_domain(c["domain"]): c for c in read_csv(wd / "companies_clean.csv")}
        out = []
        for p in read_csv(wd / "people_verified.csv"):
            if p.get("action") == "drop":
                continue
            c = companies.get(norm_domain(p.get("domain")), {})
            gaps = [g for g in c.get("dns_gaps", "").split(";") if g and g != "dmarc_p_none"]
            out.append({"id": p["person_id"], "first_name": p["first_name"], "company": c.get("name", p.get("company")),
                        "domain": c.get("domain", p.get("domain")), "hiring_for": c.get("hiring_for", ""),
                        "angle": c.get("dns_angle", "hiring"), "gap": gaps[0] if gaps else "",
                        "facts": facts_for(p, c), "signal": signal_summary(c)})
        with open(wd / "to_personalise.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(o) + "\n" for o in out)
        log("personalise", f"{len(out)} leads prepared; next: follow skills/first-line.md (or run 'template')")

    elif a.step == "template":
        items = [json.loads(l) for l in open(wd / "to_personalise.jsonl", encoding="utf-8")]
        with open(wd / "first_lines.jsonl", "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps({"id": it["id"], "first_line": template_line(it), "engine": "template"}) + "\n")
        log("personalise", f"{len(items)} template first lines written")

    else:
        lines = {}
        for l in open(wd / "first_lines.jsonl", encoding="utf-8"):
            o = json.loads(l)
            lines[o["id"]] = o
        items = {json.loads(l)["id"]: json.loads(l) for l in open(wd / "to_personalise.jsonl", encoding="utf-8")}
        rows = read_csv(wd / "people_verified.csv")
        for r in rows:
            it, fl = items.get(r["person_id"], {}), lines.get(r["person_id"], {})
            r["qualifying_signal"] = it.get("signal", "")
            r["angle"] = it.get("angle", "")
            r["first_line"] = fl.get("first_line", "")
            r["first_line_engine"] = fl.get("engine", "claude" if fl else "")
        write_csv(wd / "people_final.csv", rows)
        missing = sum(1 for r in rows if r.get("action") != "drop" and not r["first_line"])
        log("personalise", f"first lines attached; {missing} sendable leads without a line")


if __name__ == "__main__":
    main()
