---
title: systemd-resolved
author: w1100n
type: post
date: 2018-12-30T09:59:49+00:00
url: /?p=13243
categories:
  - Uncategorized

---
```bash
# check systemd-resolved status
resolvectl status

# disable dns on 53 port
vim /etc/systemd/resolved.conf
#switch off binding to port 53
DNSStubListener=no

#disable LLMNR
LLMNR=false
```