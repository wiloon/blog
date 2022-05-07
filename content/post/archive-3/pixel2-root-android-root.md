---
title: pixel2 root, android root
author: "-"
date: 2020-01-26T10:16:33+00:00
url: /?p=15417
categories:
  - Inbox
tags:
  - reprint
---
## pixel2 root, android root

    Root Android Q on Google Pixel 2, Google Pixel
  
<https://www.teamandroid.com/2019/03/17/root-android-q-beta-google-pixel-2-pixel/embed/#?secret=dymLQPYWmm>

线刷 android 10

    安卓线刷升级 flash factory image for android device
  
<http://blog.wiloon.com/?p=7296&embed=true#?secret=Im4BCxWQUv>

Enable USB Debugging mode

Download MagiskManager apk 并安装 到手机
  
从第一步线刷升级用的镜像文件 里解压出boot.img, 传到手机 上的download目录
  
打开magisk mamanger, 点击 "未安装 Magisk" 后面的安装按钮， 在弹出的菜单中选择 "选择并修补一个文件 "， 然后 选择boot.img。
  
把打好补丁的boot.img传到电脑 上 ， 打补丁之后的boot.img的名字 应该 是magisk_patched.img
  
执行 adb reboot bootloader，到bootloader
  
刷入打好补丁的 boot.img

```bash
fastboot flash boot patched_boot.img
fastboot reboot
```

重启后系统已经root成功了。
