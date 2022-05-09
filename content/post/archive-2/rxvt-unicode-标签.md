---
title: rxvt-unicode 标签
author: "-"
date: 2017-07-25T01:52:06+00:00
url: /?p=10901
categories:
  - Inbox
tags:
  - reprint
---
## rxvt-unicode 标签
http://0x3f.org/post/let-rxvt-unicode-support-tags-and-links/

为rxvt-unicode开启标签和链接支持

写完urxvt-unicode快速上手,本以为已将urxvt的用法一网打尽,不料AndyWxy网友又找到了两个新的功能: 使urxvt启用标签和在urxvt中打开网页链接。

标签功能很实用,一般为了达到复用终端窗口的目的会采用两种方式: 一是配合screen使用,另一个就是启用标签。然而前者有一个缺点就是不直观,标签页恰好能弥补这个缺陷。urxvt不愧是个功能强大的终端工具,如果在编译时开启perl支持,则urxvt可启用多标签功能。用法如下: 

一是在启动的时候加入命令行参数: 

urxvt -pe tabbed

二是在配置文件".Xresources"中添加如下配置信息: 

URxvt.perl-ext-common: default,tabbed

则默认情况下执行urxvt就会打开多标签功能。urxvt的标签支持使用鼠标操作,同时可以使用Ctrl+Shift+左右箭头来切换标签页,使用Ctrl+Shift+向下箭头开启新标签。

另外一个功能就是可以通过在urxvt中的链接上点击鼠标左键来通过设定的浏览器打开之。首先在".Xresources"文件中添加如下内容: 

URxvt.urlLauncher: firefox URxvt.matcher.button: 1

然后使用如下命令打开urxvt: 

urxvt -pe matcher

即可。也可以在配置文件中添加上述内容之后再添加一行: 

URxvt.perl-ext-common: matcher

此后即默认开启在终端窗口中打开链接的功能。注意修改".Xresources"文件后需要执行如下命令才能使修改后的配置文件生效: 

xrdb ~/.Xresources