---
title: android root nexus 6p
author: "-"
date: 2016-07-28T13:26:31+00:00
url: /?p=9156
categories:
  - Inbox
tags:
  - reprint
---
## android root nexus 6p

angler: Nexus 6P (codenamed Angler)
  
provided you've already unlocked your bootloader,

  1. Download the TWRP Recovery
  
    <https://dl.twrp.me/angler/> 

  2. Download the SuperSU and push the zip to your device.
  
    <http://www.supersu.com/download>

  3. sudo adb push SuperSU-v2.82-201705271822.zip /storage/emulated/0

  4. reboot to bootloader
  
    adb reboot bootloader

  5. flash twrp
  
    sudo fastboot flash recovery twrp.img

  6. reboot to TWRP by powering your phone off, then pressing and holding the volume down and power keys for five seconds.

  7. When TWRP boots up, tap "Install," then navigate to the Download folder and select the SuperSU ZIP without the extra delay. Then, swipe to confirm the installation, and when that's finished, tap on Reboot System and wait for Android to boot up (it might take a couple of minutes for the first boot with root).

  8. install ss apk

## -

SuperSU Stable, <https://download.chainfire.eu/969/SuperSU/UPDATE-SuperSU-v2.76-20160630161323.zip>

flash the modified boot.img:<http://forum.xda-developers.com/nexus-6p/general/stock-modified-boot-img-regular-root-t3306684>
  
Decrypt Your Data Partition, fastboot format userdata //todo remove this line?

<https://android.gadgethacks.com/how-to/root-android-o-nexus-5x-6p-0176736/>
  
<http://wccftech.com/root-android-7-1-1-nmf26f/>
  
<http://forum.xda-developers.com/nexus-6p/general/guides-how-to-guides-beginners-t3206928>
