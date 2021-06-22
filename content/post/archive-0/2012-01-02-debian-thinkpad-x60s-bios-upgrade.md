---
title: debian, thinkpad x60s, bios upgrade
author: "-"
type: post
date: 2012-01-02T09:24:52+00:00
url: /?p=2086
categories:
  - Linux

---
<http://ubuntuforums.org/showthread.php?p=5459421#post5459421>

check the current BIOS and ECP versions on your ThinkPad by using **dmidecode**. For example:

dmidecode -s bios-version

dmidecode -t 11
  
sudo dd if=win98usb.img of=/dev/sdb conv=notrunc
  
Copy the bootable ISO BIOS files to the USB stick

Boot to the USB stick and follow instructions