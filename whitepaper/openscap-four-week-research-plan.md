# OpenSCAP Report Enrichment: Four-Week Research Plan

Planning period: November 2–29, 2026  
Final submission: November 30, 2026  
Weekly reports: November 9, 16, 23, and 30  
Status: Proposed method and reusable templates; no experimental results asserted.

## 1. Research objective and boundaries

Develop and evaluate an enrichment layer that connects OpenSCAP compliance findings to relevant adversary behaviors, applicable vulnerabilities, host-specific prerequisites, and operational consequences. Refresh the assessment after remediation using a new scan and new host evidence.

**Research question:** How accurately can contextual enrichment explain selected compliance findings and track changes in attack prerequisites and service behavior after remediation?

Three supporting questions:

1. Can selected rule-to-threat mappings be justified with explicit sources and prerequisites?
2. Does the report correctly update its interpretation after remediation and rollback?
3. What security and legitimate-service changes are observed in controlled experiments?

The primary contribution is the enrichment method and its evaluation. Penetration-testing scenarios supply evidence for selected explanations. Do not claim comprehensive penetration-test coverage, universal ATT&CK prevention, or improved administrator decision-making without a separate user evaluation.

### Fixed scope

| Item | Commitment |
|---|---|
| Platform | Ubuntu Server 24.04 in Proxmox |
| Profile | One identified CIS Level 1 Server profile, with exact content version and hash |
| Enrichment | Six rules minimum; up to ten only if the minimum is complete |
| Families | SSH authentication; unnecessary service exposure; permissions or auditing |
| Experiments | Three defined scenarios, each with legitimate-function tests |
| Remediation | Preserved OpenSCAP-generated script for whole-profile comparison |
| Isolation | Selected-control interventions recorded as exact configuration changes or verified selected remediation |
| Dynamic operation | Explicit rescan and host-fact refresh, rather than continuous monitoring |
| CVEs | Only evidence-supported applicability; no requirement to attach a CVE to every rule |
| Deliverables | Mapping dataset, enrichment prototype, evidence records, four reports, whitepaper |

Reuse the existing lab where its provenance can be established. Inventory it before rebuilding anything. Freeze exact rule IDs by the end of Week 1. If a useful test involves a setting outside the selected profile, label it supplementary rather than claiming that the profile checks it.

## 2. Four-week roadmap

### Week 1 — November 2–8: Establish the method and complete one cycle

**Goal:** Complete one defensible before/after SSH example from raw evidence through enriched report.

- [ ] Inventory existing baseline and hardened VMs, snapshots, scans, scripts, and prototype work.
- [ ] Record OS, kernel, package, OpenSCAP, profile, and SCAP content versions.
- [ ] Select six actual rules across three families; explain each selection.
- [ ] Define mapping fields, review states, host assessment states, and evidence paths.
- [ ] Define EXP-001: SSH hypothesis, prerequisites, success criteria, and approved access tests.
- [ ] Capture the baseline, apply the selected intervention, rescan, and repeat identical tests.
- [ ] Produce enriched before/after outputs and a documented comparison.
- [ ] Write the whitepaper problem statement, scope, and initial methods.

**Acceptance gate:** One experiment can be traced from a report statement to a mapping, a scan, host facts, and raw test evidence. A remaining failure or inconclusive outcome is acceptable if correctly represented.

**Report due November 9:** Scope table, mapping schema, EXP-001 record, report comparison, and problems discovered.

### Week 2 — November 9–15: Complete scenarios and the profile comparison

**Goal:** Establish experimental coverage for all three families.

- [ ] Review and document all six mappings, including sources and limitations.
- [ ] Run EXP-002 for selected network-service exposure and required service functionality.
- [ ] Run EXP-003 for permissions, or auditing if selected in Week 1.
- [ ] Create or verify H0 from the documented baseline using the preserved profile remediation.
- [ ] Run the same scenario and functionality suite against B and H0.
- [ ] Perform isolated comparisons needed to explain individual-control effects.
- [ ] Record removed services, failed remediation, restarts, dependencies, and broken workflows.
- [ ] Extend the prototype to handle all selected rules and missing evidence explicitly.
- [ ] Draft the enrichment architecture and experimental setup sections.

