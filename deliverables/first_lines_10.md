# First lines: 10 rows from the workflow

Written by Claude following `skills/first-line.md`, using only the checked facts the scripts produced for each lead (`data/to_personalise.jsonl`). All 96 sendable or held leads have one in the lead sheet (`output/leads_redacted.csv` here; full contact details shared privately); these 10 are send-ready rows, mixing the three angles. Checked by `python scripts/lint_copy.py --first-lines data/first_lines.jsonl`.

## Clear domain fault

**1. Mustafa A., Co-Founder & CEO, Scalemill**  
> I ran a quick check on scalemill.com and the main domain has no SPF record, easy to miss while you are hiring an SDR.

Facts used: Scalemill is hiring an SDR; The main domain scalemill.com has no SPF record; scalemill.com receives email on Google Workspace

**2. Celia T., Sales Manager || SVP, European Sales Group**  
> I ran a quick check on europeansales.group and the main domain has no DMARC record, easy to miss while you are hiring an SDR.

Facts used: European Sales Group is hiring an SDR; The main domain europeansales.group has no DMARC record; europeansales.group receives email on Microsoft 365

**3. Karolina B., Founder and CEO, Protosell AB**  
> I ran a quick check on protosell.se and the main domain has no DMARC record, easy to miss while Protosell is hiring for outbound.

Facts used: Protosell AB is hiring for an outbound role; The main domain protosell.se has no DMARC record; protosell.se receives email on Microsoft 365

**4. Julius D., Co-Founder & CEO, REP - Revenue Excellence Partners**  
> Spotted that revenue-excellence.de has no SPF record on the main domain, worth a look as REP hires for outbound.

Facts used: REP - Revenue Excellence Partners is hiring for an outbound role; The main domain revenue-excellence.de has no SPF record; The main domain revenue-excellence.de has DMARC set to p=none, so it only monitors and does not protect; revenue-excellence.de receives email on Google Workspace

## DMARC at p=none

**5. Jakob L., Founder/CEO, Brightvision**  
> Noticed brightvision.com has DMARC set to p=none, which is fine early on but worth tightening as Brightvision hires an SDR.

Facts used: Brightvision is hiring for an outbound role and an SDR; The main domain brightvision.com has DMARC set to p=none, so it only monitors and does not protect; brightvision.com receives email on Microsoft 365

**6. Adam R., Co-Founder, Grow Surely**  
> Noticed growsurely.com has DMARC set to p=none, which is common but worth tightening as Grow Surely hires an SDR.

Facts used: Grow Surely is hiring an SDR; The main domain growsurely.com has DMARC set to p=none, so it only monitors and does not protect; growsurely.com receives email on Microsoft 365

**7. Hollie K., Managing Director, Matter**  
> A quick check of matterb2b.com shows DMARC set to p=none, worth a look while Matter is adding an SDR.

Facts used: Matter is hiring an SDR; The main domain matterb2b.com has DMARC set to p=none, so it only monitors and does not protect; matterb2b.com receives email on Microsoft 365

## Hiring signal

**8. Javier C., Founder & CEO, Flows**  
> Saw Flows is hiring for a lead generation role, which usually means more client campaigns and more inboxes to set up.

Facts used: Flows is hiring for a lead generation role; flows.es receives email on Google Workspace

**9. Zane W., Co-Founder & CEO, SalesSourcers**  
> Saw SalesSourcers is hiring an SDR, which usually means more client campaigns and more mailboxes to stand up and keep warm.

Facts used: SalesSourcers is hiring an SDR; salessourcers.com receives email on Microsoft 365

**10. Marin L., Co-founder - Growth & Partnerships, Akimbo**  
> Saw Akimbo is hiring for an outbound role, which usually means more client campaigns and more mailboxes to set up.

Facts used: Akimbo is hiring for an outbound role; akimbo.eu receives email on Google Workspace
