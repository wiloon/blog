---
title: archlinux wireless
author: "-"
date: 2015-04-26T08:29:37+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: archlinux-wireless
tags:
  - Linux
  - archlinux
  - wifi
  - remix
  - AI-assisted
categories:
  - Linux
aliases:
  - /p7520/
---
## archlinux wireless
    https://wiki.archlinux.org/index.php/Wireless_network_configuration
    
    ip link set wlp3s0 up

    wifi-menu -o

```bash
netctl start <profile>
netctl enable <profile>
netctl start wlp0s26f7u5-w1100n
```

------deleted
sudo wpa_supplicant -i wlp0s26f7u5 -c /etc/wpa_supplicant/wpa_supplicant.conf -d sudo dhcpcd wlp0s26f7u5

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Linux | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
