---
title: Making ipset,iptables persistent
author: "-"
date: 2019-09-09T09:57:13+00:00
url: /?p=14918
categories:
  - Inbox
tags:
  - reprint
---
## Making ipset,iptables persistent
```bash
ipset save > /etc/ipset.conf
systemctl enable ipset.service

iptables-save -f /etc/iptables/iptables.rules
systemctl enable iptables.service
```

https://wiki.archlinux.org/index.php/Ipset
  
https://wiki.archlinux.org/index.php/Iptables