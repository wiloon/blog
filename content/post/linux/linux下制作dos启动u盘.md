---
title: linux下制作dos启动U盘
author: "-"
date: 2012-03-29T13:53:04+00:00
url: /?p=2687
categories:
  - Linux
tags:
  - reprint
---
## linux下制作dos启动U盘
下载镜像文件win98usb.tar

[http://ubuntuforums.org/showthread.php?p=5459421#post5459421](http://ubuntuforums.org/showthread.php?p=5459421#post5459421)

查看U盘挂载点

df -h

sudo dd if=win98usb.img of=/dev/sdb conv=notrunc

unzip the package win98boot.zip

mount the usb disk

Copy the bootable ISO BIOS files to the USB stick

sudo cp -r xxx xxx

编辑config.sys

device=himem.sys /testmem:off

himem.sys后面的/testmem:off的作用是HIMEM.SYS载入时不会慢慢检查内存