---
title: hyper -v 端口映射
author: "-"
date: 2019-05-05T04:30:41+00:00
url: /?p=14286
categories:
  - Inbox
tags:
  - reprint
---
## hyper -v 端口映射

[https://www.cnblogs.com/cnxkey/articles/7815434.html](https://www.cnblogs.com/cnxkey/articles/7815434.html)

hyper -v 如何实现端口映射
  
如果你是想由虚拟机来提供相应的服务，比如虚拟机里安装web服务，将物理主机的web端口映射到虚拟机，可以使用如下命令进行设置即可，我已经成功了。
  
一、查询端口映射情况
  
netsh interface portproxy show v4tov4
  
查询这个IP所有的端口映射。
  
netsh interface portproxy show v4tov4|find "192.168.1.1"
  
二、增加一个端口映射
  
netsh interface portproxy add v4tov4 listenport=外网端口 listenaddress=主IP connectaddress=私网IP connectport=私网IP端口
  
例如:
  
netsh interface portproxy add v4tov4 listenport=8888 listenaddress=118.123.13.180 connectaddress=192.168.1.10 connectport=2222
  
三、删除一个端口映射
  
netsh interface portproxy delete v4tov4 listenaddress=主IP listenport=外网端口
  
例如:
  
netsh interface portproxy delete v4tov4 listenaddress=118.123.13.180 listenport=8888

在关闭Hyper-V虚拟机的情况下，选择Hyper-V管理界面中的"虚拟交换机管理器"
  
在弹出的对话框中"新建虚拟网络交换机"，选择"内部"，点击"创建虚拟交换机"。
  
在IP网卡 切换到"共享"标签下，勾选"允许其他网络用户通过此计算机的Internet连接来连接"并在下方"家庭网络连接"中选择刚刚创建的虚拟交换机——vEthernet (Hyper-V Switch)，点击"确认
