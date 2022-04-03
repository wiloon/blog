---
title: centos, kde, vnc
author: "-"
date: 2018-04-19T04:41:00+00:00
url: /?p=12150
categories:
  - Uncategorized

tags:
  - reprint
---
## centos, kde, vnc
转自: http://digitalocean.youhuima.cc/centos-7-kde-vnc-remote.html (侵删) 

VPS远程操作用的最多的是SSH,有时候一些特殊需求也要用到远程图形化操作,比如使用在VPS上使用浏览器访问网站。本文以Digitalocean VPS为例分享如何安装KDE和VNC实现远程图形界面访问。如果要购买Digitalocean VPS,建议使用Digitalocean优惠码,可以节省不少银子。

下面介绍安装KDE和VNC的步骤和关键注意点: 
  
1. SSH登录到VPS上以root用户权限进行整个安装过程。
  
2. 查询查询支持的软件包: 
  
yum grouplist
  
如果系统有"KDE Plasma Workspaces",说明可以安装KDE图形化界面,然后执行一键安装命令: 
  
yum groupinstall "KDE Plasma Workspaces"
  
直到安装完成。

3. 安装VNC server,一键安装: 
  

4. 配置VNC server: 
  
在centos 7里配置文件初始模版为: /lib/systemd/system/vncserver@.service
  
这个配置文件只是一个模版,是不会被调用的。需要按照如下步骤复制1份或多份并修改相应的参数来对应不同的VNC viewer客户端。下面以root用户为例。

复制一份配置文件,"@"后的1表示该配置文件对应的远程连接端口号为5901 (5900+1) : 
  
cp /lib/systemd/system/vncserver@.service /lib/systemd/system/vncserver@:1.service
  
远程连接端口号默认为5900+n,n为VNC服务端设置的连接序号,上面的序号就是配置文件名称里".service"前的1。其它的以此类推。

修改新配置文件: 将 (有两处) 改为登录用户root,VNC远程连接后将是root权限。 如果是非root用户就直接用用户名替换即可。
  
修改前: 
  
[Service]
  
Type=forking -》 需要改为simple才会启动成功

# Clean any existing files in /tmp/.X11-unix environment

ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
  
ExecStart=/sbin/runuser -l 改为root不带括号 -c "/usr/bin/vncserver %i -geometry 1024x768"
  
PIDFile=/home/改为root不带括号/.vnc/%H%i.pid
  
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'

修改后: 
  
[Service]
  
Type=simple

# Clean any existing files in /tmp/.X11-unix environment

ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
  
ExecStart=/sbin/runuser -l root -c "/usr/bin/vncserver %i -geometry 1024x768"
  
PIDFile=/home/root/.vnc/%H%i.pid
  
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'

启动VNC并设置root用户vnc的密码
  
[root@localhost /]# vncserver
  
You will require a password to access your desktops.
  
Password: 123456 #输入vnc 连接密码
  
Verify: 123456 #确认vnc密码
  
xauth: creating new authority file /root/.Xauthority
  
New 'localhost.localdomain:1 (root)' desktop is localhost.localdomain:1
  
Creating default startup script /root/.vnc/xstartup
  
Starting applications specified in /root/.vnc/xstartup
  
Log file is /root/.vnc/localhost.localdomain:1.log
  
如果是非root用户,先用su user命令切换到其它用户再执行上述命令就是设置其它用户的连接密码。

启动该服务来启用vnc的1号窗口
  
systemctl start vncserver@:1.service
  
或者
  
vncserver :1

将其设置为开机自启动
  
systemctl enable vncserver@:1.service

如果要从服务器端关闭连接,执行: 
  
systemctl stop vncserver@:1.service
  
或者
  
vncserver -kill :1

5. 安装VNC viewer: 
  
官方下载vnc viewer的地址: https://www.realvnc.com/download/viewer/windows/

VNC viewer的基本无需额外设置,点击菜单file-> new connection,然后VNC server地址填写格式: IP:5901  (端口号依据上面配置文件设置的序号加上5900即可) 。

上面就是在Digitalocean VPS上安装KDE图形界面和VNC实现远程图像化操作的整个步骤,希望对您有用。这个步骤适用于任何centos 7的VPS,比如vultr、linode、阿里云、腾讯云等热门云主机或VPS。

本文地址: http://digitalocean.youhuima.cc/centos-7-kde-vnc-remote.html

备注: 

查看启用的桌面列表

vncserver -list