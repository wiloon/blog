---
title: tightvnc, tigervnc
author: "-"
date: 2015-12-25T12:34:28+00:00
url: vnc
categories:
  - Linux
tags:
  - reprint
  - remix
---
## tightvnc, tigervnc

## tighervnc nightly build

<https://github.com/TigerVNC/tigervnc/releases>  
<http://tigervnc.bphinz.com/nightly/>

### archlinux

```bash
pacman -S tigervnc
# vncserver
# dell desktop
  
vncserver -geometry 1350x670 -dpi 96 -depth 32 :1
vncserver -geometry 1364x768 -dpi 96 -depth 32 :1
vncserver -kill :1
  
#kill 后面有空格!!!
vncviewer 192.168.2.228:1
```

```bash
#edis config file
.vnc/xstartup

#!/bin/sh
startxfce4

```

exit full screen ctrl+alt+shift+F

vncviewer: disable allow jpeg

<https://unix.stackexchange.com/questions/67096/xterm-warning-tried-to-connect-to-session-manager>

- centos

    yum -y install tigervnc-server
    yum -y install tigervnc

    install xorg
  
start xorg
  
install xfce4

install tigervnc
  
vncpasswd /root/.vnc/password
