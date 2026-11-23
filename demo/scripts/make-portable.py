#!/usr/bin/env python3
"""Publish regenerated EXP-01 HTML with portable evidence links."""

from pathlib import Path
from urllib.parse import quote
import html
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "staging"
REPORTS = ROOT / "reports"
EVIDENCE = ROOT / "evidence" / "EXP-01"

LAB_PREFIX = (
    "file:///home/attacker/masters-project/evidence/"
    "EXP-01/20261104T203112Z/"
)

PHASES = {
    "pre": "pre",
    "post": "post",
    "followup": "followup-permissions-20261105T184154Z",
}

REPORTS.mkdir(parents=True, exist_ok=True)

for phase, source_dir in PHASES.items():
    source_report = (
        STAGING / "reports" / f"exp01-{phase}-assessed.html"
    )
    input_dir = STAGING / "inputs" / phase
    evidence_dir = EVIDENCE / phase

    if not source_report.is_file():
        raise SystemExit(f"Missing report: {source_report}")

    evidence_dir.mkdir(parents=True, exist_ok=True)

    for filename in ("results.xml", "sshd-effective.txt"):
        source = input_dir / filename
        if not source.is_file():
            raise SystemExit(f"Missing evidence: {source}")

        shutil.copy2(source, evidence_dir / filename)

    report = source_report.read_text(encoding="utf-8")

    # Only rewrite exact file URLs for this experiment.
    for filename in ("results.xml", "sshd-effective.txt"):
        old = LAB_PREFIX + source_dir + "/" + filename
        new = (
            "../evidence/EXP-01/"
            + phase + "/"
            + quote(filename)
        )

        # Replace link targets, leaving prose and other URLs intact.
        report = report.replace(
            'href="' + old + '"',
            'href="' + new + '"',
        )
        report = report.replace(
            "href='" + old + "'",
            "href='" + new + "'",
        )

    destination = REPORTS / f"exp01-{phase}-assessed.html"
    destination.write_text(report, encoding="utf-8")

    # Confirm all lab-local links have been eliminated.
    remaining = re.findall(
        r"""href=["']file:///home/attacker/[^"']+["']""",
        report,
    )
    if remaining:
        raise SystemExit(
            f"Unresolved lab links in {destination}: {remaining}"
        )

    # Confirm the evidence links actually exist.
    for filename in ("results.xml", "sshd-effective.txt"):
        target = EVIDENCE / phase / filename
        assert target.is_file(), target

    print(f"Published: {destination}")

print("Portable EXP-01 reports published.")
