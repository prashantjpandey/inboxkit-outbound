# Skill: write first lines

**Input:** `data/to_personalise.jsonl`, one JSON object per lead with `id`, `first_name`, `company`, `facts` (a list of true, checked statements built by `scripts/personalise.py prepare`) and `angle` (which fact to lead with).
**Output:** `data/first_lines.jsonl`, one object per lead: `{"id": ..., "first_line": ...}`. Then run `python scripts/personalise.py apply`.

## The line

One sentence, 12 to 25 words, that opens email step 1. It must:

1. Use **only** the facts given. Never add a number, a client, a tool or a claim that is not in `facts`.
2. Lead with the fact named in `angle`:
   - `domain_gap`: state the record gap plainly and calmly, e.g. "Noticed {company}'s main domain has no DMARC record, which is easy to miss while you're busy hiring."
   - `dmarc_none`: phrase it gently, as an observation. A `p=none` policy is often deliberate.
   - `hiring`: name the role they are hiring for and connect it to more sending, e.g. "Saw {company} is hiring an SDR, which usually means more clients and more mailboxes to set up."
3. Talk about their main domain only. Never say their emails land in spam or that their deliverability is bad. We have not seen their sending domains.
4. No em dashes or en dashes. No exclamation marks. No question in the first line (the email's one ask comes later).
5. Sound like one operator writing to another: plain words, no flattery ("love what you're doing"), no "I hope this finds you well".

## Check before writing the file

- Every line passes `python scripts/lint_copy.py --first-lines data/first_lines.jsonl`.
- Read three lines aloud. If any sounds templated, rewrite it.
