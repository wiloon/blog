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

  1. Right click on &#8220;My Computer&#8221; and select &#8220;Properties&#8221;.
  2. Click on &#8220;Remote settings&#8221;.
  3. Click on the &#8220;Remote&#8221; tab.
  4. Under &#8220;Remote Desktop&#8221; select the radio button next to &#8220;Allow connections from computers running any version of Remote Desktop (less secure)&#8221;.
  5. Click &#8220;OK&#8221; to Save.

Also check to make sure you don&#8217;t have any sort of VNC Server installed (like TightVNC, Ultra VNC, RealVNC, etc). If you do then you should uninstall it to ensure that RDP connections work properly.