---
title: Too many open files in system
author: wiloon
type: post
date: 2011-10-28T04:37:22+00:00
url: /?p=1332
bot_views:
  - 14
views:
  - 1
categories:
  - Linux

---
/etc/sysctl.conf

fs.file-max = 65536

   /sbin/sysctl -p
