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
  
[http://blog.wiloon.com/android/factory-image](http://blog.wiloon.com/android/factory-image)

Enable USB Debugging mode

Download MagiskManager apk 并安装 到手机

[https://github.com/topjohnwu/Magisk](https://github.com/topjohnwu/Magisk)

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

[https://blog.csdn.net/Ender_Zhao/article/details/108615512](https://blog.csdn.net/Ender_Zhao/article/details/108615512)

[https://www.teamandroid.com/2019/03/17/root-android-q-beta-google-pixel-2-pixel/embed/#?secret=dymLQPYWmm](https://www.teamandroid.com/2019/03/17/root-android-q-beta-google-pixel-2-pixel/embed/#?secret=dymLQPYWmm)

## android root pixel

Download Magisk Root
  
[https://github.com/topjohnwu/Magisk](https://github.com/topjohnwu/Magisk)

Download the TWRP Recovery
  
[https://dl.twrp.me/sailfish/](https://dl.twrp.me/sailfish/)

刷入第三方Recovery:TWRP及Root
  
由于Pixel及Pixel XL都采用A/B升级系统,因而可以理解为手机里有2个系统,如果你按照传统刷入Twrp的方法刷入的话,那么你并不会获得一个永久的Twrp。所以需要先刷入一个临时的Twrp,在通过临时的Twrp来刷入永久的Twrp从而来获取Root权限。

下载必要软件
  
需要下载临时的Twrp、永久Twrp及Magisk三个文件。

首先,前往 TWRP 官网 Devices 下载最新版 TWRP 压缩包 (.zip) 和临时 TWRP 镜像文件 (.img) 。

我的Pixel对应选择从这个页面 Download TWRP for sailfish 下载的 3.2.3-1 版本:

twrp-pixel-installer-sailfish-3.2.3-1.zip  (永久twrp)
  
twrp-3.2.3-1-sailfish.img (临时twrp)

拷贝文件到手机
  
假设我电脑上的操作目录为: ~/test/pixel 。

将 twrp-3.2.3-1-sailfish.img 拷贝到该目录下。

将 twrp-pixel-installer-sailfish-3.2.3-1.zip 和 Magisk-v17.2.zip 拷贝到手机中。

[https://www.itfanr.cc/2018/10/16/google-pixel-unlock-bl-and-root/](https://www.itfanr.cc/2018/10/16/google-pixel-unlock-bl-and-root/)

