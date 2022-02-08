---
title: linux vnc
author: "-"
date: 2012-01-31T09:13:17+00:00
url: /?p=2203
categories:
  - Linux

tags:
  - reprint
---
## linux vnc
ubuntu自带的远程桌面是vino-server

1.vino-server

vino的好处是你的控制是跟在本地是一样的，你在远程打开的窗口，当你去本地登录时会发现这些窗口都在，如果两台机器离的不远，你甚至可以看见那个桌面上的鼠标跟着你窗口的一起在移动。但缺点就是如果你想远程连上vino，那么你得先在本地登录上账号，换句话说，你远程重启机器后，就没办法在用vino登录上那台机器了。

ubuntu下开启vino的方法倒是很简单: 

服务端: 

系统->首选项->远程桌面

选上"允许其他人查看您的桌面""允许其他用户控制您的桌面"愿意的话还有"要求用户输入此密码"，不要选上"请您确认"。

客户端: 

直接用ubuntu默认带的"远程桌面查看器"登录就行了。

2.vnc4server

vnc4的好处是可以登录多个桌面，彼此不冲突。而且不会象vino一样，必须服务端登录后才能连接。但是vnc的桌面是虚拟的，你在客户端打开的程序，在服务端是看不到的。这样有时也不太方便。

vnc4可以从新立得软件包中安装，顺便在本地把xvncviewer也装了。
  
安装后设定密码: vncpasswd
  
启用vnc服务: vncserver
  
第一次启动后会在用户的主目录下生成.vnc的文件夹，默认的使用的是twm的界面，有点丑，所以打开.vnc下的xstartup把最后一行twm &注释掉。在下面添加一行: gnome-session &。这样就OK了。

然后通过ssh启动vncserver，然后不论在windows下还是linux下，vncviewer就可以远程访问了。当然你也可以把vncserver服务设置成后台启动。这样就不必每次都要手动启动这个服务了。

vncserver -kill :1

kill 后面有一个空格

设置分辨率: vncserver -geometry 1280*1024

replace * with x


sudo apt-get install vncviewer.