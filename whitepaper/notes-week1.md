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

```sh
$ perl <<'PERL'
use strict;
use warnings;
use XML::LibXML;
use XML::LibXML::XPathContext;

my $path = "$ENV{HOME}/masters-project/content/"
         . "scap-security-guide-0.1.82/ssg-ubuntu2404-ds.xml";

my $doc = XML::LibXML->load_xml(location => $path);
my $xc = XML::LibXML::XPathContext->new($doc);
$xc->registerNs(x => 'http://checklists.nist.gov/xccdf/1.2');

for my $name (qw(
    sshd_disable_root_login
    sshd_disable_empty_passwords
    file_permissions_sshd_config
)) {
    my $id = "xccdf_org.ssgproject.content_rule_$name";
    my ($rule) = $xc->findnodes("//x:Rule[\@id='$id']");
    die "Rule not found: $id\n" unless $rule;

    print "\n$name\n";
    for my $field (qw(title description)) {
        my $text = $xc->findvalue("x:$field", $rule);
        $text =~ s/\s+/ /g;
        print "$field: $text\n";
    }
}
PERL

sshd_disable_root_login
title: Disable SSH Root Login
description: The root user should never be allowed to login to a system directly over a network. To disable root login via SSH, add or correct the following line in /etc/ssh/sshd_config.d/00-complianceascode-hardening.conf: PermitRootLogin no 

sshd_disable_empty_passwords
title: Disable SSH Access via Empty Passwords
description: Disallow SSH login with empty passwords. The default SSH configuration disables logins with empty passwords. The appropriate configuration is used if no value is set for PermitEmptyPasswords. To explicitly disallow SSH login from accounts with empty passwords, add or correct the following line in /etc/ssh/sshd_config.d/00-complianceascode-hardening.conf: PermitEmptyPasswords no Any accounts with empty passwords should be disabled immediately, and PAM configuration should prevent users from being able to assign themselves empty passwords.

file_permissions_sshd_config
title: Verify Permissions on SSH Server config file
description: To properly set the permissions of /etc/ssh/sshd_config, run the command: $ sudo chmod 0600 /etc/ssh/sshd_config

```

For exp-001, we will use root-login restriction as the primary
intervention.

# scap-exp01
```sh
sudo hostnamectl set-hostname scap-exp01

ip -br address
lo               UNKNOWN        127.0.0.1/8 ::1/128
ens18            UP             10.10.20.198/24 metric 100 fe80::be24:11ff:fe5a:fd6/64 
```

Generate experiment key on attack/test workstation.

```sh
ssh-keygen -t ed25519 -f ~/.ssh/scap-exp001-root \
-C "EXP-01 root access test"
```

Copy the public key to the clone
```sh
scp ~/.ssh/scap-exp01-root.pub \
    cis-test@10.10.20.198:~/exp01-root.pub

ssh cis-test@10.10.20.198
```

```sh
$ sudo install -d -m 0700 -o root -g root /root/.ssh
$ sudo sh -c 'cat /home/cis-test/exp01-root.pub >> /root/.ssh/authorized_keys'
$ sudo chown root:root /root/.ssh/authorized_keys
$ sudo chmod 0600 /root/.ssh/authorized_keys

$ sudo /usr/sbin/sshd -t
$ sudo /usr/sbin/sshd -T | grep -E '^(permitrootlogin|pubkeyauthentication|authorizedkeysfile) '
permitrootlogin without-password
pubkeyauthentication yes
authorizedkeysfile .ssh/authorized_keys .ssh/authorized_keys2
```

test access paths from test workstation

```sh
$ ssh -o IdentitiesOnly=yes \
  -o PreferredAuthentications=publickey \
  -o PasswordAuthentication=no \
  -o KbdInteractiveAuthentication=no \
  -i ~/.ssh/scap-exp001-root \
  root@CLONE_IP 'id'

uid=0(root) gid=0(root) groups=0(root)

$ ssh -t cis-test@10.10.20.198 'sudo id'
uid=0(root) gid=0(root) groups=0(root)
```

## capture fresh pre-intervention scan
```sh
cd ~/masters-project

DS="$HOME/masters-project/content/scap-security-guide-0.1.82/ssg-ubuntu2404-ds.xml"
PROFILE="xccdf_org.ssgproject.content_profile_cis_level1_server"
EXP="$HOME/masters-project/evidence/EXP-001/$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$EXP"/{pre,post}
sudo -v

date -Is > "$EXP/pre/start-time.txt"
sudo /usr/sbin/sshd -T > "$EXP/pre/sshd-effective.txt"

sudo oscap xccdf eval \
  --profile "$PROFILE" \
  --results "$EXP/pre/results.xml" \
  --results-arf "$EXP/pre/results-arf.xml" \
  --report "$EXP/pre/report.html" \
  "$DS" > "$EXP/pre/scan.log" 2>&1

$ SCAN_RC=$?
$ printf '%s\n' "$SCAN_RC" > "$EXP/pre/exit-code.txt"
$ date -Is > "$EXP/pre/end-time.txt"
$ printf 'Exit: %s\nEvidence: %s\n' "$SCAN_RC" "$EXP"
Exit: 2
Evidence: /home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z
```

