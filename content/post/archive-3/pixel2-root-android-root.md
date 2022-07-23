---
title: pixel2, pixel3 root, android root
author: "-"
date: 2020-01-26T10:16:33+00:00
url: /?p=15417
categories:
  - Inbox
tags:
  - reprint
---
## pixel2,pixel3 root, android root

线刷 android

安卓线刷升级 flash factory image for android device
  
<http://blog.wiloon.com/android/factory-image>

Enable USB Debugging mode

Download MagiskManager apk 并安装 到手机

<https://github.com/topjohnwu/Magisk>

从第一步线刷升级用的镜像文件 `image-blueline-sp1a.210812.016.c2.zip` 里解压出 boot.img, 传到手机上的 download 目录
  
打开magisk mamanger, 点击 "未安装 Magisk" 后面的安装按钮， 在弹出的菜单中选择 "选择并修补一个文件 "， 然后 选择boot.img。
  
把打好补丁的boot.img传到电脑上 ， 打补丁之后的boot.img的名字 应该 是magisk_patched.img
  
执行 adb reboot bootloader，到bootloader
  
刷入打好补丁的 boot.img

```bash
fastboot flash boot patched_boot.img
fastboot reboot
```

重启后系统已经root成功了。

<https://blog.csdn.net/Ender_Zhao/article/details/108615512>

<https://www.teamandroid.com/2019/03/17/root-android-q-beta-google-pixel-2-pixel/embed/#?secret=dymLQPYWmm>
