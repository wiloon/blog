---
title: linux http proxy
author: "-"
date: 2012-01-18T06:33:02+00:00
url: /?p=2151
categories:
  - Linux
  - Network

tags:
  - reprint
---
## linux http proxy

在Linux的命令行底下，一般的程序都是使用http_proxy和ftp_proxy这两个环境变量来获得代理设置的。
```bash
  
export http_proxy=http://localhost:8118/

# 需要密码的代理服务器
export http_proxy=http://username:password@proxyserver:port/
export ftp_proxy=http://username:password@proxyserver:port/

unset http_proxy
  
unset https_proxy
  
unset ftp_proxy
  
```

export no_proxy="localhost,127.0.0.0/8,*.local"

例如，假设你的代理服务器为192.168.1.1，端口是8080，用户名为cnkker，密码是123456，那么应该这样设置这两个环境变量: 

export http_proxy=http://cnkker:123456@192.168.1.1:8080
  
export ftp_proxy=http://cnkker:123456@192.168.1.1:8080

如果要使下次生效，需要把导出配置写入~/.bashrc中，这样配置之后，退出再登录一次，或者直接使用下面的命令source一下.bashrc: 
  
source ~/.bashrc
  
现在，上述程序就可以通过代理服务器访问网络了。