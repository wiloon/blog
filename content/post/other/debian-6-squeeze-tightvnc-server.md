---
title: Debian 6 squeeze TightVNC Server
author: "-"
date: 2012-12-08T03:42:58+00:00
url: /?p=4857
categories:
  - Linux

tags:
  - reprint
---
## Debian 6 squeeze TightVNC Server
# 1 安装

  
    
      如果已经安装了图形用户界面，只需要在bash中apt-get install tightvncserver。
    
    
    
      sudo apt-get install tightvnc*
    
    
    
      vnc client: xtightvncviewer
    
    
    
      2 运行
    
    
    
      2.1 普通运行
    
    
    
      在bash中输入tightvncserver，第一次运行需要设置访问密码。
    
    
    
      每次启动tightvncserver都会返回一个编号。
    
    
    
      编号在这句中: New 'X' desktop is wqvm-debian:2
    
    
    
      可见启动的编号为2。使用VNC客户端去连接时，默认用这个编号+5900得到端口号去连接。
    
    
    
      2.2 自动运行
    
    
    
      写入rc.d即可。
    
    
    
      2.3 终止运行
    
    
    
      tightvncserver -kill :2
    
    
    
      注意将上一行中的2修改为你在运行tightvncserver中得到的编号，即可关闭这个VNC Server的进程。
    
    
    
      3 与vnc4server比较
    
    
    
      貌似vnc4server最后一版是2005年发行，距今很久了。说明比较稳定，但是可能落后了。
    
    
    
      我安装了vnc4server后不能直接从客户端连接，可能还需要更多的配置。
    
    
    
      4 参考资料
    
    
    
      http://news.metaparadigma.de/linux-setting-up-a-debian-vnc-server-237/ 英文的。
    
    
    
      http://www.cnblogs.com/yangzhao/archive/2011/08/20/2147387.html
  
