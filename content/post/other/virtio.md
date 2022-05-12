---
title: Virtio
author: "-"
date: 2011-12-03T10:01:27+00:00
url: /?p=1709
categories:
  - Linux
  - VM
tags:
  - reprint
---
## Virtio
**半虚拟化驱动Virtio**

Virtio是KVM/Linux的I/O虚拟化框架，以增强KVM的IO效率,是与其他虚拟化平台的半虚拟化(Paravirtualized)类似的东西,主要应用于磁盘设备和网络接口设备。主流的linux发行版已经默认支持Virtio，如果客户机是linux则无需其他设置，直接可以使用Virtio设备，但是如果客户机是windows，则需要在客户机安装Virtio设备驱动，甚至在windows开始安装之前需要提前加载块设备驱动。windows Virtio驱动可从Fedor