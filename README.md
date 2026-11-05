---
title: "Contextual Enrichment of OpenSCAP Reports: A Method and Initial Ubuntu Case Study"
author: "Christopher Wiggins"
date: "2026-11-05"
version: "0.1"
status: "Initial draft; implementation and evaluation ongoing"
---

# Contextual Enrichment of OpenSCAP Reports: A Method and Initial Ubuntu Case Study

Christopher Wiggins · Master's Project · November 5, 2026

> Draft 0.1 contains the problem statement, bounded research scope, initial methods, and an early case study. Static enrichment is implemented for one rule. Dynamic evidence association, broader mapping coverage, and repeated evaluation are planned. This document does not report those planned capabilities as completed results.

## 1. Introduction and problem statement

OpenSCAP evaluates security configuration using SCAP content and can produce reports from the resulting assessments. ComplianceAsCode supplies machine-readable security policies, including content implementing CIS guidance [1]. These capabilities provide the foundation for this project; the proposed enrichment supplements the existing report rather than replacing its checks or remediation information.

In the initial experiment, a root-login restriction changed one compliance result from fail to pass while another rule changed from pass to fail. Aggregate counts remained unchanged. Examining those totals alone would therefore have missed both the intended improvement and a newly introduced permissions issue. The interpretation required the individual rule results, effective SSH configuration, file-permission observations, and access-test notes.

The problem addressed here is how to present that relationship consistently and traceably. A failed configuration check identifies a departure from the evaluated policy, but a useful explanation of its security relevance also needs the conditions under which a particular access or attack route is possible. A passing result likewise needs a bounded interpretation: it establishes the outcome of that check, not universal protection against an adversary technique. Operational consequences must be evaluated alongside the configuration change when a service or administrative workflow is required.

This project develops a report-enrichment method that separates reusable knowledge about a control from observations about a specific host and from the conclusions drawn using those observations. Its intended output is a report in which each substantive assessment can be traced to a mapping revision, a selected scan result, and supporting evidence. The initial implementation appends curated context to native OpenSCAP HTML. The planned extension will regenerate host-specific interpretations after a new scan and evidence refresh.

The project does not assume that existing tools lack contextual explanations, nor does it claim that this approach is novel across the literature. A comparative related-work review remains necessary before making that claim. Improved administrator comprehension is a motivation, not a measured outcome of the present laboratory study.

## 2. Research questions and scope

The primary research question is: **How accurately can contextual enrichment explain selected OpenSCAP findings and track changes in relevant prerequisites and legitimate functionality after a documented intervention?**

Three questions guide the evaluation:

1. Can each selected control-to-threat relationship be supported by explicit sources, conditions, limitations, and a review record?
2. Does the proposed assessment update appropriately when configuration and scan evidence change, including when evidence is incomplete or conflicting?
3. Which security-relevant behaviors and legitimate functions change in the tested conditions, and how accurately does the report describe those changes?

The study uses Ubuntu Server 24.04 virtual machines on Proxmox and ComplianceAsCode content version 0.1.82. The benchmark identifier is `xccdf_org.ssgproject.content_benchmark_UBUNTU_24-04`; the selected profile is `xccdf_org.ssgproject.content_profile_cis_level1_server`. This version identifies the SCAP content used, not a substituted CIS document edition. The retained datastream hash is provided in Appendix A.

Six rules were selected purposively from observed findings. They provide contrasting interpretation cases rather than a representative sample of the entire benchmark. The common identifier prefix in Table 1 is `xccdf_org.ssgproject.content_rule_`.

**Table 1. Frozen rule sample, scope version 1.0.**

| Family | Rule suffix | Purpose in the study |
|---|---|---|
| SSH authentication | `sshd_disable_root_login` | Relate configuration, a compliance transition, and controlled access tests |
| SSH authentication | `sshd_disable_empty_passwords` | Investigate a failed check alongside an effective setting that disallows empty passwords |
| Service exposure | `service_nginx_disabled` | Compare service state, reachability, and required HTTP functionality |
| Service exposure | `package_nginx_removed` | Distinguish installed software from an active service |
| File permissions | `file_permissions_sshd_config` | Explain actual read/write permissions and administrative consequences |
| File permissions | `file_permissions_sshd_drop_in_config` | Track an observed permissions regression and its correction |

