---
title: linux 格式化U盘
author: "-"
date: 2012-03-29T14:49:17+00:00
url: /?p=2691
categories:
  - Linux

tags:
  - reprint
---
## linux 格式化U盘
先卸载u盘

#umount /dev/sdb1

#注意/dev/后面的设备要根据你的实际情况而定

格式化并建立VFAT文件系统

#mkfs.vfat /dev/sdb1

最后再mount上就成了,或者把U盘拨了再插上,系统可能会自动mount上,就可以用U盘了