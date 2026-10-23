# ICP: growing outbound agencies

This file is the only input that changes between campaigns. Swap it, rerun, get a new list.
The JSON block is read by the scripts. The prose is read by Claude in the qualify and first-line steps.

```json
{
  "name": "growing-outbound-agencies",
  "company": {
    "keyword_tags": ["lead generation", "cold email", "outbound", "appointment setting", "b2b lead generation"],
    "employee_ranges": ["1,10", "11,50", "51,200"],
    "hiring_for": ["sales development representative", "sdr", "cold email", "outbound", "lead generation specialist", "appointment setter", "deliverability", "campaign manager"],
    "locations": []
  },
  "person": {
    "titles": ["founder", "co-founder", "ceo", "head of growth", "managing director", "owner"],
    "max_per_company": 2,
    "max_per_company_note": "a third contact is allowed only when it is the ops, delivery or tech lead who owns sending"
  },
  "limits": {
    "companies": 150,
    "max_enrich_credits": 100
  }
}
```

## Who we want

Founders and heads of growth at outbound, lead-gen and GTM agencies: the person who owns the sending infrastructure, not the reps who use it.

**Qualifies:** the company runs cold email or outbound for clients (lead generation agency, appointment setting agency, outbound or GTM agency, SDR-as-a-service). Agencies that also do LinkedIn or calling still qualify if email is part of the service.

**Does not qualify:**
- software vendors, including data tools and sequencers (they are partners or competitors, not buyers)
- businesses that are not agencies (cleaning, remodelling, retail) even if Apollo tags them "lead generation"
- pure telemarketing or call centres with no email service
- recruitment firms, unless they clearly sell outbound lead generation to clients

## Why now (signals, in priority order)

Every company needs signal 1 or signal 2 (the pipeline drops any with neither).

1. **Hiring outbound roles** (tier 1). More clients means more mailboxes and more setup work.
2. **A gap on their own domain** (tier 2 when it is the only signal): no DMARC, no SPF, duplicate SPF records, or DMARC at `p=none`. This leads into the audit offer.
3. **Sells mailboxes or infrastructure to clients** (website mentions done-for-you domains or inboxes). A tag for the white-label conversation, not a separate campaign.

## Offer and CTA

A free 30-minute infrastructure audit (https://www.inboxkit.com/demo). One ask per message.
