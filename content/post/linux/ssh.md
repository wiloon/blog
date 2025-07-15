---
title: ssh
author: "-"
date: 2012-01-20T01:37:12+00:00
url: ssh
categories:
  - Linux
tags:
  - reprint
---
## ssh

SSH和Session的关系是一对多的关系

SSH连接 (SSH Connection)
定义: 是客户端与服务器之间的底层加密网络连接
协议层: SSH Transport Layer Protocol
作用: 提供加密的通信通道, 作用: 提供加密、认证、完整性保护
生命周期: 从建立连接到断开连接的整个过程
数量: 通常一个客户端到服务器只有一个SSH连接

SSH Channel (SSH通道)
定义: 在SSH连接内部的逻辑通道
协议层: SSH Connection Protocol
作用: 在单个SSH连接上复用多个数据流
类型:
session - 用于命令执行、shell
direct-tcpip - 用于端口转发
forwarded-tcpip - 用于反向端口转发
x11 - 用于X11转发

SSH会话 (SSH Session)
定义: 运行在特定Channel上的服务, 是在SSH连接之上的逻辑会话
协议层: 应用层服务
作用: 用于执行具体的命令或启动shell
生命周期: 从创建会话到关闭会话
数量: 一个SSH连接可以创建多个会话
类型:
exec - 执行单个命令
shell - 启动交互式shell
subsystem - 启动子系统（如SFTP）

为什么需要会话管理？

状态隔离
每个会话有独立的环境变量、工作目录
不同命令之间不会相互影响

性能优化
复用SSH连接，避免重复建立连接的开销
会话用完即关闭，释放服务器资源


## golang ssh

[https://godoc.org/golang.org/x/crypto/ssh](https://godoc.org/golang.org/x/crypto/ssh)
  
[http://www.01happy.com/golang-exec-remote-command/](http://www.01happy.com/golang-exec-remote-command/)

