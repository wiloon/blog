---
title: gnome keyring
author: "-"
date: "2019-11-05T00:27:44+00:00"
url: "gnome-keyring"
categories:
  - "Linux"
tags:
  - "reprint"
---
## gnome keyring

### install

```bash
sudo pacman -S gnome-keyring  libsecret
```

### vim .bashrc

```bash
eval $(/usr/bin/gnome-keyring-daemon --start --components=gpg,pkcs11,secrets,ssh)
export $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)
dbus-update-activation-environment --systemd DISPLAY
```

### secret-tool, 用 secret-tool 测试 gnome keyring daemon 是否正常

secret-tool 由 libsecret 提供

```bash
secret-tool store --label='Label' foo bar
secret-tool lookup foo bar

secret-tool store --label='Label' {attribute} {value} ...
secret-tool lookup {attribute} {value} ...
secret-tool clear {attribute} {value} ...
secret-tool search [--all]{attribute} {value} ...
```

## secret-tool

secret-tool - 通过命令行访问 GNOME keyring (以及其他任何实现了DBus Secret Service API的服务) 。

secret-tool - Store and retrieve passwords

### archlinux key could not be looked up remotely

```bash
sudo pacman -S archlinux-keyring && sudo pacman -Syu
```

---

<https://wiki.archlinux.org/index.php/GNOME/Keyring#Installation>  
<https://bbs.archlinux.org/viewtopic.php?id=191279>  
<https://wiki.gnome.org/Projects/GnomeKeyring>  
