---
title: Archlinux, Pixelbook, chromeos, Crostini
author: "-"
date: 2018-09-08T04:24:14+00:00
url: /?p=12641
categories:
  - Inbox
tags:
  - reprint
---
## Archlinux, Pixelbook, chromeos, Crostini

<https://wiki.archlinux.org/title/Chromebook_Pixel_2>
<https://wiki.archlinux.org/index.php/Chrome_OS_devices/Crostini>

### Enabling Linux support

Settings > Linux > Enable

### Delete the Debian container (optional)

```bash
vmc destroy termina
vmc start termina
```

### Install an Arch linux container

Open a new terminal in Chrome (Ctrl + Alt + T)

```bash
vmc container termina arch https://us.images.linuxcontainers.org archlinux/current
vsh termina
lxc list
lxc exec arch -- bash
passwd $(grep 1000:1000 /etc/passwd|cut -d':' -f1)

pacman -S sudo
visudo

# Uncomment this line:
%wheel ALL=(ALL) ALL
usermod -aG wheel $(grep 1000:1000 /etc/passwd|cut -d':' -f1)
exit

lxc console arch
# enter user name root
ip -4 a show dev eth0
# config arch pacman mirror
# install yay
yay -S cros-container-guest-tools-git
sudo pacman -S wayland
sudo pacman -S  xorg-server-xwayland

# 第一次执行如果报错,尝试停掉container重启
lxc stop arch
lxc start arch

systemctl --user enable sommelier@0
systemctl --user enable sommelier-x@0
systemctl --user start sommelier@1
systemctl --user start sommelier-x@1

systemctl --user status sommelier@0
systemctl --user status sommelier@1
systemctl --user status sommelier-x@0
systemctl --user status sommelier-x@1

lxc stop --force arch
lxc stop --force penguin
lxc rename penguin debian
lxc rename arch penguin
lxc start penguin
```

<https://tedyin.com/posts/archlinux-on-pixelbook/>

```bash
lxc profile set default security.syscalls.blacklist "keyctl errno 38"
run_container.sh --container_name archlinux --user ymf --lxd_image archlinux/current --lxd_remote https://us.images.linuxcontainers.org/

lxc exec archlinux -- bash
```

### openvpn in crostini

```bash
# 进入crosh环境
ctrl+t
# 在crosh中执行以下命令
vmc stop termina
vmc start termina
lxc config device add penguin tun unix-char path=/dev/net/tun
# 再次打开crostini archlinux
sudo pacman -Syu
sudo pacman -S openvpn
# openvpn 可以正常使用了
```

### 显示问题, 找不到图形环境问题

```bash
# in crostini
export WAYLAND_DISPLAY=wayland-0
# <user id>替换成 当前用户的id
export XDG_RUNTIME_DIR=/run/user/<user id>
/opt/google/cros-containers/bin/sommelier -X command0
sommelier -X --x-display=1 --scale=2 bash -c 'echo Xft.dpi: 192 | xrdb -merge; firefox'
--dpi=
```

<https://chromium.googlesource.com/chromiumos/platform2/+/master/vm_tools/sommelier/>
  
<https://www.reddit.com/r/Crostini/comments/94wenl/how_to_get_other_chromeos_keyboard_shortcuts/>
  
<https://www.reddit.com/r/Crostini/comments/8nt9js/connect_to_vpn_from_the_linux_container/>

<https://pixelbook.silentselene.com/index.php/archives/33/>

<https://wiki.archlinux.org/index.php/Chromebook_Pixel_2>
  
<https://wiki.archlinux.org/index.php/Chrome_OS_devices#Installing_Arch_Linux>
  
<https://wiki.archlinux.org/index.php/Installation_guide>

## archlinux install
  
<http://blog.wiloon.com/?p=7821>
  
<https://chromium.googlesource.com/chromiumos/docs/+/master/containers_and_vms.md>
