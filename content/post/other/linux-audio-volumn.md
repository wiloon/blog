---
title: audio, 音量, 静音, ALSA
author: "-"
date: 2014-03-30T12:10:53+00:00
url: audio
categories:
  - Inbox
tags:
  - Linux

---
## audio, 音量, 静音, ALSA
## linux audio, 音量,静音
```bash
# archlinux+kde 不需要手动修改默认静音设置,安装alsa-utils, plasma-pa后重启即可。
sudo pacman -S alsa-utils
#kde
sudo pacman -S plasma-pa
# gnome
sudo pacman -S gnome-alsamixer
```

### 调音量

alsamixer

## ArchLinux安装完没有声音

### 解除静音
  
```bash
amixer -c 0 sset 'Master',0 100%,100% unmute
```

http://blog.csdn.net/weed_hz/article/details/9226055


### ALSA
https://segmentfault.com/a/1190000002918394

高级 Linux 声音体系 (Advanced Linux Sound Architecture，ALSA）是Linux中提供声音设备驱动的内核组件，用来代替原来的开放声音系统 (Open Sound System，OSSv3）。除了声音设备驱动，ALSA还包含一个用户空间的函数库，以方便开发者通过高级API使用驱动功能，而不必直接与内核驱动交互。
Arch 默认的内核已经通过一套模块提供了 ALSA，不必特别安装。
udev会在系统启动时自动检测硬件，并加载相应的声音设备驱动模块。这时，你的声卡已经可以工作了，只是所有声道默认都被设置成静音了。


