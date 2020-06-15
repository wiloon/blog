---
title: insufficient permissions for device
author: wiloon
type: post
date: 2012-06-22T15:05:20+00:00
url: /?p=3618
categories:
  - Uncategorized

---
If you&#8217;re developing on Ubuntu Linux, you need to add a rules file that contains a USB configuration for each type of device you want to use for development. Each device manufacturer uses a different vendor ID. The example rules files below show how to add an entry for a single vendor ID (the HTC vendor ID). In order to support more devices, you will need additional lines of the same format that provide a different value for the `SYSFS{idVendor}` property. For other IDs, see the table of USB Vendor IDs, below.

Log in as root and create this file: `/etc/udev/rules.d/51-android.rules`.

add lines below:

#HTC     0bb4
  
SUBSYSTEM==&#8221;usb&#8221;, SYSFS{idVendor}==&#8221;0bb4", MODE=&#8221;0666"

save file, then.

sudo adb kill-server
sudo adb start-server
sudo adb devices
sudo adb install ....apk