Confirm root-login rule's result
```sh
$ perl -MXML::LibXML -MXML::LibXML::XPathContext \
  - "$EXP/pre/results.xml" <<'PERL'
use strict;
use warnings;

my $doc = XML::LibXML->load_xml(location => $ARGV[0]);
my $xc = XML::LibXML::XPathContext->new($doc);
$xc->registerNs(x => 'http://checklists.nist.gov/xccdf/1.2');

my $id = 'xccdf_org.ssgproject.content_rule_sshd_disable_root_login';
my ($result) = $xc->findnodes("//x:rule-result[\@idref='$id']");
die "Rule result missing\n" unless $result;

print "sshd_disable_root_login: ",
      $xc->findvalue('x:result', $result), "\n";
PERL

sshd_disable_root_login: fail
```

next, apply intervention, changing root-login policy on scap-exp01, then
repeat both access tests

```sh
$ sudo test -e /etc/ssh/sshd_config.d/00-complianceascode-hardening.conf \
    && echo "EXISTS — inspect before editing" \
    || echo "ABSENT — ready to create"
ABSENT — ready to create

$ printf '%s\n' 'PermitRootLogin no' |
    sudo tee /etc/ssh/sshd_config.d/00-complianceascode-hardening.conf
PermitRootLogin no

$ sudo /usr/sbin/sshd -t && sudo systemctl reload ssh

$ sudo /usr/sbin/sshd -T | grep '^permitrootlogin '
permitrootlogin no
```
expected result was 'permitrootlogin no'

repeat tests from testing workstation

```sh
$ ssh -o ControlPath=none \
  -o IdentitiesOnly=yes \
  -o PreferredAuthentications=publickey \
  -o PasswordAuthentication=no \
  -o KbdInteractiveAuthentication=no \
  -i ~/.ssh/scap-exp01-root \
  root@10.10.20.198 'id'

$ printf 'Root SSH exit: %s\n' "$?"

Root SSH exit: 255
```
expected authentication denied, and exit 255. A timeout or connection
refusal would be a different outcome.

Test normal admin:
```sh
$ ssh -o ControlPath=none -t \
  cis-test@10.10.20.198 'sudo id'

$ printf 'Admin SSH exit: %s\n' "$?"

uid=0(root) gid=0(root) groups=0(root)
Connection to 10.10.20.198 closed.
Admin SSH exit: 0
```
expected uid=0(root) and exit 0

capture post-intervention scan:
```sh
$ date -Is > "$EXP/post/start-time.txt"
$ sudo /usr/sbin/sshd -T > "$EXP/post/sshd-effective.txt"

$ sudo oscap xccdf eval \
  --profile "$PROFILE" \
  --results "$EXP/post/results.xml" \
  --results-arf "$EXP/post/results-arf.xml" \
  --report "$EXP/post/report.html" \
  "$DS" > "$EXP/post/scan.log" 2>&1

$ SCAN_RC=$?
$ printf '%s\n' "$SCAN_RC" > "$EXP/post/exit-code.txt"
$ date -Is > "$EXP/post/end-time.txt"
$ printf 'Post-scan exit: %s\n' "$SCAN_RC"

Post-scan exit: 2
```
expected 2

```sh
$ perl -MXML::LibXML -MXML::LibXML::XPathContext \
  - "$EXP/pre/results.xml" "$EXP/post/results.xml" <<'PERL'
use strict;
use warnings;

my @labels = qw(pre post);
my $id = 'xccdf_org.ssgproject.content_rule_sshd_disable_root_login';

for my $path (@ARGV) {
    my $label = shift @labels;
    my $doc = XML::LibXML->load_xml(location => $path);
    my $xc = XML::LibXML::XPathContext->new($doc);
    $xc->registerNs(x => 'http://checklists.nist.gov/xccdf/1.2');

    my ($result) = $xc->findnodes("//x:rule-result[\@idref='$id']");
    die "Rule result missing in $path\n" unless $result;

    printf "%s: %s\n", $label, $xc->findvalue('x:result', $result);
}
PERL

pre: fail
post: pass
```
The rule changed from fail to pass, and normal administration still
works.

