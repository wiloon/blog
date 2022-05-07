---
title: 内网 dns dig 能解析出ip, ping 返回 Name or service not known
author: "-"
date: 2018-05-08T08:15:32+00:00
url: /?p=12217
categories:
  - Inbox
tags:
  - reprint
---
## 内网 dns dig 能解析出ip, ping 返回 Name or service not known
https://blog.csdn.net/jinyuxiaoqiang/article/details/78611430
  
https://blog.csdn.net/water_cow/article/details/7190880

vim /etc/nsswitch.conf

# hosts: files mymachines myhostname resolve [!UNAVAIL=return] dns

hosts: files dns myhostname