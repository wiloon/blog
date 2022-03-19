---
title: qemu basic, kvm 参数
author: "-"
date: 2011-12-03T09:17:14+00:00
url: /?p=1701
categories:
  - Linux
  - VM

tags:
  - reprint
---
## qemu basic, kvm 参数
### qemu-img create
To set up your own guest OS image, you first need to create a blank disc image. QEMU has the `qemu-img` command for creating and manipulating disc images, and supports a variety of formats. If you don't tell it what format to use, it will use raw files. The "native" format for QEMU is qcow2, and this format offers some flexibility. Here we'll create a 3GB qcow2 image to install Windows XP on:

qemu-img create -f qcow2 winxp.img 3G

-cpu host
  
-smp 1 1个CPU

Use the -cpu host option to make QEMU emulate the host's exact CPU. If you do not do this, it may be trying to emulate a more generic CPU.
  
If the host machine has multiple CPUs, assign the guest more CPUs using the -smp option.

-nographic  disable graphical output
  
-m 1024 设置虚拟系统内存1024MB
  
-localtime 使虚拟系统与宿主系统时间一致
  
-M pc 虚拟系统类型为pc

-drive file=Windows7_x86.img,cache=writeback,boot=on 硬盘选项，虚拟磁盘是Windows7_x86.img，cache方式为writeback，可引导型磁盘。
  
-net nic,macaddr=52:54:00:12:34:80 网卡选项，手工指定mac地址。
  
-net tap tap类型网络，相当于"桥模式"
  
-cdrom Windows7.iso 光驱
  
-boot d 启动顺序。d代表光驱。
  
-name kvm-win7,process=kvm-win7 为虚拟机取名，便于识别
  
-vnc :2 这里是通过vnc连接控制窗口，这里是在5902端口。client可用IP:2连接。
  
-usb -usbdevice tablet 启用usb设备中的tablet功能。开启该功能可使虚拟机内外的鼠标同步。
  
另外，在安装了磁盘和网卡的半虚拟化驱动后，可以在-drive中加入if=virtio使用磁盘半虚拟化，在-net nic中加入model=virtio使用网卡半虚拟化驱动。

创建一个Win7的虚拟主机

    qemu-kvm -m 1024 -localtime -M pc -smp 1 -drive file=Windows7_x86.img,cache=writeback,boot=on -net nic,macaddr=52:54:00:12:34:80 -net tap -cdrom Windows7.iso -boot d -name kvm-win7,process=kvm-win7 -vnc :2 -usb -usbdevice tablet