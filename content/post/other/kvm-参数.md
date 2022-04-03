---
title: kvm 参数
author: "-"
date: 2011-12-03T10:09:10+00:00
url: /?p=1711
categories:
  - Linux
  - VM
tags:
  - KVM

---
## kvm 参数
-bios file
  
指定虚拟机使用的BIOS,file指定BIOS文件路径

-smp n[,cores=cores][,threads=threads][,sockets=sockets][,maxcpus=maxcpus]
  
模拟一个有n个cpu的smp系统,可以简单的指定n为一个数值,或者分别指定socket数,core数/socket,线程数/core

-m megs
  
指定虚拟机使用的内存数量,可以使用M或G后缀

-rtc [base=utc|localtime|date][,clock=host|vm][,driftfix=none|slew]
  
指定虚拟机使用的时间,linux客户机使用-rtc base=utc,clock=host,windows客户机使用-rtc base=localtime,clock=host

-net nic,model=virtio,macaddr=52-54-00-12-34-01 -net tap,ifname=tap0
  
桥接网络，客户机网络接口通过tap接口桥接到主机网络，使用的tap接口名为tap0，由/etc/kvm/kvm-ifup来动态配置tap0接口。model=virtio指定虚拟机网卡使用半虚拟化驱动,如果有多个虚拟客户机同时运行则必须指定macaddr为一个独一无二的值,否则会出现mac地址冲突。如果通过主机的/etc/network/interfaces来静态配置tap接口,则此处应在-net tap接口处附加两个另外的参数script=no,downscript=no

-drive file=debian.img,if=virtio,index=0,media=disk,format=qcow2,cache=writeback
  
指定客户机使用的硬盘驱动器,if=virtio指定使用半虚拟化驱动,index=0指定该硬盘为接口的第一个驱动器,media=disk指定为硬盘驱动器,如果是光盘则为media=cdrom。format=qcow2为硬盘格式 (raw/qcow2) ，以创建磁盘镜像时的格式为准。旧式指定第一个硬盘驱动器的参数为-hda debian.img,已经不再推荐使用。

-drive file=debian.iso,index=2,media=cdrom或者-hdc debian.iso
  
指定光盘驱动器,debian.iso为使用的光驱映像文件

-fda file
  
指定软盘驱动器,file为软磁盘镜像

-no-fd-bootchk
  
客户机启动时不检查软盘驱动器,加速客户机启动

-boot [order=drives][,once=drives][,menu=on|off]
  
'drives': floppy (a), hard disk (c), CD-ROM (d), network (n)

指定引导顺序,c为第一个硬盘驱动器,d为第一个光盘驱动器

-boot order=c

-vnc :0
  
将虚拟机的视频输出重定向到vnc端口,通过vnc viewer可以连接到虚拟机的视频输出

error:Could not initialize SDL(No available video device) - exiting

add the parameters

> -vga std -k en-us -vnc :1

> 物理机系统: Debian 7
  
> 物理机IP: 192.168.1.100
  
> vncserver : 1
  
> 开启vnc端口1

> 这样我就能在vncview中输入192.168.1.100:1
 

### nographic 不能跟daemonize 一起用， 建议用-display

-nographic
  
禁止kvm虚拟机的视频输出/不绘制图形界面

-display none
  
<https://blog.wiloon.com/?p=14053>

-daemonize
  
后台运行虚拟机

-usb enable the USB driver (will be the default soon)
  
-usbdevice name add the host or guest USB device 'name'

## KVM中解决鼠标移动问题
kvm 加 参数

```bash
  
-usb -usbdevice tablet
  
```
