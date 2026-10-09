---
title: "KVM 的 USB 支持"
author: "-"
date: 2011-12-14T13:34:14+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: kvm-usb
categories:
  - Linux
  - Desktop
tags:
  - KVM
  - remix
  - AI-assisted
aliases:
  - /kvm的usb支持/
---
## KVM的USB支持
在启动KVM的时候，加入参数 `-usb`, 同时还要加入 `-usbdevice host:<VendorID>:<ProductID>`。 将 USB VendorID 和 ProductID 传给虚拟机，这样虚拟机就会知道有一个 USB设备插入了。
  
例如: 

```bash
  
#sudo kvm -usb -usbdevice host:VendorID:ProductID winxp.img
  
$sudo kvm -usb -usbdevice host:08ec:2039 winxp.img
  
```

如何知道VendorID:ProductID，通过lsusb命令: 

```bash
  
unanao@debian:~/Image$ lsusb
  
Bus 007 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
  
Bus 006 Device 002: ID 163c:0620
  
Bus 006 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
  
Bus 005 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
  
Bus 004 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
  
Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
  
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
  
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
  
```

ID后面的 xxxx:xxxx 就是 `<VendorID>:<ProductID>`。如要挂载第2行的USB设备: 
  
$kvm -usb -usbdevice host: 163c:0620
  
如果要加载网银盾，"-usbdevice host:" 后加网银盾的 `<VendorID>:<ProductID>` 就可以了。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `kvm-usb.md`；title 改为「KVM 的 USB 支持」；url 改为 `kvm-usb`；旧 url 加入 aliases | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
