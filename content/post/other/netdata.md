---
title: netdata
author: "-"
date: 2014-12-23T03:09:27+00:00
url: netdata
categories:
  - Linux
tags:$
  - reprint
---
## netdata

```bash
pacman -S netdata
systemctl start netdata
systemctl enable netdata

vim /etc/netdata/netdata.conf

[web]
    bind to = 0.0.0.0 [::]

```
