---
title: yubikey, archlinux sudo, challenge-response
author: "-"
date: 2018-06-24T16:32:55+00:00
url: /?p=12361
categories:
  - Inbox
tags:
  - reprint
---
## yubikey, archlinux sudo, challenge-response
install yubi pam
  
set configuration sloat 2 as hmac-sha1
  
ykpamcfg -2 -v
  
mkdir /data/yubikey
  
mv ~/.yubico/challenge-123456' /data/yubikey
  
vim /etc/pam.d/sudo
  
add line
  
auth sufficient /usr/lib/security/pam_yubico.so mode=challenge-response debug chalresp_path=/data/yubikey
  
auth sufficient /usr/lib/security/pam_yubico.so mode=challenge-response chalresp_path=/data/yubikey

```bash
pacman -S yubico-pam
pacman -S yubikey-manager
```