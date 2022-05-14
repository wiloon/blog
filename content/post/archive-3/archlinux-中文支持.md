---
title: archlinux 中文支持
author: "-"
date: 2020-04-03T02:02:29+00:00
url: /?p=15873
categories:
  - inbox
tags:
  - reprint
---
## archlinux 中文支持
```bash
vim /etc/locale.gen
en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8

locale-gen

/etc/locale.conf文件设置全局有效的locale
LANG=en_US.UTF-8

# 中文字体 
sudo pacman -S wqy-microhei

locale -a 来显示当前Linux系统支持的所有的语言环境。

```