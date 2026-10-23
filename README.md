# inboxkit-outbound

A Claude Code workflow that turns an ICP description into a verified, deduplicated, personalised lead list ready to import into Smartlead or Instantly. Built for the InboxKit GTM Engineer assignment. Nothing is sent from this repo.

**Three steps, made repeatable: find the right buyers, say one true thing to them, and do it the same way every time.**

## What is in here

| Path | What it is |
|---|---|
| `deliverables/memo.md` | One-page strategy: segment, signals, offer, 3-week plan, volume maths, scaling and cost |
| `deliverables/copy.md` | 4-step email sequence (two step-1 variants), LinkedIn note and two follow-ups |
| `deliverables/first_lines_10.md` | Ten workflow-written first lines with the facts each one used |
| `output/leads_redacted.csv` | The lead sheet: 97 rows with status, signal, source and first line (contact details masked; full sheet shared privately) |
| `output/sequencer_import.csv` | The 47 send-ready rows in Smartlead and Instantly format (created locally by the run, not published) |
| `output/linkedin_list.csv` | The 22 rows that also get HeyReach steps (created locally, not published) |
| `output/run_report.md` | Counts kept, held and dropped, by reason |
| `CLAUDE.md` | How Claude runs the workflow: the nine steps, rules, what to do on failure |
| `icp.md` | The only input. Copy a file from `icps/` over it to run a new segment |
| `skills/` | Judgment steps: `qualify.md` (is this an agency?), `first-line.md` (the opener) |
| `scripts/` | Mechanical steps: snapshot, suppression and dedupe, DNS check, verification, export, copy lint |
| `config/suppression.csv` | 108 customers, partners, competitors and own brands, from inboxkit.com and the Enrich Labs press release |
| `sample/` + `tests/` | Planted bad data and tests that prove each problem is caught |

## Run it (Python 3.10+, no installs, no keys)

```bash
python scripts/run.py sample
python -m unittest discover tests
```

The sample run works offline and shows every guard on planted data: two duplicate people, a duplicate company, a malformed email, an email domain with no mail server, an existing InboxKit partner, a competitor, a do-not-contact person, a lead already in a sales conversation, a non-agency, and a role address held back from sending. The report is printed and saved to `output/sample_run/run_report.md`.

## The real run

Open the repo in Claude Code and ask it to run the workflow; it follows `CLAUDE.md`. Judgment steps (qualify, first lines) are Claude following a skill. Everything else is a script, so it behaves the same every time:

```
icp.md
  -> find companies (Apollo, free)        -> website snapshot -> qualify (Claude)
  -> suppress customers/competitors -> dedupe -> DNS check -> drop companies with no signal
  -> find decision makers (Apollo, free)  -> reveal emails (the only paid step)
  -> suppress + dedupe people -> verify emails -> first lines (Claude) -> lint -> export
```

Every removal is logged with a reason in `dropped.csv`, and `run_report.md` counts them.

## Rules the copy follows

`python scripts/lint_copy.py deliverables/copy.md` fails on em or en dashes, more than one question per message, any link inside a message, an unfilled placeholder or a message not personalised to the example lead, an email without a sign-off, a product claim without a source note, a missing claim-sources table (every claim linked to its inboxkit.com page), or no declared opt-out footer. First lines are linted the same way and may not claim a prospect's email goes to spam.

## Contact data

This public repo contains no contact details. `output/leads_redacted.csv` is the lead sheet with names shortened, emails masked and LinkedIn URLs removed; the full sheet (names, emails, LinkedIn URLs) was shared privately with InboxKit. Files that hold contact details are git-ignored, so rerunning the workflow keeps them local.
