---
title: 'resolv.conf,search、domain、nameserver'
author: "-"
date: 2018-09-25T09:53:24+00:00
url: /?p=12701
categories:
  - Inbox
tags:
  - reprint
---
## 'resolv.conf,search、domain、nameserver'

<http://www.ttlsa.com/linux/resolv-conf-desc/>
  
resolv.conf是resolver类库使用的配置文件,每当一个程序需要通过域名来访问internet上面的其它主机时,需要利用该类库将域名转换成对应的IP,然后才可进行访问.

resolv.conf文件的配置选项不多,从man文档中看了半天,不理解domain和search使用来干嘛的。这里做个解释,防止以后忘了 (环境: ubuntu12.04) :

nameserver x.x.x.x该选项用来制定DNS服务器的,可以配置多个nameserver指定多个DNS。

domain mydomain.com这个用来指定本地的域名,在没有设置search的情况下,search默认为domain的值。这个值可以随便配,目前在我看来,domain除了当search的默认值外,没有其它用途。也就说一旦配置search,那domain就没用了。

search google.com baidu.com该选项可以用来指定多个域名,中间用空格或tab键隔开。它是干嘛的呢？

如: 在没有配置该选项时,执行

ping new
  
sping: unknown host news

ping new
  
sping: unknown host news
  
配置search google.com baidu.com后,再执行

ping news
  
PING news.google.com (74.125.128.101) 56(84) bytes of data.
  
64 bytes from hg-in-f101.1e100.net (74.125.128.101): icmp_req=1 ttl=47 time=78.9 ms
  
64 bytes from hg-in-f101.1e100.net (74.125.128.101): icmp_req=2 ttl=47 time=63.6 ms

ping news
  
PING news.google.com (74.125.128.101) 56(84) bytes of data.
  
64 bytes from hg-in-f101.1e100.net (74.125.128.101): icmp_req=1 ttl=47 time=78.9 ms
  
64 bytes from hg-in-f101.1e100.net (74.125.128.101): icmp_req=2 ttl=47 time=63.6 ms
  
它就去ping news.google.com了。原来当访问的域名不能被DNS解析时,resolver会将该域名加上search指定的参数,重新请求DNS,直到被正确解析或试完search指定的列表为止。

由于news不能被DNS解析,所以去尝试news.google.com,被正常解析。如果没有被解析还会去尝试news.baidu.com。

· /etc/resolv.conf : 这个就是设定你 Client 端连上 DNS 主机的 IP 设定文件；
  
· /etc/nsswitch.conf: 这个档案则是在『决定』先要使用 /etc/hosts 还是 /etc/resolv.conf的设定！
  
<https://www.jianshu.com/p/2c1c081cc521>

## /etc/hosts

```bash
IPAddress     Hostname          Alias
127.0.0.1     localhost         deep.openna.com
208.164.186.1 deep.openna.com   deep
208.164.186.2 mail.openna.com   mail
208.164.186.3 web.openna.com    web

```
