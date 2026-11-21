---
title: "Stage-1"
author: "Christopher Wiggins"
---

# 1. What problem are you trying to solve that OpenSCAP doesn't already solve?
Trying to make compliance/security reporting more helpful and useful to
users, namely, to provide the user with more context about why a control
was passed/failed, what conditions led to that decision by openscap, how
and why they should "fix" or "harden" that control(s), and any
documentation relevant to the report. I also want to pilot a research
method that would allow openscap reports to have documentation on what
affect certain hardening controls have on expected server functionality,
i.e. with commonly used services. For example, whether or not enacting
this/that control "breaks anything", and if it does, how to fix it.

# 2. What is the proposed solution?
An "enchanced" xslt scheme that links security controls together
"dynamically", meaning, relates certain controls together in terms of
pass/fail and how their state affects each other, why (shows relevant
documentation), and changes as the state of the server changes. I'm a
little shaky on this explanation, and I don't really understand the xslt
system very well right now. This might not even be an adequate
definition of the solution.

# 3. How does your solution work, technically?
"Enhanced" XSLT scheme that changes dynamically with changes in server
state as well as relationships to other controls. Added
information/context includes reasons why openscap marked a control as
pass/fail, how to fix it and *why*, what affect it has on server
function (?), and supporting documentation from, for example, mitre
att&ck database, Ubuntu official manuals, etc.

# 4. How did you evaulate it?
I utilized Proxmox to virtualize (kvm/qemu) an Ubuntu 24.04 LTS server,
used openscap to scan a "baseline" server (has some preliminary configuration,
will be provided in project documentation), and cloned the server for
the proceeding experiments. For the experiments, I changed security
controls in three categories: SSH, nginx, and cron.d (file permissions),
according to prior openscap report results, and documented the affects
the changes had on the report results, the function of the
server/service, and on the attack surface resulting from the change (how
it affects an attacker's ability to gain access to the system through
the hardened control)

# 5. What did you demonstrate, and what remains unproven?
Demonstrated the enhanced reports, and affects of changes to controls on
server functions. I don't think we really did that much pentesting, like
I originally wanted?