```sh
$ printf '\n--- Experiment evidence ---\n'
    find "$HOME/masters-project/evidence/EXP-001" \
    -maxdepth 4 -type f -print | sort

--- Experiment evidence ---
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/end-time.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/exit-code.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/report.html
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/results-arf.xml
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/results.xml
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/scan.log
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/sshd-effective.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/post/start-time.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/end-time.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/exit-code.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/report.html
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/results-arf.xml
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/results.xml
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/scan.log
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/sshd-effective.txt
/home/cis-test/masters-project/evidence/EXP-001/20261104T203112Z/pre/start-time.txt

$ printf '\n--- Existing enrichment mapping ---\n'
$ for base in "$HOME/openscap" "$HOME/masters-project"; do
  if [ -d "$base" ]; then
    find "$base" -type f -name 'ubuntu2404-context.xml' \
      -print -exec cat {} \;
  fi
done
--- Existing enrichment mapping ---

$ printf '\n--- Available OpenSCAP executable ---\n'
--- Available OpenSCAP executable ---
$ command -v oscap
 /usr/bin/oscap
$ oscap --version
OpenSCAP command line tool (oscap) 1.3.9
Copyright 2009--2023 Red Hat Inc., Durham, North Carolina.

==== Supported specifications ====
SCAP Version: 1.3
XCCDF Version: 1.2
OVAL Version: 5.11.1
CPE Version: 2.3
CVSS Version: 2.0
CVE Version: 2.0
Asset Identification Version: 1.1
Asset Reporting Format Version: 1.1
CVRF Version: 1.1

==== Capabilities added by auto-loaded plugins ====
SCE Version: 1.0 (from libopenscap_sce.so.25)

==== Paths ====
Schema files: /usr/share/openscap/schemas
Default CPE files: /usr/share/openscap/cpe

==== Inbuilt CPE names ====
Red Hat Enterprise Linux - cpe:/o:redhat:enterprise_linux:-
Red Hat Enterprise Linux 5 - cpe:/o:redhat:enterprise_linux:5
Red Hat Enterprise Linux 6 - cpe:/o:redhat:enterprise_linux:6
Red Hat Enterprise Linux 7 - cpe:/o:redhat:enterprise_linux:7
Red Hat Enterprise Linux 8 - cpe:/o:redhat:enterprise_linux:8
Community Enterprise Operating System 5 - cpe:/o:centos:centos:5
Community Enterprise Operating System 6 - cpe:/o:centos:centos:6
Community Enterprise Operating System 7 - cpe:/o:centos:centos:7
Community Enterprise Operating System 8 - cpe:/o:centos:centos:8
Fedora 32 - cpe:/o:fedoraproject:fedora:32
Fedora 33 - cpe:/o:fedoraproject:fedora:33
Fedora 34 - cpe:/o:fedoraproject:fedora:34
Fedora 35 - cpe:/o:fedoraproject:fedora:35

==== Supported OVAL objects and associated OpenSCAP probes ====
OVAL family   OVAL object                  OpenSCAP probe
----------    ----------                   ----------
independent   environmentvariable          probe_environmentvariable
independent   environmentvariable58        probe_environmentvariable58
independent   family                       probe_family
independent   filehash                     probe_filehash (MD5, SHA-1)
independent   filehash58                   probe_filehash58 (MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512)
independent   sql                          probe_sql
independent   sql57                        probe_sql57
independent   system_info                  probe_system_info
independent   textfilecontent              probe_textfilecontent
independent   textfilecontent54            probe_textfilecontent54
independent   variable                     probe_variable
independent   xmlfilecontent               probe_xmlfilecontent
independent   yamlfilecontent              probe_yamlfilecontent
linux         dpkginfo                     probe_dpkginfo
linux         iflisteners                  probe_iflisteners
linux         inetlisteningservers         probe_inetlisteningservers
linux         partition                    probe_partition
linux         rpminfo                      probe_rpminfo
linux         rpmverify                    probe_rpmverify
linux         rpmverifyfile                probe_rpmverifyfile
linux         rpmverifypackage             probe_rpmverifypackage
linux         selinuxboolean               probe_selinuxboolean
linux         selinuxsecuritycontext       probe_selinuxsecuritycontext
linux         systemdunitdependency        probe_systemdunitdependency
linux         systemdunitproperty          probe_systemdunitproperty
linux         fwupdsecattr                 probe_fwupdsecattr
unix          dnscache                     probe_dnscache
unix          file                         probe_file
unix          fileextendedattribute        probe_fileextendedattribute
unix          interface                    probe_interface
unix          password                     probe_password
unix          process                      probe_process
unix          process58                    probe_process58
unix          routingtable                 probe_routingtable
unix          runlevel                     probe_runlevel
unix          shadow                       probe_shadow
unix          symlink                      probe_symlink
unix          sysctl                       probe_sysctl
unix          uname                        probe_uname
unix          xinetd                       probe_xinetd

```



