---
title: wine
author: "-"
date: 2012-04-29T06:57:04+00:00
url: /?p=3068
categories:
  - Linux
tags:$
  - reprint
---
## wine
卸载wine中已经安装的软件
  
到程序的目录里面

```bash~/.wine/drive_c/Program Files/*****
wine 卸载程序.exe
```

wine，是一款优秀的Linux系统平台下的模拟器软件，用来将Windows系统下的软件在Linux系统下稳定运行，该软件更新频繁，日臻完善，可以运行许多大型Windows系统下的软件。另外英语单词wine是葡萄酒的意思。

刚刚步入Linux，难免要有时利用一下Windows的程序资源，Wine提供了一个用来运行Windows程序的平台。

Wine (Wine Is Not an Emulator)[即Wine不仅仅是一个模拟器]是一个在Linux和UNIX之上的,Windows 3.x 和 Windows APIs的实现.它是一个Windows兼容层,用通俗的话说,就是一个Windows模拟器,这个层既提供了一个用来从Windows源进出到UNIX的开发工具包(Winelib),也提供了一个程序加载器,该加载器允许不用任何修改Windows 3.1/95/NT的二进制文件,就可以运行在Intel Unix及其衍生版本下.Wine可以工作在绝大多数的UNIX版本下,包括Linux, FreeBSD, 和 Solaris. Wine不需要Microsoft Windows, 因为这是一个完全由百分之百的免费代码组成的,可以选择的实现,但是它却可以随意地使用本地系统的DLLs,如果它们是可以被利用的话.Wine的发布是完全公开源代码的,并且是免费发行的。

目前 Wine 仍在发展阶段，但是较新的版本可以运行一些著名软件，甚至是 Photoshop CS3!

Wine的官方站点是http://www.winehq.com/，虽然你可以在它的官方站点下载源代码，自己配置编译，不过这个过程可是比较繁琐的！