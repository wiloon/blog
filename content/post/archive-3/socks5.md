---
title: socks5
author: "-"
date: 2020-02-23T15:36:05+00:00
url: /?p=15619
categories:
  - Uncategorized

tags:
  - reprint
---
## socks5
socks5 是 SOCKS Protocol Version 5 的缩写，其规范定义于 RFC 1928
SOCKS是"SOCKet Secure"的缩写

http://zhihan.me/network/2017/09/24/socks5-protocol/
  
https://jiajunhuang.com/articles/2019_06_06-socks5.md.html
  
socks 是一种网络传输协议，主要用于客户端与外网服务器之间通讯的中间传递。根据 OSI 七层模型来划分，SOCKS 属于会话层协议，位于表示层与传输层之间。

当防火墙后的客户端要访问外部的服务器时，就跟socks代理服务器连接。该协议设计之初是为了让有权限的用户可以穿过过防火墙的限制，使得高权限用户可以访问外部资源。经过10余年的时间，大量的网络应用程序都支持socks5代理。

这个协议最初由David Koblas开发，而后由NEC的Ying-Da Lee将其扩展到版本4，最新协议是版本5，与前一版本相比，socks5做了以下增强: 

增加对UDP协议的支持；
  
支持多种用户身份验证方式和通信加密方式；
  
修改了socks服务器进行域名解析的方法，使其更加优雅；

### 与HTTP代理的对比

  * socks支持多种用户身份验证方式和通信加密方式。
  * socks工作在比HTTP代理更低的网络层: socks使用握手协议来通知代理软件其客户端试图进行的连接socks，然后尽可能透明地进行操作，而常规代理可能会解释和重写报头 (例如，使用另一种底层协议，例如FTP；然而，HTTP代理只是将HTTP请求转发到所需的HTTP服务器) 。
  * socks5代理支持转发UDP报文，而HTTP属于tcp协议，不支持UDP报文的转发。
  * 虽然HTTP代理有不同的使用模式，CONNECT方法允许转发TCP连接；然而，socks代理还可以转发UDP流量和反向代理，而HTTP代理不能。HTTP代理更适合HTTP协议，执行更高层次的过滤；socks不管应用层是什么协议，只要是传输层是TCP/UDP协议就可以代理。