---
author: "-"
date: "2021-04-22 16:45:29" 
title: snap
categories:
  - inbox
tags:
  - reprint
---
## snap

安装 snap 的过程还是需要些内存的, 我有个虚拟机剩余内存 230M, snap 安装失败... 

### almalinux

```Bash
sudo dnf install epel-release
sudo dnf upgrade
dnf install snapd --enablerepo=epel -y
```

### almalinux

```Bash
sudo dnf install epel-release
sudo dnf config-manager --set-enable epel
sudo dnf upgrade
sudo dnf install snapd
```

```Bash
# ubuntu: Unable to update "Snap Store": cannot refresh "snap-store": snap "snap-store" has running apps 
snap-store --quit
# 列出已经安装的 snap 包
sudo snap list
# 列出所有已安装的版本
snap list --all vlc
# update all Snap packages
sudo snap refresh
# Check for snap changes
sudo snap changes
sudo snap abort <number>
```

## archlinux

```bash
yay -S snapd
sudo systemctl enable --now snapd.socket
sudo systemctl start snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install another-redis-desktop-manager

```

## http proxy

```Bash
$ sudo snap set system proxy.http="http://<proxy_addr>:<proxy_port>"
$ sudo snap set system proxy.https="http://<proxy_addr>:<proxy_port>"
```

https://blog.csdn.net/omaidb/article/details/120581033

## 清理 Snap 缓存, 旧版本的 APP

```Bash
#!/bin/bash
#Removes old revisions of snaps
#CLOSE ALL SNAPS BEFORE RUNNING THIS
set -eu
LANG=en_US.UTF-8 snap list --all | awk '/disabled/{print $1, $3}' |
while read snapname revision; do
snap remove "$snapname" --revision="$revision"
done
```
