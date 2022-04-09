---
title: 'socks5 -> http/https proxy, privoxy/cow'
author: "-"
date: 2017-02-15T07:23:41+00:00
url: /?p=9815
categories:
  - Uncategorized

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

---

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
  
proxychains4 curl https://www.twitter.com/
  
proxychains4 git push origin master
  
Or
  
proxychains4 bash
  
curl git push origin master

privoxy 的默认监听端口是8118 (可以在刚在的配置文件里面改listen-address) ,所以直接配置http_proxy和https_proxy即可

https://program-think.blogspot.com/2014/12/gfw-privoxy.html
  
https://segmentfault.com/a/1190000002589135
  
http://colobu.com/2017/01/26/how-to-go-get-behind-GFW/
  
https://github.com/cyfdecyf/cow/