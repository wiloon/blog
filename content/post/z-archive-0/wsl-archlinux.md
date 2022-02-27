---
title: 在WSL2中安装ArchLinux
author: "-"
date: 2012-09-21T08:03:28+00:00
url: archlinux/wsl
categories:
  - linux

tags:
  - reprint
---
## 在WSL2中安装ArchLinux

>https://zhuanlan.zhihu.com/p/266585727
<https://github.com/DDoSolitary/LxRunOffline>


```bash
.\LxRunOffline i -n archlinux -f C:\workspace\apps\archlinux-bootstrap-2022.02.01-x86_64.tar.gz -d C:\workspace\apps\wsl-archlinux -r root.x86_64
 
wsl --set-version archlinux 2
wsl -d archlinux

lxrunoffline su -n archlinux -v 1000


```