The nginx rules concern the same service, while the permissions rules concern SSH configuration. These dependencies preclude treating all six rules as independent experiments. Three scenario families are planned: SSH authentication, nginx exposure and availability, and configuration-file permissions. EXP-01 supplies initial SSH evidence; the nginx and independent permissions scenarios have not yet been completed.

The study does not require an ATT&CK technique or CVE association for every rule. An unsupported association remains unassigned. CVE applicability is a separate, evidence-dependent assessment of package identity, distribution-specific fixes, and relevant conditions; no CVE detection capability is implemented in the current prototype. Comprehensive penetration-test coverage, population-level risk estimates, and administrator usability outcomes are outside the present evaluation.

## 3. Initial methods

### 3.1 Laboratory and evidence provenance

The baseline notebook identifies `scap-b` as Proxmox VM 200 with two virtual CPUs, 4 GB RAM, and a 64 GB disk. Its clean snapshot is recorded as `b00-clean-os`. The researcher confirmed the experiment target as `scap-exp01`, VM 100, with pre-experiment snapshot `exp01-pre`. Snapshot identifiers are recorded, but independent verification of the complete clone lineage remains outstanding.

Target scans used the system OpenSCAP 1.3.9 installation. Report generation used the custom source branch `feature/report-enrichment`, commit `35efc53f8`, built on a Parrot workstation. Separating scanning from rendering permits the same saved results to be rendered again without repeating the intervention. The current native command exposes `--enrichment` for report generation.

The archive retains pre/post scan XML, ARF, native HTML, effective configuration, scan logs, timestamps, and exit codes. A later permissions correction has its own directory. The researcher reports successful checksum verification of the copied evidence and captured provenance, including the mapping, source revision/status/diff, CMake cache, executable checksum, and version information. This verifies consistency with the recorded manifest at the time of checking; it does not authenticate the original collection time. The complete manifest has not been independently inspected for this draft.

### 3.2 Enrichment records

The unit of analysis is one rule result for one identified host condition and selected TestResult. The method maintains three separate records.

**Curated mapping.** The implementation matches the exact tuple of benchmark ID, benchmark version, and rule ID to external XML. The mapping supplies an explanation, any supported threat relationship, prerequisites, sources, limitations, verification guidance, and review status. Host-specific observations do not belong in this reusable record. Profile selection and content hashes are retained in provenance; they are not additional keys in the current lookup.

Mapping review states are defined as draft, self-reviewed, independently reviewed, and needs revision. These states describe the quality and review history of the mapping, independently of whether a host passes the control. The initial root-login mapping remains a project-authored draft.

**Observed evidence.** The planned structured evidence record identifies the experiment, host/VM, snapshot or condition, collection times, selected scan and hashes, command or tool, relevant connection identity, exit status, and retained output. Evidence is associated only when host, condition, and timing are consistent. Missing historical details remain missing; later observations do not replace them retrospectively.

**Derived assessment.** The planned evaluator will preserve the native scan result and add a separate, bounded interpretation with evidence references. Its proposed states are prerequisites-supported, route-restricted, indeterminate, conflicting-evidence, and not-assessed. A lack of essential evidence yields uncertainty, not an assertion of protection. A discrepancy between a scan result and effective configuration requires inspection of the check's predicate before it can be classified as contradictory evidence.

Controlled-test outcomes and legitimate-function outcomes are recorded separately from the assessment. Neither a compliance pass nor a compliance failure is substituted for an observed authentication, access, or service-test result. Nonbinary scan states remain distinct.

### 3.3 Threat relationship and interpretation boundaries

