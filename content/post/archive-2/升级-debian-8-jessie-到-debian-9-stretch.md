---
title: 升级 Debian 8 (Jessie) 到 Debian 9 (Stretch)
author: "-"
date: 2019-01-26T10:55:56+00:00
url: /?p=13495
categories:
  - Inbox
tags:
  - reprint
---
## 升级 Debian 8 (Jessie) 到 Debian 9 (Stretch)
https://www.linuxidc.com/Linux/2017-12/149050.htm

```bash
apt update

apt upgrade
编辑源列表文件。

sudo nano /etc/apt/sources.list

替换为debian 9 source
apt update

apt upgrade
```