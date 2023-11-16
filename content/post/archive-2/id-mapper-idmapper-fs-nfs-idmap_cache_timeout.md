---
title: ID Mapper, idmapper, fs.nfs.idmap_cache_timeout
author: "-"
date: 2018-08-29T02:10:29+00:00
url: /?p=12603
categories:
  - Inbox
tags:
  - reprint
---
## ID Mapper, idmapper, fs.nfs.idmap_cache_timeout

Id mapper is used by NFS to translate user and group ids into names, and to
  
translate user and group names into ids. Part of this translation involves
  
performing an upcall to userspace to request the information.

fs.nfs.idmap_cache_timeout
  
设置idmapper缓存项的最大寿命,单位是秒

[https://www.kernel.org/doc/Documentation/filesystems/nfs/idmapper.txt](https://www.kernel.org/doc/Documentation/filesystems/nfs/idmapper.txt)
  
[https://www.cnblogs.com/tolimit/p/5065761.html](https://www.cnblogs.com/tolimit/p/5065761.html)
