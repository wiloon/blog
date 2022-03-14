---
title: 'archlinux AUR,  yay,  Yaourt'
author: "-"
date: 2015-06-28T07:02:07+00:00
url: yay
tags:
  - archlinux
  - reprint
  - remix

categories:
  - linux
---
## 'archlinux AUR,  yay,  Yaourt'
Yaourt 已经不再维护
  
yay 是下一个最好的 AUR 助手。它使用 Go 语言写成,宗旨是提供最少化用户输入的 pacman 界面、yaourt 式的搜索,而几乎没有任何依赖软件。

### yay 安装
    pacman -S base-devel binutils git go

### 从 git 克隆并编译安装, 不能在 root 用户下操作
```bash
su - wiloon
git clone https://aur.archlinux.org/yay.git

cd yay
makepkg -si
```

### AUR mirror

默认的仓库  (aur.archlinux.org） 非常慢， 可以走梯子加速，或者用国内的镜像
执行以下命令修改 aururl :
```bash
yay --aururl "https://aur.tuna.tsinghua.edu.cn" --save
yay --aururl "https://aur.archlinux.org" --save
```

修改的配置文件位于 ~/.config/yay/config.json ,还可通过以下命令查看修改过的配置: 

```bash
yay -P -g
```

### 使用 命令: 
```bash
# 搜索: 
yay -Ss <package-name>

# 安装: 
yay -S <package-name>

# 查询软件包安装的文件列表
yay -Ql <package-name>
```

https://mirrors.tuna.tsinghua.edu.cn/help/AUR/

<http://bashell.nodemedia.cn/archives/install-yaourt.html>
  
https://linux.cn/article-9925-1.html

### 废弃
Yaourt (Yet AnOther User Repository Tool),是社区贡献的一个pacman的一个外壳。在pacman的基础上,它添加了AUR支持,帮助用户轻松从AUR的海量PKGBUILD中选择需要的软件进行编译安装。Yaourt的操作方式类似pacman,易于记忆使用。它提供诸如彩色输出、交互式搜索模式等一系列实用功能。

yaourt-Yet AnOther User Repository Tool

Yaourt是archlinux方便使用的关键部件之一,但没有被整合到系统安装中的工具。建议在装完系统重启之后,更新完pacman和基本系统之后,就安装这个工具。

简便的安装
  
最简单安装Yaourt的方式是添加Yaourt源至您的 /etc/pacman.conf:

[archlinuxcn]
  
#The Chinese Arch Linux communities packages.
  
SigLevel = Optional TrustAll #Optional TrustedOnly
  
Server = http://repo.archlinuxcn.org/$arch
  
同步并安装: 
  
pacman -Sy
  
pacman -S yaourt

如何使用yaourt?
  
yaourt用起来很简单,而且类似于Pacman的命令,下面是常用的一些命令:   
yaourt -S package_name – 从AUR安装软件包

https://linux.cn/article-9925-1.html?utm_source=rss&utm_medium=rss
