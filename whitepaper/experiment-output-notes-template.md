# Experiment log — <title>

## Session

- Date / time / timezone:
- Experiment ID:
- Objective:
- Hypothesis / expected outcome:
- Remote SSH target:
- VM name / role: baseline / hardened / variant
- Starting snapshot:
- OS / kernel:
- Working directory:
- OpenSCAP / content version / profile (if applicable):
- Evidence directory:

## How to use this log

Send only the contents of each `sh` block to your remote shell.
Do not include a leading `$` prompt or the Markdown fences.
Paste the resulting output into the `text` block immediately below.
Markdown itself does not execute commands; use your existing Vim-to-SSH workflow.
Duplicate the step section for each command or small related group.
Record observations separately from interpretation. Preserve errors and unexpected results.
Use a new step for retries so the original evidence remains intact.

## Step 01 — Confirm session context

**Purpose:** Confirm which host, account, and directory this session uses.

**Run on:** remote server

**Commands:**

```sh
date -Is
hostname
whoami
pwd
uname -r
```

**Output:**

```text
<paste output here>
```

**Observations:**

-

**Interpretation / notes:**

-

## Step 02 — <action or measurement>

**Time:**
**Run on:** <remote VM or local workstation>
**Purpose:**
**Expected result:**
**Preconditions / starting state:**

**Commands:**

```sh
# Replace this comment with the command(s).
```

**Output:**

```text
<paste stdout and stderr here; explicitly note if there was no output>
```

**Exit status:** <if captured>
**Evidence file(s):** <path to full log, XML, HTML, configuration, etc.>

**Observations — what actually happened:**

-

**Interpretation — what the evidence suggests:**

-

**Unexpected behavior / functionality impact:**

-

**Next action:**

-

## Before / after comparison

Use the same measurement in both states. Record any other differences.

| Measurement / rule / service | Before | After | Evidence |
| --- | --- | --- | --- |
| | | | |

- Change applied:
- Variables held constant:
- Other changes / possible confounders:
- Reboot or service restart performed:
- Snapshot / rollback point after the change:

## Report enrichment notes (optional)

- XCCDF rule ID:
- Observed result: pass / fail / other
- Relevant service / configuration:
- Proposed ATT&CK technique or CVE association:
- Source URL / version / date consulted:
- Applicability conditions:
- Mapping rationale:
- Confidence / review status:
- How context changed after remediation:

Do not treat a failed configuration rule alone as proof that a CVE is present
or that an attack will succeed. Record the evidence supporting the association.

## Session outcome

- Completed:
- Main finding:
- Evidence supporting it:
- Limitations / unanswered questions:
- Current VM state:
- Next experiment:
- Useful material for the weekly report:

## Reusable minimal step

### <step number> — <title>

**Run on:**
**Purpose:**

```sh
# Command(s) here.
```

```text
Output here.
```

**Notes:**

-
