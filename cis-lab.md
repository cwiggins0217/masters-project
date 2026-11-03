---
title: "CIS Hardening Impact Study -- Lab Notebook"
author: "Christopher Wiggins"
---

# Purpose and Scope
Study Question: What functional and security effects result from
applying a selected CIS Ubuntu 24.04 Level 2 server profile, and from
making specific exceptions to that profile?

Initial services: nginx HTTP and OpenSSH.

Measurements are separate:
1. Compliance: results reported by the selected scanner and content.
2. Functionality: whether specified legitimate operations work.
3. Security: whether specified adversarial actions succeed under a
   documented threat model.


An open port is evidence of exposure, not proof of vulnerability. A
higher compliance score is not by itself evidence that an attack was
prevented.


