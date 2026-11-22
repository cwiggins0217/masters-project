# xsl:include -> element is a top-level element that includes the contents of one style sheet into another.
Note: An included style sheet has the same precedence as the including style sheet.

xsl/xccdf-report.xsl
depends (include) on xccdf-report-impl.xsl

xsl/xccdf-report-impl.xsl
depends (include) on xccdf-branding.xsl, xccdf-references.xsl,
xccdf-resources.xsl, xccdf-share.xsl, xccdf-report-oval-details.xsl,
xccdf-report-enrichment.xsl (my addition), xccdf-report-assessment.xsl
(my addition)

xsl/xccdf-guide.xsl
depends on (include) xccdf-guide-impl.xsl

xsl/xccdf-guide-impl.xsl
depends on (include) xccdf-branding.xsl, xccdf-resources.xsl,
xccdf-share.xsl, xccdf-references.xsl

# xsl:template -> contains rules to apply when a specified node is matched.

The match attribute is used to associate the template with an XML element. The match attribute can also be used to define a template for a whole branch of the XML document (i.e. match="/" defines the whole document).

Note: xsl:template is a top-level element.

xsl/xccdf-report.xsl
template mactch "/"

xsl/xccdf-report-impl.xsl
template name="introduction"
template name="characteristics"
template name="compliance-and-scoring"
template name="references-to-json"
template name="rule-overview-leaf-table-row"
template name="rule-overview-leaf"
template name="rule-overview-inner-node"
template name="rule-overview"
template name="check-system-details-oval5"
template name="check-system-details-sce"
template name="check-system-details"
template name="result-details-leaf-table"
template name="result-details-leaf"
template name="result-details-inner-node"
template name="result-details"
template name="generate-report"


xccdf-report.xsl
│
└── template match="/"
    │
    └── call-template: generate-report
        │   Parameters:
        │   ├── testresult
        │   └── benchmark
        │
        ├── css-sources
        ├── js-sources
        ├── xccdf-report-header
        ├── introduction
        ├── characteristics
        ├── compliance-and-scoring
        ├── rule-overview
        ├── result-details
        ├── rear-matter
        └── xccdf-report-footer
        note: last 10 not really relevant for my purposes, focus on
        "generate-report"

I identified testresult and benchmark as parameters passed into generate-report.

These are particularly important because they potentially connect the transformation to two fundamental XCCDF structures:
- Benchmark: The security rules, groups, profiles, and related definitions.
- TestResult: The results of evaluating those rules against a target system.
When you resume, examine the actual XPath expressions passed into those parameters.

name="testresult" identifies the parameter in the template being called.
select="$testresult" references an existing XSLT variable or parameter named testresult in the calling scope.
The $ prefix means you're referencing a variable or parameter, not selecting an XML element directly

generate-report
    |
    +-- result-details
          |
          +-- result-details-inner-node
                |
                +-- result-details-inner-node (recursive)
                |
                +-- result-details-leaf
                      |
                      +-- result-details-leaf-table
                      |
                      +-- check-system-details
                      |
                      +-- evidence-assessment  [ADDITION]
                      |
                      +-- security-context     [ADDITION]

2. The critical mechanism: matching rules to results Look at this
   expression from line 925: <xsl:variable name="ruleresult"
   select="key('testresult_ruleresults', concat($testresult/@id, '|',
   $item/@id))"/>

And the key declaration at line 420: <xsl:key
name="testresult_ruleresults" match="//cdf:rule-result"
use="concat(ancestor::cdf:TestResult/@id, '|', @idref)"/>

This is one of the most important parts of the implementation.

The stylesheet constructs an indexed lookup connecting:
- The identifier of a particular XCCDF TestResult.
- The identifier of a particular benchmark Rule.
- The corresponding rule-result element. The lookup uses both
  identifiers to find the relevant result.

This is how the report can obtain the evaluation outcome for a rule
while traversing the benchmark's rule definitions.

It also handles multiple results for one rule, which can occur with
XCCDF multi-check behavior.

3. Your additions are integrated at the individual rule level The
   decisive lines are 976–983:
   <xsl:call-template
   name="evidence-assessment"> <xsl:with-param name="item"
   select="$item"/> <xsl:with-param name="testresult"
   select="$testresult"/> <xsl:with-param name="result"
   select="$result"/> </xsl:call-template>

<xsl:call-template name="security-context"> <xsl:with-param name="item"
select="$item"/> </xsl:call-template>

This establishes that the additional functionality is invoked while
constructing the detailed section for an individual evaluated rule.

Specifically: Template	Parameters received evidence-assessment	$item,
$testresult, $result security-context	$item