**Acceptance gate:** Each scenario has a written hypothesis, a valid starting condition, raw evidence, a paired legitimate-function test, and an explicit outcome. No unsupported finding is presented as confirmed exposure.

**Report due November 16:** Three experiment records, six mapping records, whole-profile results, and an initial operational-impact table.

### Week 3 — November 16–22: Validate transitions and repeatability

**Goal:** Determine where the enrichment is correct, incorrect, or uncertain.

- [ ] Complete three clean-state runs per condition for the primary comparison of each scenario: target 18 runs across three scenarios and two conditions.
- [ ] Report whole-profile runs separately if they are additional to those primary comparisons.
- [ ] Verify remediation and rollback transitions using fresh scans and host facts.
- [ ] Evaluate edge cases against a manually prepared expected-outcome table.
- [ ] Include failed remediation, missing host evidence, and failure with an absent attack prerequisite.
- [ ] Test handling of non-binary scan outcomes using clearly labelled fixtures where necessary.
- [ ] Request a mapping review from the professor or a colleague; record whether review occurred.
- [ ] Correct misleading explanations and record the reason for each correction.
- [ ] Draft results and threats to validity.

**Acceptance gate:** Every evaluated case is marked correct, incorrect, or indeterminate against documented expectations. Repeated trials and fixtures are distinguishable from independent real-host conditions.

**Report due November 23:** Evaluation matrix, repeatability summary, mapping review status, unresolved discrepancies, and preliminary conclusions.

### Week 4 — November 23–29: Freeze, reproduce, and write

**Goal:** Deliver a reproducible whitepaper supported by a stable evidence package.

- [ ] Freeze features and mappings on November 23; allow correctness fixes with a change record.
- [ ] Reproduce one complete scenario from the written instructions and clean snapshots.
- [ ] Close critical evidence gaps; report unresolved limitations rather than expanding scope.
- [ ] Finish results tables and evidence-linked case studies.
- [ ] Complete discussion, limitations, conclusion, and references.
- [ ] Audit every substantive claim against an evidence path or source.
- [ ] Ensure report examples use the final mapping and prototype versions.
- [ ] Prepare a short walkthrough: baseline report, remediation, new report, service consequence.
- [ ] Finalize the whitepaper and evidence index by November 29.

**Acceptance gate:** A reader can identify exactly what was tested, reproduce the procedure, and distinguish measured results from interpretation.

**Report and submission due November 30:** Final progress report, whitepaper, prototype, mapping dataset, reproduction instructions, and evidence index.

### Scope-reduction rule

If progress slips, remove extra rules, interface polish, and automated CVE retrieval first. Retain the six-rule target where feasible, three core scenarios, honest state handling, raw evidence, and writing time. If the minimum becomes infeasible, document the revised denominator and obtain academic scope guidance; do not silently omit failed tests.

## 3. Laboratory design

| State | Definition | Purpose |
|---|---|---|
| B | Documented functional baseline snapshot | Reference for whole-profile effects |
| H0 | Clone of B after preserved profile remediation and rescan | Measure combined hardening effects; not presumed fully compliant |
| A-i / T-i | Two clones of the same parent, differing in one selected intervention | Attribute changes to that control or explicit control bundle |
| Test host | Fixed network location and versioned test tools | Repeat consistent external observations |

For each experiment, declare whether its primary comparison is B/H0 or an isolated A-i/T-i pair. B/H0 can demonstrate aggregate effects but cannot alone identify which rule caused them. A relaxed control in H0 may remain masked by other defenses.

Hold workload, VM resources, network position, test accounts, package versions, and scan content constant within a pair. Freeze updates within experiments, then document any deliberate update separately. Record snapshot lineage and configuration differences. Keep attacks within the owned isolated lab using test credentials and data.

### Scenario definitions to finalize in Week 1

