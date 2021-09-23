---
title: Debian 6 installation, BootUsb
author: "-"
type: post
date: 2011-08-18T02:19:41+00:00
url: /?p=422
bot_views:
  - 6
views:
  - 1
categories:
  - Linux

---
The current released versions of Debian Install images and Debian Live images are built using isohybrid techniques, which means using them with a USB key is simple and easy, using "dd". Older Debian images were not so easy to use with USB keys and needed a lot of instructions. Those instructions are no longer helpful, so have been removed from this page.

Several of the Debian CD and Debian Live images are created using _isohybrid_ technology, which means that they may be used in two different ways:

  * They may be written to CD/DVD and used as normal for CD/DVD booting.
  * They may be written to USB flash drives, bootable directly from the BIOS of most PCs.

The most common way to copy an image to a USB flash drive is to use the <q>dd</q> command on a Linux machine:

`dd if=<file> of=<device> bs=4M; sync`

```bash
  
dd if=debian-6.0.2.1-i386-CD-1.iso of=/dev/sdb bs=4M; sync
  
```

where:

  * <file> is the name of the input image, e.g. <q>netinst.iso</q>
  * <device> is the device matching the USB flash drive, e.g. /dev/sda, /dev/sdb. Be careful to make sure you have the right device name, as this command is capable of writing over your hard disk just as easily if you get the wrong one!
  * <q>bs=4M</q> tells dd to read/write in 4 megabyte chunks for better performance; the default is 512 bytes, which will be much slower
  * The <q>sync</q> is to make sure that all the writes are flushed out before the command returns.

http://wiki.debian.org/BootUsb

http://www.debian.org/CD/faq/#write-usb

  !!!!!!!!!!!!!!!!!!!!!以下方法作废!!!!!!!!!!!!!!!!!

**方法1: **

****该方法有一个主要的缺点:  即使U盘很大，设备的逻辑尺寸还是限制在 256 MB。如果您要将该U盘用作其他用途，需要为它重新分区，为其余容量创建一个新的文件系统。次要的缺点是您无法复制完整的 CD 映象到 U 盘，只能使用较小的businesscard 或 netinst CD 镜像.

#下载boot.img.gz
  
http://ftp.nl.debian.org/debian/dists/squeeze/main/installer-i386/current/images/hd-media/

#将 hd-media/boot.img.gz 的文件(里面包含所有安装程序文件,syslinux) 解压缩到U 盘

```bash
  
sudo umount /dev/sdX
  
sudo zcat boot.img.gz > /dev/sdX
  
```

#挂载该U盘

```bash
  
sudo mount /dev/sdX /mnt
  
```

#复制 Debian netinst 到 /mnt (也就是U盘)

#重启 。从优盘引导。

**方法2: **

****＃＃＃这个我没成功, 用了install-mbr 还是不能引导。
  
用GParted 在优盘上创建一个FAT16的分区（最大4G) 
  
然后使用mkdosfs来创建FAT16文件系统 (可能需要先行安装dosfstools软件包)
  
mkdosfs可在Linux下，将磁盘格式化为MS-DOS文件系统的格式。

```bash
  
sudo umount /dev/sdb1
  
sudo mkdosfs /dev/sdb1
  
```

把syslinux放到FAT16分区,来引导系统 (如果你的系统没有 syslinux和mtools包,要先行安装)

```bash
  
sudo apt-get install syslinux
  
sudo syslinux /dev/sdb1
  
```

挂载分区

```bash
  
sudo mount /dev/sdb1 /mnt
  
```

复制下面的文件到U盘
  
下载地址:  http://ftp.nl.debian.org/debian/dists/squeeze/main/installer-i386/current/images/hd-media/
  
vmlinuz (kernel binary)
  
initrd.gz (initial ramdisk image)

创建一个syslinux.cfg配置文件,至少包含下面两行:

default vmlinuz
  
append initrd=initrd.gz

复制 netinst 的ISO到 /mnt

如果不能从U 盘启动,可能MBR不正确, 用下面这个命令修复它
  
sudo apt-get install mbr
  
sudo install-mbr /dev/sdb1

**方法3: **
  
http://wiki.debian.org/BootUsb

unmount the usb drive

```bash
  
sudo umount /dev/sdb1
  
```


```bash
  
sudo fdisk /dev/sdb
  
```

Using fdisk: Press P to see the list of all partitions.

Use D repeatedly to delete all partitions.

Create a new partition pressing N, P, 1 and accept all defaults concerning the size (minimum partition size necessary will be around 60 MB).

Set the bootable flag with A ,1

press T, 6 to create a FAT16 partition

and press W to store and exit from fdisk.

然后复制
  
vmlinuz (kernel binary)
  
initrd.gz (initial ramdisk image)
  
两个文件到U盘
  
下载地址:  http://ftp.nl.debian.org/debian/dists/squeeze/main/installer-i386/current/images/hd-media/

创建syslinux.cfg文件, 包含下面两行:

default vmlinuz
  
append initrd=initrd.gz

这个没有256M的限制可以复制第一张CD到U盘。

复制debian6 的 iso文件(debian-6.0.2.1-i386-CD-1.iso)到优盘
  
到这里还是不能用U盘引导......要用下面一步。
  
Master Boot Record
  
Some USB keys don't boot. If this is the case, it may be possible to fix them by installing a new master boot record. (Most keys boot OK by default; some cannot be fixed even by doing this. However, it helps in some cases). Run the command:

#umount the usb drive

```bash
  
#lilo -M /dev/$usbdevice
  
sudo lilo -M /dev/sdb
  
```

没有lilo的话。。要安装一下

```bash
  
sudo apt-get install lilo
  
```

安装过程中会跳出一个窗口,选OK..

<del>http://wiki.openmoko.org/wiki/Wishlist/LiveUSB_distro</del>