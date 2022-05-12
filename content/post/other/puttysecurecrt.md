---
title: PuTTY/SecureCRT
author: "-"
date: 2012-03-14T03:37:37+00:00
url: /?p=2561
categories:
  - Linux
tags:$
  - reprint
---
## PuTTY/SecureCRT
从windows访问linux，除了samba之外，日常操作用得最多的大概就是PuTTY和SecureCRT

Putty是免费的，SecureCRT是收费的 (当然，有破解版) 。
  
Putty缺省配置就很好看很好用，SecureCRT的缺省配置不是为linux准备的而且很难看。
  
Putty拿来就可以立刻使用，SecureCRT需要经过复杂的配置之后才好用，而且SecureCRT对linux下的emacs的支持不够好。
  
Putty支持vi结束之后回到以前的屏幕，SecureCRT我没发现这个功能。SecureCRT退出vi之后，屏幕上还有一堆刚才vi过的内容，不清爽。
  
以上这些区别使得SecureCRT用起来常常不顺手。

Putty不支持自动登录linux，SecureCRT支持自动登录linux。这个区别显得Putty更安全，SecureCRT更方便。
  
Putty不支持同时登录多个linux，SecureCRT可以在每个tab page里面登录一个linux。
  
以上两个区别使得SecureCRT更适合系统管理员使用。

在写代码调程序，以及平常使用的时候，我更愿意用putty。但是当我需要象系统管理员那样操作很多台linux的时候，我更愿意用SecureCRT。