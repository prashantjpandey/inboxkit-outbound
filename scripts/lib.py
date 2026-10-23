"""Shared helpers. Standard library only, so the repo runs from a clean checkout."""
import csv
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env():
    """Read .env into os.environ without overriding real environment variables."""
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def load_icp(path=None):
    """Return the JSON block from icp.md."""
    text = Path(path or ROOT / "icp.md").read_text(encoding="utf-8")
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if not m:
        raise SystemExit("icp.md has no ```json block``` with filters")
    return json.loads(m.group(1))


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = []
        for r in rows:
            fields += [k for k in r if k not in fields]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def norm_domain(value):
    """'https://www.Acme.io/about' -> 'acme.io'."""
    v = (value or "").strip().lower()
    if not v:
        return ""
    if "://" not in v:
        v = "http://" + v
    host = urllib.parse.urlparse(v).hostname or ""
    return host[4:] if host.startswith("www.") else host


_SUFFIXES = r"\b(ltd|llc|inc|gmbh|bv|limited|agency|group|co)\b"


def company_tokens(name):
    """'Hypergen - B2B Cold-Email, LLC' -> ['hypergen', 'b2b', 'cold', 'email']."""
    n = re.sub(_SUFFIXES, " ", (name or "").lower())
    return re.findall(r"[a-z0-9]+", n)


def norm_company(name):
    """'The Lead Giants, LLC' -> 'theleadgiants' (the part before ' - ' or '|')."""
    return "".join(company_tokens((name or "").split(" - ")[0].split("|")[0]))


def doh(name, rtype):
    """DNS-over-HTTPS lookup via Google's public resolver. Returns answer strings."""
    url = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": name, "type": rtype})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.load(r)
            break
        except OSError:
            if attempt == 2:
                raise
    return [a["data"].replace('" "', "").strip('"') for a in data.get("Answer", [])]


def log(step, msg):
    print(f"[{step}] {msg}")
