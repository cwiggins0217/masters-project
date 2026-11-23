#!/usr/bin/env python3
"""Assemble an offline OpenSCAP demonstration from saved reports."""

from pathlib import Path
from shutil import copy2
from html import escape
import hashlib

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "demo"
REPORTS = DEMO / "reports"

REPORTS.mkdir(parents=True, exist_ok=True)

sources = {
    "EXP-01 — Original baseline": (
        "evidence/EXP-01/20261104T203112Z/pre/report.html",
        "exp01-original-pre.html",
    ),
    "EXP-01 — Original post-hardening": (
        "evidence/EXP-01/20261104T203112Z/post/report.html",
        "exp01-original-post.html",
    ),
    "EXP-01 — Enriched baseline": (
        "reports/EXP-001/20261104T203112Z/pre-enriched.html",
        "exp01-enriched-pre.html",
    ),
    "EXP-01 — Enriched post-hardening": (
        "reports/EXP-001/20261104T203112Z/post-enriched.html",
        "exp01-enriched-post.html",
    ),
#    "EXP-02 — Original baseline": (
#        "evidence/EXP-02/20261106T171339Z/baseline/report.html",
#        "exp02-original-baseline.html",
#    ),
#    "EXP-03 — Original baseline": (
#        "evidence/EXP-03/20261116/exp03-evidence/"
#        "pre-scan-20261116T214109Z/report.html",
#        "exp03-original-pre.html",
#    ),
#    "EXP-03 — Original post-hardening": (
#        "evidence/EXP-03/20261116/exp03-evidence/"
#        "post-20261116T214632Z/report.html",
#        "exp03-original-post.html",
#    ),
}

links = []
missing = []

for title, (source, destination) in sources.items():
    src = ROOT / source
    dst = REPORTS / destination

    if src.is_file():
        copy2(src, dst)
        links.append((title, f"reports/{destination}"))
        print(f"Copied: {source}")
    else:
        missing.append(source)
        print(f"MISSING: {source}")

# Copy the current curated context file when available.
context = ROOT / "tools/openscap/lab-content/ubuntu2404-context.xml"
if context.is_file():
    target = DEMO / "context" / "ubuntu2404-context.xml"
    target.parent.mkdir(parents=True, exist_ok=True)
    copy2(context, target)
    print("Copied: current enrichment context")
else:
    print("NOTE: current enrichment context not found")

def section(title, description, items):
    rows = "\n".join(
        f'<li><a href="{escape(path, quote=True)}">'
        f'{escape(name)}</a></li>'
        for name, path in items
    )
    if not rows:
        rows = "<li>No report artifacts available</li>"

    return (
        f'<section><h2>{escape(title)}</h2>'
        f'<p>{escape(description)}</p><ul>{rows}</ul></section>'
    )

imported_reports = {
    "EXP-01 — Assessed baseline": "exp01-pre-assessed.html",
    "EXP-01 — Assessed post-hardening": "exp01-post-assessed.html",
    "EXP-01 — Assessed follow-up": "exp01-followup-assessed.html",
    "EXP-02 — Original baseline": "exp02-original-baseline.html",
    "EXP-03 — Original baseline": "exp03-original-pre.html",
    "EXP-03 — Original post-hardening": "exp03-original-post.html",
}

existing_destinations = {path for _, path in links}

for title, filename in imported_reports.items():
    destination = f"reports/{filename}"
    if (DEMO / destination).is_file() and destination not in existing_destinations:
        links.append((title, destination))

exp01 = [x for x in links if x[0].startswith("EXP-01")]
exp02 = [x for x in links if x[0].startswith("EXP-02")]
exp03 = [x for x in links if x[0].startswith("EXP-03")]

page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenSCAP — Enrichment and Assessment Demonstration</title>
<style>
:root { color-scheme: light; }
body {
    max-width: 980px;
    margin: 3rem auto;
    padding: 0 1.5rem;
    font: 16px/1.65 system-ui, sans-serif;
    background: #f7f7f5;
    color: #252a2b;
}
header { border-bottom: 1px solid #ccd0cf; padding-bottom: 1.5rem; }
h1 { font-size: 2rem; line-height: 1.2; }
h2 { font-size: 1.3rem; }
section {
    background: white;
    border: 1px solid #dadddc;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
}
a { color: #205b7a; }
li { margin: .5rem 0; }
table { width: 100%; border-collapse: collapse; }
td, th { padding: .6rem; border-bottom: 1px solid #ddd; text-align: left; }
footer { color: #666; font-size: .85rem; margin: 2rem 0; }
</style>
</head>
<body>
<header>
<h1>OpenSCAP Report Enrichment and Assessment</h1>
<p>Master's project — Ubuntu 24.04 LTS, ComplianceAsCode 0.1.82</p>
<p>An offline demonstration of contextual security reporting,
compliance assessment, and observed operational impact.</p>
</header>
<main>
"""

page += section(
    "EXP-01 — SSH",
    "Compare standard OpenSCAP results with project-enriched reports. "
    "Phase-dependent assessed reports will be added after their inputs "
    "are located and verified.",
    exp01,
)
page += section(
    "EXP-02 — nginx",
    "Running to disabled to masked: HTTP availability was lost "
    "before the service-disabled rule changed from FAIL to PASS.",
    exp02,
)
page += section(
    "EXP-03 — Cron",
    "Directory permissions changed from 0755 to 0700. The selected "
    "compliance rule passed, unprivileged read access was restricted, "
    "and the tested heartbeat continued executing.",
    exp03,
)

page += """
<section>
<h2>Experiment comparison</h2>
<table>
<tr><th>Experiment</th><th>Compliance</th><th>Observed functionality</th></tr>
<tr><td>SSH</td><td>Root-login FAIL → PASS</td>
<td>Root and administrator access tests</td></tr>
<tr><td>nginx</td><td>Service FAIL → FAIL → PASS</td>
<td>HTTP service unavailable after disabling</td></tr>
<tr><td>Cron</td><td>Directory permissions FAIL → PASS</td>
<td>Test heartbeat continued</td></tr>
</table>
</section>
<section>
<h2>Scope and limitations</h2>
<p>Security explanations are curated and project-authored.
Rule compliance, functionality, and attacker capability are
separate measurements. The available experiments do not establish
comprehensive resistance to attack.</p>
</section>
</main>
<footer>Generated from preserved repository artifacts.
Source files are not modified by this builder.</footer>
</body></html>
"""

(DEMO / "index.html").write_text(page, encoding="utf-8")

# Create a manifest for current demo files, excluding the manifest itself.
manifest = DEMO / "SHA256SUMS"
with manifest.open("w") as out:
    for path in sorted(DEMO.rglob("*")):
        if not path.is_file() or path == manifest:
            continue
        relative = path.relative_to(DEMO)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        out.write(f"{digest}  {relative}\n")

print(f"\nBuilt: {DEMO / 'index.html'}")

if missing:
    print("\nMissing sources:")
    for source in missing:
        print(f"  {source}")
    raise SystemExit(1)
