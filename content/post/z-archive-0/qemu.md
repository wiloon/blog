---
title: QEMU
author: "-"
date: 2011-11-26T09:28:37+00:00
url: /?p=1642
categories:
  - Linux
  - VM

tags:
  - reprint
---
## QEMU
# QEMU是一套由Fabrice Bellard所编写的模拟处理器的自由软件。它与Bochs，PearPC近似，但其具有某些后两者所不具备的特性，如高速度及跨平台的特性。经由kqemu这个开源的加速器，QEMU能模拟至接近真实电脑的速度。

  
    
      简介
  


  QEMU有两种主要运作模式:  * User mode模拟模式，亦即是使用者模式。QEMU能启动那些为不同中央处理器编译的Linux程序。而Wine及Dosemu是其主要目标。 * System mode模拟模式，亦即是系统模式。QEMU能模拟整个电脑系统，包括中央处理器及其他周边设备。它使得为系统源代码进行测试及除错工作变得容易。其亦能用来在一部主机上虚拟数部不同虚拟电脑。QEMU的主体部份是在GPL下发布的，而其系统模式模拟与kqemu加速器则是在GPL下发布。使用kqemu可使QEMU能模拟至接近实机速度，但其在虚拟的操作系统是 Microsoft Windows 98或以下的情况下是无用的。 
  
  
    QEMU的优点
  
  
    可以模拟 IA-32 (x86)个人电脑，AMD 64个人电脑，MIPS R4000, 升阳的 SPARC sun3 与 PowerPC (PReP 及 Power Macintosh)架构
  
  
    支持其他架构，不论在主机或虚拟系统上
  
  
    在支持硬件虚拟化的x86构架上可以使用KVM加速配合内核ksm大​页​面​备​份​内​存，速度稳定远超过VMware ESX
  
  
    增加了模拟速度，某些程序甚至可以实时运行
  
  
    可以在其他平台上运行Linux的程序
  
  
    可以储存及还原运行状态(如运行中的程序)
  
  
    可以虚拟网络卡
  
  
    QEMU的缺点
  
  
    对微软视窗及某些主机操作系统的不完善支持(某些模拟的系统仅能运行)
  
  
    对不常用的架构的支持并不完善
  
  
    除非使用kqemu加速器，否则其模拟速度仍不及其他虚拟软件，如VMware
  
  
    比其他模拟软件难安装及使用
  
  
    QEMU's 使用实例
  
  
    以下的指令可以建立一个500MB大小的"qcow"格式的硬盘映像。
  
  
    qemu-img create -f qcow c.img 500M
  
  
    而以下的指令会使虚拟机器在128MB内存，使用c.img这个用以上介绍的指令所建立的硬盘映像及以linux.iso为光盘映像的情况下运行。注意，如果使用物理光驱，请将-cdrom linux.iso这个参数变为 -cdrom /dev/cdrom或您所用的光驱。
  
  
    qemu -clock dynticks -rtc-td-hack -localtime -hda c.img -cdrom linux.iso -boot d -m 128 -enable-audio -localtime
  
  
    如果想缺省使用全萤幕启动子操作系统，可作以上指令后再加上"-full-screen"这个参数，如想在运行时离开全萤幕，请使用组合键Ctrl-Alt-F便可。
  
  
    参数简介
  
  
    -L dir 指向BIOS和VGA BIOS所在目录
  
  
    -hda/-hdb/-hdd/-hdc "文件名" 使用"文件名"作为硬盘0/1/2/3镜像。
  
  
    -cdrom "文件名" 使用"文件名"作为光盘镜像 (文件应该是ISO类型) 。
  
  
    Windows 下的使用者，可以透过下列指令使用实体光盘: 
  
  
    -cdrom //./x: -> x 代表光盘名称/位置
  
  
    例如: -cdrom //./e: -> 使用 E: 为光盘
  
  
    -fda/-fdb "文件名" 使用"文件名"作为磁盘0/1镜像。
  
  
    -boot [a|d|c] 使用磁盘，光盘<d>，或者硬盘<c>启动。
  
  
    -m 容量 指定内存的大小，单位是MB。
  
  
    -soundhw c1,... 使用声卡设备。
  
  
    -soundhw ? 列出所有可使用的声卡
  
  
    -soundhw all 使用全部声卡
  
  
    -usb 允许使用usb设备。
  
  
    -usbdevice 名字 添加一个usb设备"名字"。
  
  
    -net nic 创建一块新的网卡。
  
  
    加速模块
  
  
    kqemu
  
  
    kqemu这个加速模组是Fabrice Bellard专为Linux核心而设计的开源附加程式，目的是为了加速QEMU的子系统运行速度。在x86硬件上模拟x86的操作系统可达至实机速度。
  
  
    使用者限制条件
  
  
    QEMU 加速模组，kqemu，是一套开源商业产品。自版本 1.3.0pre10 起采 GPLv2 授权。阁下可作个人使用而不受限制。但如果阁下想使用光碟，ISO 映像档或附加套件等方法分发QEMU 加速模组， 则必须联络作者并取得其同意后方可进行。
  
  
    QVM86
  
  
    现时除了以上的kqemu这个开源的QEMU 加速模组外，亦有一个在GPL下发布的QEMU 加速模组
  
  
    在kqemu下虚拟中央处理器
  
  
    The QEMU 加速模组 (kqemu)
  
  
    kemu这个加速模组是Fabrice Bellard专为Linux核心而设计的闭源附加程序，目的是为了加速QEMU的子系统运行速度。在x86硬件上模拟x86的操作系统可达到主机速度。
  
  
    QEMU 加速模组 - 使用者限制条件
  
  
    QEMU 加速模组，kqemu，是一套闭源商业产品。可作个人使用而不受限制。但如果想使用光碟, ISO 映像或附加套件等方法分发QEMU加速模组，则必须联络作者并取得其同意后方可进行。
  
  
    QVM86
  
  
    现时除了以上的kqemu这个闭源的QEMU 加速模组外，亦有一个在GPL下发布的QEMU 加速模组。
  
