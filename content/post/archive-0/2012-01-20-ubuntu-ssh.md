---
title: ubuntu ssh
author: wiloon
type: post
date: 2012-01-20T01:37:12+00:00
url: /?p=2162
categories:
  - Linux

---
sudo apt-get install openssh-server

Ubuntu缺省安装了openssh-client,所以在这里就不安装了，如果你的系统没有安装的话，再用apt-get安装上即可。
  
然后确认sshserver是否启动了：

ps -e |grep ssh

如果只有ssh-agent那ssh-server还没有启动，需要/etc/init.d/ssh start，如果看到sshd那说明ssh-server已经启动了。

ssh-server配置文件位于/ etc/ssh/sshd_config，在这里可以定义SSH的服务端口，默认端口是22，你可以自己定义成其他端口号，如222。然后重启SSH服务：

sudo /etc/init.d/ssh resar