---
title: FQDN
author: "-"
date: 2018-07-03T12:08:46+00:00
url: /?p=12391
categories:
  - Inbox
tags:
  - reprint
---
## FQDN
https://blog.csdn.net/u012842205/article/details/51931017
  
FQDN是完全合格域名/全程域名缩写,Fully Qualified Domain Name,即是域名,访问时将由DNS进行解析,得到IP。

FQDN = Hostname + DomainName

当我们申请了一个域名时,就可以使用这个域名来得到IP,但若这个域名下挂在很多主机如何？我是不是得申请很多很多域名给每个主机？不需要,域名即创建了一个域,就如命名空间,在这个命名空间下,其他主机都可以创建自己的名称。这个名称就是通过以上公式得来。

举个例子,一个公司申请了域名comp.com,这时候有一台主机名为web,则可以使用web.comp.com得到这个主机IP。若还有两台提供邮件和OA服务的主机cmail,oa,则这时候可以用以下FQDN: 

cmail.comp.com

oa.comp.com

类似例子也在安装linux系统时,很多时候我们安装Ubuntu,Debian或Kali时,会需要你填写一个域,这个域即是你自己的,只是没有注册,且只能在本地网络使用。

Linux下查看方式: 

hostname, 查看主机名

hostname -f 查看FQDN

dnsdomainname 查看域

uname -h 查看主机名

注: 主机名作为一个网络节点的标示。