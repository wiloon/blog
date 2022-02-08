---
title: linux 下解锁 nexus 7
author: "-"
date: 2013-03-23T01:54:26+00:00
url: /?p=5335
categories:
  - Linux

tags:
  - reprint
---
## linux 下解锁 nexus 7
Requirements
  
1. You must have the sdk installed and you are able to access, and use adb and fastboot.
  
2. You must have debugging enabled on your Nexus 7.
  
3. Download Su here (Chainfire's thread for supersu) (Thanks Eric_Eric_Eric)
  
4. Download CWM here. Scroll down to Nexus 7 and choose whether touch or regular.

Pre-Steps
  
To make this easier, you should put the su zip on the sdcard for later.

  1. In terminal, cd to the directory you have your sdk in. Then cd into platform-tools.
  2. Type adb push path-to-zip/JB-SuperSU.zip /sdcard

Unlocking Your Nexus 7

To unlock your device
  
1. cd to platform-tools
  
2. Reboot to the bootloader - adb reboot bootloader
  
3. Unlock your device* -
  
fastboot oem unlock
  
*You will have to accept and erase all the user data on the tablet.
  
*You must run this as sudo in Linux

http://forum.xda-developers.com/showthread.php?t=1741395