---
title: 'dns tool, dig/drill, dnsutils to ldns dig -> dirll'
author: "-"
date: 2016-07-12T05:16:26+00:00
url: /?p=9125
categories:
  - Inbox
tags:
  - reprint
---
## 'dns tool, dig/drill, dnsutils to ldns dig -> dirll'
```bash
# install dig
## archlinux
sudo pacman -S ldns

## cenos
yum install bind-utils

# install drill
#ubuntu
sudo apt install ldnsutils
#alpine
apk add drill

dig +trace wiloon.com
dirll -T wiloon.com

drill wiloon.com @192.168.50.1
drill wangyue.dev NS
```

dig,其实是一个缩写,即Domain Information Groper。

dig @8.8.8.8 www.baidu.com A //命令格式为dig @dnsserver name querytype

https://www.archlinux.org/todo/dnsutils-to-ldns-migration/

http://imdjh.github.io/toolchain/2015/10/07/drill-if-you-can-dig-if-you-have-to.html

We are removing dnsutils from [core]. (It cannot be built independently from bind anymore, and the whole thing is becoming a mess anyhow.)

Please update your packages to depend on ldns instead (already in [core]).

While dnsutils provided three similar DNS query tools (dig, host, nslookup), ldns provides drill, a near-drop-in replacement for dig (which can therefore easily replace host and nslookup too). To update, you must replace all calls to dig/host/nslookup in your packages to calls to drill. Simple calls such as `dig archlinux.org` can simply be rewritten as `drill archlinux.org`; see `drill -h` for more details and please contact me if you cannot figure out how to migrate.


  
    《dig挖出DNS的秘密》-linux命令五分钟系列之三十四
  


http://roclinux.cn/?p=2449&embed=true#?secret=9AchPRSDEE