The initial mapping references ATT&CK T1078.003, Local Accounts, which describes adversarial abuse of local-account credentials [2]. The proposed connection to the root-login control is an author interpretation: restricting direct root SSH removes or constrains one possible route for such abuse, subject to effective policy and the other access prerequisites. It is not an official CIS-to-ATT&CK mapping or a claim that the entire technique is prevented.

The distinction between root authentication modes is material. OpenSSH documents `without-password` as an alias for `prohibit-password`, which disables password and keyboard-interactive authentication for root; `no` disallows root login [3]. The enrichment must therefore avoid describing the observed precondition as unrestricted root password access. It must also distinguish an effective policy from a verified connection outcome.

### 3.4 Experimental procedure

For future runs, the protocol will define the hypothesis, intervention, prerequisites, and success criteria before evaluation. A baseline scan and relevant host facts will be retained, followed by a documented change, fresh scan, refreshed facts, and repeated access/function tests. The report will be regenerated using the same mapping revision where possible. Changes in scanner, content, or mapping revision will be disclosed rather than attributed to the intervention.

Comparisons will examine individual rule transitions, effective configuration, assessed prerequisites, controlled-test outcomes, and operational consequences. Newly failing rules will be retained. Targeted follow-ups will be compared only on their evaluated rules and will not replace full-profile totals.

For EXP-02, planned nginx conditions are running, disabled with the package retained, and package removed, each derived from a documented baseline. Measurements will include package inventory, service state, listeners, remote HTTP behavior, and required page retrieval. For EXP-03, planned measurements include file ownership/mode, unprivileged read/write capability, syntax validation, and retained administrative access. The permissions observation within EXP-01 will remain supporting evidence rather than being counted as an independent EXP-03 trial.

### 3.5 Validation design and implementation boundary

The static renderer is implemented and has generated the two real EXP-01 reports. Supplied test output records eight passing renderer tests. Automatic evidence association, derived assessments, and automated before/after comparison remain planned. The current reports contain identical curated context for the mapped rule in both conditions.

Validation will separately examine correct mapping selection, evidence association, assessment state, explanation, and operational outcome. Expected outputs will be documented before new cases are evaluated; the present EXP-01 interpretation is retrospective. Planned cases include remediation, unsuccessful remediation, rollback, absent mappings, missing or stale evidence, conflicting observations, nonbinary scan results, and changes in another control. Synthetic fixtures will be distinguished from real-host runs.

Cases will be classified as correct, incorrect, or indeterminate against the documented expectations, with reasons and denominators retained. Repeated runs will assess repeatability, not represent additional independent hosts. The renderer tests do not validate threat relationships or demonstrate prevention of attacks. No numerical explanation-accuracy result is available yet.

## 4. Initial case study: EXP-01

The notebook records provisioning a public key for root and obtaining root identity through a pre-intervention SSH test. A separate administrative login followed by `sudo id` also returned root identity. These were controlled tests with deliberately provisioned credentials, not attempts to steal credentials or exploit a software vulnerability.

The intervention created `/etc/ssh/sshd_config.d/00-complianceascode-hardening.conf` with `PermitRootLogin no` using `printf` piped to `sudo tee`. The recorded procedure then validated the SSH configuration and reloaded the service. Effective output changed from `without-password` to `no`. The original creation step did not explicitly set the file mode.

**Table 2. Observed rule transitions.**

| Rule suffix | Pre-intervention | Initial post-intervention | Targeted permissions follow-up |
|---|---|---|---|
| `sshd_disable_root_login` | fail | pass | pass |
| `file_permissions_sshd_drop_in_config` | pass | fail | pass |

The two full-profile reports each contained 229 passing, 114 failing, and 65 not-applicable rule-detail entries. Across the 408 inspected entries, these were the only two result transitions. The improvement and regression therefore offset each other in the aggregate counts. Not-selected rules are outside this inspected-entry denominator.

The saved post-scan ARF excerpt recorded the new hardening file as owned by user/group IDs 0:0 with mode 0644 and no extended ACL. Current inspection confirmed those permissions and the root-login directive. Group and other read permissions explained the permissions noncompliance; write permission remained restricted to root. After changing the mode to 0600, a separately saved two-rule scan reported both controls passing and exit code 0. This follow-up does not establish full-profile compliance or a repeated functionality outcome.

