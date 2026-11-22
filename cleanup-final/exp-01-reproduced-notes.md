## EXP-01: Assessment Pipeline and Reproducibility Verification

**Verification date:** November 21, 2026  
**Experiment:** EXP-01 — SSH Root Login and Configuration Permissions  
**Target:** `scap-exp01`  
**Assessment phases:** Pre-hardening, post-hardening, permissions follow-up

### 1. Input Evidence

Evidence directory:

```text
/home/attacker/masters-project/evidence/EXP-01/20261104T203112Z/
```

Inputs:

- `pre/results.xml`
- `pre/sshd-effective.txt`
- `post/results.xml`
- `post/sshd-effective.txt`
- `followup-permissions-20261105T184154Z/results.xml`
- `followup-permissions-20261105T184154Z/sshd-effective.txt`

### 2. Evidence Processing Pipeline

1. **`compare-exp01.pl`** — Reads saved OpenSCAP XCCDF results and effective SSH configuration evidence using Perl and `XML::LibXML`.
2. **`comparison.json`** — Stores extracted rule outcomes, SSH settings, assessment phases, consistency checks, comparisons, file paths, and SHA-256 hashes.
3. **`comparison-to-xml.pl`** — Converts the comparison JSON into structured assessment XML.
4. **`assessment.xml`** — Stores phase-specific assessment records, rule results, observed settings, provenance, comparisons, and limitations.
5. **`xccdf-report-assessment.xsl`** — Loads the assessment XML, selects the appropriate phase and rule, validates consistency with the XCCDF `TestResult`, and renders assessment information.
6. **`xccdf-report-impl.xsl`** — Integrates the assessment renderer into the original OpenSCAP HTML report through the `evidence-assessment` template call.

### 3. Reproduction Commands

Generate the comparison JSON:

```sh
EVIDENCE="/home/attacker/masters-project/evidence/EXP-01/20261104T203112Z"

perl week2-comparison/compare-exp01.pl \
  --pre "$EVIDENCE/pre" \
  --post "$EVIDENCE/post" \
  --followup "$EVIDENCE/followup-permissions-20261105T184154Z" \
  --format json > comparison.json
```

Generate the assessment XML:

```sh
perl week2-renderer/comparison-to-xml.pl \
  comparison.json > assessment.xml
```

Validate the generated XML:

```sh
xmllint --noout assessment.xml
```

Compare against the original assessment artifact:

```sh
diff -u \
  week2-renderer/assessment.xml \
  assessment.xml
```

### 4. Verification Results

- [x] All six original evidence files located.
- [x] Comparison program executed successfully (exit status `0`).
- [x] Generated JSON validated successfully.
- [x] Expected rule-result transitions recovered.
- [x] Consistency status reported as `consistent` for all three phases.
- [x] SSH settings extracted with `observed` status.
- [x] Assessment XML regenerated.
- [x] Generated XML validated without reported errors.
- [x] Comparison with original assessment XML produced no differences.

### 5. Observed Rule Transitions

| Security Rule | Pre | Post | Follow-up |
|---|---|---|---|
| `sshd_disable_root_login` | fail | pass | pass |
| `file_permissions_sshd_drop_in_config` | pass | fail | pass |

Interpretation:

- **Root SSH login:** The control improved from FAIL to PASS following hardening and remained PASS during follow-up.
- **SSH drop-in permissions:** The control regressed from PASS to FAIL after the initial intervention, then returned to PASS following corrective action.
- **Consistency:** Extracted SSH configuration observations agreed with the recorded scan verdicts according to the script's consistency checks.

### 6. Reproducibility Finding

The regenerated `assessment.xml` was identical to the original assessment artifact, as demonstrated by an empty `diff` result.

This verifies that the assessment data can be reproduced from saved experimental evidence using the two Perl processing scripts.

The result supports the reproducibility of the evidence-processing and serialization stages. It does not independently establish the historical accuracy of captured evidence or prove that the hardening prevented an attack.

### 7. Implementation Limitations

- The extractor currently supports two selected SSH-related security rules.
- Experimental phases are identified by researcher-supplied directory arguments.
- The extractor does not independently verify VM snapshot lineage or experimental conditions.
- SHA-256 hashes identify input contents but do not authenticate their historical origin.
- Scan-result transitions do not establish exploitability or attack prevention.
- Effective SSH configuration observations do not establish successful or unsuccessful authentication.
- The permissions follow-up is a targeted evaluation and should not be treated as a complete profile assessment.
- The assessment XML generator is separate from the curated security-context enrichment process.

### 8. Remaining Work

- [ ] Trace the `xccdf-report-enrichment.xsl` data flow.
- [ ] Document how `context.xml` is populated and matched to XCCDF rules.
- [ ] Reproduce the complete HTML report from the regenerated assessment XML.
- [ ] Record script versions or Git commit identifiers used during verification.
- [ ] Incorporate the verified architecture and reproducibility findings into the whitepaper's methodology and implementation sections.

### Enrichment Architecture — Final Findings

- The report implementation includes `xccdf-report-enrichment.xsl`.
- The `result-details-leaf` template invokes `security-context`, passing the current XCCDF rule through `$item`.
- The enrichment stylesheet receives the external XML path through the `enrichment-file` parameter.
- The `document()` function loads the enrichment XML.
- The stylesheet selects the enrichment root element and checks its schema version.
- The current benchmark is obtained through `$item/ancestor::cdf:Benchmark`.
- An enrichment entry is selected using benchmark ID, benchmark version, and rule ID.
- Duplicate matching entries terminate the transformation.
- A missing matching entry produces an explicit message.
- Matching entries render curated guidance, sources, explanations, references, and limitations according to conditional XSLT logic.
- The current Ubuntu 24.04 enrichment file contains entries for SSH root-login and SSH configuration drop-in permissions.
- The contextual information is marked project-authored and pending independent review.
- No automated content generator was identified by the provenance search.
- The November 5 provenance snapshot predates the expanded November 11 enrichment file.
- The enrichment content is rule-specific but not directly dependent on the current compliance verdict.
- Phase-dependent assessment information is supplied separately through `xccdf-report-assessment.xsl`.

**Conclusion:** The enrichment extension provides curated, version-specific security context, while the assessment extension supplies experimental evidence and evaluation-specific interpretation. Both are integrated into OpenSCAP's existing XSLT report-generation process.
