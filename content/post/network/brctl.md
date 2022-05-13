---
author: "-"
date: "2020-08-09 15:34:27" 
title: "brctl"
categories:
  - inbox
tags:
  - reprint
---
## "brctl"
## brctl

brctl is deprecated use bridge command from iproute2 insted
https://wiki.archlinux.org/index.php/Network_bridge

### 查询网桥信息
    brctl show

```bash
pacman -S bridge-utils
apt-get install bridge-utils

# 查看网桥
brctl show
```