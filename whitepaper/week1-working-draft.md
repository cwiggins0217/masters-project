# Weekly Research Progress — Week 1

**Project:** Dynamic Contextual Enrichment of OpenSCAP Reports\
**Researcher:** Christopher Wiggins\
**Reporting period:** November 2–8, 2026\
**Updated through:** November 5, 2026\
**Submission date:** November 9, 2026 (planned)\
**Overall status:** In progress; EXP-01 paired scans and static enriched reports completed; permissions failure identified and corrected with a passing two-rule follow-up; dynamic assessment and evidence audit pending.

> Working draft. The uploaded pre-enriched.html and post-enriched.html were inspected for rule results and enrichment content. Configuration values, build/test results, and access-test outcomes are based on supplied terminal output. Raw scan XML, complete access-test logs, snapshot lineage, and hashes have not yet been independently audited.

## 1. Weekly summary

This week's work established a baseline and completed the first paired SSH scan comparison for EXP-01. Saved configuration output changed from `permitrootlogin without-password` to `permitrootlogin no`, and `sshd_disable_root_login` changed from fail to pass. A custom OpenSCAP build on the Parrot workstation generated enriched HTML reports from the saved scans, with one project-authored ATT&CK T1078.003 mapping. Eight renderer tests passed. Inspection of the reports also identified a second transition: `file_permissions_sshd_drop_in_config` changed from pass to fail. Consequently, aggregate pass/fail counts remained unchanged. A saved post-scan file observation subsequently identified mode 0644 on the root-login hardening drop-in. After a correction to 0600, a separate targeted scan reported both affected controls passing with exit code 0. The reports currently display identical curated context in both conditions; automatic interpretation based on scan results and host evidence remains to be implemented.

## 2. Planned work and completion

| Commitment for this week                     | Status                                                           | Completed output / evidence                                                                                                 | Remaining work                                                                                  |
| -------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Define research scope and reporting workflow | Substantially complete                                           | Four-week research plan and weekly reporting template prepared; focus is OpenSCAP contextual enrichment and dynamic updates | Six exact rule IDs and scenario allocation frozen below; detailed future-run protocols remain                                           |
| Establish current Ubuntu 24.04 baseline      | Partial                                                          | CIS Level 1 Server scan completed on `scap-b`; evidence directory recorded below                                            | Baseline inventory and content hashes recovered from notes; retain raw manifest and clone provenance     |
| Extract candidate findings                   | Complete for initial inspection                                  | Rule-status output for SSH, services, and protected files reported                                                          | Selected subset frozen; archive extraction script/version                                |
| Demonstrate report enrichment                | Completed for one real paired example                            | Custom native build generated pre/post HTML with the Ubuntu root-login mapping; eight renderer tests passed                 | Provenance and checksum capture reported complete; add result-dependent assessment                      |
| Complete first SSH before/after cycle        | Paired scans and static reports complete; evidence audit partial | EXP-01 fail → pass root-login result; post access-test output reported                                                     | Retain notes as evidence; document missing root-test stderr/key identity; follow-up archive verified by researcher |
| Begin whitepaper                             | Initial draft v0.1 complete               | Scope, method, and evidence structure outlined in research plan                                                             | Review draft v0.1; expand related work and evaluation as new evidence becomes available                                          |

## 3. Experiments and findings

**Comparison used:** Historical November 3 baseline plus a separate paired pre/post EXP-01 evidence set on `scap-exp01`. EXP-01 is a selected SSH intervention, not a whole-profile hardened comparison. Experiment VM ID 100 and pre-experiment snapshot `exp01-pre` were confirmed by the researcher. Baseline notes identify VM 200 and clean snapshot `b00-clean-os`; exact clone provenance is not independently audited.

### Baseline scan

**Host:** `scap-b` (reported shell context: `cis-test@scap-b`)\
**Operating system:** Ubuntu 24.04\
**Profile:** `xccdf_org.ssgproject.content_profile_cis_level1_server`\
**Evidence directory:** `/home/cis-test/masters-project/evidence/baseline-20261103T211104Z`\
**Reported scan exit code:** `2`

| Reported result              | Count |
| ---------------------------- | ----: |
| pass                         |   229 |
| fail                         |   114 |
| notapplicable                |    65 |
| notselected                  |   240 |
| Total of reported categories |   648 |

The reported output establishes a set of baseline compliance findings for experiment selection. It does not establish that any associated attack is feasible or has succeeded. The counts are not a vulnerability count or a risk score.

### Candidate findings inspected

Rule names below omit the common prefix `xccdf_org.ssgproject.content_rule_`.

