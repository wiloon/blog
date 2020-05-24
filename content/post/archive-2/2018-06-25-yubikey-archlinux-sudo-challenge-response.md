---
title: yubikey, archlinux sudo, challenge-response
author: wiloon
type: post
date: 2018-06-24T16:32:55+00:00
url: /?p=12361
categories:
  - Uncategorized

---
install yubi pam
  
set configuration sloat 2 as hmac-sha1
  
ykpamcfg -2 -v
  
mkdir /data/yubikey
  
mv ~/.yubico/challenge-123456&#8242; /data/yubikey
  
vim /etc/pam.d/sudo
  
add line
  
auth sufficient /usr/lib/security/pam\_yubico.so mode=challenge-response debug chalresp\_path=/data/yubikey
  
auth sufficient /usr/lib/security/pam\_yubico.so mode=challenge-response chalresp\_path=/data/yubikey

```bashpacman -S yubico-pam
pacman -S yubikey-manager
```