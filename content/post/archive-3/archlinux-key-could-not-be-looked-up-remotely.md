---
title: gnome keyring
author: "-"
date: 2019-11-05T00:27:44+00:00
url: /?p=15111
categories:
  - Linux
tags:
  - reprint
---
## gnome keyring

### install
    sudo pacman -S gnome-keyring  libsecret

### vim .bashrc
    eval $(/usr/bin/gnome-keyring-daemon --start --components=gpg,pkcs11,secrets,ssh)
    export $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)
    dbus-update-activation-environment --systemd DISPLAY

### secret-tool, 用secret-tool测试gnome keyring daemon是否正常
    secret-tool store --label='Label' foo bar

### archlinux key could not be looked up remotely
sudo pacman -S archlinux-keyring && sudo pacman -Syu

---

https://wiki.archlinux.org/index.php/GNOME/Keyring#Installation  
https://bbs.archlinux.org/viewtopic.php?id=191279  
https://wiki.gnome.org/Projects/GnomeKeyring  