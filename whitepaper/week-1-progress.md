# Weekly Research Progress — Week [1–4]

**Project:** Dynamic Contextual Enrichment of OpenSCAP Reports  
**Researcher:** Christopher Wiggins
**Reporting period:** 11/3/26
**Submission date:** 11/9/26
**Overall status:** In progress; EXP-01 paired scans and static enriched
reports completed; dynamic assessment and investigation of a new
permissions failure pending.

```abstract
Working draft. The uploaded pre-enriched.html and post-enriched.html
were inspected for rule results and enrichment content. Configuration
values, build/test results, and access-test outcomes are based on
supplied terminal output. Raw scan XML, complete access-test logs,
snapshot lineage, and hashes have not yet been independently audited.
```

## 1. Weekly summary

This week's work established a baseline and completed the first paired
SSH scan comparison for EXP-001. Saved configuration output changed from
permitrootlogin without-password to permitrootlogin no, and
sshd_disable_root_login changed from fail to pass. A custom OpenSCAP
build on the Parrot workstation generated enriched HTML reports from the
saved scans, with one project-authored ATT&CK T1078.003 mapping. Eight
renderer tests passed. Inspection of the reports also identified a
second transition: file_permissions_sshd_drop_in_config changed from
pass to fail. Consequently, aggregate pass/fail counts remained
unchanged. The reports currently display identical curated context in
both conditions; automatic interpretation based on scan results and host
evidence remains to be implemented.

## 2. Planned work and completion

| Commitment for this week              | Status                                                                  | Completed output / evidence                                                                        | Remaining work or reason for delay                                                 |
|---                                    |---                                                                      |---                                                                                                 |---                                                                                 |
| Define scope and workflow             | Substantially complete                                                  | Four-week plan, reporting template                                                                 | Finalize six rule IDs and precise scenario hypothesis                              |
| Establish current Ubuntu baseline     | Partial                                                                 | CIS level 1 server scan completed on scap-b; evidence recorded                                     | Attack host inventory, snapshot ID, scan-content hash, and installed tool versions |
| Extract candidate findings            | Complete for initial inspection                                         | Rule-status output for SSH, services, protected files reported                                     | Freeze selected subset and archive extraction script/version                       |
| Demonstrate report enrichment         | Completed for one real paired example                                   | Custom native build generated pre/post HTML with the root-login mapping; eight render tests passed | Archive mapping hadh and build provenance; add result-dependent assessment         |
| Complete first SSH before/after cycle | EXP-01 fail -> pass root-login result; post access-test output reported | Attach complete access logs and exact intervention; investigate new drop-in permissions failure    |                                                                                    |
| Begin whitepaper                      | Planning comlete; manuscript progress unconfirmed                       | Scope, method, and evidence structure outlined in research plan                                    | Draft problem, scope and experimental-method sections                              |

## 3. Experiments and findings

**Comparison used:** Historical November 3 baseline plus a separate
paired pre/post EXP-01 evidence set on scap-exp01 is a selected SSH
intervention, not a whole-profile hardened comparison. Snapshot names and
lineage remain to be recorded.

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

## EXP-01 -- Disable direct root SSH login
**Target:** scap-exp01, Ubuntu 24.04 LTS
**Evidence Directory:** /home/cis-test/masters-project/EXP-01/20261104T203112Z
**Scanner used on target:** system OpenSCAP 1.3.9
**Report Generation:** custom OpenSCAP on the attacker/test workstation, using saved XCCDF results.


| Observation                          | Before                                | After                           | Evidence basis                                                          |
|---                                   |---                                    |---                              |---                                                                      |
| sshd_disable_root_login              | fail                                  | pass                            | inspected enriched HTML rule details                                    |
| file_permissions_sshd_drop_in_config | pass                                  | fail                            | inspected enriched HTML rule details                                    |
| permitrootlogin                      | without-password                      | no                              | supplied output from saved sshd-effective.txt                           |
| pubkeyauthentication                 | yes                                   | yes                             | supplied output from saved sshd-effective.txt                           |
| passwordauthentication               | yes                                   | yes                             | supplied output from saved sshd-effective.txt                           |
| Root SSH access test                 | Full pre-test transcript not attached | Exit 255 reported               | Complete command and stderr needed to verify failure reason             |
| Administrative Access test           | Full pre-test transcript not attached | Exit 0 and uid=0(root) reported | consistent with retained administrative access; full transcript pending |

The root-login rule detail records evaluation times of 2026-11-04
20:35:06 UTC (pre) and 21:01:56 UTC (post). These are rule timestamps,
not whole-scan start/end times.

