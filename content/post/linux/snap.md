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

```Bash
# 列出已经安装的 snap 包
sudo snap list

# 列出所有已安装的版本
snap list --all vlc
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
