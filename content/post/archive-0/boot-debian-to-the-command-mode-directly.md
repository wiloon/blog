---
title: boot debian to the command mode directly
author: "-"
date: 2011-12-11T03:12:57+00:00
url: /?p=1839
categories:
  - Linux

---
## boot debian to the command mode directly
方法是把gdm从run level 2中删除。
  
可以使用如下的命令: 
  
1. update-rc.d -f gdm remove
  
2. update-rc.d gdm start 21 3 4 5 . stop 01 0 1 6 .