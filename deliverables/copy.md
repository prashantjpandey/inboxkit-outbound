# Copy: growing outbound agencies

Sender: Prashant, InboxKit. Offer: free 30-minute infrastructure audit. One ask per message. Merge tags are Smartlead style (`{{first_name}}`, `{{company_name}}`, `{{first_line}}`); in Instantly use `{{firstName}}`, `{{companyName}}` and the custom variable `{{first_line}}`. `first_line` comes from the workflow (see `output/leads.csv`).

Lines starting with `>` are notes for the reviewer, not part of the message. Every product claim links the inboxkit.com page it came from. `python scripts/lint_copy.py deliverables/copy.md` checks the rules.

## Schedule (3 weeks; LinkedIn only for leads with a clear domain gap)

| Day | Email (all leads) | LinkedIn (leads with a clear domain gap and a LinkedIn profile) |
|---|---|---|
| 1 | Email 1 (A/B split) | View profile, send connection note |
| 3 | | Follow-up 1, if connected |
| 4 | Email 2 | |
| 8 | Email 3 | |
| 10 | | Follow-up 2 |
| 15 | Email 4 (close the loop) | |
| 15 to 21 | Reply handling; stop all steps on any reply | |

### Email 1A (signal + what we do)

Subject: {{company_name}} sending setup

Hi {{first_name}},

{{first_line}}

As an agency adds clients, the infrastructure work grows with it: new domains, mailboxes, DNS records and warmup for every account. InboxKit runs that layer: Google Workspace, Microsoft 365 and Azure mailboxes on your domains, authentication records published for you, warmup, and monitoring of blacklists, DNS and bounces (https://www.inboxkit.com/about).

We offer a free 30-minute infrastructure audit: a live check of your SPF, DKIM and DMARC and a fix list you can act on the same day (https://www.inboxkit.com/demo). Worth a look for {{company_name}}?

Prashant
InboxKit

Reply "no" and I won't email again.

> Claims: about page (what InboxKit provisions and monitors); audit contents from the offer on every page, booked via /demo.

### Email 1B (signal + proof)

Subject: replies at {{company_name}}

Hi {{first_name}},

{{first_line}}

One outbound agency, Cymate, ran its old mailboxes and InboxKit side by side on about 10,000 sends each. Positive replies went from 10 to 26 (https://www.inboxkit.com/case-studies/cymate-recovered-client-pipeline-inboxkit).

A free 30-minute infrastructure audit is the quickest way to see where your own setup stands (https://www.inboxkit.com/demo). Open to one?

Prashant
InboxKit

Reply "no" and I won't email again.

> Cymate test on the case study page: 9,965 sent and 10 positive on the previous vendor, 10,545 sent and 26 positive on InboxKit. The previous vendor is not named.

### Email 2 (day 4: time cost of growth)

Subject: re: {{company_name}} sending setup

Hi {{first_name}},

When agencies grow, mailbox setup quietly eats the ops team. Anevo Marketing, a multi-client agency, went from one to two weeks to set up a new client to one to two hours, and now runs over 4,000 mailboxes this way (https://www.inboxkit.com/case-studies/anevo-marketing-scaled-infrastructure-inboxkit).

Should I send a couple of times for the audit?

Prashant

Reply "no" and I won't email again.

> Anevo case study: client setup 1 to 2 hrs (was 1 to 2 weeks); 4.3K active mailboxes.

### Email 3 (day 8: one bad domain)

Subject: one bad domain

Hi {{first_name}},

The failure agencies tell us about most is one domain getting burnt and pulling a client's campaign down with it. On InboxKit each domain gets its own admin panel, so a damaged domain stays isolated from the rest (https://www.inboxkit.com/), and InfraGuard rechecks blacklists, DNS and bounces every six hours (https://www.inboxkit.com/pricing).

If that is useful for {{company_name}}, the free audit covers it (https://www.inboxkit.com/demo). Want me to hold a slot?

Prashant

Reply "no" and I won't email again.

> Homepage: "Dedicated Panel for Each Domain". Pricing page: InfraGuard "Blacklist, DNS and bounce monitoring every 6 hours".

### Email 4 (day 15: close the loop)

Subject: closing the loop

Hi {{first_name}},

I'll leave it here. If sending infrastructure moves up the list as {{company_name}} hires, the free 30-minute audit stands (https://www.inboxkit.com/demo).

Prashant

Reply "no" and I won't email again.

### LinkedIn connection note

Hi {{first_name}}, I work on email infrastructure at InboxKit and keep an eye on how outbound agencies scale. Saw {{company_name}} is hiring, so thought I'd connect.

> No pitch and no link in the note. Under 300 characters.

### LinkedIn follow-up 1 (day 3, after connecting)

Thanks for connecting, {{first_name}}. I also sent you a short email about {{company_name}}'s domain setup. The short version: we run a free 30-minute infrastructure audit for agencies, a live check of SPF, DKIM and DMARC plus a fix list (https://www.inboxkit.com/demo). Happy to set one up if it helps.

### LinkedIn follow-up 2 (day 10)

{{first_name}}, one more and then I'll stop. LeadHaste runs 100+ client campaigns on InboxKit and reports zero suspensions since moving (https://www.inboxkit.com/case-studies/leadhaste-millions-emails-automated-dns-inboxkit). If burnt domains ever come up as you grow, worth a 30-minute look?

> LeadHaste case study: "Zero: suspensions on InboxKit", "100+: client campaigns".
