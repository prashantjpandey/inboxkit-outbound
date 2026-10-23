# ICP: AI-SDR companies (practice segment)

This file is the only input that changes between campaigns. Copy it over `icp.md`, rerun, get a new list.

```json
{
  "name": "ai-sdr-companies",
  "company": {
    "keyword_tags": ["ai sdr", "ai sales agent", "ai outbound", "sales automation", "ai agents"],
    "employee_ranges": ["11,50", "51,200"],
    "hiring_for": ["sales development representative", "account executive", "deliverability", "email deliverability", "growth"],
    "locations": []
  },
  "person": {
    "titles": ["founder", "co-founder", "ceo", "cto", "head of growth", "vp engineering", "head of deliverability"],
    "max_per_company": 2,
    "max_per_company_note": "founder or CEO first, then whoever owns sending infrastructure (CTO, deliverability, growth)"
  },
  "limits": {
    "companies": 20,
    "max_enrich_credits": 10
  }
}
```

## Who we want

Software companies whose product is an AI SDR or AI outbound agent that **sends cold email on behalf of its customers**. They need mailboxes at scale for every customer, so infrastructure is part of their product. The buyer is the founder, the CTO or the person who owns deliverability.

**Qualifies:** the website says the product sends outbound or cold email automatically (an "AI SDR", "AI BDR", "autonomous outbound" or "AI sales agent" that books meetings).

**Does not qualify:**
- sequencers and data tools without an AI agent (they are integrations or partners)
- AI tools for calling only, chat, support or inbound
- agencies (that is a different campaign)
- anyone in `config/suppression.csv` (11x is already an InboxKit logo customer)

## Why now (signals, in priority order)

Every company needs signal 1 or signal 2.

1. **Hiring sales or deliverability roles** (tier 1): growth means more customer mailboxes to run.
2. **A gap on their own domain** (tier 2 when it is the only signal): no DMARC, no SPF, duplicate SPF, or DMARC at `p=none`.

## Offer and CTA

The same free 30-minute infrastructure audit (https://www.inboxkit.com/demo). For this segment the conversation usually turns to the API and white-label, which the copy can mention with links.
