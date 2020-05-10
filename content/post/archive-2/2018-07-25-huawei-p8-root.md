---
title: huawei p8 root
author: wiloon
type: post
date: 2018-07-25T12:50:36+00:00
url: /?p=12442
categories:
  - Uncategorized

---
https://forum.xda-developers.com/huawei-p8/how-to/rooting-huawei-p8-marshmallow-emui4-0-1-t3431249
  
install twrp
  
Download: https://www.androidfilehost.com/?fid=529152257862681510
  
&#8211; rename the .img to &#8220;TWRP&#8221; (TWRP.img) and flash it with ADB.
  
&#8211; first store the TWRlP.img in C:\Program Files (x86)\Minimal ADB and Fastboot, after open the Program (Phone must be connected with USB to PC)
  
&#8211; tap: adb devices (your device must listed with ID)
  
&#8211; tap: adb reboot bootloader (Phone restart in Fastboot-Mode &#8211; you will see, your bootloader is unlocked now)
  
&#8211; tap: fastboot flash recovery TWRP.img
  
If the flashing of the Recovery is succesfully done &#8211; disconnect your Phone from USB!
  
&#8211; press the Vol+ button first (staying on Vol+) and simultaneously press the Power Button
  
&#8211; wait until the phone reboot &#8211; in the moment you see the Huawei Logo skip pressing the Power Button but stay on Vol+ until you are succesfully bootet to TWRP
  
&#8211; TWRP ask you by the first start for root access &#8220;Allow to modify system partion&#8221; &#8211; swype to confirm &#8220;yes&#8221;
  
&#8211; go to button &#8220;Backup&#8221;, select your external Storage and make a complete Nandroid Backup of all shown partititions
  
&#8211; after you can Root your Phone now &#8211; see description
  
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
  
6.) Swype to confirm flash &#8211; after use: Reboot
  
7.) If TWRP ask you for Root &#8211; &#8220;Your device does not appear to be rooted &#8211; Install SuperSU now?&#8221; &#8211; NO &#8211; use: DO NOT INSTALL Button!
  
Older Versions of TWRP ask you this &#8211; the newest TWRP 3.0.2 dont.
  
8.) P8 reboots now 2 times and rebooted finaly to system.
  
9.) Open the SuperSU App (it will be on an empty site of your home) &#8211; you have now systemless Root
  
10.) Open Playstore an Update the SuperSU and after say yes to Update the Binary.
  
11.) The Phone must be restarted and you are up-do-date with the Root.