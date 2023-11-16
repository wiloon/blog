---
title: archlinux clean
author: "-"
date: 2018-09-03T08:17:29+00:00
url: archlinux/clean
categories:
  - Linux
tags:
  - reprint
---
## archlinux clean

```bash
# pacman 缓存 目录
/var/cache/pacman/pkg

# 查看缓存目录大小
du -sh /var/cache/pacman/pkg

# remove cached packages that are not currently installed
pacman -Sc

# remove all files from the cache
pacman -Scc

# 定时删除 pacman 缓存
pacman -S pacman-contrib
# dry run
paccache -d
# 软件包保留最近的两个版本
paccache -dk2
paccache -rk2

# 删除已经卸载的软件包
paccache -ruk0

# 启用 paccache timer 每周清理
systemctl enable paccache.timer

pacman -Qtdq

du -sh ~/.cache

du -sh ~/.config
du -sh ~/.local/share
# clean Trash

pacman -S rmlint

rmlint /home/wiloon
# 命令行的磁盘空间管理工具
pacman -S ncdu

# 图形化的磁盘空间管理工具
pacman -S filelight
```

>https://bynss.com/linux/471439.html

## 'clean arch  linux'

```bash
  
sudo pacman -R $(pacman -Qtdq)

pacman -Scc
  
rm -rf ~/.cache
  
sudo pacman -S rmlint # remove duplicate file
  
sudo pacman -S ncdu
  
sudo pacman -S filelight
  
```

[https://www.youtube.com/watch?v=3OoMvyHYWDY](https://www.youtube.com/watch?v=3OoMvyHYWDY)
