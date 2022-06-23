---
title: archlinux 连接 蓝牙键盘
author: "-"
date: 2017-02-17T13:30:10+00:00
url: /?p=9834
categories:
  - Inbox
tags:
  - reprint
---
## archlinux 连接 蓝牙键盘

filco 配对 ctrl+alt+fn
  
忘记已配对设备 connect 长按3秒

```bash
  
#mac of bluetooth keyboard
  
# 00:18:00:3C:A4:C5

bluetoothctl

# show help info
  
help

# show keyboard info, paired, trusted, connected
  
info 00:18:00:3C:A4:C5

power on
  
devices
  
agent on
  
pair 00:18:00:3C:A4:C5
  
trust 00:18:00:3C:A4:C5
  
connect 00:18:00:3C:A4:C5

systemctl start bluetooth
  
```

<https://wiki.archlinux.org/index.php/Bluetooth_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.AE.89.E8.A3.85>
  
<https://bbs.archlinux.org/viewtopic.php?id=217451>