Here $item represents the benchmark rule definition, while $result is
the selected evaluation outcome.

This gives your new templates access to rule identity and, for the
assessment template, the overall evaluation context and result.

Important: This confirms where your templates are invoked, but not yet
how they use external assessment.xml and context.xml. We still need to
inspect their implementations.

I'm not replacing its evaluation mechanism. I'm extending its XSLT-based
presentation layer to incorporate additional information alongside
existing XCCDF results.

That distinction is central to your whitepaper because it defines the
scope of your contribution and separates compliance evaluation from
post-evaluation interpretation and assessment.

My assessment stylesheet loads the external XML document.
<xsl:variable name="a"
    select="document($assessment-uri)/assessment[@schema='1.0']"/>


Here's what happens:
1. document($assessment-uri) loads the XML document identified by
   $assessment-uri.
2. /assessment[@schema='1.0'] selects its assessment root element,
   provided the schema attribute equals 1.0.
3. <xsl:variable name="a"> assigns the selected node-set to $a.
   Important: $a contains a reference to the selected XML node, not the
   XML document's text or filename.


Your custom stylesheets are included in the report generator
<xsl:include href="xccdf-report-enrichment.xsl" /> <xsl:include
href="xccdf-report-assessment.xsl" />

These declarations make the templates defined in your two stylesheets
available to xccdf-report-impl.xsl.

However, including a stylesheet does not execute its templates.
Execution occurs when a template is invoked, for example through
xsl:call-template.

We already established from your earlier output that result-details-leaf
calls both: <xsl:call-template name="evidence-assessment">


and: <xsl:call-template name="security-context">

Your implementation now has a verified execution path
xccdf-report.xsl
  └── match="/"
       └── generate-report
            └── result-details
                 └── result-details-inner-node
                      ├── result-details-inner-node (recursive)
                      └── result-details-leaf
                           ├── result-details-leaf-table
                           ├── check-system-details
                           ├── evidence-assessment
                           └── security-context


phase selection, conditional rendering, and report-wide limitations.
1. Line 9 — Selecting the assessment phase <xsl:variable name="p"
   select="$a/phase[@name=$assessment-phase]"/>


You've already established that $a references the root <assessment>
element.

This expression selects its <phase> children whose name attribute
matches $assessment-phase.

For example, if the parameter is post, it selects: <phase name="post">
... </phase>


This is how your report can select between assessment phases without
changing the XSLT itself.
2. Line 13 — Deciding whether to display an assessment <xsl:if
   test="$item/@id='xccdf_org.ssgproject.content_rule_sshd_disable_root_login'
   or
   $item/@id='xccdf_org.ssgproject.content_rule_file_permissions_sshd_drop_in_config'
   or $a/phase/rule[@id=$item/@id]">


This condition evaluates to true if any of the following holds:
1. The current XCCDF rule is sshd_disable_root_login.
2. The current XCCDF rule is file_permissions_sshd_drop_in_config.
3. A matching rule exists in any phase of the assessment XML. The third
   condition is especially interesting: $a/phase/rule[@id=$item/@id]


It searches all assessment phases, not just the selected phase $p.

That means an assessment section may be displayed for a rule even when
that rule has no assessment record in the currently selected phase.

This might be deliberate, particularly if you want to communicate
missing evidence. But it's worth investigating.

Also, the first two conditions are hardcoded rule identifiers. They
ensure that those rules receive assessment rendering regardless of
whether a corresponding assessment record exists.

For your whitepaper, this is an implementation limitation worth
documenting if those exceptions remain in the final version.
3. Line 163 — Rendering limitations <h5>Limitations</h5> <ul>
   <xsl:for-each select="$a/limitation"> <li><xsl:value-of
   select="."/></li> </xsl:for-each> </ul>


This iterates over every <limitation> directly beneath the <assessment>
root.

Each limitation becomes an HTML list item.

Notice that it uses $a, not $p.

Consequently, these limitations are assessment-wide, rather than
specific to the selected phase or individual rule.

assessment.xml
    |
    v
document($assessment-uri)
    |
    v
assessment[@schema='1.0']
    |
    v
   $a
    |
    +-- phase[@name=$assessment-phase]
    |       |
    |       v
    |      $p
    |       |
    |       v
    |   [Phase-specific assessment processing]
    |
    +-- phase/rule[@id=$item/@id]
    |       |
    |       v
    |   Determines assessment visibility
    |
    +-- limitation
            |
            v
        HTML list items


complete assessment lookup
assessment.xml
      |
      v
document($assessment-uri)
      |
      v
assessment[@schema='1.0']
      |
      v
$a
      |
      v
