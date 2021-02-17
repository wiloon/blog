---
title: virtualbox STATUS_OBJECT_NAME_NOT_FOUND
author: w1100n
type: post
date: 2018-11-14T02:10:42+00:00
url: /?p=12881
categories:
  - Uncategorized

---
https://forums.virtualbox.org/viewtopic.php?t=66442

Went to the C:\Program Files\Oracle\VirtualBox\drivers\vboxdrv directory, right clicked on VBoxDrv.inf and selected Install. I then went back to my console and typed 'sc start vboxdrv' and got this:

SERVICE_NAME: vboxdrv
  
TYPE : 1 KERNEL_DRIVER
  
STATE : 4 RUNNING
  
(STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
  
WIN32_EXIT_CODE : 0 (0x0)
  
SERVICE_EXIT_CODE : 0 (0x0)
  
CHECKPOINT : 0x0
  
WAIT_HINT : 0x0
  
PID : 0
  
FLAGS :