| ID | Candidate scenario | Security observable | Legitimate-function observable |
|---|---|---|---|
| EXP-001 | Selected SSH authentication restriction | Defined authentication path accepted/rejected, with server evidence | Approved key-based administration succeeds |
| EXP-002 | Selected unnecessary service removal or disablement | Service reachable/usable from fixed test position | Required application or transfer task succeeds/fails |
| EXP-003 | Selected file-permission control | Unprivileged test account reads/writes protected test resource or is denied | Authorized account/service can still perform required operation |

If EXP-003 uses auditing instead, measure event presence, attribution, and retrieval. Do not interpret logging alone as attack prevention. A successful valid-password login establishes an authentication path, not a demonstrated password-guessing attack. A port scan establishes reachability, not exploitation.

## 4. Repeatable research workflow

### A. Research and review a mapping

1. Identify the exact rule, title, content version, profile selection, and underlying setting.
2. Read the rule rationale and authoritative documentation for the affected mechanism.
3. Propose an ATT&CK relationship only where the described behavior fits; record the causal explanation.
4. Specify prerequisites: network reachability, authentication mechanism, local privileges, packages, and other controls.
5. Record CVE applicability separately. Check distribution-specific package/advisory status where relevant; a version banner alone is insufficient.
6. Write expected outcomes before executing the experiment.
7. Mark the mapping draft, self-reviewed, independently reviewed, rejected, or needs revision. Record reviewer and date.

### B. Execute a controlled run

1. Assign experiment ID, condition, run number, and timestamp.
2. Restore the specified clean snapshot and verify preconditions.
3. Capture scan results and host facts before testing.
4. Run legitimate-service tests to establish a usable starting state.
5. Execute the predefined bounded security scenario; preserve client output and target evidence.
6. For the treatment condition, apply the documented intervention before its measurement sequence, including required reboot/restart. Record its logs and verify effective state.
7. Generate the enriched output from that condition's scan and facts.
8. Compare observations with the prewritten expectation and with the other condition.
9. Archive the run, including errors and inconclusive results; restore before repetition.

Use the same measurement order in each condition. Tests that modify state require a reset or documented cleanup before subsequent measurements. Never treat an interrupted or invalid test as a blocked attack.

### C. Evaluate dynamic behavior

1. Preserve the baseline report, scan, host facts, and mapping version.
2. Apply remediation and capture a fresh scan plus fresh facts.
3. Regenerate the report and inspect changed explanations, prerequisites, and operational notes.
4. Restore the baseline snapshot and repeat the observation to verify reversal.
5. Hold mapping/prototype versions constant when attributing differences to host changes. Evaluate mapping revisions separately.

Dynamic means the interpretation is recomputed from current evidence. A passing rule retains its threat explanation and history; it does not become a universal statement that the technique is impossible.

### D. Close the session and the week

At the end of each lab session, preserve outputs, update the experiment record, record one finding and one next action, and update the evidence index. At the end of the week, summarize completed evidence rather than hours spent. Move validated findings into the whitepaper immediately.

## 5. Evidence and evaluation rules

Keep these separate:

| Category | Allowed interpretation |
|---|---|
| Scan result | Preserve original pass/fail/error/unknown/notselected/notapplicable and other emitted states |
| Mapping review | Quality/review status of the relationship, independent of host exposure |
| Host applicability | Prerequisites observed, absent, or unresolved, with timestamps |
| Scenario outcome | Succeeded, blocked, prerequisite absent, test error, or inconclusive |
| Functional outcome | Passed, failed, not run, or inconclusive |

Missing or stale evidence must not produce a confident secure state. Record scan and host-fact collection times; define an acceptable collection interval per run. Treat a material configuration change between collection steps as grounds to recollect evidence.

### Evaluation matrix

Prepare expectations manually before viewing the generated explanation. Use at least these cases, distinguishing real-host runs from synthetic fixtures:

| Case | Required behavior |
|---|---|
| Rule fails; scenario prerequisites present | Explain conditional relevance without asserting untested exploitation |
| Rule fails; relevant service absent/unreachable | Explain absent prerequisite and limits of the observation |
| Rule passes after remediation | Show updated evidence and residual limits |
| Remediation does not fix the rule | Retain failure and explain observed state |
| Scan error or required host fact missing | Mark uncertainty; do not assert protection |
| Rule not selected/not applicable | Preserve that distinction |
| Rollback restores initial state | Restore the appropriate contextual interpretation |

