---
title: "Master's Project Pilot"
author: "Christopher Wiggins"
date: "Wed Sep 9 2026"

geometry: margin=1in

mainfont: "DejaVu Sans"
monofont: "DejaVu Sans Mono"
fontsize: "11pt"
---

\newpage

# Project Purpose

The purpose of this project is to experimentally evaluate the security
and operational effects of selected CIS Benchmark configuration controls
on an Ubuntu 24.04 LTS server. Rather than treating benchmark compliance
in simple pass/fail terms, the study will examine whether individual
hardening controls materially alter the outcome of attacks against an
otherwise equivalent system.

This project will compare a baseline Ubuntu 24.04 LTS installation
against systems with selected CIS controls applied individually and in
combination. Each system will be subjected to repeatable attack
scenarios designed to measure whether a control prevents an attack,
limits its effects, changes the attacker's required technique, or has no
meaningful effect.

The study will also evaluate the operational consequences of each
control. A security control may successfully interfere with an attack
while simultaneously disrupting legitimate administrative or application
behavior. These effects will be documented alongside the security
results.

This pilot evaluates whether the selected CIS hardening recommendations
produce repeatable changes in a defined attack outcome without
unnecessarily disrupting legitimate system use.


# Research Question

To what extent do selected CIS Benchmark configuration controls change
the outcome of attacks against an Ubuntu 24.04 LTS system, and what
operational consequences result from implementing those controls?

## Supporting Research Questions

- Does a selected CIS control prevent exploitation, or does it primarily
restrict attacker activity after initial compromise?
- Does the control reduce the attacker's ability to execute code,
escalate privileges, establish persistence, access resources, or otherwise
expand the compromise?
- Can an attacker bypass the control using commonly available alternative
techniques?
- Does combining multiple related CIS controls provide a measurable security
benefit beyond applying them individually?
- What legitimate system administration, software installation, application,
or user workflows are disrupted by each control?
- Can observed attack effects be associated with particular CVEs, vulnerability
classes, or attack techniques in a way that provides useful context beyond the
CIS Benchmark itself?

# Working Hypothesis

Systems configured with selected CIS Benchmark hardening controls will exhibit
measurably reduced attack impact compared with an otherwise equivalent unhardened
system, but the effectiveness and operational cost of the controls will vary
substantially by control and attack technique.

More specifically, controls that restrict filesystem behavior, privileges,
or execution are expected to be more effective at limiting post-exploitation
activity than at preventing the initial exploitation of a vulnerable service.

Some controls are also expected to be bypassable. A control should therefore
not automatically be classified as ineffective when bypass is possible.
Instead, the experiment will measure whether the control increases the number,
complexity, or prerequisites of the actions required by the attacker.

## Independent Variable

The primary independent variable is the CIS hardening configuration applied
to the system.

For example:

- No hardening control (baseline)
- /tmp mounted with nodev
- /tmp mounted with nosuid
- /tmp mounted with noexec
- /var/tmp with equivalent restrictions
- /dev/shm with equivalent restrictions
- Selected combinations of these controls

Only the control or control set under investigation should be intentionally
changed between the baseline and experimental systems.

## Dependent Variables

The dependent variables are the observable security and operational outcomes
resulting from each configuration.

Security measurements may include:

- Initial exploitation success or failure
- Arbitrary command/code execution
- Execution of attacker-controlled files
- Privilege escalation
- Persistence
- Access to protected resources
- Ability to stage tools or payloads
- Ability to bypass the tested control
- Additional steps required to accomplish the attack objective
- Changes in attack technique required

Operational measurements may include:

- Application failures
- Package installation or upgrade failures
- Administrative script failures
- Temporary-file failures
- Service startup failures
- Changes to normal administrator workflows
- Additional configuration necessary to maintain legitimate functionality

## Primary Attack Outcomes:

Each attack trial should be classified according to its final result rather than
simply as "vulnerable" or "not vulnerable."