| Rule suffix                    | Baseline result |
| ------------------------------ | --------------- |
| `file_permissions_etc_group`   | pass            |
| `file_permissions_etc_gshadow` | pass            |
| `file_permissions_etc_passwd`  | pass            |
| `file_permissions_etc_shadow`  | pass            |
| `service_httpd_disabled`       | pass            |
| `package_nginx_removed`        | fail            |
| `service_nginx_disabled`       | fail            |
| `package_rsync_removed`        | fail            |
| `service_rsyncd_disabled`      | fail            |
| `file_groupowner_sshd_config`  | pass            |
| `file_owner_sshd_config`       | pass            |
| `file_permissions_sshd_config` | fail            |
| `sshd_disable_empty_passwords` | fail            |
| `sshd_disable_root_login`      | fail            |
| `sshd_set_max_auth_tries`      | fail            |
| `service_auditd_enabled`       | notselected     |

`notselected` is retained separately from failure. Failed service-removal or disablement checks require package, service, and network evidence before making claims about actual reachability or use.

### Frozen six-rule scope — November 5, 2026

Scope version: 1.0. Platform: Ubuntu Server 24.04. Benchmark: `xccdf_org.ssgproject.content_benchmark_UBUNTU_24-04`, ComplianceAsCode content version 0.1.82. Profile: `xccdf_org.ssgproject.content_profile_cis_level1_server`.

These six rules were selected from findings already observed in the baseline or EXP-01. This is a purposive sample for evaluating enrichment, not a representative sample of all CIS controls. All rules must retain their exact IDs in the mapping dataset.

| Family | Exact rule ID | Observed starting evidence | Selection rationale |
|---|---|---|---|
| SSH authentication | `xccdf_org.ssgproject.content_rule_sshd_disable_root_login` | EXP-01 fail → pass | Existing end-to-end case linking a compliance transition, effective setting, and controlled access tests |
| SSH authentication | `xccdf_org.ssgproject.content_rule_sshd_disable_empty_passwords` | Baseline fail; notebook reports effective `permitemptypasswords no` | Tests whether enrichment can distinguish a failed check from effective authentication behavior without asserting empty-password access |
| Service exposure | `xccdf_org.ssgproject.content_rule_service_nginx_disabled` | Baseline fail | Compare service configuration/state, listener reachability, and required HTTP functionality |
| Service exposure | `xccdf_org.ssgproject.content_rule_package_nginx_removed` | Baseline fail | Distinguish installed software from an active, reachable service; compare disablement and removal as separate interventions |
| File permissions | `xccdf_org.ssgproject.content_rule_file_permissions_sshd_config` | Baseline fail; notebook mode 0644 root:root | Evaluate permission findings against actual read/write capabilities and legitimate administration |
| File permissions | `xccdf_org.ssgproject.content_rule_file_permissions_sshd_drop_in_config` | EXP-01 pass → fail → pass | Existing unintended compliance regression and correction; tests whether explanations distinguish excess read permission from unauthorized write access |

**Planned scenario allocation:**

- **EXP-01: SSH authentication.** Keep the completed root-login run intact. Evaluate the empty-password rule as a separately identified extension/condition with its own evidence; do not retrospectively add it to the original intervention. Inspect the exact OVAL predicate and matched configuration before explaining the baseline scan/effective-setting discrepancy. Document whether an explicit setting changes compliance without changing effective behavior. Do not infer authentication success from configuration alone.
- **EXP-02: nginx service exposure and availability.** Compare a documented running baseline, a service-disabled condition with package retained, and a package-removed condition derived from the same baseline. Record both rule results, package inventory, service state, listeners, remote HTTP outcome, and legitimate page retrieval. State whether the web service is required in each interpretation. A failed package-removal rule alone is not evidence of a reachable or vulnerable web server.
- **EXP-03: SSH configuration file permissions.** Evaluate the main configuration and drop-ins with distinct before/after permission evidence, unprivileged read/write capability checks, SSH syntax validation, and retained administrative access. Reuse the EXP-01 regression as supporting evidence, but do not count it as an independent EXP-03 trial. Do not weaken write permissions merely to obtain a more dramatic result.

**Limits and acceptance criteria:** Six selected rules do not mean six independent attacks, completed mappings, or six independent experiments. nginx rules share one service, and permission rules share SSH configuration; their dependence must be disclosed. For each mapping, record rationale, prerequisites, sources, review state, applicable evidence, and qualified failing/passing/missing-evidence interpretations. CVE and ATT&CK associations require separate justification and may remain unassigned. Broader generalization beyond these three families is outside this sample. Any subsequent substitution requires a dated reason; preserve this scope version.

### EXP-01 — Disable direct root SSH login

**Target:** `scap-exp01`, Proxmox VM ID `100`, pre-experiment snapshot `exp01-pre`, Ubuntu 24.04.\
**Evidence directory:** `/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z`.\
**Scanner used on target:** system OpenSCAP 1.3.9, as reported.\
**Report generation:** custom OpenSCAP on the Parrot workstation, using saved XCCDF results.

