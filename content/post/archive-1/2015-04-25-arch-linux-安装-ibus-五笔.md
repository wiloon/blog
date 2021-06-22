---
title: Arch Linux 安装 ibus 五笔
author: "-"
type: post
date: 2015-04-25T06:47:39+00:00
url: /?p=7507
tags:
  - Arch Linux

---
第一步
  
$ sudo pacman -S ibus ibus-qt ibus-pinyin ibus-table
  
$ ibus-setup

$ vim ~/.bashrc
  
export GTK_IM_MODULE=ibus
  
export XMODIFIERS=@im=ibus
  
export QT_IM_MODULE=ibus

第二步
  
```bash

sudo pacman -S -needed gcc make automake autoconf
  
yaourt -Ssq ibus
  
yaourt -S ibus-table-chinese

```
  
或者: 

```bash

$ sudo pacman -S -needed gcc make cmake wget
  
sudo pacman -S pkg-config
  
```

(在 http://code.google.com/p/ibus/downloads/list 网页上找到正确的文件名)
  
$ wget http://ibus.googlecode.com/files/ibus-table-chinese-1.4.6-Source.tar.gz
  
$ tar xzf ibus-table-chinese-1.4.0-Source.tar.gz
  
$ cd ibus-table-chinese-1.4.0-Source
  
$ cmake .
  
$ make
  
$ sudo make install

第三步
  
1. 在屏幕右上角的 IBus 输入法框架 上点击鼠标右键，选择"重新启动"。

2. 在屏幕右上角的 IBus 输入法框架 上点击鼠标右键，选择"首选项"，在"输入法"选项卡中添加"汉语 - 极点五笔86"。

其他未尽事宜，请参阅: ArchWiki: IBus(简体中文)

http://www.cnblogs.com/skyivben/archive/2012/09/18/2691006.html
