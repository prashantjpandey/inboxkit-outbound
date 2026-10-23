# Copy: growing outbound agencies

**Example lead:** Mustafa, Scalemill (scalemill.com). Co-Founder and CEO of a B2B lead-gen agency that is hiring an SDR and whose main domain has no SPF record.

Every message below is shown exactly as Mustafa would receive it. The workflow writes the personal parts for each lead from checked facts (see "How the personal parts are filled" at the end).

- **Offer:** a free 30-minute infrastructure audit. **One ask per message.**
- **Plain text, no links:** links hurt placement and pull clicks away from the reply. Every product claim comes from inboxkit.com; the sources sit under each email (not sent) and in the table at the end.
- **Opt-out:** the sequencer adds its standard footer to every email ("If it's not a priority, reply 'no' and I'll stop."), so it is not repeated below.

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

### Email 1A (day 1: signal, then what changes)

**Subject:** Scalemill sending

> Hi Mustafa,
>
> I ran a quick check on scalemill.com and the main domain has no SPF record, easy to miss while you are hiring an SDR. If the main domain has a gap, the sending domains behind your client campaigns are worth a look too.
>
> Every new client needs its own domains, mailboxes and warmup, and one bad domain can drag a client's results down. InboxKit takes that whole layer off your team, from DNS and warmup to blacklist monitoring.
>
> Worth a free 30-minute audit of Scalemill's setup?
>
> Best,<br>
> Prashant<br>
> InboxKit

<sub>_Sources (not sent): what InboxKit runs, about page; the audit offer, demo page._</sub>

### Email 1B (day 1: signal, then proof)

**Subject:** replies at Scalemill

> Hi Mustafa,
>
> I ran a quick check on scalemill.com and the main domain has no SPF record, easy to miss while you are hiring an SDR. If the main domain has a gap, the sending domains behind your client campaigns are worth a look too.
>
> Worth knowing: Cymate, an outbound agency, ran their old mailboxes against InboxKit on about 10,000 sends each, and positive replies went from 10 to 26.
>
> Open to a free 30-minute audit to see where Scalemill stands?
>
> Best,<br>
> Prashant<br>
> InboxKit

<sub>_Sources (not sent): Cymate case study (9,965 sent and 10 positive on the previous vendor; 10,545 sent and 26 positive on InboxKit). The previous vendor is not named._</sub>

### Email 2 (day 4: setup time)

**Subject:** re: Scalemill sending

> Hi Mustafa,
>
> Following up on my note about the missing SPF record on scalemill.com. As an agency grows, client setup is where ops time quietly disappears. Anevo Marketing went from one to two weeks per new client to one to two hours after moving to InboxKit.
>
> Should I send over a couple of times for the audit?
>
> Best,<br>
> Prashant<br>
> InboxKit

<sub>_Sources (not sent): Anevo case study (client setup 1 to 2 hrs, was 1 to 2 weeks)._</sub>

### Email 3 (day 8: one bad domain)

**Subject:** one bad domain

> Hi Mustafa,
>
> One burnt domain can take a client's whole campaign down with it. On InboxKit every domain gets its own admin panel, so the damage stays isolated, and InfraGuard rechecks blacklists, DNS and bounces every six hours.
>
> Want me to hold an audit slot for Scalemill?
>
> Best,<br>
> Prashant<br>
> InboxKit

<sub>_Sources (not sent): homepage ("Dedicated Panel for Each Domain"); pricing page (InfraGuard every 6 hours)._</sub>

### Email 4 (day 15: close the loop)

**Subject:** closing the loop

> Hi Mustafa,
>
> I'll leave it here. If sending infrastructure moves up the list at Scalemill, reply to this and I'll set up the free audit.
>
> Best,<br>
> Prashant<br>
> InboxKit

### LinkedIn connection note

> Hi Mustafa, I work on email infrastructure at InboxKit and spend most of my time with outbound agency founders, so Scalemill caught my eye. Would be good to connect.

<sub>_No pitch. Under 300 characters._</sub>

### LinkedIn follow-up 1 (day 3, after connecting)

> Thanks for connecting, Mustafa. I noticed the missing SPF record on scalemill.com, a quick fix but easy to miss. We run a free 30-minute infrastructure audit for agencies, happy to set one up if it helps.

<sub>_Sources (not sent): the audit offer, demo page._</sub>

### LinkedIn follow-up 2 (day 10)

> Mustafa, last note from me. LeadHaste runs 100+ client campaigns on InboxKit and has had zero suspensions since moving. If burnt domains ever come up as Scalemill grows, worth a 30-minute look?

<sub>_Sources (not sent): LeadHaste case study ("Zero: suspensions on InboxKit", "100+: client campaigns")._</sub>

## How the personal parts are filled

The sequencer template uses merge fields; the workflow fills them per lead in `sequencer_import.csv`:

| In Mustafa's emails | Merge field | Filled from |
|---|---|---|
| Mustafa | `{{first_name}}` | Apollo |
| Scalemill | `{{company_name}}` | Apollo |
| "I ran a quick check on scalemill.com and the main domain has no SPF record, easy to miss while you are hiring an SDR." | `{{first_line}}` | Written by Claude from checked facts (`skills/first-line.md`) |
| "If the main domain has a gap, the sending domains behind your client campaigns are worth a look too." | `{{signal_bridge}}` | Chosen by signal type (`scripts/personalise.py`) |
| "the missing SPF record on scalemill.com" | `{{signal_short}}` | Built from the same facts (`scripts/personalise.py`) |

A lead with only a hiring signal gets wording that fits it. For SalesSourcers (hiring an SDR, no domain gap):

- Email 1 opens: "Saw SalesSourcers is hiring an SDR, which usually means more client campaigns and more mailboxes to stand up and keep warm. That is usually the stage where one burnt domain starts costing a client real replies."
- Email 2 opens: "Following up on my note about the SDR roles you are hiring for."
- LinkedIn steps are skipped (LinkedIn goes only to leads with a clear domain gap). Ten more first lines with the facts behind them are in `first_lines_10.md`.

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
