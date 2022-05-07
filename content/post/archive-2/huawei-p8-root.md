---
title: huawei p8 root
author: "-"
date: 2018-07-25T12:50:36+00:00
url: /?p=12442
categories:
  - Inbox
tags:
  - reprint
---
## huawei p8 root
https://forum.xda-developers.com/huawei-p8/how-to/rooting-huawei-p8-marshmallow-emui4-0-1-t3431249
  
install twrp
  
Download: https://www.androidfilehost.com/?fid=529152257862681510
  
- rename the .img to "TWRP" (TWRP.img) and flash it with ADB.
  
- first store the TWRlP.img in C:\Program Files (x86)\Minimal ADB and Fastboot, after open the Program (Phone must be connected with USB to PC)
  
- tap: adb devices (your device must listed with ID)
  
- tap: adb reboot bootloader (Phone restart in Fastboot-Mode - you will see, your bootloader is unlocked now)
  
- tap: fastboot flash recovery TWRP.img
  
If the flashing of the Recovery is succesfully done - disconnect your Phone from USB!
  
- press the Vol+ button first (staying on Vol+) and simultaneously press the Power Button
  
- wait until the phone reboot - in the moment you see the Huawei Logo skip pressing the Power Button but stay on Vol+ until you are succesfully bootet to TWRP
  
- TWRP ask you by the first start for root access "Allow to modify system partion" - swype to confirm "yes"
  
- go to button "Backup", select your external Storage and make a complete Nandroid Backup of all shown partititions
  
- after you can Root your Phone now - see description
  
Note: If you make something wrong booting first time to TWRP and the Phone reboot to system instead of TWRP, Stock-Recovery will be reflashed and you must flash TWRP again with ADB

root
  
Download SuperSU
  
https://forum.xda-developers.com/attachment.php?attachmentid=3951105&d=1480325170
  
Boot to TWRP and make a complete Nandroid Backup first (if you dont have it already)
  
3.) In TWRP go to the Advanced button and use the Terminal.
  
On the first screen tap on the ok button and after write following Force Systemless Command:
  
echo SYSTEMLESS=true>>/data/.supersu
  
and quit this with the ok tab
  
4.) Navigate back to the main menu and use the Install button
  
5.) Navigate to the location of the placed SuperSU 2.67
  
6.) Swype to confirm flash - after use: Reboot
  
7.) If TWRP ask you for Root - "Your device does not appear to be rooted - Install SuperSU now?" - NO - use: DO NOT INSTALL Button!
  
Older Versions of TWRP ask you this - the newest TWRP 3.0.2 dont.
  
8.) P8 reboots now 2 times and rebooted finaly to system.
  
9.) Open the SuperSU App (it will be on an empty site of your home) - you have now systemless Root
  
10.) Open Playstore an Update the SuperSU and after say yes to Update the Binary.
  
11.) The Phone must be restarted and you are up-do-date with the Root.