| Result category in inspected HTML rule details | Before | After | Change |
|---                                             |---     |---    |---     |
| pass                                           | 229    | 229   | 0      |
| fail                                           | 114    | 114   | 0      |
| notapplicable                                  | 65     | 65    | 0      |
| Total inspected rule-detail entries            | 408    | 408   | 0      |

The 408 inspected entries exclude not-selected rules; the earlier
baseline's 240 not-selected results are reported separately above.

**Principal finding:** The intended root-login control improved while
the drop-in configuration permissions became noncompliant. These were
the only result transitions found among the 408 inspected rule-detail
entries. Aggregate totals concealed the two opposing changes.

**Interpretation:** The captured configuration and scan result agree
that direct root SSH login was disabled. The unchanged
passwordauthentication yes value must not be interpreted as disabled
password authentication for other users. The new permissions failure was
observed after the intervention, but its affected file, actual mode, and
causal relationship to the intervention remain unverified.

**Operational Outcome:** The reported post-change administrative test
returned success and root identity. This supports continued access
through the tested administrative path, subject to verification of the
complete command and transcript. Root SSH exit 255 alone does not
distinguish authentication rejection from other SSH errors.

**Limits:**  One paired evidence set has been reviewed; repeatability,
rollback, and attack effectiveness have not been established. No
credential theft or general prevention of ATT&CK T1078.003 is claimed.
Preserve the original post-state evidence; any permission correction
should be recorded as a separate follow-up condition.

**Invalid or inconclusive runs:**  Not yet audited against raw logs; no
verified count assigned.

<!-- Security outcomes: succeeded, blocked, prerequisite absent, test error,
or inconclusive. Service outcomes: passed, failed, not run, or inconclusive.
If no experiments ran, say so and describe setup/prototype work in Section 2.
A failed compliance check alone does not demonstrate attack success. -->

## 4. Report enrichment and dynamic behavior

The custom OpenSCAP implementation was built successfully on Parrot
Security 7.4 (echo). Its native CLI exposes --enrichment for xccdf
generate report. The supplied renderer-test output reports eight passing
tests. The generated pre/post HTML files were inspected and each
contains one mapped Security context panel for sshd_disable_root_login.

The mapping includes an explanation, ATT&CK T1078.003 relationship,
prerequisites, source, limitations, verification guidance, and draft
review status. The relationship is project-authored and conditional:
disabling direct root SSH restricts one possible route for abusing a
local account. It does not establish host exploitability or prevent the
entire technique. No CVE applicability has been established.


| Measure                                                       | This week                                                            |
|---                                                            |---                                                                   |
| Rules with draft enrichment                                   | One reported example: sshd_disable_root_login                        |
| Native real-scan report generation                            | Completed for both EXP-01 conditions                                 |
| Renderer regression tests                                     | Eight passed in supplied terminal output                             |
| Mapping review                                                | Draft; independent review pending; formal self-review not documented |
| Paired result comparison                                      | Root-login fail -> pass; drop-in permissions pass -> fail            |
| Dynamic host-specific assessment                              | Not yet evaulated                                                    |
| Rollback, missing evidence, and repeated real-host evaluation | Pending                                                              |

**Prototype version:** cwiggins0217/openscap, branch feature/report-enrichment, commit 35efc53f8.
**Workstation checkout:** /home/attacker/Repos/github.com/cwiggins0217/masters-project/tools/openscap
**Mapping:** lab-content/ubuntu2404-context.xml relative to the
checkout; mapping commit/hash not yet recorded.
**Mapping Scope:** Benchmark xccdf_org.ssgproject.content_benchmark_UBUNTU_24-04, version 0.1.82,
exact root-login rule ID. Datastream hash remains pending.

| Report element                   | Before                                      | After                | Assessment                                              |
|---                               |---                                          |---                   |---                                                      |
| Native root-login result         | fail                                        | pass                 | correct transition present                              |
| Curated root-login context       | T1078.003, conditions, limits, draft review | identical text       | Expected for current static renderer                    |
| Host evidence in enrichment      | Not joined                                  | Not joined           | saved settings and access logs sill require integration |
| Drop-in permisions result        | pass                                        | fail                 | New failure identified through comparison               |
| Context for other rendered rules | 407 unmatched panels                        | 407 unmatched panels | Explicit mapping coverage gap                           |

The native build and real-input rendering milestone is complete for this
example. Dynamic explanation remains a separate milestone: the renderer
currently selects curated context by benchmark ID, version, and rule ID,
without deriving an assessment from the selected result or saved host
facts. The next implementation should display the result, associated
evidence, and qualified interpretation while preserving the reusable
mapping. It should also expose newly failing controls rather than
relying on aggregate scores.