The post-intervention administrative test returned root identity and exit 0. The recorded root SSH test returned 255, but its stderr was not retained. The notebook also uses different pre/post key filenames and a placeholder target in the pre-test command; these may reflect transcription or naming changes, but identical test inputs cannot be established from the excerpts alone. The failure therefore cannot be conclusively attributed to policy rejection. The configuration and compliance transition are supported independently of that incomplete access-test evidence.

The current case demonstrates real-input static enrichment and the value of reporting individual changes. It does not yet validate dynamic explanations. The original post-state failure is retained, and the permission correction is reported as a separate condition rather than overwriting the initial result.

## 5. Limitations and next evaluation steps

This draft reports one paired case and one targeted correction. Broader efficacy, repeatability, rollback behavior, and the remaining scenarios are not established. The selected sample favors controls already observed in the lab and includes dependencies among rules. It cannot support conclusions about the benchmark as a whole.

The same researcher authors the mappings and prepares expected outcomes, introducing interpretation bias. Independent mapping review is planned but has not occurred. Source revisions and observations must remain attributable, and incomplete access-test records limit causal interpretation. The native reports also contain inconsistent descriptive permission guidance, underscoring the need to inspect exact checks and evidence rather than copy prose commands uncritically.

The next work is to implement evidence-dependent assessments, complete and review the six mappings, and execute the remaining controlled scenarios with prospectively defined measurements. A related-work section will compare existing enrichment approaches before any novelty claim. The final discussion and conclusion will be written after that evaluation; no general security-benefit estimate is asserted here.

## References

[1] OpenSCAP Project. *OpenSCAP User Manual*, documentation for version 1.4.1. https://static.open-scap.org/openscap-1.4.1/oscap_user_manual.html. Accessed November 5, 2026. Background reference; the experiment used scanner 1.3.9, as established by its own records.

[2] MITRE ATT&CK. *Valid Accounts: Local Accounts (T1078.003).* https://attack.mitre.org/techniques/T1078/003/. Accessed November 5, 2026. Supports the technique definition, not the author's control mapping.

[3] OpenSSH. *sshd_config(5)*, PermitRootLogin. https://man.openbsd.org/sshd_config#PermitRootLogin. Accessed November 5, 2026. Supports setting semantics; target-specific observations are retained separately.

## Appendix A. Reproduction identifiers and evidence index

| Item | Recorded value |
|---|---|
| Canonical experiment | EXP-01 |
| Target / Proxmox VM / snapshot | scap-exp01 / 100 / exp01-pre |
| Content release | ComplianceAsCode 0.1.82, from retained archive |
| Prototype source | cwiggins0217/openscap; feature/report-enrichment; 35efc53f8 |
| Mapping file | lab-content/ubuntu2404-context.xml |
| Current Parrot archive | /home/attacker/masters-project/evidence/EXP-01/20261104T203112Z |
| Conditions | pre/; post/; followup-permissions-20261105T184154Z/ |
| Historical naming | Original transcripts use EXP-001; canonical notes now use EXP-01 |

Recorded datastream SHA-256:

```text
e311189ac70ff73be54121311fca324d6188f8c12ab53416090f595ff00e070c
```

Recorded release archive SHA-256:

```text
765e84bdce7f9055f9b9c2dd0ee2b713d4255f8eec94eac6d35ea4973c28919c
```

Project evidence:

- [Week 1 progress and method record](whitepaper/week1-working-draft.md).
- [Original Week 1 notebook]().
- [Pre-intervention enriched report](evidence/).
- [Post-intervention enriched report]().

Raw XML/ARF, effective configuration, scan logs, timestamps, and exit codes are referenced by the condition directories above. Mapping/build provenance and checksums are retained in the local archive; the exact generated manifest basename and full digest listing remain to be inserted into the final reproduction appendix. Project links identify evidence artifacts and are not substitutes for public research references.
