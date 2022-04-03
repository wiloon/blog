---
title: centos6
author: "-"
date: 2015-01-18T03:38:49+00:00
url: centos6
categories:
  - Uncategorized

tags:
  - reprint
---
## centos6

默认安装系统盘是 LVM 

## 静态ip
```bash
ifconfig
vi /etc/sysconfig/network-scripts/ifcfg-eth0

ONBOOT=no > ONBOOT=yes

service network restart

```

>https://segmentfault.com/a/1190000005932003

