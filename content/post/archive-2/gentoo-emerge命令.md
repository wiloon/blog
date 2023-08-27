---
title: Gentoo emerge命令
author: "-"
date: 2015-10-05T04:39:37+00:00
url: /?p=8379
categories:
  - Inbox
tags:
  - reprint
---
## Gentoo emerge命令

Gentoo的包管理工具称为portage。emerge是这个portage的字符界面管理工具,图形界面工具还有portato,porthole,kuroo,himerge等。

ebuild

ebuild是Portage包管理程序的根本。它是一个纯文本文件,而每一个ebuild都会对应一个包 (软件包) 。ebuild会告诉 portage要下载的文件、该包可运行的平台、如何编译它、它所依赖的ebuild和一些修补代码的patch。Portage内有一个ebuild大集合,称为Portage tree,是gentoo网站所提供的ebuild。它包含了大部份常用的包,并会不时更新。如果要使用的包不在其内,也可以手动加入。

USE标志

USE标志的设置位于Gentoo系统的/etc/make.conf文档中,作用是使得Emerge在处理依赖关系的时候可以做到不安装不需要的软件包 (例如安装Gnome的用户没有必要因为一个软件包的依赖关系而安装KDE与Qt) ,而安装指定的软件包 (同样以Gnome举例,Gnome的用户基本上都会安装GTK+) ,把系统的设置专注化。

Gentoo的emerge命令参数用法详解

查找名称包含mozilla的包

emerge -s mozilla
  
emerge search mozilla

查找描述包含mozilla

emerge -S mozilla
  
emerge -searchdesc mozilla

使用本地编好的包,没有就下源码(尽量避免编译)

emerge -k mozilla
  
emerge -usepkg mozilla

只使用本地编好的,否则不安装(绝对不编译,所有依赖的包都有binary才装)

emerge -K mozilla
  
emerge -usepkgonly mozilla

卸载

emerge -C mozilla
  
emerge unmerge mozilla

升级portage树

emerge -sync

下载snapshot包来完成sync

emerge-webrsync

查看已安装包的changelog

emerge -pl mozilla
  
emerge -pretend -changelog mozilla

查看依赖关系(这个包还没装)
  
(–pretend保证这一次操作实际上不做任何事情,可以跟任何options组合)

emerge -p mozilla
  
emerge -pretend mozilla

只下载某个软件的源码(以及它所依赖的)

emerge -f mozilla
  
emerge -fetchonly mozilla

查看从哪下的源码

emerge -fp mozilla

安装指定版本号的

emerge "..........."

emerge -k "

从网上下binary包来装

emerge -g mozilla
  
emerge -getbinpkg mozilla

(注意,实际上没有任何binary包存在于官方的mirror中
  
所以这个基本上是无用,在manpage也没有出现。除非自
  
己用livecd来setup一个这样的站点。不知道以后会不会
  
出现这样的mirror。gentoo.org论坛上似乎也有讨论这个。)

查看binary包依赖

emerge -gp mozilla
  
emrege -getbinpkg -pretend mozilla

查看依赖关系(这个包已经装了)

emerge -ep opera
  
emerge -emptytree -pretend opera

(不用pretend会重新编译这所有依赖的包, glibc 因为安全关系没有列出)

不使用依赖关系安装软件

emerge -O opera
  
emerge -nodeps opera

只安装其依赖的软件

emerge -o opera
  
emerge -onlydeps opera

升级软件

emerge -u opera
  
emerge -update opera

升级系统软件

emerge -u system

升级整个系统

emerge -u world

避免升级覆盖掉版本更高的软件

emerge -uU world
  
emerge -update -upgradeonly world

查看可用的USE参数
  
emerge -pv opera

参考文档: <http://www.gentoo.org/doc/zh_cn/index.xml>
  
永久链接 : <http://www.ha97.com/3192.html>
