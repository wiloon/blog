---
title: Debian系统回收站无法清空解决办法
author: "-"
date: 2012-08-16T23:43:21+00:00
url: /?p=3903
categories:
  - Linux
tags:$
  - reprint
---
## Debian系统回收站无法清空解决办法
Debian系统回收站无法清空: 
  
 (1) 切换到root身份 su -
  
 (2) chown -R wiloon /home/wiloon/.local/share/Trash
  
 (3) 退出su权限 exit
  
 (4) chmod -R +w /home/wiloon/.local/share/Trash
  
 (5) 接下来就可以去清空回收站了

rm -rf /home/wiloon/.local/share/Trash/files/*