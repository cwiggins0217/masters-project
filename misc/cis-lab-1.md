# How to use This Notebook

Edit this in emacs. Send only the contents of a selected shell block to
the indicated host. Org should paste the output to the following text
block. Run blocks individually, inspect the output, and then continue.

- Replace TODO values before execution
- commands assume bash on ubuntu
- reboots and shutdowns have their own blocks because they interrupt the
  session
- record errors and failures as evidence.
- for reruns, duplicate command/output entry with a new timestamp
- Never paste passwords, private keys, or other credentials here
- Save this notebook and supporting reports outside the experimental VMs
- this is a staged procedure, not a script to execute from top to bottom

# Purpose and Scope

Study question: What functional and security effects result from
applying a selected CIS Ubuntu 24.04 Level 2 Server profile, and from
making specific exceptions to that profile?

\*\*Initial services:\* nginx HTTP and OpenSSH.

Measurements are separate:

1.  Compliance: results reported by the selected scanner and content
2.  Functionality: whether specified operations work
3.  Security: whether specified adversarial actions succeed under a
    documented threat model.

An open port is evidence of exposure, not proof of vulnerability. A
higher compliance score is not by itself evidence that an attack was
prevented.

## Environment roles

  Label   Role                         Starting Point              ChangePolicy
  ------- ---------------------------- --------------------------- -------------------------------------------
  C0      working service baseline     fresh Ubuntu 24.04 Server   freeze after tools and evidence are ready
  H0      hardened reference           full clone of frozen C0     apply selected profile; verify and freeze
  E01     first experimental variant   full clone of frozen H0     only documented experimental changes
  T0      independent test client      separate Ubuntu VM          keep tools and test procedures consistent

H0 means the profile was applied. It does not imply full compliance.

## Decisions

  Decision                Planned Choice                              Actual Choice/reason for deviation
  ----------------------- ------------------------------------------- ------------------------------------
  Hypervisor              Proxmox                                     TODO
  Target OS               Ubuntu Server 24.04 LTS                     TODO
  Services                nginx and SSH                               TODO
  Hardening engine        OpenSCAP                                    TODO
  Content Provider        ComplianceAsCode                            TODO
  Intended Profile        CIS Level 2 Server                          Exact ID pending verification
  Target resources        2 vCPU, 4GB RAM, 40GB disk                  TODO
  Test Client resources   2 vCPU, 2GB RAM, 20GB disk                  TODO
  Disk layout             Default installer layout;                   TODO
  Trial policy            same tests and conditions for each target   TODO

# Preserve the Pilot

Before retiring the old environment:

- [ ] preserve remediation scripts and their checksums
- [ ] Preserve scanner results, reports, and logs
- [ ] Keep a recoverable VM backup or snapshot until replacements are
  verified
- [ ] Distinguish pilot observations from results of this new study

Archive Location: TODO Old VM IDs: TODO Date Archived: TODO Recovery
verified:TODO

# Proxmox and Network record

Configure networking through the existing proxmox setup. Do not
repurpose the management bridge

- [ ] Dedicated lab network selected.
- [ ] T0 can reach the targets
- [ ] Installation/update internet access available.
- [ ] No inbound internet port forwarding to targets
- [ ] proxmox console recovery available
- [ ] static IPs or DHCP reservations assigned
- [ ] Testing contained to the authorized lab

  Item                                  Actual Value
  ------------------------------------- --------------
  Proxmox Version/node                  TODO
  Lab bridge/VLAN                       TODO
  Gateway                               TODO
  DNS                                   TODO
  Internet egress policy during tests   TODO
  Management access path                TODO
  Host resource contention              TODO

  Label   Proxmox VM ID   Hostname   IP/Prefix   MAC address   Admin Username
  ------- --------------- ---------- ----------- ------------- ----------------
  C0      TODO            c0         TODO        TODO          TODO
  H0      TODO            TODO       TODO        TODO          TODO
  E01     TODO            TODO       TODO        TODO          TODO
  T0      TODO            t0         TODO        TODO          TODO

Clone identity changes must be recorded. ensure unique mac/IP addresses.
Record hostname, machine identity, SSH host-key handling so intentional
clone differences are distinguishable from hardening changes.

# Install C0

Date/Time: TODO

  Installer Item                     Actual Value
  ---------------------------------- --------------
  ISO filename and source            TODO
  ISO SHA-256                        TODO
  Ubuntu release / point release     24.04 LTS
  Installation type                  TODO
  Disk layout/LVM choice             TODO
  CPU type / vCPU                    TODO
  RAM / ballooning                   TOOD
  Disk controller/ storage backend   TODO
  firmware / machine type            TODO
  NIC model                          TODO

Installer checklist:

- [x] Standard Ubuntu Server installation
- [x] Hostname c0
- [x] ordinary administrator account with sudo
- [x] OpenSSH server installed
- [x] optional application bundles skipped
- [ ] QEMU guest agent enabled in proxmox VM options

# C0 -- Identify the session

Executed at: TODO

```{=org}
#+src: bash
```
date -Is hostnamectl whoami cat /etc/os-release uname -r

```{=org}
#+end_src
```
# C0 -- update and install services

```{=org}
#+src: bash
```
sudo apt update sudo apt full-upgrade -y sudo apt install -y nginx curl
openssh-sever qemu-guest-agent sudo systemctl enable -- now nginx ssh
qemu-guest-agent

```{=org}
#+end_src
```
# C0 -- reboot

```{=org}
#+src: bash
```
sudo reboot

```{=org}
#+end_src
```
# C0 -- create HTTP marker

```{=org}
#+src: bash
```
printf \'%s`\n`{=latex}\' \'cis-lab-web-ok\' \| sudo tee
/var/www/html/health.txt sudo nginx -t curl --fail --silent --show-error
<http://127.0.0.1/heath.txt> printf \'curl~exit~=%s`\n`{=latex}\'
\"\$?\"

```{=org}
#+end_src
```
****Expected:**** nginx configuration test succeeds; reponse is
cis-lab-web-ok; curl exit status 0.

# C0 -- inspect services and listeners

```{=org}
#+src: bash
```
systemctl is-active nginx ssh systemctl status qemu-guest-agent
--no-pager sudo ss -lntup

```{=org}
#+end_src
```
****Interpretation:**** TODO

# Configure T0 and verify remotely

```{=org}
#+src: bash
```
sudo apt update sudo apt install -y curl openssh-client nmap

```{=org}
#+end_src
```
# T0 -- set session variables

```{=org}
#+src: bash
```
TARGET=\'TODO~C0~\_IP\' ADMIN=\'TODO~ADMIN~\_USERNAME\' date -Is
hostname printf\'target=%s admin=%s`\n`{=latex}\' \"\$TARGET\"
\"\$ADMIN\"

```{=org}
#+end_src
```
# F-HTTP-01 -- retrieve known content

Execution host: T0 Target: C0 Executed at: TODO

```{=org}
#+src: bash
```
curl --fail --silent --show-error --max-time 5
\"<http://$TARGET/health.txt>\" printhf \'curl~exit~=%s`\n`{=latex}\'
\"\$?\"

```{=org}
#+end_src
```
