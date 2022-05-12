---
title: Telnet, SSH
author: "-"
date: 2011-12-04T06:43:49+00:00
url: telnet/ssh
categories:
  - Network
tags:
  - reprint
---
## Telnet, SSH
### Telnet
telnet: TCP/IP终端仿真协议 (TCP/IP Terminal Emulation Protocol): 通过TCP建立服务器与客户机之间的连接。连接后，TELNET服务器与客户机进入协商阶段 (决定可选项) ，选定双方都支持连接操作每个连接系统可以协商可选项或重协商旧可选项 (在任何时候) 。通常TELNET任一端尽量执行所有可选项以实现系统最大化性能。

在终端使用者的电脑上使用telnet程序，用它连接到服务器。终端使用者可以在telnet程序中输入命令，这些命令会在服务器上运行，就像直接在服务器的控制台上输入一样。可以在本地就能控制服务器。要开始一个telnet会话，必须输入用户名和密码来登录服务器。Telnet是常用的远程控制 Web服务器的方法。

传统telnet连线会话所传输的资料并未加密，这代表所输入和显示的资料，包括帐号名称及密码等敏感数据，可能会遭其他人窃听，因此有许多服务器会将telnet服务关闭，改用更为安全的SSH。

### SSH Secure Shell Protocol

SSH是一种在不安全网络上提供安全远程登陆及其他安全网络服务的协议.SSH是指Secure shell,SSH协议族由IETF(internet engineering task force)的network working group制定,SSH协议的内容SSH协议是建立在应用层和传输层基础上的安全协议.传统的网络服务程序,如FTP,POP和TELNET其本质上都是不安全的;因为它们在网络上用明文传送数据,用户帐号和用户口令,很容易受到中间人(man-in-the-middle)攻击方式的攻击.就是存在另一个人或者一台机器冒充真正的服务器接收用户传给服务器的数据,然后在冒充用户把数据传给真正的服务器.SSH是目前比较可靠的远程登录会话和其他网络服务提供安全性的协议.利用SSH协议可以有效防止远程管理过程中的信息泄露问题.通过SSH,可以把所有传输的数据进行加密,也能够防止DNS欺骗和IP欺骗.SSH,还有一个额外的好处就是传输的数据是经过压缩的,所以加以加快传输的速度.SSH有很多功能,它既可以代替TELNET,又可能为FTP,POPPPP提供一个安全的"通道".
