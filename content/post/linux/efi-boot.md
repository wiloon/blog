---
title: EFI boot
author: "-"
date: 2012-07-02T04:59:13+00:00
url: /?p=3714
categories:
  - Hardware
tags:
  - reprint
---
## EFI boot

EFI boot 介绍

EFI 的全称是可扩展固件接口 (Extensible Firmware Interface)，它是 Intel 公司为全新类型的固件体系结构、接口和服务提出的建议性标准。该标准有两个主要用途: 向操作系统的引导程序和某些在计算机初始化时运行的应用程序提供一套标准的运行环境；为操作系统提供一套与固件通讯的交互协议。
  
简单说，EFI 是 BIOS 的替代者。它为操作系统和固件提供了更加强大、安全、方便的交互途径。EFI 规范定义的接口，包括数据表包含平台的信息，可在 OS Loader 和 OS 的启动和运行时服务。 EFI 固件提供了几种技术优势:

* 引导能力支持大容量磁盘 (超过 2 TIB )
* 更快的启动
* 独立 CPU 的体系结构
* CPU 的独立的驱动程序
* 灵活的预操作系统环境，包括网络功能
* 模块化设计

EFI 启动还需要一个特殊的分区表，该分区表指向一个特殊的文件。通常情况下该文件位于 EFI 路径，EFI 启动涉及到一个写入到 firmware 中的 boot loader, EFI 并不把启动程序放置在 MBR 中，firmware 知道如何读取分区表以及 FAT 的文件格式。EFI 系统分区是用 FAT 格式格式化的特定分区，其中包含 boot loader, 该 boot loader 是 EFI 可执行程序，可被 EFI boot manager 载入和运行。

Boot loader 被设置为一个可以通过固件访问的文件。Boot loader 允许用户选择并加载操作系统。所有的 boot manager 都包含一个 EFI 变量，该变量被用来定义固件配置参数。

对于 64 位 Linux，例如 RedHat EFI boot loader 位于 EFIRedHatelilo.efi， Suse 位于 EFISuSEelilo.efi. 该 EFI 文件包含一个修改过的 LILO. 一般叫做 elilo 文件。ELILO, 包含一个二级的启动选项，在 elilo.conf 文件中配置。Elilo 是一个 boot loader, 只能用于启动 Linux 系统。

制作支持 EFI 平台的启动光盘的步骤

ELILO 是一种基于 EFI 开发的 boot loader，而不是基于 BIOS 平台 , ELILO 允许用户在系统开机过程中自己选择哪个系统或内核，同时也支持用户传参数给内核。 ELILO 的配置文件，一般位于 EFI 启动分区。下面的实例就是将 elilo 作为 EFI 平台的 boot loader。

### linux系统内查看是bios启动的还是uefi启动

在系统内运行shell命令：

    [ -d /sys/firmware/efi ] && echo UEFI || echo BIOS
