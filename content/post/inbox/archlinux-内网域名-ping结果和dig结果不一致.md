---
title: archlinux 内网域名 ping结果和dig结果不一致
author: "-"
date: 2018-03-08T05:26:41+00:00
url: /?p=11977
categories:
  - Inbox
tags:
  - reprint
---
## archlinux 内网域名 ping结果和dig结果不一致

确认/etc/resolv.conf配置是否正确: 没问题；

确认/etc/hosts中是否添加了额外域名: 没问题；

确认域名服务器中正确的内网域名对应的IP,并和同事确认发现内网域名更新过,ping的结果指向了旧的IP,nslookup的解析结果正确；
  
linux服务器本地会有域名缓存以加快域名解析,centos下用的是nscd

ping一般会直接使用缓存的域名,nslookup会直接到域名服务器查询

systemctl restart systemd-resolved
