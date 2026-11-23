#!/usr/bin/env python3
"""Rewrite known EXP-01 file URLs to bundled evidence paths."""

from pathlib import Path
from urllib.parse import quote
import os
import re
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: rewrite-evidence-links.py PHASE REPORT.html")

phase = sys.argv[1]
report_path = Path(sys.argv[2]).resolve()

phases = {
    "pre": "pre",
    "post": "post",
    "followup": "followup-permissions-20261105T184154Z",
}

if phase not in phases:
    sys.exit(f"Invalid phase: {phase}")

demo = Path(__file__).resolve().parents[1]
evidence_dir = demo / "evidence" / "EXP-01" / phase

text = report_path.read_text(encoding="utf-8")
original = text

for filename in ("results.xml", "sshd-effective.txt"):
    target = evidence_dir / filename

    if not target.is_file():
        sys.exit(f"Missing packaged evidence: {target}")

    old = (
        "file:///home/attacker/masters-project/evidence/"
        "EXP-01/20261104T203112Z/"
        f"{phases[phase]}/{filename}"
    )

    relative = os.path.relpath(target, report_path.parent)
    replacement = quote(relative, safe="/.")

    text = text.replace(
        'href="' + old + '"',
        'href="' + replacement + '"',
    )
    text = text.replace(
        "href='" + old + "'",
        "href='" + replacement + "'",
    )

if re.search(r"""href=["']file:///home/attacker/""", text):
    sys.exit("Unresolved absolute evidence link found")

report_path.write_text(text, encoding="utf-8")
print(f"Portable evidence links verified: {report_path}")