| Observation                            | Before                                | After                             | Evidence basis                                                          |
| -------------------------------------- | ------------------------------------- | --------------------------------- | ----------------------------------------------------------------------- |
| `sshd_disable_root_login`              | fail                                  | pass                              | Inspected enriched HTML rule details                                    |
| `file_permissions_sshd_drop_in_config` | pass                                  | fail                              | Inspected enriched HTML rule details                                    |
| `permitrootlogin`                      | without-password                      | no                                | Supplied output from saved `sshd-effective.txt`                         |
| `pubkeyauthentication`                 | yes                                   | yes                               | Supplied output from saved `sshd-effective.txt`                         |
| `passwordauthentication`               | yes                                   | yes                               | Supplied output from saved `sshd-effective.txt`                         |
| Root SSH access test                   | Root `id` output recorded; exit code not saved | Exit 255 recorded; stderr absent                 | Notes include commands; key-file identity and rejection reason remain unverified         |
| Administrative access test             | `sudo id` returned root identity; exit code not saved | Exit 0 and `uid=0(root)` recorded | Pre/post command and output excerpts are present in notes |

The root-login rule detail records evaluation times of 2026-11-04 20:35:06 UTC (pre) and 21:01:56 UTC (post). These are rule timestamps, not whole-scan start/end times.

| Result category in inspected HTML rule details | Before | After | Change |
| ---------------------------------------------- | -----: | ----: | -----: |
| pass                                           |    229 |   229 |      0 |
| fail                                           |    114 |   114 |      0 |
| notapplicable                                  |     65 |    65 |      0 |
| Total inspected rule-detail entries            |    408 |   408 |      0 |

The 408 inspected entries exclude not-selected rules; the earlier baseline's 240 not-selected results are reported separately above.

**Principal finding:** The intended root-login control improved while the drop-in configuration permissions control became noncompliant. These were the only result transitions found among the 408 inspected rule-detail entries. Aggregate totals concealed the two opposing changes.

**Interpretation:** The captured configuration and scan result agree that direct root SSH login was disabled. The unchanged `passwordauthentication yes` value must not be interpreted as disabled password authentication for other users. The supplied saved post-scan ARF excerpt identifies `/etc/ssh/sshd_config.d/00-complianceascode-hardening.conf` with owner/group IDs 0:0 and mode 0644. Current inspection confirmed root ownership, mode 0644, and the directive `PermitRootLogin no`. Group and other read bits explain the permissions noncompliance; unprivileged write permission was not present. The uploaded notes record the file as absent before creation with `printf` piped to `sudo tee`, followed by SSH syntax validation and service reload. No explicit file-mode setting is recorded at creation; the later saved ARF records mode 0644. The process umask was not captured.

**Operational outcome:** The reported post-change administrative test returned success and root identity. This supports continued access through the tested administrative path, as documented by the saved command and output excerpt in `notes-week1.md`. Root SSH exit 255 alone does not distinguish authentication rejection from other SSH errors.

**Limits:** One paired evidence set has been reviewed; repeatability, rollback, and attack effectiveness have not been established. No credential theft or general prevention of ATT&CK T1078.003 is claimed. Preserve the original post-state evidence; any permission correction should be recorded as a separate follow-up condition.

**Invalid or inconclusive runs:** Not yet audited against raw logs; no verified count assigned.

### Permissions correction and targeted follow-up — November 5

The saved post-scan ARF excerpt recorded group and other read permissions on `00-complianceascode-hardening.conf`, with no extended ACL. A current inspection at 2026-11-05T18:39:41Z confirmed mode 0644, root:root ownership, and `PermitRootLogin no`. The accompanying `50-cloud-init.conf` file was mode 0600. The pre-scan extraction returned no matching file items; this alone does not establish that the directory was empty.

The hardening drop-in was corrected using `chmod 0600`, and the supplied subsequent `stat` output confirmed mode 0600 with root ownership. A fresh two-rule evaluation then reported:

| Control | Original pre-scan | Original post-scan | Permissions follow-up |
|---|---|---|---|
| `sshd_disable_root_login` | fail | pass | pass |
| `file_permissions_sshd_drop_in_config` | pass | fail | pass |

**Follow-up scan exit:** `0`, reported terminal output.  
**Evidence directory:** `/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/followup-permissions-20261105T184154Z`.

This is a separate targeted condition, not a new full-profile evaluation. Its two passing results must not be substituted into the original full-profile totals. Original pre/post artifacts remain the evidence for the opposing initial transitions. The follow-up scan output has been supplied; its raw XML/ARF and logs have not yet been independently inspected. Access tests were not reported again for this follow-up.

