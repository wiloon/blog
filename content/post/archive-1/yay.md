---
title: archlinux AUR, yay, Yaourt
author: "-"
date: 2015-06-28T07:02:07+00:00
url: yay
tags:
  - archlinux
  - reprint
  - remix
categories:
  - Linux
---
## archlinux AUR, yay, Yaourt

Yaourt 已经不再维护

yay 是下一个最好的 AUR 助手。它使用 Go 语言写成,宗旨是提供最少化用户输入的 pacman 界面、yaourt 式的搜索,而几乎没有任何依赖软件。

## yay 安装

```bash
sudo pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay-bin.git && cd yay-bin && makepkg -si
```

### AUR mirror

默认的仓库  (aur.archlinux.org） 非常慢, 可以走梯子加速, 或者用国内的镜像
执行以下命令修改 aururl :

```bash
yay --aururl "https://aur.tuna.tsinghua.edu.cn" --save
yay --aururl "https://aur.archlinux.org" --save
```

修改的配置文件位于 ~/.config/yay/config.json, 可以通过以下命令查看修改过的配置

```bash
yay -P -g
```

### 使用 命令

```bash
# 搜索: 
yay -Ss <package-name>

# 安装: 
yay -S <package-name>

# 查询软件包安装的文件列表
yay -Ql <package-name>
```

><https://mirrors.tuna.tsinghua.edu.cn/help/AUR/>
<http://bashell.nodemedia.cn/archives/install-yaourt.html>
><https://linux.cn/article-9925-1.html>
