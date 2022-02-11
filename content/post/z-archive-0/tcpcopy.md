---
title: tcpcopy
author: "-"
date: 2022-02-11 00:51:30
url: tcpcopy
categories:
  - network
tags:
  - network
  - remix
  - reprint

---
## tcpcopy

### 环境

- 测试服务器,目标服务器, target server, 192.168.50.101
  - 1025 端口提供服务
- 辅助服务器, assistant server, 192.168.50.102
- 线上服务器, online source server, 192.168.50.10
  - 1025 端口提供服务
- 测试用的tcp服务 tcp-echo-server 监听 1025 端口

### 线上服务器安装 tcpcopy

```bash
git clone https://github.com/session-replay-tools/tcpcopy.git
cd tcpcopy
./configure
make
make install
ls /usr/local/tcpcopy

```

### 辅助服务器安装 intercept

```bash
yum -y install libpcap-devel
git clone https://github.com/session-replay-tools/intercept.git
cd intercept
./configure
make
make install
ls /usr/local/intercept

```

## 实时复制流量

### 测试服务器, 192.168.50.101

测试服务器配置路由，将响应包路由到辅助机

```bash
# 添加一条路由规则
ip route add 192.168.60.0/24 via 192.168.50.102 src 192.168.50.101 dev ens18
# 192.168.60.0/24, tcpcopy修改后的源端地址网段
# via 192.168.50.102: 网关, 下一跳的路由IP, 把响应包目标地址在 192.168.60.0/24 网段的包路由到 辅助机 192.168.50.102
# src 192.168.50.101, 源端地址/测试机地址
# dev ens18, 网卡

# 启动测试服务并监听在 1025 端口
./tcp-echo-server
```

### 辅助服务器, 192.168.50.102

辅助服务器捕获目标机/测试机器发来的响应包

```bash
# ./intercept -F <filter> -i <device,>
./intercept -i ens18 -F 'tcp and src port 1025'
./intercept -i ens18 -F 'tcp and src port 1025' -d
# -i ens18, 捕获网卡 ens18 ，源端口 1025 基于tcp的包, 测试服务运行在 1025 端口, 所以源端口是 1025
# -d, daemon
```

### 线上服务器, 192.168.50.10

线上服务器捕获包 (1025 端口), 并修改目的及源地址, 并把包发送给目标服务器 ( 192.168.50.101 ), 等待辅助服务器(192.168.50.102)发送响应包

源地址会被修改成 192.168.60.x 网段的地址.

```bash
# 线上服务监听在 1025 端口
./tcp-echo-server

# intercept 要先启动, tcpcopy 要连接 intercep的 36524端口
# ./tcpcopy -x localServerPort-targetServerIP:targetServerPort -s <intercept server,> [-c <ip range,>]
./tcpcopy -x 1025-192.168.50.101:1025 -s 192.168.50.102 -c 192.168.60.x
./tcpcopy -x 1025-192.168.50.101:1025 -s 192.168.50.102 -c 192.168.60.x -d
# -x 1025-192.168.50.101:1025, 复制 1025 端口的流量, 发到测试服务器 192.168.50.101:1025
# -s 192.168.50.102, 辅助服务器, 等辅助服务器回包
# -c 192.168.60.x, 修改之后的源端地址网段
# -d, daemon

./tcpcopy -x 1025-192.168.50.101:1025 -s 192.168.50.102 -c 192.168.60.x -d  #全流量复制 
./tcpcopy -x 1025-192.168.50.101:1025 -s 192.168.50.102 -c 192.168.60.x -r 20 -d #复制20%的流量 
./tcpcopy -x 1025-192.168.50.101:1025 -s 192.168.50.102 -c 192.168.60.x -n 2 -d #复制2倍流量

```


### tcpcopy 拷贝一次流量访问的步骤如下

1. 一个客户端请求到达线上机器
2. 拷贝IP层（或者数据链路层）的包到tcpcopy进程
3. tcpcopy修改包的目的及源地址(源地址改成了一个不存在的网段的地址 192.168.60.x, 目标地址改成了目标机/测试机: 192.168.50.101 )，发给目标机/测试机
4. 拷贝的包到达目标测试机
5. 目标机/测试机的应用处理请求，并返回结果给辅助机 (通过路由规则发送到辅助机, 判断 目标地址在 192.168.60.x, 发到辅助机)
6. 返回结果在辅助机的数据链路层被截获，drop 响应的 body，copy 返回的 ip header；
7. 辅助机将响应 header 发送给线上机器的 tcpcopy 进程。

<https://www.cnblogs.com/gnivor/p/12845145.html>  
<https://github.com/session-replay-tools/tcpcopy>  
https://blog.csdn.net/wangbin579/article/details/8949315

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
