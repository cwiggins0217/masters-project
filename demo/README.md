# OpenSCAP Report Enrichment and Assessment Demonstration

## Purpose

Demonstrate an extension to OpenSCAP's XCCDF report
generation that adds:

1. Curated, rule-specific security context.
2. Evidence-based assessment of compliance findings.
3. Explanations of operational consequences and limitations.

## Environment

Target operating system: Ubuntu 24.04 LTS
Security content: ComplianceAsCode 0.1.82
Profile: CIS Level 1 Server

## Experiments

### EXP-01: SSH hardening

Compare baseline, post-hardening, and follow-up reports.

Demonstrates rule enrichment, evidence-based assessment,
and interpretation of administrative-access behavior.

### EXP-02: nginx hardening

Compare three states:

- Baseline: nginx running, HTTP available, both rules FAIL.
- Disabled: nginx inactive, HTTP unavailable, both rules FAIL.
- Masked: nginx inactive and masked, HTTP unavailable,
  service-disabled rule PASS.

Demonstrates why OVAL implementation details and
functionality measurements matter.

### EXP-03: Cron directory permissions

Compare pre- and post-intervention states.

- /etc/cron.d mode: 0755 to 0700.
- file_permissions_cron_d: FAIL to PASS.
- Unprivileged directory listing and file reading denied.
- Tested scheduled heartbeat remains operational.

## Scope and limitations

The enrichment content is project-authored and pending
independent review.

The experiments establish selected compliance and operational
effects, not comprehensive resistance to attack.

The demonstration uses preserved evidence rather than
performing live hardening on production systems.

## Reproducibility

The final bundle will include the report inputs, selected
evidence, generation instructions, and file integrity hashes.
