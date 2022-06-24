---
title: VirtualBox
author: "-"
date: 2011-11-26T07:16:06+00:00
url: VirtualBox
categories:
  - VM
tags:
  - reprint
---
## VirtualBox

## 剪贴板共享

Settings> General> Advanced> Shared Clipboard: Bidirectional

## NAT 端口转发

虚拟机> 设置> 网络> 网卡1> 高级> 端口转发> 添加

- 名称: ssh
- 协议: TCP
- 主机IP: 0.0.0.0
- 主机端口: 22
- 子系统IP: 10.0.2.15
- 子系统端口: 22

## archlinux guest

在 virtual box 内安装的archlinux, 需要安装 virtualbox-guest-utils, 可以获得更流畅的图形界面,如 virtual的无缝模式。

```bash
# for VirtualBox Guest utilities with X support
sudo pacman -S virtualbox-guest-utils
# 启用vboxservice, 否则无缝模式(seamless mode)的选项会是灰色的不可用状态
sudo systemctl --now enable vboxservice.service
```

<https://wiki.archlinux.org/index.php/VirtualBox>
<https://bbs.archlinux.org/viewtopic.php?id=118986>

---

<https://www.virtualbox.org/wiki/Downloads>

VirtualBox 是一款开源 x86 虚拟机软件。Oracle VM VirtualBox 是由Sun Microsystems公司出品的软件，原由德国innotek公司开发，2008年Sun收购了Innotek，而Sun于2010年被Oracle收购，2010年1月21日改名成 Oracle VM VirtualBox。2007 年1月InnoTek 以 GNU General Public License (GPL) 释出 VirtualBox，并提供二进位版本及开放源码版本的代码。VirtualBox 可在 Linux 和 Windows 主机中运行，并支持在其中安装 Windows (NT 4.0、2000、XP、Server 2003、Vista)、DOS/Windows 3.x、Linux (2.4 和 2.6)、OpenBSD 等系列的客户操作系统。

简介
  
2008年2月12日，Sun Microsystems宣布将以购买股票的方式收购德国Innotek软件公司，新版不再叫做Innotek VirtualBox，而改叫Sun xVM VirtualBox。
  
2010年1月21日，欧盟终于同意Oracle收购Sun，VirtualBox再次改名变成 Oracle VM VirtualBox。VirtualBox 3.2.0支持的操作系统包括: Windows, Mac OS X(Intel), Solaris 10,Linux(例如:Debian, Fedora, Mandriva, OpenSolaris, PCLiunxOS, Red Hat, SUSE Linux, Ubuntu, Xandros, openSUSE)等。Oracle VM VirtualBox 支持的客户端操作系统包括: 从 3.1到Vista的所有版本的Windows、Linux 2.2、2.4和 2.6内核、Solaris x86、OS/2、、OpenBSD、 Netware 、FreeBSD 和 DOS 。

## VirtualBox磁盘镜像文件(VDI, VMDK, VHD, HDD)

(1)由VirtualBox的虚拟磁盘映像 (VDI) 的文件作为其自己的容器格式为主机硬盘。这是当用户创建一个新的虚拟机与一个新的磁盘将用于的格式。
  
(2)VirtualBox也支持VMware的VMDK容器格式。这种格式是颇为流行，和其他虚拟化软件使用。

(3)微软的VHD格式也完全由VirtualBox的支持；Microsoft Virtual PC的默认格式。

HDD: Parallels的第2版 (硬盘格式) 的镜像文件也被VirtualBox支持.由于缺乏新的格式 (3和4) 的文档,所以VirtualBox不支持。但是，可以使用由Parallels提供的工具版本2格式转换镜像文件。

Windows7的引导程序能够引导vhd格式的虚拟硬盘，而VirtualBox创建的虚拟硬盘文件是vdi格式的，

VirtualBox提供了VBoxManager.exe用来转换格式。

## virtualbox STATUS_OBJECT_NAME_NOT_FOUND

<https://forums.virtualbox.org/viewtopic.php?t=66442>

Went to the C:\Program Files\Oracle\VirtualBox\drivers\vboxdrv directory, right clicked on VBoxDrv.inf and selected Install. I then went back to my console and typed 'sc start vboxdrv' and got this:

SERVICE_NAME: vboxdrv
  
TYPE : 1 KERNEL_DRIVER
  
STATE : 4 RUNNING
  
(STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
  
WIN32_EXIT_CODE : 0 (0x0)
  
SERVICE_EXIT_CODE : 0 (0x0)
  
CHECKPOINT : 0x0
  
WAIT_HINT : 0x0
  
PID : 0
  
FLAGS :

## virtualbox mount shard folder

<https://wiki.archlinux.org/index.php/VirtualBox#Shared_Folders_as_Arch_Linux_Guest>

```bash
  
#manual
  
mount -t vboxsf xxx /mnt/xxx/

#mount on boot
  
#edit /etc/fstab
  
sharedFolderName /path/to/mntPtOnGuestMachine vboxsf uid=user,gid=group,rw,dmode=700,fmode=600,comment=systemd.automount 0 0
  
```

## VirtualBox 共享文件夹

<http://blkstone.github.io/2016/08/05/virtualbox-shared-folder/>

前提是已经安装过增强功能。

步骤
  
设置宿主机共享文件夹
  
重启完成后点击"设备(Devices)" -> 共享文档夹(Shared Folders)菜单,添加一个共享文档夹,选项固定和临时是指该文档夹是否是持久的。共享名能够任取一个自己喜欢的,比如"gongxiang",尽量使用英文名称。

挂载共享文件夹
  
重新进入虚拟Ubuntu,在命令行终端下输入:

sudo mkdir /mnt/shared
  
sudo mount -t vboxsf gongxiang /mnt/shared
  
其中"gongxiang"是之前创建的共享文档夹的名字。OK,现在Ubuntu和主机能够互传文档了。

假如您不想每一次都手动挂载,能够在/etc/fstab中添加一项

gongxiang /mnt/shared vboxsf rw,gid=username,uid=username,auto 0 0
  
以上的 vboxsf 是群组名称 username 是你的 用户名 就是 /home/下的文件夹名称
  
/mnt/shared 是挂载目录

取消挂载
  
sudo umount -f /mnt/shared
  
注意:
  
共享文档夹的名称千万不要和挂载点的名称相同。

参考资料
  
[1] Virtualbox虚拟机Ubuntu共享文件夹设置自动挂载

<https://wiki.archlinux.org/title/VirtualBox>
