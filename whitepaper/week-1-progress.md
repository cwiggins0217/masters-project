# Weekly Research Progress — Week [1–4]

**Project:** Dynamic Contextual Enrichment of OpenSCAP Reports  
**Researcher:** Christopher Wiggins
**Reporting period:** 11/3/26
**Submission date:** 11/9/26]
**Overall status:** On track

```abstract
Working draft based on results and screenshots reported during project
sessions. Remote evidence files have not been independently inspected
for this report. Pending items remain explicit so this draft can be
updated as week 1 continues.
```

## 1. Weekly summary

This week's objective is to establish a reproductible baseline and and
demonstrate how an OpenSCAP finding can be enriched with attack context
that changes after a measured configuration change. The project scope
was narrowed to contextual report enrichment, supported by controlled
security and service tests. An initial SSH enrichment prototype was
demonstrated, and a subsequent baseline scan on the current Ubuntu 24.04
lab VM reported 229 passing, 114 failing, 65 not-applicable, and 240
not-selected rule results. Candidate SSH, service, and file-permission
findings have been extracted for experiment selection. A controlled
intervention, rescan, and comparison of enriched explanations remain to
be completed; no reduction in attack success or service-impact result is
claimed yet for this week's baseline.

## 2. Planned work and completion

| Commitment for this week              | Status                                            | Completed output / evidence                                                     | Remaining work or reason for delay                                                                |
|---                                    |---                                                |---                                                                              |---                                                                                                |
| Define scope and workflow             | Substantially complete                            | Four-week plan, reporting template                                              | Finalize six rule IDs and precise scenario hypothesis                                             |
| Establish current Ubuntu baseline     | Partial                                           | CIS level 1 server scan completed on scap-b; evidence recorded                  | Attack host inventory, snapshot ID, scan-content hash, and installed tool versions                |
| Extract candidate findings            | Complete for initial inspection                   | Rule-status output for SSH, services, protected files reported                  | Freeze selected subset and archive extraction script/version                                      |
| Demonstrate report enrichment         | Initial prototype demonstrated                    | Earlier SSH report displayed contextual information for sshd_disable_root_login | Preserve prototype/mapping versions and reproduce against the current baseline                    |
| Complete first SSH before/after cycle | Pending                                           | Baseline candidate findings available                                           | Record intervention, security test, legitimate administrative test, rescan, and report transition |
| Begin whitepaper                      | Planning comlete; manuscript progress unconfirmed | Scope, method, and evidence structure outlined in research plan                 | Draft problem, scope and experimental-method sections                                             |

## 3. Experiments and findings

**Comparison used:** Current baseline only. No paired hardened result
has been reported for this baseline. Snapshot names and lineage remain
to be recorded.

### Baseline Scan

**Host:** scap-b (reported shell context: cis-test@scap-b)
**Operating System:** Ubuntu 24.04
**Profile:** xccdf_org.ssgproject.content_profile_cis_level1_server
**Evidence Directory:** /home/cis-test/masters-project/evidence/baseline-20261103T211104Z
**Reported scan exit code:** 2

| Reported Result | Count |
|---              |---    |
| pass            | 229   |
| fail            | 114   |
| notapplicable   | 65    |
| notselected     | 240   |
| total           | 648   |

The reported output establishes a set of baseline compliance findings
for experiment selection. It does not establish that any associated
attack is feasible or has succeeded. The counts are not a vulnerability
or a risk score.

### Candidate findings inspected
Rule names below omit the common prefix xccdf_org.ssgproject.content_rule_.

| Rule suffix                  | Baseline result |
|---                           |---              |
| file_permissions_etc_group   | pass            |
| file_permissions_etc_gshadow | pass            |
| file_permissions_etc_passwd  | pass            |
| file_permissions_etc_shadow  | pass            |
| service_httpd_disabled       | pass            |
| package_nginx_removed        | fail            |
| service_nginx_disabled       | fail            |
| package_rsync_removed        | fail            |
| service_rsyncd_disabled      | fail            |
| file_groupowner_sshd_config  | pass            |
| file_owner_sshd_config       | pass            |
| file_permissions_sshd_config | fail            |
| sshd_disable_empty_passwords | fail            |
| sshd_disable_root_login      | fail            |
| sshd_set_max_auth_tries      | fail            |
| service_auditd_enabled       | notselected     |

