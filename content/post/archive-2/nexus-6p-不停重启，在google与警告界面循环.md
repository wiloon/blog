---
title: nexus 6p 不停重启,在google与警告界面循环
author: "-"
date: 2017-09-26T15:38:37+00:00
url: /?p=11209
categories:
  - Inbox
tags:
  - reprint
---
## nexus 6p 不停重启,在google与警告界面循环

<http://bbs.gfan.com/android-9177501-1-1.html>
  
<https://forum.xda-developers.com/nexus-6p/general/guide-fix-nexus-6p-bootloop-death-blod-t3640279>

Boot your phone into bootloader (hold power and volume down).
  
Connect your phone to the computer.
  
Go to the folder where you have the modified files, then hold shift and right click in a blank space, click on "open command prompt here" in the menu that pops up.
  
In the command prompt: type "fastboot flash boot [name of the file here]" and then press enter. If you're flashing TWRP, replace boot with recovery. (Linux users, make sure you're running as root)
  
Edit: With the new EX zip, you shouldn't need to flash the boot.img anymore, you can just flash twrp, and then flash EX in twrp.
  
Boot up your phone, and hopefully it should work!
