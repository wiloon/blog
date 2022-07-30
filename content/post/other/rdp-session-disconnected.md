---
title: RDP Session Disconnected
author: "-"
date: 2015-06-01T12:40:45+00:00
url: /?p=7738
categories:
  - Inbox
tags:
  - Arch Linux

---
## RDP Session Disconnected

## To resolve

  1. Right click on "My Computer" and select "Properties".
  2. Click on "Remote settings".
  3. Click on the "Remote" tab.
  4. Under "Remote Desktop" select the radio button next to "Allow connections from computers running any version of Remote Desktop (less secure)".
  5. Click "OK" to Save.

Also check to make sure you don't have any sort of VNC Server installed (like TightVNC, Ultra VNC, RealVNC, etc). If you do then you should uninstall it to ensure that RDP connections work properly.