Report counts with denominators: reviewed mappings/selected mappings; enriched rules/selected rules; correct determinate cases/all determinate cases; indeterminate cases/all cases; unsupported exposure or protection claims/all evaluated claims. Report security outcomes and functionality outcomes separately. Repeated clones demonstrate repeatability, not independent population-level evidence.

## 6. Evidence organization

Use one project directory, version-controlled for text/code where practical. Keep large raw evidence in dated run directories and reference it from an index.

| Relative path | Contents |
|---|---|
| `plan.md` | Approved scope, milestones, decision log |
| `mappings/` | Versioned rule-to-context records |
| `experiments/EXP-001.md` | Hypothesis, protocol, interpretation, run links |
| `evidence/EXP-001/A/run-01/` | Immutable scan, host facts, test outputs, logs, enriched report |
| `evidence/EXP-001/T/run-01/` | Corresponding treatment evidence |
| `reports/2026-11-09.md` | Weekly report; one dated file per submission |
| `paper/` | Whitepaper draft and figures |
| `evidence-index.md` | Claim-to-evidence links |

Capture stdout, stderr, exit codes, timestamps, effective configuration, relevant service logs, and intervention diffs. Preserve the original XML/ARF and remediation script. Record hashes of key inputs. Keep real credentials and private keys out of shareable evidence.

## 7. Reusable mapping record

```markdown
# Mapping: MAP-___

- Rule ID/title:
- Benchmark/profile/content version:
- Setting and expected value:
- Security purpose:
- ATT&CK technique/sub-technique and dataset version:
- Relationship: prevention / detection / exposure reduction / other
- Mapping rationale:
- Required prerequisites:
- Other relevant controls/dependencies:
- Host evidence required:
- CVE: none established / candidate / confirmed affected / not affected
- CVE applicability evidence and distribution advisory:
- Expected interpretation when failing:
- Expected interpretation when passing:
- Expected interpretation with missing evidence:
- Operational consequence to investigate:
- Sources: URL, title, relevant passage/location, retrieval date
- Review status/reviewer/date:
- Supporting experiment IDs:
- Limits and revisions:
```

## 8. Reusable experiment record

```markdown
# EXP-___: [Scenario title]

## Question and hypothesis

- Question:
- Hypothesis written on:
- Rule/mapping IDs:
- Primary comparison: B/H0 or isolated A/T
- Independent variable/intervention:
- Security success criterion:
- Legitimate-function success criterion:
- Prerequisites and attacker position:
- Confounders and controls:

## Environment and protocol

- Parent snapshot and clone IDs:
- OS/kernel/package versions:
- OpenSCAP/content/profile/hash:
- Prototype/mapping version:
- Test tool versions:
- Reset procedure:
- Intervention, reboot/restart, and verification:
- Ordered test commands/procedure:
- Expected outcomes written before testing:

## Run record (duplicate for each condition and repetition)

- Run ID/condition/date/time/timezone:
- Snapshot restored:
- Preconditions verified:
- Scan and host-fact timestamps:
- Evidence directory:
- Commands and raw output paths:
- Security outcome:
- Legitimate-function outcome:
- Report assessment and expected assessment:
- Agreement: correct / incorrect / indeterminate
- Deviations/errors:

## Comparison and interpretation

| Measure | A or B | T or H0 | Evidence |
|---|---|---|---|
| Rule result | | | |
| Effective setting | | | |
| Security outcome | | | |
| Functional outcome | | | |
| Enriched explanation | | | |

- Observation (what occurred):
- Interpretation (what it supports):
- Alternative explanations:
- Limits (what cannot be concluded):
- Repeatability:
- Report/mapping changes needed:
- Claim suitable for the whitepaper:
- Next action:
```

## 9. Weekly progress report template

Target one to two pages of summary, with links to detailed records. Keep planned work separate from completed results. Copy this template for each of the four reporting dates.

