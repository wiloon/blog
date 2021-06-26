---
title: linux ping 时间戳
author: "-"
type: post
date: 2020-03-10T05:39:11+00:00
url: /?p=15720
categories:
  - Uncategorized

---
```bash
ping 192.168.2.1 -c 10 | awk '{ print $0"\t" strftime("%H:%M:%S",systime()) } '
```