---
title: docker 网络
author: "-"
date: 2020-04-19T04:48:45+00:00
url: /?p=15990
categories:
  - Uncategorized

tags:
  - reprint
---
## docker 网络
安装 Docker 时，它会自动创建 3 个网络。可以使用 docker network ls 命令列出这些网络。

$ docker network ls
  
NETWORK ID NAME DRIVER
  
7fca4eb8c647 bridge bridge
  
9f904ee27bf5 none null
  
cf03ee007fb4 host host

运行一个容器时，可以使用 the -net 标志指定您希望在哪个网络上运行该容器。

bridge 网络表示所有 Docker 安装中都存在的 docker0 网络。除非使用 docker run -net=<NETWORK>选项另行指定，否则 Docker 守护进程默认情况下会将容器连接到此网络。在主机上使用 ifconfig命令，可以看到此网桥是主机的网络堆栈的一部分。
  
none 网络在一个特定于容器的网络堆栈上添加了一个容器。该容器缺少网络接口。
  
host 网络在主机网络堆栈上添加一个容器。您可以发现，容器中的网络配置与主机相同。
  
用户定义的网络
  
您可以创建自己的用户定义网络来更好地隔离容器。Docker 提供了一些默认网络驱动程序来创建这些网络。您可以创建一个新 bridge 网络或覆盖一个网络。也可以创建一个网络插件或远程网络并写入您自己的规范中。
  
您可以创建多个网络。可以将容器添加到多个网络。容器仅能在网络内通信，不能跨网络进行通信。一个连接到两个网络的容器可与每个网络中的成员容器进行通信。当一个容器连接到多个网络时，外部连接通过第一个 (按词典顺序) 非内部网络提供。