notselected is retained separately from failure. Failed service-removal
or disablement check require package, service, and network evidence
before making clams about actual reachability or use.

| Experiment / rule IDs                                         | Conditions and valid runs per condition                           | Security outcome before → after | Legitimate-service outcome before → after | Evidence                          |
|---                                                            |---                                                                |---                              |---                                        |---                                |
| EXP-001: selected SSH restriction; exact intervention pending | one baseline scan reported: paired intervention/test runs pending | Not evaluated                   | Not evaulated                             | baseline evidence directory above |

**Principal finding:** The baseline contains useable failed SSH and
service controls for the planned study, while several protected-file
permission checks already pass.

**Interpretation:** The scan provides starting conditions for controlled
experiments and report-enrichment cases. A successful test must
separately show the configuration change, resulting scan state, relevant
security behavior, and effect on legitimate use.

**Limits:** No current-baseline attack trial, post-hardening scan, or
service-impact comparison has been reported. Earlier SSH and hardening
exercises are background work and are not counted as paired results for
this baseline.

**Invalid or inconclusive runs:**  Not yet audited against raw logs; no
verified count assigned.

<!-- Security outcomes: succeeded, blocked, prerequisite absent, test error,
or inconclusive. Service outcomes: passed, failed, not run, or inconclusive.
If no experiments ran, say so and describe setup/prototype work in Section 2.
A failed compliance check alone does not demonstrate attack success. -->

## 4. Report enrichment and dynamic behavior

The November 2 prototype work produced an enriched HTML report for the
failed sshd_disable_root_login rule. The demonstrated context associated
the finding with ATTA&CK T1078.003 (Local Accounts) and included an
explanation, conditions, source, limitations, and verification guidance.
This remains a project-authored draft relationship, not a vaildated
claim that the host is exploitable.

The earlier configuration output showed permitrootlogin
without-password. This must not be summarized as unrestricted root
password login. Actual root key access and the attack prerequisites were
not demonstrated. The earlier prototype and November 3 baseline are
separate evidence sets until their inputs and lineage are reconciled.

| Measure                                          | This week                                     | Cumulative            |
|---                                               |---                                            |---                    |
| Rules with draft enrichment                      | One reported example: sshd_disable_root_login | Not yet established   |
| Completed, reviewed enrichment records           | not yet established                           | Not yet established   |
| Mappings self-reviewed                           | Review not documented                         | Review not documented |
| Mappings independently reviewed                  | Review not documented                         | Review not documented |
| Evaluation cases                                 | Not yet evaluated                             | Not yet evaluated     |
| Current baseline before/after report transitions | Not yet evaulated                             | Not yet evaluated     |

**Prototype version:** [Commit/tag not yet recorded]
**Mapping dataset version:** [Commit/tag not yet recorded]
**Scan content and profile:** Benchmark
xccdf_org.ssgproject.content_benchmark_UBUNTU_24-04, reported content
version 0.1.82, CIS Level 1 Server profile. Verify the current
baseline's content version/hash separately.

| Finding / rule | Before: scan result and explanation                  | After: scan result and explanation | Correct update? / evidence                                 |
|---             |---                                                   |---                                 |---                                                         |
| sshd_disable_  | earlier prototype, failed control                    | no post-change                     | not evaluated; earlier output                              |
| root_login     | with conditional context, baseline also reports fail | result recorded                    | reported at ~/openscap/scan-results/baseline-enriched.html |

- **Transitions checked:** No verified remediation, failed-remediation,
  rollback or missing-evidence transition recorded yet.
- **ATT&CK/CVE research:** One draft ATT&CK relationship demonstrated.
  No host-specific CVE applicability finding established.
- **Review status:** Describes the review of a mapping relationship; it
  does not describe whether the server is secure.
- **Explanation validation:** Formal assessment of correctnes and
  misleading explanations remains pending.

<!-- Mapping review status describes review of the relationship, not the
server's security. Count mappings separately from rules when one rule has
multiple relationships. Label synthetic evaluation cases as fixtures. -->

