---
title: adb, no permission
author: "-"
date: 2012-06-23T01:35:19+00:00
url: /?p=3627
categories:
  - Linux
tags:
  - reprint
---
## adb, no permission

<http://www.blogjava.net/brian/articles/316019.html>

在ubuntu(9.10)下执行adb devices命令, 返回的结果是:
  
List of devices attached
  
???????????? no permissions
  
这意味着,USB连接的设备是能够被识别的。Google之后，得知adb server需要以root的权限启动，于是有了如下命令:
  
brian@brian-laptop:~/Dev/Java/Android/android-sdk-linux_86/tools$ **./adb kill-server**
  
brian@brian-laptop:~/Dev/Java/Android/android-sdk-linux_86/tools$ **sudo ./adb start-server**
  
\* daemon not running. starting it now \*
  
\* daemon started successfully \*

第一条命令用来杀死当前正在运行的server, 第二条命令则以root的权限启动了新的server. 我们可以再次查看devices:
  
brian@brian-laptop:~/Dev/Java/Android/android-sdk-linux_86/tools$ **./adb devices**
  
List of devices attached
  
HT848KV04386 device

这次设备就被正确识别了。自然地, 像ddms之类的工具也能派上用场了。

如果你的机器不能识别，或不是Ubuntu环境，请参考官方文档:<http://developer.android.com/guide/developing/device.html>。

### insufficient permissions for device

If you're developing on Ubuntu Linux, you need to add a rules file that contains a USB configuration for each type of device you want to use for development. Each device manufacturer uses a different vendor ID. The example rules files below show how to add an entry for a single vendor ID (the HTC vendor ID). In order to support more devices, you will need additional lines of the same format that provide a different value for the `SYSFS{idVendor}` property. For other IDs, see the table of USB Vendor IDs, below.

Log in as root and create this file: `/etc/udev/rules.d/51-android.rules`.

add lines below:

HTC     0bb4
  
SUBSYSTEM=="usb", SYSFS{idVendor}=="0bb4", MODE="0666"

save file, then.

sudo adb kill-server
sudo adb start-server
sudo adb devices
sudo adb install ....apk
