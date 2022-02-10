---
title: tcpcopy
author: "-"
date: 2012-03-27T06:16:21+00:00
url: tcpcopy
categories:
  - network
tags:
  - network

---
## tcpcopy

tcpcopy拷贝一次流量访问的步骤如下：

一个客户请求到达线上机器；
拷贝IP层（或者数据链路层）的包到tcpcopy进程；
tcpcopy修改包的目的及源地址，发给目标测试机；
拷贝的包到达目标测试机；
目标测试机的应用处理访问，并返回结果给辅助机；
返回结果在辅助机的数据链路层被截获，drop响应的body，copy返回的ip header；
辅助机将响应header发送给线上机器的tcpcopy进程。

### 环境
- 测试服务器, target server, 61.135.233.160
  - 8080 端口提供服务
- 辅助服务器, assistant server, 61.135.233.161
- 线上服务器, online source server, 61.135.233.162
  - 8080 端口提供服务

### 线上服务器安装tcpcopy
```bash
git clone https://github.com/session-replay-tools/tcpcopy.git
cd tcpcopy
./configure
make
make install
ls /usr/local/tcpcopy

```

### 辅助服务器安装intercept
```bash
git clone https://github.com/session-replay-tools/intercept.git
cd intercept
./configure
make
make install
ls /usr/local/intercept

```

## 实时复制流量

### 线上服务器 61.135.233.162
线上服务器捕获包(80端口)，并修改目的及源地址，并把包发送给目标机器(61.135.233.160)，等待辅助服务器(61.135.233.161)发送响应包

源地址会被修改成 62.135.200.x 网段的地址.

```bash
# ./tcpcopy -x localServerPort-targetServerIP:targetServerPort -s <intercept server,> [-c <ip range,>]
./tcpcopy -x 80-61.135.233.160:8080 -s 61.135.233.161 -c 62.135.200.x
# -x 80-61.135.233.160:8080, 复制 80 端口的流量发到 测试服务器 61.135.233.160:8080
# -s 61.135.233.161, 辅助服务器, 等辅助服务器回包
# -c 62.135.200.x, 修改之后的源端地址网段

/opt/tcpcopy/sbin/tcpcopy -x 18001-10.1.2.3:18001 -s 10.1.2.4  -c 10.1.2.x  -d       #全流量复制 
/opt/tcpcopy/sbin/tcpcopy -x 18001-10.1.2.3:18001 -s 10.1.2.4  -c 10.1.2.x -r 20 -d  #复制20%的流量 
/opt/tcpcopy/sbin/tcpcopy -x 18001-10.1.2.3:18001 -s 10.1.2.4  -c 10.1.2.x -n 2  -d  #复制2倍流量
```

### 测试服务器 61.135.233.160
测试服务器配置路由，将响应包路由到辅助机
```bash
route add -net 62.135.200.0 netmask 255.255.255.0 gw 61.135.233.161
# 把响应包目标地址在 62.135.200.0 网段的包路由到 辅助机 61.135.233.161
# 61.135.233.161 辅助服务器 ip
```

### 辅助服务器 61.135.233.161
辅助服务器捕获目标机器发来的响应包
```bash
# ./intercept -F <filter> -i <device,>
./intercept -i eth0 -F 'tcp and src port 8080' -d
# 捕获网卡 eth0 ，源端口 8080 基于tcp的包, 测试服务运行在8080端口, 所以源端口是8080
```

>https://www.cnblogs.com/gnivor/p/12845145.html
>https://github.com/session-replay-tools/tcpcopy
>https://blog.csdn.net/wangbin579/article/details/8949315


### tcpcopoy
>https://github.com/session-replay-tools/tcpcopy
### goreplay
>https://github.com/buger/goreplay
### tcpcopy 架构漫谈
>https://blog.csdn.net/wangbin579/article/details/8949315
>https://segmentfault.com/a/1190000039285429
>https://github.com/buger/goreplay
### 流量复制方案对比：Tcpcopy vs Goreplay
>https://segmentfault.com/a/1190000039285429


## 流量复制

几款流量复制工具：

gor: https://github.com/buger/goreplay
tcpreplay: https://github.com/appneta/tcpreplay
tcpcopy: https://github.com/session-replay-tools/tcpcopy
Nginx模块ngx_http_mirror_module，在Nginx 1.13.4中开始引入，使用前请检查nginx版本

### goreplay
Goreplay 只能复制http流量 goreplay的pro版支持tcp，每年980刀

### tcpreplay
c 语言实现
https://github.com/appneta/tcpreplay

### tcpcopy
c 语言实现
https://github.com/session-replay-tools/tcpcopy
