---
title: urxvt
author: "-"
date: 2017-02-10T04:08:47+00:00
url: /?p=9768
categories:
  - Uncategorized

tags:
  - reprint
---
## urxvt
urxvt is a highly customizable terminal emulator.

```bash
sudo pacman -S rxvt-unicode
#start rxvt-unicode
urxvt

#加载 urxvt 配置文件
xrdb -load ~/.Xresources
xrdb ~/.Xresources

# 'rxvt-unicode-256color': unknown terminal type.
urxvt -tn xterm
#or
mkdir -p ~/.terminfo/r/
scp /usr/share/terminfo/r/rxvt-unicode-256color user@remotehost:.terminfo/r/

```

配置文件在$HOME/.Xresources这个文件中。
   
! 起始的行是注释
  
!!$HOME/.Xresources
  
URxvt.preeditType:Root
  
!!调整此处设置输入法
  
URxvt.inputMethod:fcitx
  
!!颜色设置
  
URxvt.depth:32
  
!!中括号内数表示透明度
  
URxvt.inheritPixmap:true
  
URxvt.background:#000000
  
URxvt.foreground:#ffffff
  
URxvt.colorBD:Gray95
  
URxvt.colorUL:Green
  
URxvt.color1:Red2
  
URxvt.color4:RoyalBlue
  
URxvt.color5:Magenta2
  
URxvt.color8:Gray50
  
URxvt.color10:Green2
  
URxvt.color12:DodgerBlue
  
URxvt.color14:Cyan2
  
URxvt.color15:Gray95
  
!!URL操作
  
URxvt.urlLauncher:chromium
  
URxvt.matcher.button:1
  
Urxvt.perl-ext-common:matcher
  
!!滚动条设置
  
URxvt.scrollBar:False
  
URxvt.scrollBar_floating:False
  
URxvt.scrollstyle:plain
  
!!滚屏设置
  
URxvt.mouseWheelScrollPage:True
  
URxvt.scrollTtyOutput:False
  
URxvt.scrollWithBuffer:True
  
URxvt.scrollTtyKeypress:True
  
!!光标闪烁
  
URxvt.cursorBlink:True
  
URxvt.saveLines:3000
  
!!边框
  
URxvt.borderLess:False
  
!!字体设置
  
Xft.dpi:96
  
URxvt.font:xft:Source Code Pro:antialias=True:pixelsize=18,xft:WenQuanYi Zen Hei:pixelsize=18
  
URxvt.boldfont:xft:Source Code Pro:antialias=True:pixelsize=18,xft:WenQuanYi Zen Hei:pixelsize=18

终端软件有很多,gnome有gnome terminal,kde有konsole,还有xfce-terminal,xterm,rxvt, aterm, eterm等等,这里我选择的是rxvt-unicode。主要因为我们所需要的终端,需要具有以下的特性: 

快速 (rxvt-unicode基于rxvt,rxvt基于xterm,xterm的快速是毋庸置疑的) ；
  
支持utf8,否则不能正确显示简体和繁体中文 (从rxvt-unicode的名字就可以看出来了) ；
  
易配置,更换系统时只需要保留配置文件就能恢复 (rxvt-unicode配置可以写在~/.Xdefaults或者~/.Xresources中) ；
  
支持透明,因为我们需要eyecandy来防止审美疲劳 (rxvt-unicode不光支持伪透明,也可以做到真透明,不过我没有试过) 。
  
符合上面条件的,以我所知,就只有rxvt-unicode (如果我错了请纠正我) 。除了这些特性,rxvt-unicode还具有以下特性: 

可以以server/client模式启动,更加节省系统资源 (urxvtcd) ;
  
显示彩色man page。

urxvt的复制和黏贴
  
复制 就是直接选定
  
黏贴就是鼠标中键
  
从非urxvt复制并黏贴入urxvt用shitf+insert

http://yuex.in/post/2013/09/terminal-switching.html
  
https://dimit.me/blog/2015/01/28/urxvt-term-support-ssh/
  
http://forum.ubuntu.com.cn/viewtopic.php?f=21&t=120199
  
http://forum.ubuntu.org.cn/viewtopic.php?t=66302
  
https://wiki.archlinux.org/index.php?title=Rxvt-unicode&redirect=no#Installation
  
http://blog.liangzan.net/blog/2012/01/19/my-solarized-themed-arch-linux-setup/