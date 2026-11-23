---
title: "Context-aware Assessment of Linux Hardening"
subtitle: "Enriching OpenSCAP Reports with Security and Functional Impact"
author: "Christopher Wiggins"
date: "November 2026"

documentclass: article
fontsize: 11pt
geometry:
    - margin=1.00in
---

```abstract

```

# Introduction

One of the leading problems in the current Information Systems Industry is
effective security hardening of servers and the systems they run. One of
the most important aspects of the solution is the scanning, detection
and remediation of security vulnerabilities. The Security Content Automation
Protocol (SCAP), developed by the National Institute of Standards and
Technology (NIST), was created to facilitate this solution, and is an
attempt to provide a standard that could be used by different products
to automate security compliance scanning and hardening.

One of the weaknesses of the current implementation of SCAP is that the
reports generated can be difficult to read and use by the user. The
current reports provide information about identified deviations from
security baselines, but do not provide additional relevant context
around why the rules were considered compliant/noncompliant (what
preconditions led to this), what effect the proposed change would have
on a system and it's services, whether an improvement leads to a
meaningful reduction in attack surface, and leaves the decision making to the
user who may need to perform additional research on their own.

OpenSCAP evaluates security configuration using SCAP content and can
produce reports from the resulting assessments. ComplianceAsCode
supplies machine-readable security policies, including content
implementing CIS guidance [1]. These capabilities provide the foundation
for this project; the proposed enrichment supplements the existing
report rather than replacing its checks or remediation information.

## Research Question

To what extent can OpenSCAP compliance reports be extended with
contextual assessments that explain configuration findings, remediation
effects, and their implications for system functionality and attack
surface?

The problem addressed here is how to present that relationship
consistently and traceably. A failed configuration check identifies a
departure from the evaluated policy, but a useful explanation of its
security relevance also needs the conditions under which a particular
access or attack route is possible, as well as the holistic
configuration of surrounding services. A passing result likewise needs a
bounded interpretation: it establishes the outcome of that check, not
universal protection against an adversary technique. Operational
consequences must be evaluated alongside the configuration change when a
service or administrative workflow is required.

## Proposed Solution

The proposed solution provided in this project is a system for an
"Enhanced Report" generation added to OpenSCAP that separates reusable
knowledge about a control from observations about a specific host and
from the conclusions drawn using those observations. Its intended output
is a report in which each substantive assessment can be traced to a
mapping revision, a selected scan result, and supporting evidence. The
initial implementation appends curated context to native OpenSCAP HTML.
The planned extension will regenerate host-specific interpretations
after a new scan and evidence refresh.

The project does not assume that existing tools lack contextual
explanations, nor does it claim that this approach is novel across
literature. A comparative related-work review remains necessary before
making that claim. Improved administrator comprehension is a motivation,
not a measured outcome of the present laboratory study.

## Contributions
In this project, I produced blah.

# Technical Background

## OpenSCAP

OpenSCAP is an open source implementation of the National Institute
of Standards and Technology (NIST)'s Security Content Automation Protocol
(SCAP), developed by Red Hat. (https://static.open-scap.org/openscap-1.3/oscap_user_manual.html).
The OpenSCAP ecosystem provides multiple tools that allow administrators to
assess, measure, and enforce security controls (open-scap.org).

## XCCDF and how it's used by OpenSCAP

XCCDF is "A structured collection of security configuration rules for
some set of target systems." It is designed to support generating
documentation for organizational and situational tailoring and automate
compliance testing through scoring. The specification defines a data
model and format for storing results of checklists and other guides, and
therefore facilitates a more common use of better security practices.

## Overview of XSLT

## Existing Limitations

# System Design and Implementation

# Experimental Methodology

# Results

# Discussion

# Conclusion and Future Work

# References 
