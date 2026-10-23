"""Check copy against the brief's rules before anything is staged.

Rules: no em or en dashes; one ask (at most one question mark) per message; every email has an
opt-out; any message that makes a product claim links a page on inboxkit.com.

Copy file format: each message is a '### ' section. Sections whose title starts with 'Email' are emails.
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


def sections(text):
    parts = re.split(r"^### (.+)$", text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def body_of(sec):
    """Message text only: drop the 'Sources' / notes lines that start with '>'."""
    return "\n".join(l for l in sec.splitlines() if not l.startswith(">"))


def lint_copy(path):
    errors = []
    text = open(path, encoding="utf-8").read()
    for m in DASHES.finditer(text):
        line = text[: m.start()].count("\n") + 1
        errors.append(f"line {line}: em/en dash")
    for title, sec in sections(text):
        body = body_of(sec)
        if body.count("?") > 1:
            errors.append(f"{title}: {body.count('?')} question marks (one ask per message)")
        if title.lower().startswith("email") and not OPT_OUT.search(body):
            errors.append(f"{title}: no opt-out")
        if CLAIM_WORDS.search(body) and "inboxkit.com" not in sec:
            errors.append(f"{title}: product claim without an inboxkit.com link")
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