**Host identity note:** Researcher confirmed experiment identifier `EXP-01`, VM ID `100`, hostname `scap-exp01`, and snapshot `exp01-pre`. Historical excerpts contain `EXP-001` paths, which are retained here as recorded source locations, not assertions about current renamed directories. The researcher reports correcting local naming inconsistencies.

**Content-quality observation:** Both original HTML reports describe a command using `chown 0600` on directories, whereas the generated shell remediation uses `chmod` on files. The descriptive command was not used for the correction. Record this as an inconsistency in the rendered benchmark guidance; it does not by itself invalidate the OVAL result.

### Evidence recovered from the Week 1 notebook

Source: [notes-week1.md](https://chatgpt.com/library?file_id=libfile_20e2d211ec788191948d366cb9b9ed56&account_id=personal), supplied November 5. These are saved notebook excerpts, not a complete timestamped terminal transcript. Original notes have not been edited.

| Evidence | Recovered detail |
|---|---|
| Baseline VM | `scap-b`, Proxmox VM 200; 2 CPUs, 4 GB RAM, 64 GB disk |
| Baseline snapshot | `b00-clean-os`; notebook time 2026-11-02 19:59:21, timezone not specified |
| Baseline OS/kernel | Ubuntu 24.04.5 LTS; `6.8.0-147-generic`, as recorded |
| Baseline OpenSCAP package | `1.3.9+dfsg-1.1ubuntu2` |
| Baseline OpenSSH package | `1:9.6p1-3ubuntu13.20` |
| Baseline nginx package | `1.24.0-2ubuntu7.19` |
| Baseline guest agent package | `1:8.2.2+ds-0ubuntu1.18` |
| Experiment test preparation | Public key added to root authorized_keys; directory mode 0700 and authorized_keys mode 0600; effective public-key authentication enabled |
| Pre-intervention root access | Notebook records `uid=0(root) gid=0(root) groups=0(root)` for the root SSH test; exit code not recorded |
| Pre-intervention admin access | Notebook records the same root identity from `ssh -t cis-test@10.10.20.198 'sudo id'`; exit code not recorded |
| Intervention | File existence check returned ABSENT; `printf '%s\n' 'PermitRootLogin no'` piped to `sudo tee /etc/ssh/sshd_config.d/00-complianceascode-hardening.conf`; `sshd -t` followed by SSH reload; effective setting then `no` |
| Post-intervention root access | Command and exit 255 recorded; stderr is not preserved |
| Post-intervention admin access | `sudo id` returned root identity; SSH exit 0 recorded |
| Full-profile scans | Pre/post commands, result paths, and exit 2 recorded; extracted root rule result fail → pass |

**Recorded content SHA-256 values:**

```text
765e84bdce7f9055f9b9c2dd0ee2b713d4255f8eec94eac6d35ea4973c28919c  scap-security-guide-0.1.82.zip
e311189ac70ff73be54121311fca324d6188f8c12ab53416090f595ff00e070c  ssg-ubuntu2404-ds.xml
```

**Access-test limitation:** The recorded pre-test uses `~/.ssh/scap-exp001-root` and the placeholder `CLONE_IP`; the recorded post-test uses `~/.ssh/scap-exp01-root` and an explicit address. The key-generation and public-key-copy lines likewise differ in filename. These may be transcription or renaming differences, but the preserved notebook does not establish that both tests used the same key. The post-test also adds `ControlPath=none`. Therefore, report the recorded root-test failure without claiming a rigorously identical test or conclusively attributing exit 255 to authentication policy. The scan/configuration transition and retained administrative path remain separately supported. No private keys are required to resolve provenance; public-key fingerprints or an explicit researcher clarification would suffice if available.

**Experiment interpretation:** A deliberately provisioned root test key demonstrated an allowed access path in the precondition. This is a controlled access test using known credentials, not a demonstration of credential theft or exploitation. The effective configuration, compliance transition, and permission correction provide the strongest retained evidence. Missing historical stderr should remain a stated limitation; a later repeat would be a new run.

## 4. Report enrichment and dynamic behavior

The custom OpenSCAP implementation was built successfully on Parrot Security 7.4 (echo). Its native CLI exposes `--enrichment` for `xccdf generate report`. The supplied renderer-test output reports eight passing tests. The generated pre/post HTML files were inspected and each contains one mapped Security context panel for `sshd_disable_root_login`.

The mapping includes an explanation, ATT&CK T1078.003 relationship, prerequisites, source, limitations, verification guidance, and draft review status. The relationship is project-authored and conditional: disabling direct root SSH restricts one possible route for abusing a local account. It does not establish host exploitability or prevent the entire technique. No CVE applicability has been established.

| Measure                                                       | Current status                                                       |
| ------------------------------------------------------------- | -------------------------------------------------------------------- |
| Rules with demonstrated enrichment                            | One: `sshd_disable_root_login`                                       |
| Native real-scan report generation                            | Completed for both EXP-01 conditions                                |
| Renderer regression tests                                     | Eight passed in supplied terminal output                             |
| Mapping review                                                | Draft; independent review pending; formal self-review not documented |
| Paired result comparison                                      | Root-login fail → pass; drop-in permissions pass → fail              |
| Dynamic host-specific assessment                              | Not yet implemented                                                  |
| Rollback, missing-evidence, and repeated real-host evaluation | Pending                                                              |

**Prototype source:** `cwiggins0217/openscap`, branch `feature/report-enrichment`, commit `35efc53f8`.\
**Workstation checkout:** `/home/attacker/Repos/github.com/cwiggins0217/masters-project/tools/openscap`.\
**Mapping:** `lab-content/ubuntu2404-context.xml` relative to the checkout; mapping copy included in the reported verified provenance archive; digest listing not supplied here.\
**Mapping scope:** Benchmark `xccdf_org.ssgproject.content_benchmark_UBUNTU_24-04`, version `0.1.82`, exact root-login rule ID. Datastream SHA-256 is recorded in the notes below; equality of each scan input with that hashed file has not been independently checked.

| Report element                   | Before                                      | After                | Assessment                                               |
| -------------------------------- | ------------------------------------------- | -------------------- | -------------------------------------------------------- |
| Native root-login result         | fail                                        | pass                 | Correct transition present                               |
| Curated root-login context       | T1078.003, conditions, limits, draft review | Identical text       | Expected for current static renderer                     |
| Host evidence in enrichment      | Not joined                                  | Not joined           | Saved settings and access logs still require integration |
| Drop-in permissions result       | pass                                        | fail                 | New failure identified through comparison                |
| Context for other rendered rules | 407 unmatched panels                        | 407 unmatched panels | Explicit mapping coverage gap                            |

The native build and real-input rendering milestone is complete for this example. Dynamic explanation remains a separate milestone: the renderer currently selects curated context by benchmark ID, version, and rule ID, without deriving an assessment from the selected result or saved host facts. The next implementation should display the result, associated evidence, and qualified interpretation while preserving the reusable mapping. It should also expose newly failing controls rather than relying on aggregate scores.

**Sources included in the mapping:**

- MITRE ATT&CK T1078.003, Local Accounts: [https://attack.mitre.org/techniques/T1078/003/](https://attack.mitre.org/techniques/T1078/003/)
- OpenSSH `PermitRootLogin` documentation: [https://man.openbsd.org/sshd_config#PermitRootLogin](https://man.openbsd.org/sshd_config#PermitRootLogin)

Source snapshots/version records and formal mapping review remain outstanding. Review status describes the mapping's review, not host security.

### Formal enrichment method — version 1.0, November 5

**Purpose and unit of analysis.** The method explains one selected XCCDF rule result for one identified host condition and scan. It keeps compliance, threat relevance, observed behavior, and operational impact distinct. The six-rule scope in section 3 defines the sample. This section specifies the method; planned operations below are not claims of completed implementation.

#### Implemented and planned components

| Component | Status at the end of this work session |
|---|---|
| Read saved results and render native HTML | Implemented; pre/post EXP-01 reports inspected |
| Load external XML context through `--enrichment` | Implemented |
| Match benchmark ID, benchmark version, and rule ID | Implemented; one real rule mapped |
| Render rationale, conditions, sources, limitations, and review status | Implemented |
| Join scan-specific host facts and access tests | Manual in the experiment record; automatic join planned |
| Derive an evidence-dependent assessment | Method defined below; not implemented in the renderer |
| Compare per-rule transitions across conditions | Performed during report analysis; automated comparison planned |

#### Three separate records

**1. Curated mapping.** A reusable explanation is matched by the exact tuple `(benchmark_id, benchmark_version, rule_id)`. Profile ID and content hash are recorded in scan provenance; the current mapping lookup does not match on profile. A content-hash difference requires a comparability review even when benchmark version strings match.

| Field | Purpose | Current representation |
|---|---|---|
| Schema version and namespace | Identify the expected mapping format | Root `schema-version="1"`; `urn:openscap:report-enrichment:1` |
| Benchmark ID/version; rule ID | Restrict the explanation to its intended content | `benchmark/@id`, `benchmark/@version`, `rule/@id` |
| Explanation | Describe setting, purpose, and relevant distinctions | `explanation` |
| Threat relationship | State the proposed relationship rather than imply equivalence | `attack/@technique`, `attack/@relationship`, `justification` |
| Prerequisites | State conditions required for the described access or attack route | `conditions` |
| Sources | Support the relationship and setting semantics | `source/@href`; source versions/access dates to be retained in provenance |
| Limitations and verification | Bound claims and identify required checks | `limitation`, `verification` |
| Review status | Describe review of the mapping, independently of host state | `rule/@review-status` |
| Mapping revision | Reproduce the explanation used in a report | Archived XML hash and Git/provenance record |

Host observations must not be hard-coded into this reusable mapping. An ATT&CK association is project-authored unless an authoritative source explicitly establishes the relationship. No association is required for a rule lacking adequate support. A failed configuration rule does not establish a CVE. Future CVE applicability requires a separately sourced assessment of the installed distribution/package version, vendor fix or backport status, and relevant conditions. The present implementation does not perform CVE detection.

Mapping review states are `draft`, `self-reviewed`, `independently-reviewed`, and `needs-revision`. Record reviewer, date, mapping revision, and review notes outside the current free-text attribute until structured review metadata is implemented. A passing host result never promotes mapping review status. Existing T1078.003 mapping remains draft; defining this method does not constitute an independent review.

**2. Scan and host-evidence record.** Each future assessment must identify the experiment, VM ID, hostname, snapshot/condition, scan file hash, selected TestResult ID, benchmark/profile, scanner version, scan start/end times, and mapping revision. Individual evidence items include a stable ID, artifact path/hash, collection time, command/tool, target and execution identity, relevant connection context, exit status, stdout/stderr, and test purpose. Missing fields are explicitly marked rather than reconstructed. Keep secrets and private keys out of the evidence package; use public-key fingerprints where needed to establish test identity.

Join evidence only when host, condition, and collection interval are consistent. A shared hostname or filename alone is insufficient. Relevant intervening configuration changes invalidate a simple join. Record the observed timing difference rather than inventing a universal freshness threshold. For SSH, preserve the user/source context needed to evaluate Match conditions. Store effective configuration, policy assessment, and observed authentication outcomes as different facts. An absent matching OVAL item is missing evidence unless the collection result establishes absence.

**3. Derived assessment.** Preserve the original XCCDF result verbatim. Add a separate assessment of the specific mapped route or prerequisite, with evidence references and an explanation. The following states are proposed project terms, not existing OpenSCAP result values:

| Assessment state | Decision rule |
|---|---|
| `prerequisites-supported` | All prerequisites required for the bounded claim have supporting, correctly associated evidence; this does not establish exploitation |
| `route-restricted` | Evidence establishes that a necessary prerequisite or the specifically assessed access route is restricted; limit the statement to that route, host condition, and evidence |
| `indeterminate` | Mapping exists but essential evidence is missing, stale, ambiguous, or insufficient |
| `conflicting-evidence` | Relevant observations cannot be reconciled for the same claimed condition; show the discrepancy and withhold a definitive route conclusion |
| `not-assessed` | No applicable mapping or no requested assessment for the selected rule/condition |

Conflict takes precedence over a supported/restricted conclusion; otherwise insufficient evidence yields indeterminate. A scan failure with a secure effective setting is initially a discrepancy to investigate, not automatically contradictory evidence: the check may examine a different predicate. Inspect that predicate before deciding whether the observations truly conflict.

Keep test outcomes separate as `succeeded`, `failed`, `inconclusive`, or `not-performed`, with the exact action and success criterion. Compliance `pass` or `fail` cannot determine a test outcome. Preserve `error`, `unknown`, `notchecked`, `notselected`, `notapplicable`, `informational`, and `fixed` as distinct scan states where present; none is silently converted to pass. Independently collected evidence can still be described, but an unevaluated rule cannot be presented as compliant.

#### Processing and comparison procedure

1. Freeze the input scan, mapping revision, and evidence set; verify recorded hashes and select the intended TestResult explicitly when multiple results exist.
2. Match the exact benchmark/version/rule tuple. Display no matching context when absent. The current renderer rejects unsupported mapping schema and duplicate matches for a rendered rule; no fuzzy cross-version fallback is permitted by this method.
3. Display the original rule result and the curated context without modifying the source scan or its score.
4. For the planned dynamic stage, associate host evidence, evaluate the documented prerequisites, and emit a bounded assessment with cited evidence IDs, missing/conflicting facts, test outcomes, and operational consequence. Prefer deterministic rules/templates whose decision inputs are inspectable.
5. After a documented intervention, obtain a fresh scan and fresh relevant host facts, repeat the defined access/function tests, and generate another report with the same mapping revision. If mapping or scanner/content versions differ, disclose the differences and review comparability.
6. Compare rule-level results, effective settings, route assessments, and legitimate-service outcomes. Include newly failing controls. Report targeted follow-ups separately from full-profile comparisons; compare common selected rules without equating aggregate totals from different scopes.

“Dynamic” means explicit regeneration from a new scan and associated evidence. It does not mean continuous monitoring, rewriting earlier observations, or merely replacing the word fail with pass.

#### Worked interpretation: EXP-01

| Condition | Supported statement | Claim withheld |
|---|---|---|
| Pre-intervention | Root-login rule failed; saved effective setting was `without-password`; notes record successful root-key access | No claim of credential theft or uncontrolled compromise |
| Initial post-intervention | Root-login rule passed and captured effective setting was `no`; admin test returned root identity; permissions rule newly failed | Exit 255 alone, absent stderr and verified identical key identity, does not conclusively prove policy-caused rejection |
| Permissions follow-up | Hardening drop-in mode was corrected from 0644 to 0600; both selected checks passed in the targeted scan | No claim that every profile rule passes or that functionality was retested in this follow-up |

The mapping remains reusable across these conditions. Their observations and qualified interpretations differ. The current HTML still contains static context; the table demonstrates the manually applied method, not an implemented dynamic feature.

#### Validation and completion criteria

Maintain expected outcomes for each mapping before evaluating new runs. Record whether expectations were prospective or retrospective; EXP-01's present interpretation is retrospective. Evaluate the original scan result, selected mapping, evidence association, derived state, explanation, and operational outcome separately. Label synthetic fixtures distinctly from real-host observations.

The eight existing renderer tests support mapping/rendering behavior only. They do not validate the proposed dynamic evaluator, prove threat mappings correct, or establish real-host attack prevention. Add tests for pass/fail transitions, no mapping, wrong benchmark/version, multiple TestResults, missing/stale/conflicting evidence, nonbinary results, and a regression in another control. Escape evidence text in HTML and retain the existing safe-link behavior. Check that input hashes remain unchanged and that evidence references resolve.

A case is `correct`, `incorrect`, or `indeterminate` against a documented expected outcome, with reasons. Report counts and denominators by case type; do not silently remove incomplete or failed cases. A traceable report statement must lead to its mapping revision, selected scan result, host evidence, and interpretation rule. Claims about administrator decision-making require a separate user evaluation and are outside this experiment.


## 5. Whitepaper progress

- **Sections drafted or revised:** Research scope, four-week roadmap, laboratory comparison design, and reporting workflow documented in planning material. Formal enrichment method version 1.0 is now documented in section 4. Whitepaper draft v0.1 now contains the problem statement, research questions, six-rule scope, initial methods, EXP-01 case study, limitations, and evidence appendix: [openscap-whitepaper-draft.md](https://chatgpt.com/library?file_id=libfile_05b6a9327fbc81918cdc14611be80897&account_id=personal).
- **Evidence-backed tables added:** This report records the November 3 baseline, EXP-01 rule transitions, saved configuration values, static enrichment validation, and the unchanged aggregate totals.
- **Sources reviewed:** Source/version inventory for individual mapping claims remains to be recorded. Planning references should not be counted as completed literature review without review notes.

## 6. Problems, decisions, and guidance needed

| Issue or decision                                                              | Effect on research / deadline                                                | Next action                                                                                                        | Owner / target date     |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| Prefer Perl for project scripts; `XML::LibXML` unavailable on the working host | Initial extraction approach required adjustment                              | Retain the working extraction approach, record dependencies and script version; candidate output has been obtained | Researcher / Week 1     |
| Earlier prototype and new baseline use different evidence paths                | Could lead to mixing inputs or overstating reproducibility                   | Record each input ARF, content version, mapping version, and output path separately                                | Researcher / November 8 |
| Six-rule subset frozen November 5                                                  | Two rules per family selected; remaining mappings and trials are future work              | Implement mappings and detailed protocols within scope version 1.0                                                       | Researcher / November 8 |
| Drop-in permissions control changed from pass to fail                          | Mode 0644 confirmed in saved post evidence; corrected to 0600; both targeted checks pass | Archive targeted follow-up and retain original pre/post evidence; retain recovered intervention commands from notes                             | Researcher / Week 1     |
| Enrichment text is static                                                      | Before/after reports show result changes but identical curated explanations  | Add result-dependent assessment and scan-specific evidence joins, including missing/conflicting evidence           | Researcher / Week 1     |
| VM/snapshot IDs, content hashes, and partial test transcripts recovered                    | Limits reproducibility and auditability                                      | Retain recovered notes; artifact/mapping checksum verification reported successful; retain missing stderr/key identity limitations                                                                  | Researcher / November 8 |

**Scope or method changes:** Contextual enrichment is the primary contribution. Controlled security and service tests will evaluate selected explanations and remediation consequences. Whole-profile hardening and isolated-control experiments must remain distinguishable.

**Guidance requested from professor:** No specific request recorded yet.

## 7. Next-week commitments

### Week 1 deliverable status

| Deliverable | Status at November 5 | Remaining action |
|---|---|---|
| Six-rule scope | Frozen, version 1.0 | Record any later scope changes |
| EXP-01 evidence record | Completed with explicit limitations | Retain missing historical stderr/key-identity limitations |
| Reproducibility capture | Archive and checksum verification reported complete | Insert exact manifest basename/digests in final reproduction appendix |
| Formal enrichment method | Documented, version 1.0 | Implement and validate dynamic stages |
| Initial whitepaper | Draft v0.1 created | Review wording, develop related work and subsequent results |
| November 9 weekly submission | Working report updated; not submitted | Researcher review and submission |

**Carryover to Week 2:** Dynamic host-specific assessment remains unimplemented. Formal mapping review and broader scenario evaluation remain outstanding; neither is counted as complete merely because its method has been documented.

### Proposed Week 2 commitments

| Deliverable                            | Observable completion criterion                                                              | Target date        |
| -------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------ |
| Service-change scenario                | Controlled comparison with both security/reachability and legitimate-function observations   | November 15        |
| Expanded enrichment and state handling | Versioned records for selected findings; documented behavior for observed post-change states | November 15        |
| Whitepaper methods update              | Methods and initial results traceable to experiment records                                  | November 16 report |

**Next milestone and outlook:** November 9 Week 1 report. The paired scan and static enrichment milestone is complete. The permissions failure has been identified and corrected, with both selected rules passing in the follow-up. Scope and enrichment method are now documented. The initial whitepaper draft is complete. Remaining research work includes implementation/validation of dynamic host-specific assessment, mapping review, and further scenarios; historical evidence limitations remain explicit.

**Checklist status:** Items 1–3 (permissions investigation, evidence record with stated limitations, and reproducibility capture) are complete to the documented standard; archive verification is researcher-reported. Item 4 (six-rule scope) is now complete. Item 5 (formal enrichment method) is documented in section 4. Item 6 (initial whitepaper sections) is complete as draft v0.1. All six wrap-up items are documented; historical evidence limits remain, and this is not completion of the full research project. Dynamic assessment is not yet implemented.

## 8. Supporting evidence

- **Current baseline:** `/home/cis-test/masters-project/evidence/baseline-20261103T211104Z` (reported remote path; individual filenames and hashes pending).
- **Earlier prototype input:** `/home/cis-test/openscap/scan-results/arf.xml` (reported remote path).
- **Earlier enriched report:** `/home/cis-test/openscap/scan-results/baseline-enriched.html` (reported remote path; screenshots shown during prototype discussion).
- **Planning document:** `openscap-four-week-research-plan.md`.
- **Report structure:** `openscap-weekly-progress-template.md`.
- **EXP-01 raw evidence:** `/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/{pre,post}/`, with `results.xml`, `results-arf.xml`, `report.html`, `sshd-effective.txt`, `scan.log`, `start-time.txt`, `end-time.txt`, and `exit-code.txt` listed in supplied output. Artifact checksum capture and verification reported complete; historical access-test limitations remain.
- **Inspected enriched reports:** [pre-enriched.html](https://chatgpt.com/library?file_id=libfile_d4fb4e66cfc08191a1c4c6ea5d4ebdf7\&account_id=personal) and [post-enriched.html](https://chatgpt.com/library?file_id=libfile_5f3702154f448191afefe1dbf49a9c5e\&account_id=personal).
- **Current Parrot archive:** `/home/attacker/masters-project/evidence/EXP-01/20261104T203112Z`; pre/post and targeted follow-up result files confirmed present. Researcher reports every file in the generated SHA256SUMS manifest verified OK. Exact manifest timestamp and digest listing have not been supplied. Historical EXP-001 source paths above are retained as originally recorded.
- **Mapping and prototype:** `lab-content/ubuntu2404-context.xml`; prototype branch `feature/report-enrichment`, commit `35efc53f8`; mapping copy, Git commit/status/diff, CMake cache, binary checksum, version output, and workstation OS captured through the supplied provenance procedure; checksum verification reported successful, actual manifest not independently inspected.
- **Permissions follow-up:** `followup-permissions-20261105T184154Z/` under the EXP-01 evidence directory; terminal output reports both selected rules pass and exit 0; archived on Parrot with successful checksum verification reported; raw artifacts not independently inspected.
- **Original notebook:** [notes-week1.md](https://chatgpt.com/library?file_id=libfile_20e2d211ec788191948d366cb9b9ed56&account_id=personal); includes baseline inventory, content hashes, intervention, scan commands, and partial access-test output.
- **Current whitepaper:** [openscap-whitepaper-draft.md](https://chatgpt.com/library?file_id=libfile_05b6a9327fbc81918cdc14611be80897&account_id=personal), version 0.1, November 5, 2026.

\<!-- Update this draft with actual remaining Week 1 observations. Preserve the distinction between reported historical evidence, inspected raw files, and planned work. -->
