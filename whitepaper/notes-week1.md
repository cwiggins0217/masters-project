---
title:
author: "Christopher Wiggins"
---

VM name: scap-b
Proxmox VM ID: 200
Role: baseline under preparation
Installation ISO filename:
CPU / RAM / disk: 2 / 4Gb / 64Gb
Network bridge / VLAN:
IP address: 10.10.20.198
Clean snapshot name: b00-clean-os
Clean snapshot created: 2026-11-02 19:59:21
Guest agent working: yes
SSH login from workstation working: yes
Nginx installed and externally tested: yes / no / not yet

```sh
cis-test@scap-b$ date -Is
2026-11-03T18:03:07+00:00
```

```sh
cis-test@scap-b:~$ hostnamectl
 Static hostname: scap-b
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: 0541d48fb8ca457bbfa178a814443641
         Boot ID: c6c754481ab1486f8a5d46b76c13ea87
  Virtualization: kvm
Operating System: Ubuntu 24.04.5 LTS
          Kernel: Linux 6.8.0-147-generic
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _i440FX + PIIX, 1996_
Firmware Version: rel-1.17.0-0-gb52ca86e094d-prebuilt.qemu.org
   Firmware Date: Tue 2014-04-01
    Firmware Age: 12y 7month 3d
```

```sh
cis-test@scap-b:~$ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.5 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```

```sh
cis-test@scap-b:~$ uname -r
6.8.0-147-generic
```

```sh
cis-test@scap-b:~$ ip -br address
lo               UNKNOWN        127.0.0.1/8 ::1/128
ens18            UP             10.10.20.198/24 metric 100 fe80::be24:11ff:feb9:6812/64
```

```sh
cis-test@scap-b:~$ lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS
NAME                      SIZE FSTYPE      MOUNTPOINTS
sda                        64G
├─sda1                      1M
├─sda2                      2G ext4        /boot
└─sda3                     62G LVM2_member
  └─ubuntu--vg-ubuntu--lv  31G ext4        /
```

```sh
cis-test@scap-b:~$ dpkg-query -W -f='${binary:Package}\t${Version}\n' \
> qemu-guest-agent openssh-server nginx openscap-scanner
nginx	1.24.0-2ubuntu7.19
openscap-scanner	1.3.9+dfsg-1.1ubuntu2
openssh-server	1:9.6p1-3ubuntu13.20
qemu-guest-agent	1:8.2.2+ds-0ubuntu1.18
```

```sh
cis-test@scap-b:~$ command -v oscap
/usr/bin/oscap
```

```sh
cis-test@scap-b:~/masters-project$ sha256sum content/scap-security-guide-0.1.82.zip \
  content/scap-security-guide-0.1.82/ssg-ubuntu2404-ds.xml \
  | tee evidence/setup/content-sha256.txt

765e84bdce7f9055f9b9c2dd0ee2b713d4255f8eec94eac6d35ea4973c28919c  content/scap-security-guide-0.1.82.zip
e311189ac70ff73be54121311fca324d6188f8c12ab53416090f595ff00e070c  content/scap-security-guide-0.1.82/ssg-ubuntu2404-ds.xml
```

```sh
$ sudo /usr/sbin/sshd -T | grep -E \
'^(permitrootlogin|permitemptypasswords|passwordauthentication|kbdinteractiveauthentication|usepam|authenticationmethods|maxauthtries) '
usepam yes
maxauthtries 6
permitrootlogin without-password
passwordauthentication yes
kbdinteractiveauthentication no
permitemptypasswords no
authenticationmethods any

$ sudo passwd -S root
root L 2026-02-10 0 99999 7 -1

$ sudo stat -Lc '%a %U:%G %n' /etc/ssh/sshd_config /etc/shadow
644 root:root /etc/ssh/sshd_config
640 root:shadow /etc/shadow

$ sudo grep -RniE \
'[[:space:]]*(Include|Match|PermitRootLogin|PermitEmptyPasswords|PasswordAuthentication|AuthenticationMethods)' \ /etc/ssh/sshd_config /etc/ssh/sshd_config.d
/etc/ssh/sshd_config:12:Include /etc/ssh/sshd_config.d/*.conf

/etc/ssh/sshd_config:42:#PermitRootLogin prohibit-password
/etc/ssh/sshd_config:66:#PasswordAuthentication yes
/etc/ssh/sshd_config:67:#PermitEmptyPasswords no
/etc/ssh/sshd_config:88:# PasswordAuthentication.  Depending on your PAM configuration,
/etc/ssh/sshd_config:90:# the setting of "PermitRootLogin prohibit-password".
/etc/ssh/sshd_config:92:# PAM authentication, then enable this but set PasswordAuthentication
/etc/ssh/sshd_config:127:#Match User anoncvs
/etc/ssh/sshd_config.d/50-cloud-init.conf:1:PasswordAuthentication yes
```


