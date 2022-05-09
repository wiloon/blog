---
title: linux 查看 SATA 速度, 版本
author: "-"
date: 2019-04-14T02:33:16+00:00
url: /?p=14159
categories:
  - Inbox
tags:
  - reprint
---
## linux 查看 SATA 速度, 版本
https://www.cyberciti.biz/faq/linux-command-to-find-sata-harddisk-link-speed/

```bash
sudo pacman -S smartmontools

sudo smartctl -a /dev/DEVICE-NAME-HERE
sudo smartctl -i /dev/DEVICE-NAME-HERE
sudo smartctl -a /dev/sda | grep "^SATA"
sudo smartctl -i /dev/sdb | grep "^SATA"
sudo smartctl -a /dev/sda
sudo smartctl -i /dev/sdb

dmesg | grep -i sata | grep 'link up'

```