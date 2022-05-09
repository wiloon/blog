---
title: Qt, GTK
author: "-"
date: 2013-02-24T02:09:28+00:00
url: /?p=5239
categories:
  - Inbox
tags:
  - reprint
---
## Qt, GTK

### 查看Qt 版本

qmake -v

### Qt debug

```bash
export QT_DEBUG_PLUGINS=1
```

Qt 是一个跨平台的 C++ 图形用户界面库，由挪威 TrollTech公司出品，目前包括Qt， 基于 Framebuffer 的 Qt Embedded，快速开发工具 Qt Designer，国际化工具 Qt Linguist 等部分. Qt支持所有 Unix 系统，当然也包括 Linux，还支持WinNT/Win2k，Win95/98 平台。

Trolltech 公司在 1994 年成立，但是在 1992 年，成立 Trolltech 公司的那批程序员就已经开始设计 Qt 了，Qt 的第一个商业版本于 1995 年推出然后 Qt 的发展就很快了，下面是 Qt 发展史上的一 些里程碑:
  
1996 Oct KDE 组织成立
  
1998 Apr 05 Trolltech 的程序员在 5 天之内将 Netscape5.0 从 Motif 移植到
  
Qt 上
  
1998 Apr 08 KDE Free Qt 基金会成立
  
1998 Jul 09 Qt 1.40 发布
  
1998 Jul 12 KDE 1.0 发布
  
1999 Mar 04 QPL 1.0 发布
  
1999 Mar 12 Qt 1.44 发布
  
1999 Jun 25 Qt 2.0 发布
  
1999 Sep 13 KDE 1.1.2 发布
  
2000 Mar 20 嵌入式 Qt 发布
  
2000 Sep 06 Qt 2.2 发布
  
2000 Oct 05 Qt 2.2.1 发布
  
2000 Oct 30 Qt/Embedded 开始使用 GPL 宣言
  
2000 Sep 04 Qt free edition 开始使用 GPL

基本上，Qt 同 X Window 上的 Motif，Openwin，GTK 等图形界 面库和Windows 平台上的 MFC，OWL，VCL，ATL 是同类型的东西，但是 Qt 具有下列优点:
  
1.优良的跨平台特性:
  
Qt支持下列操作系统: Microsoft Windows 95/98， Microsoft Windows NT，Linux， Solaris， SunOS， HP-UX， Digital UNIX (OSF/1， Tru64)，Irix， FreeBSD， BSD/OS， SCO， AIX， OS390，QNX 等等。
  
2.面向对象:
  
Qt 的良好封装机制使得 Qt 的模块化程度非常高，可重用性较好，对于用户开发来说是非常方便的。 Qt 提供了一种称为 signals/slots 的安全类型来替代callback，这使得各个元件 之间的协同工作变得十分简单。
  
3.丰富的 API:
  
Qt 包括多达 250 个以上的 C++ 类，还替供基于模板的 collections，serialization， file， I/O device， directory management， date/time 类。甚至还包括正则表达式的处理 功能。

4.支持 2D/3D 图形渲染，支持 OpenGL
  
5.大量的开发文档
  
6.XML 支持

但是真正使得 Qt 在自由软件界的众多 Widgets (如 Lesstif，Gtk，EZWGL，Xforms，fltk 等等)中脱颖而出的还是基于 Qt 的重量级软件 KDE 。 有趣的是，KDE 也是使得 Trolltech 公司承受巨大压力的一个原因。下面我们将来看看这场著名的自由软件圣战 - "KDE/QT .VS. Gnome/Gtk" 是怎么发生的。

在 Unix 的图形界面一向是以 MIT 的 X Window 系统为标准， 可是在商业应用上有两大流派，一派是以 Sun 公司领导的 Openlook 阵营，一派是 IBM/HP 领导的OSF (Open Software Foundation) 的 Motif， 双方经过多年竞争之后， Motif 最终胜出，成为最普遍使用的界面库， 后来双方又妥协出一个 CDE(Common Desktop Enviroment) 作为一个标准的图形界面。 但是 Motif/CDER 的价格非常昂贵，在这同时微软的 Windows 图形界面发展速度非常快，而 Unix 界的后起之秀Linux 也急需一个可靠并且免费的图形界面。
  
