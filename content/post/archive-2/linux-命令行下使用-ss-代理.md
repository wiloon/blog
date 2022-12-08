---
title: linux 命令行下使用socks 代理
author: "-"
date: 2016-12-23T05:58:43+00:00
url: /?p=9610
categories:
  - Inbox
tags:
  - reprint
---
## linux 命令行下使用socks 代理

二、将 Socks5 代理转化为 http 代理
  
socks5 代理转换成 http 代理需要借助第三方软件完成,这里使用 privoxy,Ubuntu 下使用如下命令安装 privoxy

apt-get install privoxy -y

编辑配置文件

# 先备份原配置文件

mv /etc/privoxy/config /etc/privoxy/config.bak

# 在新建一个配置文件

vim /etc/privoxy/config

privoxy 配置样例如下

# 转发地址

forward-socks5 / 127.0.0.1:1080 .

# 监听地址

listen-address localhost:8118

# local network do not use proxy

forward 192.168._._/ .
  
forward 10._._._/ .
  
forward 127._._._/ .

最后启动 privoxy,Ubuntu 16 启动命令如下

# 启动

systemctl start privoxy

# 查看状态

systemctl status privoxy

三、创建快捷代理命令
  
完成上两步配置后,即可将需要代理的软件指向 127.0.0.1:8118 端口即可,但是有些命令行操作并无法设置,只能通过全局代理变量 http_proxy 等设置,此时设置后全局都受影响,为此可以写一个代理脚本,如下

vim /usr/local/bin/proxy

脚本内容如下

# !/bin/bash
  
http_proxy=<http://127.0.0.1:8118> https_proxy=<http://127.0.0.1:8118> $*

赋予可执行权限

chmod +x /usr/local/bin/proxy

最后,对任何想要走代理的命令,只需要在前面加上 proxy 即可,样例如下

proxy gvm install go1.6.3
