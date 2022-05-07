---
title: dns ttl
author: "-"
date: 2018-11-24T11:27:20+00:00
url: /?p=12924
categories:
  - Inbox
tags:
  - reprint
---
## dns ttl
https://jaminzhang.github.io/dns/DNS-TTL-Understanding-and-Config/

DNS TTL 值理解及配置

我们有配置域名时,不同情况下,不同业务下,需要增大或减小 DNS TTL 值。这是为什么呢？ 这需要我们重新理解下 DNS TTL 值的含义。

什么是域名的 TTL 值
  
TTL(Time-To-Live),就是一条域名解析记录在 DNS 服务器中的存留时间。
  
当各地的 DNS 服务器接受到解析请求时,就会向域名指定的 NS 服务器发出解析请求从而获得解析记录；
  
在获得这个记录之后,记录会在 DNS 服务器中保存一段时间,这段时间内如果再接到这个域名的解析请求,
  
DNS 服务器将不再向 NS 服务器发出请求,而是直接返回刚才获得的记录；
  
而这个记录在 DNS 服务器上保留的时间,就是 TTL 值。