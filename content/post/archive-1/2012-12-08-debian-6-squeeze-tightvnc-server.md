---
title: Debian 6 squeeze TightVNC Server
author: wiloon
type: post
date: 2012-12-08T03:42:58+00:00
url: /?p=4857
categories:
  - Linux

---
# <span style="font-size: 13px;">1 安装</span>

<div>
  <div id="cnblogs_post_body">
    <p>
      如果已经安装了图形用户界面，只需要在bash中apt-get install tightvncserver。
    </p>
    
    <p>
      sudo apt-get install tightvnc*
    </p>
    
    <p>
      vnc client: xtightvncviewer
    </p>
    
    <p>
      2 运行
    </p>
    
    <p>
      2.1 普通运行
    </p>
    
    <p>
      在bash中输入tightvncserver，第一次运行需要设置访问密码。
    </p>
    
    <p>
      每次启动tightvncserver都会返回一个编号。
    </p>
    
    <p>
      编号在这句中：New &#8216;X&#8217; desktop is wqvm-debian:2
    </p>
    
    <p>
      可见启动的编号为2。使用VNC客户端去连接时，默认用这个编号+5900得到端口号去连接。
    </p>
    
    <p>
      2.2 自动运行
    </p>
    
    <p>
      写入rc.d即可。
    </p>
    
    <p>
      2.3 终止运行
    </p>
    
    <p>
      tightvncserver -kill :2
    </p>
    
    <p>
      注意将上一行中的2修改为你在运行tightvncserver中得到的编号，即可关闭这个VNC Server的进程。
    </p>
    
    <p>
      3 与vnc4server比较
    </p>
    
    <p>
      貌似vnc4server最后一版是2005年发行，距今很久了。说明比较稳定，但是可能落后了。
    </p>
    
    <p>
      我安装了vnc4server后不能直接从客户端连接，可能还需要更多的配置。
    </p>
    
    <p>
      4 参考资料
    </p>
    
    <p>
      http://news.metaparadigma.de/linux-setting-up-a-debian-vnc-server-237/ 英文的。
    </p>
    
    <p>
      http://www.cnblogs.com/yangzhao/archive/2011/08/20/2147387.html
    </p>
  </div>
</div>