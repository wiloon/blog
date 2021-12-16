---
title: KVM的USB支持
author: "-"
date: 2011-12-14T13:34:14+00:00
url: /?p=1881
categories:
  - Linux
  - VM
tags:
  - KVM

---
## KVM的USB支持
在启动KVM的时候，加入参数 "-usb", 同时还要加入  "-usbdevice host:<VendorID>:<ProductID>"。 将 USB VendorID 和 ProductID 传给虚拟机，这样虚拟机就会知道有一个 USB设备插入了。
  
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

ID后面的 xxxx:xxxx 就是<VendorID>:<ProductID>。如要挂载第2行的USB设备: 
  
$kvm -usb -usbdevice host: 163c:0620
  
如果要加载网银盾，"-usbdevice host:" 后加网银盾的<VendorID>:<ProductID>就可以了。