## 5. Whitepaper progress

- **Sections drafted or revised:** Research scope, four-week roadmap,
  laboratory comparison design, and reporting workflow documented in
  planning material. A current manuscript section/version has not been
  confirmed.
- **Evidence-backed claims or tables added:** This report records the
  November 3 baseline totals and inspected candidate-rule results.
- **Sources reviewed:** Source/version inventory for individual mapping
  claims remains to be recorded. Planning references should not be
  counted as completed literature review without review notes.

## 6. Problems, decisions, and guidance needed

| Issue or decision                                                     | Effect on research / deadline                              | Next action                                                                                                        | Owner / target date     |
|---                                                                    |---                                                         |---                                                                                                                 |---                      |
| Perfer perl over python for scripts; XML::LibXML unavailabled on host | initial extraction approach required adjustment            | retain the working extraction approach, record dependencies and script version; candidate output has been obtained | Researcher / Week 1     |
| earlier prototype and baseline use different evidence paths           | could lead to mixing inputs or overstating reproducibility |record each input ARF, content version, mapping version, and output path separately                                 | Researcher November 8   |
| six-rule subset and first intervention not finalized                  | blocks a clearly bounded paired experiment                 | select exact rules from the baseline and define expected observations before changing configuration                | Researcher / November 8 |
| snapshot IDs, hashes, and test transcripts not yet attached           | limis reproducibility and auditability                     | add an evidence manifest and exact run references                                                                  | Researcher / November 8 |

**Scope or method changes:** Contextual enrichment is the primary
contribution.  Controlled security and service tests will evaluate
selected explanations and remediation consequences. Whole-profile
hardening and isolated-control experiments must remain distinguishable.

**Guidance requested from professor:** No specific request recorded yet.

## 7. Next-week commitments

### Week 1 Work

| Deliverable                                | Observable completion criterion                                                                                      | Target date |
|---                                         |---                                                                                                                   |---          |
| Frozen initial scope and baseline manifest | six exact rule IDs, scan-content version/hash, host facts, and snapshot lineage recorded                             | November 8  |
| First SSH experiment                       | Before/after raw evidence, fresh scan, legitimate administration check, and enriched report comparison               | November 8  |
| Initial mapping record and method draft    | Versioned record with prerequisites, rationale, sources, limitations, and review state; written experiment procedure | November 8  |
| Week 1 report finalized                    | Replace pending entries with actual outcomes or explicity carryover; link retained evidence                          | November 9  |

### Proposed Week 2 Commitments

| Deliverable                            | Observable completion criterion                                                              | Target date        |
|---                                     |---                                                                                           |---                 |
| Sevice-change scenario                 | controlled comparison with both security/rechability and legitimate-function observations    | November 15        |
| Expanded enrichment and state handling | Versioned records for selected findings; documented behavior for observed post-change states | November 15        |
| Whitepaper methods update              | Methods and initial results traceable to experiment records                                  | November 16 report |

**Next milestone and outlook:** November 9 Week 1 report. Baseline
acquisition and initial prototype work are established; completion of
the first documented before/after cycle is the main outstanding
milestone.

## 8. Supporting evidence

- **Current baseline:** /home/cis-test/masters-project/evidence/baseline-20261103T211104Z (reported remote path; individual filenames and hashes pending).
- **Earlier prototype input:** /home/cis-test/openscap/scan-results/arf.xml (reported remote path).
- **Earlier enriched report:** /home/cis-test/openscap/scan-results/baseline-enriched.html (reported remote path; screenshots shown during prototype discussion).
- **Planning document:** openscap-four-week-research-plan.md.
- **Report structure:** openscap-weekly-progress-template.md.
- **Experiment records:** Current paired-run record pending.
- **Mapping dataset and prototype:** Repository/file paths and commit identifiers pending.
- **Current whitepaper:** Draft path/version not yet recorded.

<!-- Before submission:
- Every finding has evidence or is explicitly marked provisional.
- Planned work is not described as completed.
- Invalid runs and broken legitimate services are disclosed.
- Whole-profile effects are not attributed to an individual rule without evidence.
- Counts have clear denominators; unevaluated items are labelled.
- Next-week commitments have measurable completion criteria.
>
