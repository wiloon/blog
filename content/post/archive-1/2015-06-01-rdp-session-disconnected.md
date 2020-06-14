---
title: RDP Session Disconnected
author: wiloon
type: post
date: 2015-06-01T12:40:45+00:00
url: /?p=7738
categories:
  - Uncategorized
tags:
  - Arch Linux

---
## To resolve:

  1. Right click on "My Computer&#8221; and select "Properties&#8221;.
  2. Click on "Remote settings&#8221;.
  3. Click on the "Remote&#8221; tab.
  4. Under "Remote Desktop&#8221; select the radio button next to "Allow connections from computers running any version of Remote Desktop (less secure)&#8221;.
  5. Click "OK&#8221; to Save.

Also check to make sure you don&#8217;t have any sort of VNC Server installed (like TightVNC, Ultra VNC, RealVNC, etc). If you do then you should uninstall it to ensure that RDP connections work properly.