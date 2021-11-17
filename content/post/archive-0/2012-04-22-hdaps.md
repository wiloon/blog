---
title: HDAPS
author: "-"
date: 2012-04-22T01:37:04+00:00
url: /?p=2981
categories:
  - Hardware

---
## HDAPS
Thinkpad HDAPS 依靠笔记本内部的2D 加速度传感器检测笔记本位移， 将数据写入sysfs，系统中有一个demon （守护进程) 负责监视这个sysfs interface，必要时执行硬盘磁头parking 动作。