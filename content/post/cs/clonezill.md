---
title: clonezill
author: "-"
date: 2019-03-15T05:23:40+00:00
url: clonezill
categories:
  - CS
tags:
  - reprint
  - remix
---
## clonezill

download clonezill iso from https://clonezilla.org/downloads.php

install balenaEtcher

```Bash
dd bs=1M conv=fdatasync if=./clonezilla-live-3.2.0-5-amd64.iso of=/dev/sdx
```

```
start clonezilla
device-image
nfs_server
dhcp
nfs4
192.168.50.227
/backup_xxxx/
beginner
save parts
```
