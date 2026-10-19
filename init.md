---
title: "CIS Hardening Exception Experiment"
author: "Christopher Wiggins"
date: "[2026-10-16]"
---

# Experiment identification

- Experiment ID: [E01]
- Title: [Restoring Nginx after automated hardening]
- Researcher: [Name]
- Start/end time and timezone: [Record]
- Status: [Planned / running / completed]

# Research question and hypothesis

**Question:** Does restoring Nginx on a clone of H0 restore HTTP service, and which compliance checks and network exposures change?

**Hypothesis:** Reinstalling, unmasking, and enabling Nginx will restore local HTTP service and may make selected service-removal checks fail. Remote access depends on the existing network and firewall configuration.

**Scope:** This experiment measures service availability, compliance changes, and network exposure. An open HTTP port is not evidence of successful exploitation.

# Systems and provenance

| Field                          | B0                             | H0                                                  |
|---                             |---                             |---                                                  |
| Proxmox VM ID                  |                                |                                                     |
| Parent snapshot and timestamp  | os-ready-01 10/07/26 3:35:47pm | H0-pre-remediation 10/14/26 8:46:43am               |
| Hostname / IP                  | baseline-web 10.10.20.117      | H0 10.10.20.199                                     |
| Ubuntu release / kernel        | Ubuntu 24.04/6.8.0-147         | Ubuntu 24.04/6.8.0-147                              |
| vCPU / RAM / disk              | 2core/8gb/60gb                 | 2core/8gb/60gb                                      |
| OpenSCAP version               | none, baseline is not hardened | 1.3.9                                               |
| Profile ID / benchmark version | none                           | xxccdf_org.ssgproject.content_profile_level2_server |
| Nginx package version          | 1.24.0                         | 1.24.0                                              |
| Network / firewall state       |                                |                                                     |

Use the same saved data stream and profile for every scan. H0 is the observed post-remediation baseline; full CIS compliance has not been established. Assign the clone a unique IP before running it alongside H0. Record identity changes separately from experimental changes.

# Established observations

- The supplied remediation log and APT history show Nginx removal and service masking on H0.
- A later, separate autoremove removed nginx-common.
- UFW was removed; the effective firewall state still needs measurement.
- The provided evidence does not establish that remediation removed Apache, vsftpd, Dovecot, or the database packages.
- An unattended-upgrade transaction occurred; record whether package versions actually changed.

# Experimental design

- Independent variable: Nginx restoration as a bundle of package installation, unmasking, and service enablement.
- Dependent variables: local/remote HTTP response, TCP 80 state, service state, rule-level scan outcomes.
- Constants: VM resources, network path, test client, scan content/profile, HTTP request, and other hardening settings.
- Confounders: changed package versions, default configuration replacing the original site, automatic updates, firewall changes, or differences in test-client routing.
- Comparison: H1 before restoration versus H1 after restoration, with preserved H0 as reference.
- Repetition: three HTTP requests per state are repeatability checks, not independent experimental replicates. For independent repeats, restore the same parent snapshot and repeat the intervention.
- Stop condition: unexpected package changes, invalid Nginx configuration, or failed service startup. Capture evidence before troubleshooting.

# Procedure and change log

| Step                              | Timestamp | Command / action | Expected outcome | Actual outcome | Evidence file |
|---                                |---        |---               |---               |---             |---            |
| Preserve H0 snapshot              |           |                  |                  |                |               |
| Clone and assign H1 identity      |           |                  |                  |                |               |
| Capture baseline and scan         |           |                  |                  |                |               |
| Test HTTP before restoration      |           |                  |                  |                |               |
| Reinstall Nginx                   |           |                  |                  |                |               |
| Unmask and validate configuration |           |                  |                  |                |               |
| Enable/start Nginx                |           |                  |                  |                |               |
| Test HTTP after restoration       |           |                  |                  |                |               |
| Repeat compliance scan            |           |                  |                  |                |               |
| Compare rule outcomes             |           |                  |                  |                |               |

Record all recovery actions separately. Do not rerun automatic remediation during the measurement phase.

# Functional and exposure results

| Measurement             | H0 | H1 before | H1 after | Evidence |
|---                      |--- |---        |---       |---       |
| Nginx installed/version |    |           |          |          |
| Service enabled/masked  |    |           |          |          |
| Service active          |    |           |          |          |
| TCP 80 listener         |    |           |          |          |
| Local HTTP status/body  |    |           |          |          |
| Remote HTTP status/body |    |           |          |          |
| Remote TCP 80 scan      |    |           |          |          |
| Existing SSH access     |    |           |          |          |

| HTTP trial | Target/state | Timestamp | Client IP | curl exit status | HTTP status | Interpretation |
|---         |---           |---        |---        |---               |---          |---             |
| 1          |              |           |           |                  |             |                |
| 2          |              |           |           |                  |             |                |
| 3          |              |           |           |                  |             |                |

Differentiate connection refused, timeout, HTTP error response, and expected content. If local HTTP works but remote HTTP fails, investigate filtering/routing without immediately changing the firewall.

# Compliance results

| Result category                        | Before | After | Difference |
|---                                     |---     |---    |---         |
| pass                                   |        |       |            |
| fail                                   |        |       |            |
| error / unknown                        |        |       |            |
| notchecked                             |        |       |            |
| notapplicable                          |        |       |            |
| notselected                            |        |       |            |
| Reported score (record scoring system) |        |       |            |

| Rule ID                           | Benchmark reference | Before | After | Explanation / evidence |
|---                                |---                  |---     |---    |---                     |
| [Use actual IDs from the reports] |                     |        |       |                        |

Do not treat error, unknown, or notchecked as passes. Do not infer security strength from the aggregate compliance score alone.

# Security validation

- Test ID and exact action: [Record; use “not performed” if no exploitation test ran]
- Attacker/test-client starting privileges and network position: [Record]
- Prerequisites: [Record]
- Success criterion defined before test: [Record]
- H0 outcome: [Observed / not performed]
- H1 outcome: [Observed / not performed]
- Evidence: [Paths]

For E01, remote HTTP and port enumeration measure exposure only. Keep exploit success marked not tested unless a separate reproducible exploit experiment is performed.

# Interpretation and limitations

- Was the hypothesis supported? [Explain using evidence]
- What functionality was restored? [Specify]
- Which controls changed? [List actual rule IDs]
- What security outcome was measured? [Exposure, prevention, detection, or exploitation]
- Alternative explanations and limitations: [Record]
- Required-service applicability: [Explain why the web server is required and whether the benchmark permits a documented exception]

# Evidence inventory and next experiment

| Filename                 | Description                  | SHA-256 / timestamp |
|---                       |---                           |---                  |
| before.xml / before.html | Pre-change compliance scan   |                     |
| after.xml / after.html   | Post-change compliance scan  |                     |
| session.log              | Terminal transcript          |                     |
| package-state.txt        | Exact installed versions     |                     |
| network-state.txt        | Listeners and firewall rules |                     |
| remote-http.txt          | Client-side HTTP results     |                     |

- Final snapshot name: [Record]
- Follow-up experiment: [A single targeted control on a service-preserving baseline]
- Rollback: Restore the documented pre-experiment snapshot.

# References

- OpenSCAP manual: https://static.open-scap.org/openscap-1.4.1/oscap_user_manual.html
- Content release used: https://github.com/ComplianceAsCode/content/releases/tag/v0.1.82
- Nginx command options: https://nginx.org/en/docs/switches.html
- Exact CIS benchmark title/version and rule references: [Fill from the content/report]