phase[@name=$assessment-phase]
      |
      v
$p
      |
      v
rule[@id=$item/@id]
      |
      v
$r (matching assessment record)


1. First, the assessment verifies its inputs Look at line 18: <xsl:when
   test="count($p)!=1 or count($r)!=1 ...">


This checks whether exactly one assessment phase and exactly one
matching rule record were found.

Remember:
- $p contains the selected assessment phase.
- $r contains the matching rule assessment within that phase.
- count($r)!=1 means a unique matching assessment record was not found.
  This prevents the stylesheet from treating missing or duplicate
  records as valid evidence.

Next, line 21 checks whether the assessment metadata agrees with the
XCCDF TestResult, including:
- Test result ID
- Scan start and end times
- Evaluation target
- Selected profile
- Rule result status This is significant for your research: The
  implementation checks whether assessment evidence corresponds to the
  scan being presented, rather than simply displaying arbitrary
  assessment data.

It does not independently prove the evidence is authentic, but it can
detect certain inconsistencies.
2. The assessment interprets results conditionally Your stylesheet
   contains special handling for SSH root-login and file-permission
   rules.

For example: <xsl:when test="$p/consistency/@status!='consistent' or
not($p/consistency/@status) or (($setting/value='no') !=
($result='pass'))">


This compares the observed PermitRootLogin configuration with the
OpenSCAP result.

Conceptually: Captured setting	Scan result	Interpretation no	pass
Configuration and result agree Not no	fail	Configuration and result
agree under the rule's expected condition no	fail	Potential
inconsistency Not no	pass	Potential inconsistency

This interpretation is conditional on the captured configuration being
relevant to the scan and the rule's applicability. The stylesheet also
checks the explicit consistency status.

This is particularly relevant to your EXP-01 experiment, where you
encountered differences between saved SSH configuration and scan
results.
3. The template generates several distinct report sections Your output
   shows logic for: Section	Purpose Reason for OpenSCAP result	Explains
   the recorded pass/fail outcome using available evidence Configuration
   evidence	Displays recorded settings and observations Related rule
   results	Checks other scan findings associated with the SSH
   configuration Recommended action	Provides conditional remediation or
   verification guidance Supporting evidence	Identifies recorded
   results and configuration evidence Documentation	Links to relevant
   rule and configuration references Limitations	Communicates
   constraints on the interpretation

These are derived from the expressions and HTML fragments in your
output; the exact complete section structure would require examining the
full stylesheet.


4. Your reconstructed architecture

OpenSCAP XCCDF TestResult

Rule identifier, verdict, scan metadata


result-details-leaf

Invokes evidence-assessment for the current rule


Assessment lookup

assessment.xml → $a → $p → $r

Selects the assessment phase and matching rule record


Validation and conditional interpretation

Checks metadata consistency, recorded observations, and scan verdicts


Enriched HTML rule assessment

Reasoning, evidence, recommendations, documentation, limitations


One important qualification: your uploaded search results show that
validation conditions exist, but we haven't inspected every surrounding
branch. We should not yet claim that every invalid input prevents all
assessment output.
5. One potential design limitation Your assessment implementation
   contains specialized logic for particular SSH and file-permission
   rules.

That means it is not yet necessarily a general-purpose engine for
interpreting arbitrary CIS controls.

It is more accurately described as a rule-aware reporting extension with
experimental evidence validation and specialized interpretation logic.

That is a defensible scope for your project. You can demonstrate the
architecture using a controlled collection of rules without claiming
that it automatically explains every possible hardening control.


Assessment data
    |
    v
week2-renderer/assessment.xml
    |
    v
xsltproc
    | --stringparam assessment-uri
    | --stringparam assessment-phase
    v
xccdf-report-assessment.xsl
    |
    v
Phase and rule selection
    |
    v
Assessment validation
    |
    v
HTML report

our latest search identified the program responsible for converting comparison data into assessment.xml:
week2-renderer/comparison-to-xml.pl


More importantly, we also found the upstream comparison program:
week2-comparison/compare-exp01.pl


This is the missing link in the architecture we've been reconstructing.
1. The evidence
Your search output contains:
week2-renderer/comparison-to-xml.pl:15:
    print '<phase name="',$phase,'">';

week2-renderer/comparison-to-xml.pl:16:
    for my $key (qw(test_result_id start_time end_time)) {
        print el($key,$p->{metadata}{$key});
    }


This establishes that comparison-to-xml.pl emits XML phase elements and scan metadata.

