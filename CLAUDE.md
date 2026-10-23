# CLAUDE.md: how to run this workflow

You turn `icp.md` into a verified, deduplicated, personalised lead list that imports into Smartlead or Instantly. Nothing is ever sent from this repo.

**Principle:** judgment steps (is this an agency? what is the best first line?) are skills you follow. Mechanical steps (snapshot, suppression, dedupe, DNS, verification, export) are scripts, so they behave the same on every run and can be tested.

## Before you start

1. Read `icp.md`. It is the only input. In a review call someone may replace it with a new segment; nothing else needs to change.
2. Check `config/suppression.csv` exists. Add any CRM export of open deals (`reason=in_conversation`) or unsubscribes (`reason=do_not_contact`) with `--extra-suppression` or by appending rows.
3. Prove the repo works: `python scripts/run.py sample` then `python -m unittest discover tests`. Both run offline in seconds.

## The run (nine steps)

| # | Step | Who | Command or skill | Output |
|---|---|---|---|---|
| 1 | Find companies | Claude | Apollo MCP `apollo_organizations_lookup` (free), `keyword_tags` and `employee_ranges` from `icp.md`, `per_page` 60 to 100. **Tier 1:** one call per entry in `company.hiring_for` (as `q_organization_job_titles`); write hits as `role\|name\|domain\|org_id`. **Tier 2:** one call with tighter agency tags and no hiring filter; write hits with role `-`. Save to `data/_apollo_pull_<date>.txt`, then `python scripts/import_pull.py data/_apollo_pull_<date>.txt data/companies.csv` (merges, keeps earlier work) | `data/companies.csv` |
| 2 | Website snapshot | script | `python scripts/snapshot.py data/companies.csv` | title, description, keywords per company |
| 3 | Qualify | Claude | follow `skills/qualify.md`; write `data/qualify_decisions.csv` (`domain,qualified,qualify_reason`), then `python scripts/apply_qualify.py data/qualify_decisions.csv data/companies.csv` | `qualified` column |
| 4 | Suppress, dedupe, DNS, signal rule | script | `python scripts/run.py companies`: drops customers and competitors first, then non-qualified and duplicate companies, checks DNS, and drops any company with neither an open role nor a domain gap | `data/companies_clean.csv`, `data/dropped.csv` |
| 5 | Find decision makers | Claude | Apollo MCP `apollo_mixed_people_api_search` (free) with `organization_ids` from `data/companies_clean.csv` and `person_titles` from `icp.md`; for agencies with no founder match, retry with `person_seniorities` (owner, founder, c_suite, vp, head, director). Keep at most `max_per_company`, founders first, then the ops or delivery lead who owns sending. Skip `has_email: false`. Write `data/people_shortlist.csv` | `data/people_shortlist.csv` |
| 6 | Reveal emails | Claude | Apollo MCP `apollo_people_bulk_match` by person id, batches of 10. **Costs credits.** Check the balance first, state the count and credits, get approval, never exceed `limits.max_enrich_credits`, no waterfall unless approved. Write `data/people_enriched.csv` (columns as in `sample/people_enriched.csv`) | `data/people_enriched.csv` |
| 7 | Suppress, dedupe, verify, prepare | script | `python scripts/run.py people` | `data/people_verified.csv`, `data/to_personalise.jsonl` |
| 8 | First lines | Claude | follow `skills/first-line.md` on `data/to_personalise.jsonl`, write `data/first_lines.jsonl` | first lines |
| 9 | Lint and export | script | `python scripts/run.py finish` | `output/leads.csv`, `output/sequencer_import.csv`, `output/linkedin_list.csv`, `output/run_report.md` |

Credits are spent only in step 6, after qualification, suppression, deduplication and the signal rule, so no credit is wasted on a customer, a competitor, a non-agency, a duplicate or a company with no reason to write now.

No Apollo connector? Any CSV export (Apollo, Clay, Prospeo) with the same columns works: put it at step 1 or step 5 and carry on. No network? `run.py sample` shows every stage on fixtures.

## Rules

- Never send, schedule or upload anything to a sequencer. The output is a CSV for a human to import.
- Never spend more Apollo credits than `limits.max_enrich_credits` in `icp.md`.
- First lines use only the facts in `to_personalise.jsonl`. No invented numbers, clients or tools.
- Copy rules (enforced by `scripts/lint_copy.py`): no em or en dashes, one ask per message, plain text with no links in messages, every message personalised from the lead's signal, every product claim sourced to an inboxkit.com page in the claim-sources table, the sequencer's opt-out footer on every email, no attacks on named companies.
- Only `action=send` rows (valid email) go into `sequencer_import.csv`. `hold` rows wait for a second verifier.

## When something fails

| Symptom | What to do |
|---|---|
| A stage exits non-zero | Read the `[stage]` log line above the error, fix the input file, rerun only that stage (each script takes explicit input and output paths). |
| Apollo returns nothing | Broaden one filter at a time (`employee_ranges`, then `hiring_for`) in `icp.md`; note the change in the run report. |
| Apollo plan or credit limit | Stop. Report it. Do not switch data sources without asking. |
| Many `unsure` in qualify | Snapshot failed (site blocked). Run `python scripts/snapshot.py data/companies.csv --retry-failed` once, spot-check five by hand, and leave the rest out rather than guessing. |
| Enrichment reveals a company is out of scope (e.g. a headline says phone-only) | Change its row in `data/qualify_decisions.csv` to `no` with the evidence, rerun `apply_qualify.py` and `run.py companies`, then `run.py people`: its people are dropped as `company_no_longer_qualified`. Mention the wasted credits in the report. |
| `lint_copy.py` fails | Fix the line it names. Never skip the lint. |
| Bounce risk (`risky` > 20%) | Do not export them. Run them through a paid verifier (BounceBan) first. |

## Live rerun on a new segment (review call)

1. Edit the JSON block and prose in `icp.md` (roles, keyword tags, who qualifies).
2. Run steps 1 to 9 with a small `limits.companies` (e.g. 20) and `max_enrich_credits` of 10, in a fresh work folder (`--workdir data_live`) so the main run is untouched.
3. Show `output/run_report.md` and three first lines.