### 1. Prevented

The attack cannot achieve its intended objective because of the tested control.

### 2. Constrained

Initial compromise succeeds, but the control prevents or substantially limits a
later stage of the attack.

For example, an attacker obtains a shell but cannot execute a staged binary
from the intended temporary filesystem.

### 3. Bypassed

The original attack path is blocked, but the attacker can achieve the same
objective using an alternative technique.

The bypass method and additional requirements should be recorded.

### 4. Delayed / Increased Complexity

The attack remains possible, but the control requires additional steps, 
knowledge, tools, privileges, or system interaction.

### 5. Unaffected

There is no meaningful difference between the hardened and baseline systems for 
the tested attack.

These categories allow the experiment to capture an important distinction that 
a simple pass/fail measurement would miss: a control may provide security value 
even when it does not completely prevent compromise.

# Operational Impact Outcome

Each tested control should also receive an operational-impact classification:

**None**: No observed effect on legitimate operation.

**Minor**: A legitimate workflow requires a simple adjustment or workaround.

**Moderate**: Common administrative or application behavior fails and requires 
configuration changes.

**Severe**: The control prevents an important service or expected system function 
from operating normally.

The exact failure, workaround, and affected software should be recorded rather 
than relying exclusively on the categorical rating.

# Experimental Comparison and Scope

The fundamental experimental structure is:

### Control System

Ubuntu 24.04 LTS with the test filesystems present but without the CIS
hardening option being evaluated.

versus

### Experimental System

An otherwise equivalent Ubuntu 24.04 LTS system with the selected CIS
control applied.

Each attack should first be demonstrated against the baseline system.
This establishes that the attack scenario is functional before testing
whether a hardening control changes its outcome.

# Experimental Unit

A trial consists of:

**Known VM state → selected configuration → defined attack → observed
outcome → restoration to known state **

VM snapshots or clones should be used to return the system to the same initial 
condition before subsequent trials. This prevents artifacts from previous 
attacks from contaminating later results.

Where practical, trials should be repeated to distinguish reproducible control 
effects from incidental system behavior.

# Proposed Dataset

Each experimental observation can ultimately become a structured record 
containing fields such as:

**CIS Control → System Configuration → Attack Technique → CVE/CWE (when
applicable) → Baseline Outcome → Hardened Outcome → Bypass → Operational
Impact → Evidence → Confidence**

For example:

**CIS /tmp noexec control → arbitrary code execution scenario → baseline
payload executes → hardened payload cannot execute directly from /tmp →
alternative execution technique investigated → administrative impact
recorded**

This structure connects benchmark compliance to empirical security behavior 
rather than merely reporting whether a configuration passes a compliance scanner.

# Expected Contribution

The expected contribution of the project is not to demonstrate that CIS 
Benchmarks are universally effective or ineffective. Instead, the project seeks 
to provide empirical context for selected controls.

The resulting data should help answer a more useful administrative question than 
"Does this system pass the CIS Benchmark?"

The question becomes:

What security outcome does this control change, under what circumstances does 
it change it, how easily can its protection be bypassed, and what does 
implementing it cost operationally?

This information can ultimately supplement existing compliance-scanning tools 
such as OpenSCAP by providing administrators with security-effectiveness and 
operational-impact context when evaluating remediation recommendations.

\newpage

# Some examples of "control" configuration commands on an Ubuntu VM

Linux Distribution
: Ubuntu Server 24.04 LTS

Hypervisor :: Proxmox VE

Target VM :: Ubuntu Server 24.04

Test VM :: TBD

Benchmark :: TBD

Attack Scenario :: Unauthorized SSH access through password guessing

Primary Controls :: TBD

Repetitions :: Minimum 5 per condition

# Repository Layout

**`Repo Layout`**
```bash
.
├── README.md
├── data
├── evidence
├── img
├── init.md
├── logs
└── scripts
```

