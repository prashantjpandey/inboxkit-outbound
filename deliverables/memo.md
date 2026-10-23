# InboxKit outbound: 15 demos in 30 days

Prashant Pandey · GTM Engineer assignment · 23 October 2026

**Find agencies whose sending is about to get harder, tell them one true thing about their own domain, offer the audit InboxKit already runs.** The repo turns any `icp.md` into that list.

## 1. Segment and signal

**Outbound, lead-gen and appointment-setting agencies (1 to 200 staff): founders, heads of growth, and the ops lead who owns sending.** They are InboxKit's proven buyer: all 11 [case studies](https://www.inboxkit.com/customer-stories/case-studies) are agencies, 56 sit in the [partner directory](https://www.inboxkit.com/partners), and the [agency page](https://www.inboxkit.com/agency-email-solution) claims "500+ agencies". Their stated pains: burnt mailboxes, manual setup per client, one bad domain dragging a client down.

Every row carries at least one signal:
- **Hiring outbound roles** (SDR, BDR, appointment setter): more clients means more mailboxes to set up. Apollo job filter, free.
- **A gap on their own domain** (no SPF, no DMARC, duplicate SPF, or DMARC at `p=none`): a true opener that leads straight into an audit. Public DNS check in the repo, free.

**What the data showed:** broad Apollo tags with a hiring filter were only 17% real agencies (39 of 231), tighter tags 51%, so qualification runs before any credit is spent. 60% of qualified agencies had a domain gap. Hiring alone covers about 60 agencies at a time, so the domain gap is the signal that scales.

## 2. Offer and single CTA

**A free 30-minute infrastructure audit**: live SPF, DKIM and DMARC check, a warmup plan and a same-day fix list ([offer](https://www.inboxkit.com/pricing), booked via [/demo](https://www.inboxkit.com/demo)). One ask in every message. It is already InboxKit's offer and the first item on the JD's offer list.

## 3. Three weeks, interleaved

| Day | Email (all leads) | LinkedIn, HeyReach (clear domain gap + profile) |
|---|---|---|
| 1 | Email 1, A/B: signal + what we do / signal + Cymate proof | Connection note, no pitch |
| 3 | | Follow-up 1: the audit |
| 4 | Email 2: setup time as clients grow (Anevo) | |
| 8 | Email 3: one bad domain (isolation, InfraGuard) | |
| 10 | | Follow-up 2: LeadHaste proof |
| 15 | Email 4: close the loop | |

Any reply stops every step and routes to Attio. Stop rule (JD): pause a variant above 1,000 emails per positive after 1,500 sends.

## 4. Volume maths, 15 demos back to contacts

| Step | Assumption | Result |
|---|---|---|
| Positive replies | 50% of positives book (assumption) | 30 |
| Emails | under 500 per positive (JD target) | 15,000 |
| Contacts | 4 emails each; plus 10% lost to cleaning | 3,750 → about 4,150 sourced |
| Infrastructure | 15 emails per mailbox a day, 3 per domain, 14-day warmup ([warmup](https://www.inboxkit.com/email-warmup)) | 1,000 a day = 67 mailboxes, 23 domains, ordered 2 weeks early |
| Cost | $3 mailbox + $3 warmup a month ([pricing](https://www.inboxkit.com/pricing)) | about $400 a month, run on InboxKit itself |

At 300 emails per positive it drops to about 2,250 contacts.

## 5. The list, scaling and cost

**The lead sheet, 97 rows, built by the workflow (`output/leads_redacted.csv` in the repo; full contact details shared privately):** 308 companies reviewed, 81 qualified, 6 customers and competitors suppressed, 99 people revealed, 2 dropped after enrichment showed a phone-only agency. **47 send-ready, 49 held for a second verifier** (44 catch-all domains, 5 off-domain emails), 1 with no email. Every row has a fact-based first line (10 shown in `first_lines_10.md`). I stopped at 97 rather than pad with weaker fits.

**To 2,000:** the tight-tag search without the hiring filter, keeping agencies with a role or a gap, at about 1.7 contacts each: roughly 1,200 agencies from 2,600 looked at, free until the reveal.

**Cost per contact:** 1.02 Apollo credits per row, since credits are spent only after qualification, suppression and dedupe, and no-matches are free. About 2 per send-ready contact until held catch-alls clear BounceBan, the main lever on the 3% bounce target. Human cost: a 5-minute spot check per 100.
