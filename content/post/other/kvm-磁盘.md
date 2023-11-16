---
title: kvm 磁盘
author: "-"
date: 2011-12-04T01:13:03+00:00
url: /?p=1739
categories:
  - Linux
  - VM
tags:
  - reprint
---
## kvm 磁盘
[http://forum.ubuntu.org.cn/viewtopic.php?f=65&t=302055](http://forum.ubuntu.org.cn/viewtopic.php?f=65&t=302055)

固定大小虚拟磁盘效率最高
  
虚拟磁盘效率最大决定因素在于碎片，而非格式。通常用的动态大小磁盘映像虽然灵活，但其效率自然不如固定大小。以往很多人因创建固定磁盘费时费力而直接使用物理磁盘，不仅有相当风险，且有不便之处，也未必能满足所需功能。
  
xfs 和 NTFS 早已支持空间预分配，但 ext 系列直到 ext4 才支持该功能。现如今，ext4 已然稳定。用 fallocate 命令在其上创建固定大小的 raw 格式映像甚为简单，创建速度与 qemu-img 创建的稀疏文件无异，瞬间完成。比如: 
  
fallocate -l 15G disk1.img

virtio 提高的效率是什么效率
  
直接给 qemu 用 -hda 指定硬盘，谁用谁知道，慢如蜗牛不说，还能听见磁头辛勤地哀鸣，心痛不？网上有人说 cache=writeback ，没错，这是关键，速度快了不说，也不用再担心磁头累跨了。还有人说 if=virtio ，更有甚者 virtio 与 writeback 不可兼得，晕不？其实 virtio 节省的只不过是 CPU 模拟设备所需的运算时间，并不能降低磁盘访问，只有 writeback 才是关键。当然，若你愿意完全可两者并用， if=virtio,cache=writeback 没有任何问题。所谓有问题只不过是拿那已安装的 Windows 来更改设备造成的。

virtio 安装 Windows 小问题
  
对于新磁盘映像，用 if=virtio 安装 WindowsXP/2003 加载驱动后，依然会碰到找不到某某文件问题。因为一个 bug 没错，但也不能指望微软修正，设法绕过吧。
  
随便弄张 Linux LiveCD 启动，用 fdisk /dev/vda 为其分区 (一定要 fdisk 而非 cfdisk ，其它未试) ，全部大小只用于一个主分区，指定分区 ID 标志为 0x0b 。再用 mkfs.vfat /dev/vda1 创建文件系统。重新启动 Windows 安装便可绕过上述 bug 。
  
当 Windows 安装程序进入选择分区时，一定要删除原有分区，重新创建，否则将得到一张有问题的分区表。因为 Linux 和 Windows 所认的 CHS 参数不一，即便一开始就在 qemu 命令中指定 CHS 参数，仍会无济于事。
  
第一阶段，复制文件结束后重启会失败，依然是 CHS 的问题，只要关闭重启 qemu 即可。

virtio 磁盘无法引导
  
BIOS 中都找不到 virtio 磁盘，自然无法引导。当前 Debian squeeze 的 seabios 版本为 0.5.1-3 ，升级到 sid 的 0.6.0+git20100710-2 以上版本即可。

虚拟机运行 Windows 时不时会听见磁盘作响
  
无论是固定大小或是动态磁盘映像，都会时不时听见 Windows 访问磁盘的声音。在设备管理器中，找到磁盘，其"策略"一页选选中"启用高级性能"即可。