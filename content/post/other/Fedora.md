---
title: Fedora
author: "-"
date: 2011-12-14T13:42:00+00:00
url: fedora
categories:
  - Linux
tags:
  - Fedora

---
## Fedora

配置方法
1. 备份
mv /etc/yum.repos.d/fedora.repo /etc/yum.repos.d/fedora.repo.backup
mv /etc/yum.repos.d/fedora-updates.repo /etc/yum.repos.d/fedora-updates.repo.backup
2. 下载新的 fedora.repo 和 fedora-updates.repo 到 /etc/yum.repos.d/
fedora

wget -O /etc/yum.repos.d/fedora.repo http://mirrors.aliyun.com/repo/fedora.repo
或者

curl -o /etc/yum.repos.d/fedora.repo http://mirrors.aliyun.com/repo/fedora.repo