We also found:
week2-comparison/compare-exp01.pl:54:
    $s->{metadata} = {
        test_result_id => $tr->getAttribute('id'),


And an intermediate artifact:
masters-project/analysis/week2-exp01/comparison.json


The assessment XML itself contains a json-sha256 attribute, which suggests that its generation is linked to a JSON comparison input.

2. The reconstructed pipeline
OpenSCAP scan results and saved observations

Experimental evidence


compare-exp01.pl

Extracts and compares experimental data


comparison.json

Intermediate structured comparison


comparison-to-xml.pl

Serializes comparison data to assessment XML


assessment.xml

Phases, rule results, settings, provenance and limitations


xccdf-report-assessment.xsl

Selects, validates and renders assessment data


Enriched HTML report

Assessment and supporting context


The converter's complete input and output behavior still needs
verification, but the two scripts and intermediate JSON strongly support
this pipeline.
3. What this changes about our understanding Earlier, we suspected that
   assessment.xml might have been manually constructed.

We now have evidence of a programmatic conversion process.

However, we still need to distinguish automatically extracted
information from manually supplied observations and interpretations.

That distinction matters for your methodology because it determines how
much of the assessment pipeline is automated.


1. The complete data pipeline
results.xml

OpenSCAP scan results


sshd-effective.txt

Captured SSH configuration




compare-exp01.pl

Extracts results, compares phases, checks consistency, records provenance


comparison.json

Intermediate assessment data


comparison-to-xml.pl

Converts JSON assessment data into XML


assessment.xml

Phase-specific assessment records


xccdf-report-assessment.xsl

Matches assessment records to XCCDF rule results and renders assessment content


Enriched HTML report

OpenSCAP results with contextual explanations and supporting evidence


This diagram represents the assessment branch. The complete report
transformation also receives the original XCCDF results.xml and the
separate enrichment context input.

2. What the comparison script actually does
compare-exp01.pl performs several distinct operations.
Operation	Implementation
Reads scan results	Parses results.xml with XML::LibXML
Identifies evaluations	Locates XCCDF TestResult elements
Extracts selected rules	Finds rule-result entries using idref
Extracts SSH settings	Parses sshd-effective.txt
Compares phases	Evaluates pre/post and post/followup transitions
Checks consistency	Compares root-login scan results with saved PermitRootLogin
Records provenance	Calculates SHA-256 hashes of input files
Handles missing evidence	Produces indeterminate values and explanatory reasons

The implementation is deliberately scoped to two controls:
- sshd_disable_root_login
- file_permissions_sshd_drop_in_config
It also extracts three SSH configuration settings.

This is a specialized evidence extractor, not a general-purpose CIS assessment engine.
3. How the assessment is calculated
The script identifies rule-result transitions and classifies them.

For example, its logic distinguishes:
Pre	Post	Assessment
fail	pass	improved
pass	fail	regressed
pass	pass	unchanged
fail	fail	unchanged
unknown	pass	indeterminate

The script also evaluates consistency between the root-login rule's verdict and the captured PermitRootLogin value.

This is a separate assessment from whether the configuration change actually prevented an attack or preserved functionality.

The code explicitly acknowledges that limitation.
4. What comparison-to-xml.pl adds
The second script is primarily a serializer.

It reads the comparison JSON and produces the XML structure expected by your assessment XSLT.

It also:
- Escapes XML-special characters.
- Validates the JSON schema version.
- Computes a SHA-256 hash of the JSON input.
- Includes source paths and hashes.
- Writes phase-specific records and comparisons.
- Adds an explicit follow-up capture note.
An important distinction: the XML converter does not independently verify the experimental evidence. It serializes the results supplied by the comparison script, with some additional fixed explanatory content.
5. What this means for your whitepaper
You can now accurately describe the implementation as three stages:

Evidence extraction and comparison: A Perl program processes saved OpenSCAP results and SSH configuration observations, producing structured JSON with rule outcomes, comparison classifications, consistency checks, and source hashes.

Assessment serialization: A second Perl program converts the intermediate JSON into an XML document conforming to the assessment structure expected by the report extension.

Report integration: The modified OpenSCAP XSLT renderer uses phase and rule identifiers to select assessment records, checks their agreement with the current XCCDF evaluation, and renders additional explanatory information.

This is a stronger architectural account than simply describing the project as an XSLT modification.
6. Two methodological limitations worth documenting
There are two issues in the source that you should preserve in your research discussion.

First, the comparison script receives experiment directories through command-line arguments. It does not independently verify that the directories correspond to the correct VM snapshot or experimental condition.

Second, the root-login consistency check compares saved effective SSH configuration values with scan results. It does not prove whether SSH authentication actually succeeded or failed.

These are meaningful boundaries on what the assessment can conclude.


