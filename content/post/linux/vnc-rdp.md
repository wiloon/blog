---
title: vnc rdp
author: "-"
date: 2021-03-13T15:13:27+00:00
url: /?p=2556
categories:
  - Linux

tags:
  - reprint
---
## vnc rdp

VNC是什么？
简单来说，所谓的 VNC（Virtual Network Computing ）是一种图形化的桌面共享系统，它使用远程帧缓冲协议 (RFB) 来远程控制另一台计算机。它将键盘和鼠标事件从一台计算机传输到另一台计算机，通过网络向另一个方向转发图形屏幕更新。

类似这样的技术VNC不是绝无仅有，但VNC 的流行和普及却因为其具有的过人之处 –

VNC是平台无关的—— 有多种客户端和服务器的实现，几乎涵盖了所有的主流平台。甚至一些VNC的实现被称“无客户端”，这是因为不需要安装插件或客户端软件而，而是依靠HTML5技术，只需要一个浏览器就可以访问远程桌面了。
VNC 是开源的—— VNC最初是在英国剑桥的Olivetti & Oracle研究实验室开发的。原始的VNC源代码和许多现代的衍生品在GNU通用公共许可证下是开放源码的。
VNC的协议是简单、普适的—— VNC使用的是 RFB(Remote Framebuffer) 协议。这是一个开放且简单的协议。因为它在framebuffer级别工作，协议是基于**像素**的所以适用于所有窗口系统和应用程序，包括Microsoft Windows、macOS和X Window系统。这个协议的性能表现是很出色的。

RDP 又是什么？
有过 Windows 使用经验的人对于远程桌面（Remote Desktop Protocol ，RDP）一定不会陌生。RDP 是由微软公司开发的一种专有协议，它为用户提供了通过网络连接到另一台计算机的图形界面。在使用上，用户需要使用 RDP 客户端软件，而在远程另一台计算机则需要运行 RDP 服务器软件。

VNC协议是基于像素的。尽管这带来了极大的灵活性，可以显示任何类型的桌面，但它的效率往往不如那些更好地理解底层图形布局(例 如： X11)或桌面(例如：RDP )的解决方案。这些协议以更简单的形式(例如：打开窗口)发送图形原语或高级命令，而 VNC 的 RFB 协议尽管支持压缩但只能是发送原始像素数据。

<https://aws.amazon.com/cn/blogs/china/vnc-or-rdp-how-to-choose-a-remote-desktop-on-the-cloud/>