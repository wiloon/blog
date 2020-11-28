---
title: systemd 添加开机启动运行shell脚本
author: w1100n
type: post
date: 2019-01-01T03:05:58+00:00
url: /?p=13278
categories:
  - Uncategorized

---
http://lxiaogao.lofter.com/post/1cc6a101_62292d3

systemd 添加开机启动运行shell脚本
  
1.首先在/etc/systemd/systemd/下新建一个开机启动服务名为cs.service
  
格式如下

* * *

[Unit]

Description=test shell ------->开机启动会打印【ok】 started test shell

[Service]

ExecStart=/bin/sh /home/root/cs.sh ------->你要开机运行的脚本必须绝对位置 /bin/sh 为shell解释器不能省

[Install]

WantedBy=multi-user.target

Requires=pulseaudio.service -------->你要安排在哪个服务后面才启动（如依赖的服务）

After=pulseaudio.service --------->你要安排在哪个服务后面才启动（如依赖的服务）

* * *

2.写好之后 敲入 #systemctl enable cs.service 将它添加到开机启动

注 脚本里的命令也必须是写绝对路径！！！！！！！！！！！！！！！