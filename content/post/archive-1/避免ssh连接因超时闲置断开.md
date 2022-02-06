---
title: 避免SSH连接因超时闲置断开
author: "-"
date: 2013-10-20T05:48:51+00:00
url: /?p=5861
categories:
  - Uncategorized
tags:
  - linux
  - SSH

---
## 避免SSH连接因超时闲置断开

用SSH过程连接电脑时，经常遇到长时间不操作而被服务器踢出的情况，常见的提示如: 
  
  Write failed: Broken pipe
  
这是因为如果有一段时间在SSH连接上无数据传输，连接就会断开。解决此问题有两种方法。[1]
  
## 方案一: 在客户端设置
  
方法很简单，只需在客户端电脑上编辑（需要root权限) /etc/ssh/ssh_config，并添加如下一行:
  
  ServerAliveInterval 60
  
此后该系统里的用户连接SSH时，每60秒会发一个KeepAlive请求，避免被踢。
  
## 方案二: 在服务器端设置
  
如果有相应的权限，也可以在服务器端设置，即编辑/etc/ssh/sshd_config，并添加:
  
  ClientAliveInterval 60
  
重启SSH服务器后该项设置会生效。每一个连接到此服务器上的客户端都会受其影响。应注意启用该功能后，安全性会有一定下降（比如忘记登出时……)