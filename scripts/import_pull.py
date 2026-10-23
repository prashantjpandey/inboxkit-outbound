"""Add a raw company pull to data/companies.csv, merging the roles each company was found under.

Input lines: role|name|domain|org_id  (written by Claude from Apollo MCP results, or exported from any tool)
Usage: python scripts/import_pull.py data/_apollo_pull_<date>.txt data/companies.csv
"""
import sys
from pathlib import Path

from lib import log, norm_domain, read_csv, write_csv


def main(src, dst):
    # Merge into an existing file so snapshot and qualify work already done is kept
    companies = {r["domain"]: r for r in read_csv(dst)} if Path(dst).exists() else {}
    for line in open(src, encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        role, name, domain, org_id = [p.strip() for p in line.split("|")]
        key = norm_domain(domain)
        c = companies.setdefault(key, {"org_id": org_id, "name": name, "domain": key,
                                       "source": "apollo:organizations_lookup", "hiring_for": ""})
        roles = [r for r in c["hiring_for"].split(";") if r]
        if role != "-" and role not in roles:  # "-" = found without a hiring filter
            c["hiring_for"] = ";".join(roles + [role])
    write_csv(dst, list(companies.values()))
    log("import", f"{len(companies)} unique companies written to {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
