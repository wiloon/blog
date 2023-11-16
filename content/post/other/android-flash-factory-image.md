---
title: 安卓线刷升级, flash factory image for android
author: "-"
date: 2015-01-29T15:55:53+00:00
url: android/factory-image
categories:
  - inbox
tags:
  - reprint
---
## 安卓线刷升级, flash factory image for android

### download factory image from

[https://developer.android.com/preview/get](https://developer.android.com/preview/get)
  
[https://developers.google.com/android/images](https://developers.google.com/android/images)

[https://developer.android.com/about/versions/12/download](https://developer.android.com/about/versions/12/download)

```bash
wget https://dl.google.com/dl/android/aosp/angler-opr6.170623.013-factory-a63b2f21.zip

#edit flash-all.sh and remove the -w command

for linux
https://wiki.archlinux.org/index.php/android#Detect_the_device
```

### 开发者模式

...

### unlock

开发者模式>oem unlock
    adb reboot bootloader
     fastboot flashing unlock
     # 按方向键切换到unlock
     # 按电源键解锁

手机开启 开发者模式，打开usb调试,oem unlock
  
将手机连接到电脑

```bash
# 进入root
sudo -s
#restart adb:
adb kill-server
adb start-server
adb devices

#reboot to bootloader:
adb reboot bootloader

#不用sudo会一直waiting device, 另外一种waiting device的情况 是连接 电脑的typc线有问题，比如只有充电功能...我的pixelbook带的线就不能刷机用。
./flash-all.sh
```

* * *

if failed, flash image manually

```bash
adb reboot bootloader
fastboot flash bootloader bootloader文件名.img
fastboot reboot-bootloader
fastboot flash radio <radio文件名>.img
fastboot reboot-bootloader
fastboot flash recovery recovery.img
fastboot flash boot boot.img
fastboot flash system system.img
fastboot flash cache cache.img
fastboot flash userdata userdata.img
fastboot reboot
```

```bash
  
#format userdata
  
fastboot format userdata

#format cache
  
fastboot format cache
  
```

[http://www.inexus.co/thread-386-1-1.html](http://www.inexus.co/thread-386-1-1.html)

[https://blog.nraboy.com/2014/11/manually-update-nexus-device-android-5-0-lollipop/](https://blog.nraboy.com/2014/11/manually-update-nexus-device-android-5-0-lollipop/)
  
nexus中文网原创教程，本文以nexus 5为例编写，其他nexus设备原理一样，只需下载不同的系统底包即可，转贴请注明。

谷歌目前针对nexus 4/6/7/9/10发布了安卓5.0.1系统底包，如果等不急ota的同学可以使用本教程升级！

准备工具: 需要保证您的手机解锁了，如果没有解锁的话，需要先解锁，inexus论坛也很多办法，建议您用论坛置顶的帖子 (其实bootloader模式里，用fastboot oem unlock即可解锁 ) ，已经解锁过的同学可以忽略。

以下是具体的步骤:  (同学们如果有不明白的地方请单独发贴，不然无法回应)

最后你将有类似以下的文件 (图比较老，仅供参考，各个设备的安卓系统包内不完全一样) :

4.如果想保留数据升级到安卓5.0.1 nexus 5,nexus 7,nexus 6,nexus 9,nexus 10用户用下面的办法修改flash-all.bat:

pc电脑用文本编辑器例如记事本等打开flash-all.bat,linux或者mac使用相关编辑器打开里面的flash-all.sh,将 fastboot update命令之前的"-w"给去掉，如果不去掉这个-w的话，您的数据将被删除。

这里以nexus 5举个列子，用文本编辑器将flash-all.bat (PC) 或者flash-all.sh(mac或者linux电脑)里的 fastboot -w update image-hammerhead-lrx21o.zip
  
, 您需要改成 fastboot update image-hammerhead-lrx21o.zip
  
，其实就是去掉-w了，由于不同的设备flash-all.bat或者.sh要刷的.zip不同，这里您只需要记住找到对应的设备安卓5.0镜像包里的flash-all，去掉 fastboot -w update image.xxxx.zip里的-w,然后保存，按照下面的办法运行，就可以保留数据了。

5.连结你nexus 5和PC，开启USB调试，不知道如何开启USB调试的请阅读新手入门

然后打开命令提示符，将手机进入到fastboot模式，输入相关dos命令进入c:/adb/ 目录，然后输入: adb reboot bootloader，具体的输入见下图
  
如果不想使用命令，也可以手动切换到Bootloader模式 (关机情况下，同时按电源键+音量减键) .
  
这一步非常重要，不然会遇到"waitting for the device"的错误提示.
  
待手机进入这个模式后，再输入 flash-all.bat，见下图(一定要使用去掉-w的.bat，不然就会清空数据的)，或者直接在电脑上双击flash-all.bat运行它。

然后就是等待，如果出现遇到"missing system.img"问题，恭喜您，需要移步到小编写的另外一个教程来进行手动刷机，见解决手动升级安卓5.0遇到"missing system.img"问题
  
如果您严格按照上面的办法做了，就不会失败了。

亲自测试成功。

* * *

adb devices
  
List of devices attached
  
84B5T15A13002784 unauthorized

  1. Check if authorized:

\platform-tools>adb devices
  
List of devices attached
  
4df798d76f98cf6d unauthorized
  
2. Revoke USB Debugging on phone

If the device is shown as unauthorized, go to the developer options on the phone and click "Revoke USB debugging authorization" (tested with JellyBean & Samsung GalaxyIII).

    Restart ADB Server:
  
Then restarted adb server

adb kill-server
  
adb start-server
  
4. Reconnect the device

The device will ask if you are agree to connect the computer id. You need to confirm it.

    Now Check the device
  
It is now authorized!

adb devices
  
\platform-tools>adb devices
  
List of devices attached
  
4df798d76f98cf6d device

>[https://stackoverflow.com/questions/23081263/adb-android-device-unauthorized](https://stackoverflow.com/questions/23081263/adb-android-device-unauthorized)

[http://sspai.com/27429](http://sspai.com/27429)