```markdown
# Weekly Research Progress — Week [1–4]

Project: Dynamic Contextual Enrichment of OpenSCAP Reports
Reporting period:
Submission date:
Overall status: on track / at risk / blocked

## 1. Summary

[Three to five sentences: objective, completed evidence, principal finding,
and effect on the next milestone. Do not present expected results as findings.]

## 2. Commitments and completion

| Previous commitment | Status | Evidence/deliverable | Explanation of variance |
|---|---|---|---|
| | Complete / partial / not started | | |

## 3. Experimental results

| Experiment | Conditions and valid run count | Security result | Functional result | Evidence |
|---|---|---|---|---|
| | | | | |

- Invalid/inconclusive runs and reasons:
- Most important observation:
- What the evidence supports:
- What it does not establish:

## 4. Enrichment progress

- Selected rules: ___
- Rules enriched: ___ / ___
- Mappings self-reviewed: ___ / ___
- Mappings independently reviewed: ___ / ___ (reviewer: ___)
- Evaluation cases: correct ___; incorrect ___; indeterminate ___
- Unsupported claims identified and correction status:
- Dynamic transitions verified:
- Mapping/prototype version:

## 5. Whitepaper progress

- Sections drafted or revised:
- New evidence-backed claims/tables:
- References added and relevance:

## 6. Problems, decisions, and scope changes

| Issue | Impact | Action/decision | Owner | Due |
|---|---|---|---|---|
| | | | | |

- Specific guidance requested from professor, if any:

## 7. Next-week commitments

| Deliverable | Acceptance criterion | Target date |
|---|---|---|
| | | |

## 8. Evidence index

- Experiment records:
- Raw run directories:
- Mapping version:
- Before/after report examples:
- Current whitepaper draft:
```

### Week 1 report starter — planned work only

Reporting period: November 2–8. Submission: November 9.

| Commitment | Acceptance evidence | Current status |
|---|---|---|
| Freeze scope and six rule IDs | Scope table and scan references | Planned; inventory not yet verified |
| Complete first SSH cycle | EXP-001 plus raw before/after evidence | Planned |
| Define mapping and state model | Reviewed schema and one populated record | Planned |
| Begin whitepaper | Problem, scope, and methods draft | Planned |

Do not fill the findings section until the runs have been executed. Previously completed work may be credited after its inputs and evidence are verified.

## 10. Whitepaper assembly and completion checklist

Suggested structure: problem and scope; related work; enrichment design; experimental method; results; discussion; limitations; conclusion; reproducibility appendix.

- [ ] Every selected rule has an exact identifier and version.
- [ ] Every mapping has rationale, prerequisites, sources, and review status.
- [ ] CVE claims are supported by applicability evidence or explicitly unresolved.
- [ ] All three scenarios include legitimate-function measurements.
- [ ] Aggregate hardening effects are distinguished from isolated control effects.
- [ ] Repetition, invalid runs, fixtures, and missing observations are disclosed.
- [ ] Dynamic output is demonstrated with fresh evidence and rollback.
- [ ] All claims trace to sources or retained experiment evidence.
- [ ] No claim of universal protection or administrator benefit exceeds the evaluation.
- [ ] Final versions and reproduction instructions are preserved.

## Methodological references

These are starting references established during planning, not evidence that any proposed experiment has run. Record the exact source version and retrieval date when using a source in a mapping.

- [OpenSCAP User Manual](https://static.open-scap.org/openscap-1.4.1/oscap_user_manual.html): machine-readable results, report generation, and remediation workflows. Match commands to the installed version.
- [MITRE CTID Mapping Methodology](https://ctid.mitre.org/mappings/about/methodology/): control capabilities, technique selection, rationale, and mapping review.
- [MITRE ATT&CK Enterprise Mitigations](https://attack.mitre.org/mitigations/): candidate relationships to examine, not automatic proof of host protection.
- [NVD Vulnerability Detail Pages](https://nvd.nist.gov/vuln/vulnerability-detail-pages): vulnerability applicability and affected configurations.
