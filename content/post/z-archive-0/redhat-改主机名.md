---
title: redhat 改主机名
author: "-"
date: 2011-11-24T04:32:39+00:00
url: /?p=1578
categories:
  - Linux
tags:
  - RedHat

---
## redhat 改主机名
/etc/sysconfig/network

NETWORKING=yes
NETWORKING_IPV6=no
HOSTNAME=YOURHOSTNAME

/etc/hosts

127.0.0.1               YOURHOSTNAME           localhost