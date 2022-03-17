---
title: linux下挂载kvm磁盘文件
author: "-"
date: 2012-04-07T12:16:59+00:00
url: /?p=2844
categories:
  - Linux
  - VM

tags:
  - reprint
---
## linux下挂载kvm磁盘文件
宿主机Debian, 客户机winxp, 磁盘文件格式raw

```bash

sudo mount -o loop,offset=32256 -t ntfs winxp.img   /mnt

```

<http://stackoverflow.com/questions/8171179/kvm-virtual-machine-running-windows-xp-how-to-get-files-from-guest-to-host>

winxp.img and loop1 is not a single partition (which can be mounted), it is image of full hard disk with own partition table.

You should read partition table from loop1 with fdisk; compute offset of first partition and do:

    sudo mount -o offset=N -t ntfs /dev/loop1 /home/robert/kvm/images/tmp 

where N is offset in bytes.

_Telepathic mode on_ N is 32256 _Telepathic mode off_

and finally, google mode on (I'll google "offset 32256"):

http://en.wikibooks.org/wiki/QEMU/Images#Mounting_an_image_on_the_host

> Linux and other Unix-like hosts can mount images created with the raw format type using a loopback device. From a root login (or using sudo), mount a loopback with an offset of 32,256.

> `mount -o loop,offset=32256 /path/to/image.img /mnt/mountpoint`