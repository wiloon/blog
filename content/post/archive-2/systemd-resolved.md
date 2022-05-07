---
title: systemd-resolved
author: "-"
date: 2018-12-30T09:59:49+00:00
url: /?p=13243
categories:
  - Inbox
tags:
  - reprint
---
## systemd-resolved
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

---

https://cloud-atlas.readthedocs.io/zh_CN/latest/linux/redhat_linux/systemd/systemd_resolved.html