### Sources included in the mapping:
- MITRE ATT&CK T1078.003, Local Accounts: https://attack.mitre.org/techniques/T1078/003/
- OpenSSH PermitRootLogin documentation: https://man.openbsd.org/sshd_config#PermitRootLogin

Source snapshots/version records and formal mapping review remain
outstanding. Review status describes the mapping's review, not host
security.

<!-- Mapping review status describes review of the relationship, not the
server's security. Count mappings separately from rules when one rule has
multiple relationships. Label synthetic evaluation cases as fixtures. -->

## 5. Whitepaper progress

- **Sections drafted or revised:** Research scope, four-week roadmap,
  laboratory comparison design, and reporting workflow documented in
  planning material. A current manuscript section/version has not been
  confirmed.
- **Evidence-backed claims or tables added:** This report records the
  November 3 baseline, EXP-001 rule transitions, saved configuration
  values, static enrichment validation, and the unchanged aggregate
  totals.
- **Sources reviewed:** Source/version inventory for individual mapping
  claims remains to be recorded. Planning references should not be
  counted as completed literature review without review notes.

## 6. Problems, decisions, and guidance needed

| Issue or decision                                                     | Effect on research / deadline                              | Next action                                                                                                        | Owner / target date     |
|---                                                                    |---                                                         |---                                                                                                                 |---                      |
| Perfer perl over python for scripts; XML::LibXML unavailabled on host | initial extraction approach required adjustment            | retain the working extraction approach, record dependencies and script version; candidate output has been obtained | Researcher / Week 1     |
| earlier prototype and baseline use different evidence paths           | could lead to mixing inputs or overstating reproducibility |record each input ARF, content version, mapping version, and output path separately                                 | Researcher November 8   |
| six-rule subset not finalized | EXP-01 covers one selected control; broader scope remains open | Freeze the six-rule subset and remaining scenario hypotheses | Researcher / November 8 |
| Drop-in permissions control changed from pass to fail | could represent an unintended configuration consequence, cause is unverified | inspect saved OVAL evidence and exact affected path/mode; preserve original post-state | Researcher / week 1 |
| Enrichment text is static | before/after reports show result changes but identical curated explanations | add result-dependent assessment and scan-specific evidence joins, including missing/conflicting evidence | Researcher / Week 1 |
| snapshot IDs, hashes, and test transcripts not yet attached           | limis reproducibility and auditability                     | add an evidence manifest and exact run references                                                                  | Researcher / November 8 |

**Scope or method changes:** Contextual enrichment is the primary
contribution.  Controlled security and service tests will evaluate
selected explanations and remediation consequences. Whole-profile
hardening and isolated-control experiments must remain distinguishable.

**Guidance requested from professor:** No specific request recorded yet.

## 7. Next-week commitments

### Week 1 Work

| Deliverable                                | Observable completion criterion                                                                                                      | Target date |
|---                                         |---                                                                                                                                   |---          |
| Frozen initial scope and baseline manifest | six exact rule IDs, scan-content version/hash, host facts, and snapshot lineage recorded                                             | November 8  |
| Close EXP-01 evidence gaps                 | attach complete pre/post access logs, exact intervention and hashes; investigate permissions regression; preserve initial comparison | November 8  |
| Dynamic enrichment assessment              | Generate different qualified assessments from the selected result and paired host evidence; test missing/conflicting inputs          | November 8  |
| Initial mapping record and method draft    | Versioned record with prerequisites, rationale, sources, limitations, and review state; written experiment procedure                 | November 8  |
| Week 1 report finalized                    | Replace pending entries with actual outcomes or explicity carryover; link retained evidence                                          | November 9  |

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
- **EXP-01 raw evidence:** /home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/{pre,post}/, with results.xml, results-arf.xml,
report.html, sshd-effective.txt, scan.log, start-time.txt, end-time.txt, and exit-code.txt listed in supplied output. Input hashes and full
access-test logs remain pending.
- **Inspected enriched reports:** pre-enriched.html and post-enriched.html.
- **Parrot evidence copy:** HOME/masters-project/evidence/EXP-001/20261104T203112Z; pre/post inputs confirmed readable in supplied output.
- **Mapping and prototype:** lab-content/ubuntu2404-context.xml; prototype branch feature/report-enrichment, commit 35efc53f8; exact mapping version/hash and full build manifest pending.
- **Current whitepaper:** Draft path/version not yet recorded.

<!-- Before submission:
- Every finding has evidence or is explicitly marked provisional.
- Planned work is not described as completed.
- Invalid runs and broken legitimate services are disclosed.
- Whole-profile effects are not attributed to an individual rule without evidence.
- Counts have clear denominators; unevaluated items are labelled.
- Next-week commitments have measurable completion criteria.
>
