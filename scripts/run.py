"""Run the deterministic stages of the workflow. Claude does the judgment stages in between (see CLAUDE.md).

  python scripts/run.py sample                 full offline demo on sample/ data -> output/sample_run/
  python scripts/run.py companies --workdir data   snapshot -> suppress -> DNS   (then Claude qualifies)
  python scripts/run.py people    --workdir data   suppress -> verify -> prepare (then Claude writes first lines)
  python scripts/run.py finish    --workdir data   apply first lines -> lint -> export to output/
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from lib import ROOT

PY = [sys.executable]
EXTRA_SUPPRESSION = []  # sample mode adds sample/suppression_sample.csv


def step(script, *args):
    cmd = PY + [str(ROOT / "scripts" / script), *map(str, args)]
    if subprocess.run(cmd, cwd=ROOT).returncode != 0:
        raise SystemExit(f"stage failed: {script} {' '.join(map(str, args))}")


def companies(wd, offline=False, fixture=None):
    step("snapshot.py", wd / "companies.csv", *(["--offline"] if offline else []))
    step("suppress.py", "companies", wd / "companies.csv", wd / "companies_clean.csv", *EXTRA_SUPPRESSION)
    step("dns_check.py", wd / "companies_clean.csv", *(["--fixture", fixture] if fixture else []))


def people(wd, mx_fixture=None):
    step("suppress.py", "people", wd / "people_enriched.csv", wd / "people_clean.csv", *EXTRA_SUPPRESSION,
         "--companies", wd / "companies_clean.csv")
    step("verify.py", wd / "people_clean.csv", wd / "people_verified.csv", *(["--mx-fixture", mx_fixture] if mx_fixture else []))
    step("personalise.py", "prepare", "--workdir", wd)


def finish(wd, out):
    step("personalise.py", "apply", "--workdir", wd)
    step("lint_copy.py", "--first-lines", wd / "first_lines.jsonl")
    step("export.py", "--workdir", wd, "--out", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["sample", "companies", "people", "finish"])
    ap.add_argument("--workdir", default="data")
    ap.add_argument("--out", default="output")
    a = ap.parse_args()

    if a.stage == "sample":
        wd = ROOT / "output" / "sample_run"
        shutil.rmtree(wd, ignore_errors=True)
        wd.mkdir(parents=True)
        for f in ("companies.csv", "people_enriched.csv"):
            shutil.copy(ROOT / "sample" / f, wd / f)
        EXTRA_SUPPRESSION.extend(["--extra-suppression", ROOT / "sample" / "suppression_sample.csv"])
        companies(wd, offline=True, fixture=ROOT / "sample" / "dns_fixture.json")
        people(wd, mx_fixture=ROOT / "sample" / "mx_fixture.json")
        step("personalise.py", "template", "--workdir", wd)
        finish(wd, wd)
        print((wd / "run_report.md").read_text(encoding="utf-8"))
        return

    wd = (ROOT / a.workdir) if not Path(a.workdir).is_absolute() else Path(a.workdir)
    {"companies": lambda: companies(wd),
     "people": lambda: people(wd),
     "finish": lambda: finish(wd, ROOT / a.out)}[a.stage]()


if __name__ == "__main__":
    main()
