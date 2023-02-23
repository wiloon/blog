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

## archlinux

```bash
yay -S snapd
sudo systemctl enable --now snapd.socket
sudo systemctl start snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install another-redis-desktop-manager

```
