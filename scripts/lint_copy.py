"""Check copy against the brief's rules before anything is staged.

Rules:
- no em or en dashes; one ask (at most one question mark) per message
- no links inside messages (plain text places better and keeps the ask on the reply)
- messages are shown as the example lead receives them: no unfilled {{placeholders}}, and each
  one names the example lead's company or domain (declared in an '**Example lead:**' line)
- every email ends with a sign-off
- any message that makes a product claim carries a 'Sources (not sent)' note, and the file has a
  '## Claim sources' table linking the inboxkit.com page for each claim
- the opt-out footer the sequencer adds to every email is declared once in the file

Copy file format: each message is a '### ' section (ending at the next '## ' heading). The message
itself is the '**Subject:**' line plus the quoted '> ' lines; anything else in the section is a note.
Sections whose title starts with 'Email' are emails.
Usage:
  python scripts/lint_copy.py deliverables/copy.md
  python scripts/lint_copy.py --first-lines data/first_lines.jsonl
"""
import argparse
import json
import re
import sys

DASHES = re.compile("[–—]")
OPT_OUT = re.compile(r"reply ['\"]?(no|stop|unsubscribe)|unsubscribe|won't email again|not reach out again", re.I)
CLAIM_WORDS = re.compile(r"\b(mailbox|mailboxes|warmup|InfraGuard|DNS|DMARC|SPF|DKIM|Azure|white.label|\$\d|per month)\b", re.I)


LINK = re.compile(r"https?://|www\.", re.I)


def sections(text):
    parts = re.split(r"^### (.+)$", text, flags=re.M)
    # a section ends at the next level-2 heading (e.g. '## Claim sources')
    return [(parts[i].strip(), re.split(r"^## ", parts[i + 1], flags=re.M)[0]) for i in range(1, len(parts), 2)]


def body_of(sec):
    """Message text only: the subject line plus the quoted ('> ') lines; notes and sources are not sent."""
    lines = [l for l in sec.splitlines() if l.startswith(">") or l.startswith("**Subject:**")]
    return "\n".join(l.lstrip("> ").replace("<br>", "") for l in lines)


def example_lead(text):
    """'**Example lead:** Mustafa, Scalemill (scalemill.com).' -> ['Scalemill', 'scalemill.com']"""
    m = re.search(r"\*\*Example lead:\*\*\s*[^,]+,\s*([^(]+)\(([^)]+)\)", text)
    return [m.group(1).strip(), m.group(2).strip()] if m else []


def lint_copy(path):
    errors = []
    text = open(path, encoding="utf-8").read()
    for m in DASHES.finditer(text):
        line = text[: m.start()].count("\n") + 1
        errors.append(f"line {line}: em/en dash")
    if not OPT_OUT.search(text):
        errors.append("no opt-out footer declared for the emails")
    sources = re.split(r"^## Claim sources", text, flags=re.M)
    if len(sources) < 2 or "inboxkit.com" not in sources[1]:
        errors.append("missing '## Claim sources' table with inboxkit.com links")
    lead = example_lead(text)
    if not lead:
        errors.append("missing '**Example lead:** Name, Company (domain).' line")
    for title, sec in sections(text):
        body = body_of(sec)
        if not body.strip():
            errors.append(f"{title}: no message found (quote the message with '> ')")
            continue
        if body.count("?") > 1:
            errors.append(f"{title}: {body.count('?')} question marks (one ask per message)")
        if LINK.search(body):
            errors.append(f"{title}: link inside the message")
        if "{{" in body:
            errors.append(f"{title}: unfilled placeholder; show the message as the example lead receives it")
        if lead and not any(x in body for x in lead):
            errors.append(f"{title}: not personalised to the example lead ({' / '.join(lead)})")
        if title.lower().startswith("email") and not re.search(r"^(Best|Thanks|Cheers|Regards),\s*$", body, re.M):
            errors.append(f"{title}: no sign-off")
        if CLAIM_WORDS.search(body) and not re.search(r"Sources \(not sent\):", sec):
            errors.append(f"{title}: product claim without a 'Sources (not sent)' note")
    return errors


def lint_lines(path):
    errors = []
    for n, l in enumerate(open(path, encoding="utf-8"), 1):
        line = json.loads(l)["first_line"]
        words = len(line.split())
        if DASHES.search(line):
            errors.append(f"row {n}: em/en dash")
        if "?" in line or "!" in line:
            errors.append(f"row {n}: question or exclamation mark")
        if not 8 <= words <= 30:
            errors.append(f"row {n}: {words} words")
        if re.search(r"spam|deliverability is (bad|poor)", line, re.I):
            errors.append(f"row {n}: claims their mail lands in spam")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--first-lines", action="store_true")
    a = ap.parse_args()
    errors = lint_lines(a.path) if a.first_lines else lint_copy(a.path)
    for e in errors:
        print("FAIL", e)
    print(f"[lint] {a.path}: {'OK' if not errors else str(len(errors)) + ' problem(s)'}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
