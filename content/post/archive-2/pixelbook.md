---
title: pixelbook, chromeos, developer mode, crouton
author: "-"
date: 2018-02-04T09:22:37+00:00
url: /?p=11818
categories:
  - chrome
tags:
  - reprint
---

## pixelbook, chromeos, developer mode, crouton

developer mode
  
<https://www.theverge.com/2017/11/16/16656420/google-pixelbook-chromebook-development-linux-crouton-how-to>
  
hold the Esc, Refresh, and power button for a little while and the laptop reboots into Recovery Mode. Once you're there, you hit Ctrl-D to boot into Developer Mode.
  
同时按esc refresh, poeer button, 直到出现recovery mode, 就是提示插入u盘的界面,这个时候按ctrl-d(不需要插入u盘, 插入u盘会自动进入恢复模式。)
  
开启 开发者模式会清空数据。

### crouton

<https://github.com/dnschneid/crouton>

```bash
sudo crouton -r list
sudo cronton -t list
sudo crouton -t xfce
# ubuntu 16.4
sudo crouton -r xenial -t xfce
sudo startxfce4
sudo enter-chroot startxfce4
sudo delete-chroot -a
```

### chromeos ubuntu 切换

ctrl+shift+alt+back
  
ctrl+shift+alt+refresh

seabios legacy boot
  
MrChromebox.com

enable legacy boot
  
sudo crossystem dev_boot_usb=1 dev_boot_legacy=1

```bash
sudo enter-chroot
```

### shell

```bash
ctrl+alt+t
shell
sudo -s
```

<https://gist.github.com/daemonp/ecead946317b175e3b54731a513efe94>
