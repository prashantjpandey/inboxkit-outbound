# Skill: qualify companies

**Input:** `data/companies.csv` after `scripts/snapshot.py` (columns include `name`, `domain`, `site_title`, `site_description`, `site_keywords`).
**Output:** `data/qualify_decisions.csv` with columns `domain,qualified,qualify_reason`, then run
`python scripts/apply_qualify.py data/qualify_decisions.csv data/companies.csv`. Companies you do not list become `unsure` and are not enriched.

## How to judge

Read the "Who we want" and "Does not qualify" sections of `icp.md`. Then, for each company:

1. Use `name`, `domain` and the website snapshot. Do not guess from the name alone if the snapshot says otherwise (Apollo tagged a cleaning company and a roofing-leads firm as "lead generation"; "Cleaning in Motion" turned out to be a real B2B lead-gen agency).
2. `yes`: the snapshot or name clearly shows an agency that runs outbound, cold email or lead generation for clients.
3. `no`: a software product, a data vendor, a sequencer, a recruiter, a trainer, a VA or BPO shop, phone-only calling, LinkedIn-only, or a non-agency business.
4. `unsure`: the snapshot is empty or ambiguous. Leave it out rather than guess.

## Rules

- Customers and competitors are removed by `config/suppression.csv` whatever you decide. Do not spend time on them.
- Keep the reason factual and short, quoting the site where possible: `site: B2B appointment setting agency`.
- After the pass, print counts (`yes`, `no`, `unsure`) and five random `yes` rows for a human spot check. The JD asks for spot checks before anything goes live.
