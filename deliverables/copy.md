# Copy: growing outbound agencies

**Sender:** Prashant, InboxKit. **Offer:** free 30-minute infrastructure audit. **One ask per message.**

**Personalisation (from the workflow, per lead):**
- `{{first_line}}`: the opener, written from checked facts (their domain gap or open role). See `deliverables/first_lines_10.md`.
- `{{signal_short}}`: the same signal as a short phrase for follow-ups, e.g. "the missing DMARC record on acme.io" or "the SDR hire".
- Tags are Smartlead style; in Instantly use `{{firstName}}`, `{{companyName}}` and the custom variables `{{first_line}}`, `{{signal_short}}`.

**Plain text, no links.** Links in cold email hurt placement and pull clicks away from the reply. Every product claim comes from inboxkit.com; the source page for each is listed under "Claim sources" at the bottom, for reviewers only.

**Opt-out:** every email carries the sequencer's standard footer ("If it's not a priority, reply 'no' and I'll stop."), handled at the sending layer, so it is not repeated below.

Lines starting with `>` are notes for the reviewer. `python scripts/lint_copy.py deliverables/copy.md` checks the rules.

## Schedule (3 weeks; LinkedIn only for leads with a clear domain gap)

| Day | Email (all leads) | LinkedIn (clear domain gap + profile) |
|---|---|---|
| 1 | Email 1 (A/B split) | View profile, send connection note |
| 3 | | Follow-up 1, if connected |
| 4 | Email 2 | |
| 8 | Email 3 | |
| 10 | | Follow-up 2 |
| 15 | Email 4 (close the loop) | |
| 15 to 21 | Reply handling; any reply stops every step | |

### Email 1A (signal, then what changes)

Subject: {{company_name}} sending

Hi {{first_name}},

{{first_line}}

That is usually the point where agency sending starts to creak: every new client needs its own domains, mailboxes and warmup, and one bad domain can drag a client's results down.

InboxKit takes that whole layer off your team, from DNS and warmup to blacklist monitoring. Worth a free 30-minute audit of {{company_name}}'s setup?

Prashant
InboxKit

> Sources: what InboxKit runs (about page); the audit offer (demo page).

### Email 1B (signal, then proof)

Subject: replies at {{company_name}}

Hi {{first_name}},

{{first_line}}

Worth knowing: Cymate, an outbound agency, ran their old mailboxes against InboxKit on about 10,000 sends each, and positive replies went from 10 to 26.

Open to a free 30-minute audit to see where {{company_name}} stands?

Prashant
InboxKit

> Source: Cymate case study (9,965 sent and 10 positive on the previous vendor; 10,545 sent and 26 positive on InboxKit). The previous vendor is not named.

### Email 2 (day 4: setup time)

Subject: re: {{company_name}} sending

Hi {{first_name}},

Following up on {{signal_short}}. As an agency grows, client setup is where ops time quietly disappears. Anevo Marketing went from one to two weeks per new client to one to two hours after moving to InboxKit.

Should I send over a couple of times for the audit?

Prashant

> Source: Anevo case study (client setup 1 to 2 hrs, was 1 to 2 weeks).

### Email 3 (day 8: one bad domain)

Subject: one bad domain

Hi {{first_name}},

The thing agency founders tell us hurts most is one burnt domain taking a client's campaign down with it. On InboxKit every domain gets its own admin panel, so the damage stays isolated, and InfraGuard rechecks blacklists, DNS and bounces every six hours.

Want me to hold an audit slot for {{company_name}}?

Prashant

> Sources: homepage ("Dedicated Panel for Each Domain"); pricing page (InfraGuard every 6 hours).

### Email 4 (day 15: close the loop)

Subject: closing the loop

Hi {{first_name}},

I'll leave it here. If sending infrastructure moves up the list at {{company_name}}, reply to this and I'll set up the free audit.

Prashant

### LinkedIn connection note

Hi {{first_name}}, I work on email infrastructure at InboxKit and spend most of my time with outbound agency founders, so {{company_name}} caught my eye. Would be good to connect.

> No pitch. Under 300 characters.

### LinkedIn follow-up 1 (day 3, after connecting)

Thanks for connecting, {{first_name}}. I noticed {{signal_short}} while looking at {{company_name}}, a quick fix but easy to miss. We run a free 30-minute infrastructure audit for agencies, happy to set one up if it helps.

> Source: the audit offer (demo page).

### LinkedIn follow-up 2 (day 10)

{{first_name}}, last note from me. LeadHaste runs 100+ client campaigns on InboxKit and has had zero suspensions since moving. If burnt domains ever come up as {{company_name}} grows, worth a 30-minute look?

> Source: LeadHaste case study ("Zero: suspensions on InboxKit", "100+: client campaigns").

## Claim sources

| Claim in the copy | Page on inboxkit.com |
|---|---|
| Mailboxes, DNS and authentication, warmup, blacklist monitoring | https://www.inboxkit.com/about |
| Free 30-minute infrastructure audit (SPF, DKIM, DMARC, fix list) | https://www.inboxkit.com/demo |
| Cymate: positive replies 10 to 26 on about 10,000 sends each | https://www.inboxkit.com/case-studies/cymate-recovered-client-pipeline-inboxkit |
| Anevo: client setup from 1 to 2 weeks to 1 to 2 hours | https://www.inboxkit.com/case-studies/anevo-marketing-scaled-infrastructure-inboxkit |
| Dedicated admin panel per domain | https://www.inboxkit.com/ |
| InfraGuard rechecks blacklists, DNS and bounces every 6 hours | https://www.inboxkit.com/pricing |
| LeadHaste: 100+ client campaigns, zero suspensions | https://www.inboxkit.com/case-studies/leadhaste-millions-emails-automated-dns-inboxkit |