1996 年 10 月，由开发图形排版工具Lyx的德国人 Matthias Ettrich 发起了 KDE计划。 KDE 的全称为 K Desktop Environment，可以看出是针对 CDE。 KDE 本身是采用 GPL 宣言的，但是 KDE 却是使用 Qt 来作为其底层库，因为当时 Qt 已经将其 Unix 版 本自由发布了，但是 Qt 并不遵循 GPL， 因此 KDE 被很多自由软件的作者攻击，认为利用非自 由软件开发违背了 GPL 的精神，于是 GNU 的狂热信徒兵分两路，一路是去制作 Harmonny，试图重写一套兼容于 Qt 的替代品，另一路是由一个 26 岁的墨西哥程序员 Miguel De Icaza 领导 下重新开发一套叫OME(GNU Network Object Enviroment)来替代 KDE。
  
由于 Linux 界的老大 RedHat 不喜欢 KDE/Qt 的版权，因此 RedHat 甚至专门派出了几个全职程序员来加入 GNOME 进行开发工作，于是一场同 Motif VS Openlook 相似的圣战就这么打起来了。 Trolltech 为了 KDE 曾数次修改 Qt 的版权，从成立 KDE Free Qt 基 金会到采用 QPL，可谓是费尽心机，但是 GNOME 采用的 GTK 一开始就是完全的 GPL，因此在这个方 面 GNOME 有一定的优势，加上 Qt/KDE 采用 C++ 开发，入门的门槛比较高，而 GTK/Gnome 采用 C， 因此GNOME 吸引了更多的自由软件开发者，但是 KDE 毕竟先走了一步， 推出的KDE1.1.2 十分稳定， 而当时急忙中推出的 GNOME1.0 的系统稳定性奇差，有人甚至笑称 GNOME1.0 还没有 KDE 1.0 Alpha 稳定。但是 GNOME 后来发展比较快，大有迎头赶上的势头。 当时双方的开发者在网络 上炒得天翻地覆，连 Linux 之父 Linus 只是说了一句喜欢用 KDE 都倍受指责。
  
战争到了第三个年头，也就是2000年，可谓是风云突变，一个接一个重大的事件先后发生: 首先是一批从 Apple 公司出来的工程师成立了一个叫 Eazel 的公司替GNOME 设计界面，然后是一批 GNOME 程序员成立了一个 Helix Code 公司替GNOME 提供商业支持，而大家期待以久的 KDE 2.0 也终于发布了，这恐怕是目前最为庞大的自由 软件了之一， 除了 KDE 本身，还包括 Koffice 套件，和集成开发环境 Kdevelop 等等大批软件，其主力软件 Kounqueror 也是第一个可以同微软的Internet Exploer 相抗衡的浏览器。 而 Sun 公司，Red Hat 公司， Eazel 公司， Helix Code 等一批公司成立了一个GNOME 基金会， Sun 还宣布将把重量级办公软件 Star office 同 GNOME 集成， Trolltech 公司自然不能坐以 待毙，于10 月4 日将 Qt 的 free edition 变为 GPL 宣言，彻底解决了 KDE 的版权问题， 又推出了嵌入式 Qt ，给了 GNOME 阵营一个有力的回击。
  
到现在为止，这场战争还在继续。一般说来， 目前GNOME 吸引的公司比较多，但是 KDE/Qt 的开发的效率和质量比GNOME 高，而且在 Office/嵌入式 环境中先走一步，在一定时间内还将处于优势地位。
  
那么对于用户来说，如何在 Qt/GTK 中作出选择呢?一般来说，如果用户使用C++，对库的稳定性，健壮性要求比较高，并且希望跨平台开发的话，那么使用 Qt是较好的选择， 但是值得注意的是，虽然 Qt 的 Free Edition 采用了 GPL 宣言，但是如果你开发 Windows 上的 Qt 软件或者是 Unix 上的商业软件，还是需要向Trolltech 公司支付版权费用的。
  
本文转自<http://herisee.bokee.com/1929875.html>
