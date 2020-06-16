---
title: linux audio, 音量,静音
author: wiloon
type: post
date: 2014-03-30T12:10:53+00:00
url: /?p=6452
categories:
  - Uncategorized
tags:
  - linux

---
```bash
# archlinux+kde 不需要手动修改默认静音设置，安装alsa-utils, plasma-pa后重启即可。
sudo pacman -S alsa-utils
#kde
sudo pacman -S plasma-pa
# gnome
sudo pacman -S gnome-alsamixer
```

调音量

alsamixer

解除静音
  
amixer -c 0 sset 'Master',0 100%,100% unmute

http://blog.csdn.net/weed_hz/article/details/9226055