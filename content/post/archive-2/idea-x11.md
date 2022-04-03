---
title: X11 forwarding
author: "-"
date: 2018-06-11T07:25:48+00:00
url: /?p=12295
categories:
  - Uncategorized

tags:
  - reprint
---
## X11 forwarding

>https://wiki.archlinux.org/title/OpenSSH

```bash
pacman -S xorg-xauth xorg-xhost

/etc/ssh/sshd_config
X11Forwarding yes
AllowTcpForwarding yes
X11UseLocalhost yes
X11DisplayOffset 10

systemctl restart sshd

pacman -S xorg-xclock

```
>https://gist.github.com/vietlq/8b20d09fdfe5f02f8b511c7847df39ee

## win 10 xserver, x11forward

Install VcXsrv Windows X Server
Download and install: https://sourceforge.net/projects/vcxsrv/
Check that VcXsrv runs and right-click, get logs to find DISPLAY=127.0.0.1:0.0
Note down the value of $DISPLAY and pass it ot PuTTY
Configure PuTTY
Navigate to SSH => X11 => Tick Enable X11 forwarding
Pass the value of $DISPLAY (which is 127.0.0.1:0.0) to the field X display location
Launch from Ubuntu
Use PuTTy to log in as normal
Run gvim for example on the Ubuntu via PuTTY
Use the GVim window

## idea x11
https://confluence.jetbrains.com/display/~link/Using+Intellij+as+Remote+X+Windows+App