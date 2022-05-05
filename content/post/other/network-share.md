---
title: Windows 共享网络设置 (有线网络和无线网络）
author: "-"
date: 2014-01-01T08:06:12+00:00
url: /?p=6089
categories:
  - windows

tags:
  - reprint
---
## Windows 共享网络设置 (有线网络和无线网络）

有线共享网络

1. 打开连接Internet的“本地连接 属性”窗口，切换到“共享”标签页

2. 在“共享”标签页中，勾选“允许其他网络用户通过此计算机的Internet连接来连接”，确定；如果网络连接中超过两个连接，则还需要选择需要共享的连接

3.打开另一个需要共享的连接的“本地连接 属性”窗口，选择“Internet 协议版本4 (TCP/IPV4）属性”，设置静态IP，这里的设置的IP网段应避开连接Internet的网段，否则易造成IP冲突等问题



这样配置后，这个网卡就想当于共享网络的网关，其他要共享此连接的电脑只需要设置将IP地址配置成同一网段与上述不同即可 (如192.168.71.2），其余配置不变

无线共享网络

无线共享在双网卡的情况下，用于共享需要是无线网卡，这里可以采用与上述相同的方式进行无线网络共享；当然也可使用如360出的免费360wifi，可以不用进行配置



如果进行上述配置后，各连接正常，但是无法访问Internet，则是由于Internet Connection Sharing(ICS)服务未启动。

右键“我的电脑”-》管理-》服务和应用程序-》服务-》双击Internet Connection Sharing(ICS)-》启动

双击Internet Connection Sharing(ICS)状态栏显示“已启动”即可
————————————————
版权声明：本文为CSDN博主「小蜗coding」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/acsder2010413/article/details/40395621

