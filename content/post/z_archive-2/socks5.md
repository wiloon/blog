---
title: 'socks5 -> http/https proxy, privoxy/cow'
author: "-"
date: 2017-02-15T07:23:41+00:00
url: /?p=9815
categories:
  - Inbox
tags:
  - reprint
---
## 'socks5 -> http/https proxy, privoxy/cow'

```bash
curl -L git.io/cow | bash

#edit /home/user0/.cow/rc
  
listen = http://127.0.0.1:7777
  
proxy = socks5://127.0.0.1:1080

#config http/https proxy
  
export http_proxy=http://127.0.0.1:7777
  
export https_proxy=http://127.0.0.1:7777
  
```

sudo pacman -S privoxy

edit /etc/privoxy/config
  
forward-socks5 / 127.0.0.1:1080 .
  
listen-address 127.0.0.1:8118

sudo systemctl start privoxy

* * *

## proxychains

```bash
#Arch Linux
sudo pacman -S proxychains-ng

#Debian/Ubuntu  
apt-get install proxychains

#Mac OS X  
brew install proxychains-ng

# 用户级配置文件
  
编辑~/.proxychains/proxychains.conf:

# 系统级配置文件
vim /etc/proxychains.conf

# content
[ProxyList] 
socks5  192.168.50.205 1080 
http    127.0.0.1 4321
```

### 使用

```bash
proxychains4 git svn rebase
```

strict_chain
  
proxy_dns
  
remote_dns_subnet 224
  
tcp_read_time_out 15000
  
tcp_connect_time_out 8000
  
localnet 127.0.0.0/255.0.0.0
  
quiet_mode

[ProxyList]
  
socks5 127.0.0.1 1080
  
通过 proxychains 运行命令:
  
proxychains4 curl [https://www.twitter.com/](https://www.twitter.com/)
  
proxychains4 git push origin master
  
Or
  
proxychains4 bash
  
curl git push origin master

privoxy 的默认监听端口是8118 (可以在刚在的配置文件里面改listen-address) ,所以直接配置http_proxy和https_proxy即可

[https://program-think.blogspot.com/2014/12/gfw-privoxy.html](https://program-think.blogspot.com/2014/12/gfw-privoxy.html)
  
[https://segmentfault.com/a/1190000002589135](https://segmentfault.com/a/1190000002589135)
  
[http://colobu.com/2017/01/26/how-to-go-get-behind-GFW/](http://colobu.com/2017/01/26/how-to-go-get-behind-GFW/)
  
[https://github.com/cyfdecyf/cow/](https://github.com/cyfdecyf/cow/)

## socks5

socks5 是 SOCKS Protocol Version 5 的缩写，其规范定义于 RFC 1928
SOCKS是"SOCKet Secure"的缩写

[http://zhihan.me/network/2017/09/24/socks5-protocol/](http://zhihan.me/network/2017/09/24/socks5-protocol/)
  
[https://jiajunhuang.com/articles/2019_06_06-socks5.md.html](https://jiajunhuang.com/articles/2019_06_06-socks5.md.html)
  
socks 是一种网络传输协议，主要用于客户端与外网服务器之间通讯的中间传递。根据 OSI 七层模型来划分，SOCKS 属于会话层协议，位于表示层与传输层之间。

当防火墙后的客户端要访问外部的服务器时，就跟socks代理服务器连接。该协议设计之初是为了让有权限的用户可以穿过过防火墙的限制，使得高权限用户可以访问外部资源。经过10余年的时间，大量的网络应用程序都支持socks5代理。

这个协议最初由David Koblas开发，而后由NEC的Ying-Da Lee将其扩展到版本4，最新协议是版本5，与前一版本相比，socks5做了以下增强:

增加对UDP协议的支持；
  
支持多种用户身份验证方式和通信加密方式；
  
修改了socks服务器进行域名解析的方法，使其更加优雅；

### 与 HTTP 代理的对比

* socks支持多种用户身份验证方式和通信加密方式。
* socks工作在比HTTP代理更低的网络层: socks使用握手协议来通知代理软件其客户端试图进行的连接socks，然后尽可能透明地进行操作，而常规代理可能会解释和重写报头 (例如，使用另一种底层协议，例如FTP；然而，HTTP代理只是将HTTP请求转发到所需的HTTP服务器) 。
* socks5代理支持转发UDP报文，而HTTP属于tcp协议，不支持UDP报文的转发。
* 虽然HTTP代理有不同的使用模式，CONNECT方法允许转发TCP连接；然而，socks代理还可以转发UDP流量和反向代理，而HTTP代理不能。HTTP代理更适合HTTP协议，执行更高层次的过滤；socks不管应用层是什么协议，只要是传输层是TCP/UDP协议就可以代理。
