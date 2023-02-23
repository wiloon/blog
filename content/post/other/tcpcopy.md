---
title: tcpcopy, 流量复制
author: "-"
date: 2022-02-11 00:51:30
url: tcpcopy
categories:
  - network
tags:
  - remix
  - reprint

---
## tcpcopy, 流量复制

## 公有云环境

<https://github.com/session-replay-tools/tcpcopy/issues/336>

云环境下，安全策略可能会干扰测试的进行
采用如下步骤可以规避麻烦：

1. 测试机器和 intercept 部署到一台机器
2. tcpcopy端 -c 参数采用 tcpcopy 所在的线上机器ip地址
3. 在线上机器设置iptables黑洞来过滤掉测试服务器的响应包 `iptables -I INPUT -p tcp --sport 测试服务的端口 -j DROP -s` 测试服务所在机器的ip地址
4. 千万要注意在测试服务器不要设置路由了，否则会受到干扰

### 环境

- 测试用的 tcp 服务 tcp-echo-server
- 线上服务器, online source server, xxx.xxx.20.50
  - 2000 端口提供服务 (tcp-echo-server)
- 测试服务器, 目标服务器, target server, xxx.xxx.20.45， 192.168.50.102
  - 3000 端口提供服务 (tcp-echo-server), 不能跟 online server 用同一个端口
- 辅助服务器, assistant server,  xxx.xxx.20.45, intercept 跟测试服务部署到同一个机器, 不使用单独的服务器

### 线上服务器安装 tcpcopy

```bash
git clone https://github.com/session-replay-tools/tcpcopy.git
cd tcpcopy
./configure --single
make
make install
ls /usr/local/tcpcopy

```

### 辅助服务器 (intercept) 安装

```bash

git clone https://github.com/session-replay-tools/intercept.git
cd intercept
./configure --single
make
make install
ls /usr/local/intercept
```

### 实时复制流量

### 测试服务器 192.168.50.102

测试服务器不添加路由规则.

```bash
# 启动测试服务并监听在 3000 端口
./tcp-echo-server -log-console=true -log-file=false -log-level=info -port=3000
```

### 辅助服务器 192.168.50.102

辅助服务器捕获`目标机/测试机`器发出的响应包

```bash
# ./intercept -F <filter> -i <device,>
/usr/local/intercept/sbin/intercept -i eth0 -F 'tcp and src port 3000'
/usr/local/intercept/sbin/intercept -i eth0 -F 'tcp and src port 3000' -d

/usr/local/intercept/sbin/intercept -i ens18 -F 'tcp and src port 3000'

# -i eth0, 捕获网卡 eth0 ，基于 tcp 的, 源端口是 3000 的包, 测试服务运行在 3000 端口, 所以源端口是 3000
# -d, daemon
```

### 线上服务器，192.168.50.101

线上服务器捕获包 (2000 端口), 并修改目的及源地址, 把包发送给目标服务器, 然后等待辅助服务器发送响应包

源地址使用 线上服务器 IP

```bash
# 线上服务监听在 2000 端口
./tcp-echo-server -log-console=true -log-file=false -log-level=info -port=2000

# intercept 要先启动, tcpcopy 要连接 intercep 的 36524 端口
# ./tcpcopy -x localServerPort-targetServerIP:targetServerPort -s <intercept server,> [-c <ip range,>]
/usr/local/tcpcopy/sbin/tcpcopy -x 2000-xxx.xxx.20.45:3000 -s xxx.xxx.20.45 -c xxx.xxx.20.50
/usr/local/tcpcopy/sbin/tcpcopy -x 2000-xxx.xxx.20.45:3000 -s xxx.xxx.20.45 -c xxx.xxx.20.50 -d
# -x 2000-xxx.xxx.20.45:3000, 复制 2000 端口的 tcp 流量, 发到测试服务器 xxx.xxx.20.45:3000
# -s xxx.xxx.20.45, 辅助服务器, 等辅助服务器回包
# -c xxx.xxx.20.50, 修改之后的源端地址
# -d, daemon

# 新建 iptables 规则, 抛掉测试服务器的回包
iptables -I INPUT -p tcp --sport 3000 -j DROP -s xxx.xxx.20.45

/usr/local/tcpcopy/sbin/tcpcopy -x 2000-192.168.50.102:3000 -s 192.168.50.102 -c 192.168.50.101
sudo iptables -I INPUT -p tcp --sport 3000 -j DROP -s 192.168.50.102

#./tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -d  #全流量复制 
#./tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -r 20 -d #复制20%的流量 
#./tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -n 2 -d #复制2倍流量

```

## 常规环境

### 环境

1. 测试用的 tcp 服务 tcp-echo-server 监听 2000 端口
2. 线上服务器, online source server, 192.168.50.101

- 2000 端口提供服务 (tcp-echo-server)

3. 测试服务器, 目标服务器, target server, 192.168.50.102

- 2000 端口提供服务 (tcp-echo-server)

4. 辅助服务器, assistant server, 192.168.50.103

### 线上服务器安装 tcpcopy

```bash
git clone https://github.com/session-replay-tools/tcpcopy.git
cd tcpcopy
./configure
make
make install
ls /usr/local/tcpcopy
```

### 辅助服务器 (intercept) 安装

```bash
git clone https://github.com/session-replay-tools/intercept.git
cd intercept
./configure
make
make install
ls /usr/local/intercept
```

### 实时复制流量

### 测试服务器, 192.168.50.102

测试服务器添加一条路由规则，将响应包路由到辅助机

```bash
# 添加一条路由规则
ip route add 192.168.60.0/24 via 192.168.50.103 src 192.168.50.102 dev ens18
# 192.168.60.0/24, tcpcopy 修改后的源端地址网段 (一个不存在的网段, 不会影响生产环境的数据)
# via 192.168.50.103: 网关, 下一跳的路由IP, 辅助服务器的地址, 把响应包目标地址在 192.168.60.0/24 网段的包路由到 辅助机 192.168.50.103
# src 192.168.50.102, 源端地址/测试服务器的地址
# dev ens18, 网卡

# 启动测试服务并监听在 2000 端口
./tcp-echo-server
```

### 辅助服务器, 192.168.50.103

辅助服务器捕获 `目标机/测试机` 器发来的响应包

```bash
# run intercept
# ./intercept -F <filter> -i <device,>
/usr/local/intercept/sbin/intercept -i ens18 -F 'tcp and src port 2000'
/usr/local/intercept/sbin/intercept -i ens18 -F 'tcp and src port 2000' -d
# -i ens18, 捕获网卡 ens18 ，源端口 2000 基于tcp 的包, 测试服务运行在 2000 端口, 所以源端口是 2000
# -d, daemon
```

### 线上服务器, 192.168.50.101

线上服务器捕获包 (2000 端口), 并修改目的及源地址, 然后发送给目标服务器 ( 192.168.50.102 ), 等待辅助服务器 (192.168.50.102) 发送响应包

源地址会被修改成 192.168.60.x 网段的地址.

```bash
# 线上服务监听在 2000 端口
./tcp-echo-server

# intercept 要先启动, tcpcopy 要连接 intercep的 36524端口
# ./tcpcopy -x localServerPort-targetServerIP:targetServerPort -s <intercept server,> [-c <ip range,>]
/usr/local/tcpcopy/sbin/tcpcopy -x 2000-192.168.50.102:2000 -s 192.168.50.103 -c 192.168.60.x
/usr/local/tcpcopy/sbin/tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -d
# -x 2000-192.168.50.102:2000, 复制 2000 端口的 tcp 流量, 发到测试服务器 192.168.50.102:2000
# -s 192.168.50.102, 辅助服务器, 等辅助服务器回包
# -c 192.168.60.x, 修改之后的源端地址网段
# -d, daemon

./tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -d  #全流量复制 
./tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -r 20 -d #复制20%的流量 
./tcpcopy -x 2000-192.168.50.101:2000 -s 192.168.50.102 -c 192.168.60.x -n 2 -d #复制2倍流量

```

### tcpcopy 拷贝一次流量访问的步骤如下

1. 一个客户端请求到达线上机器
2. 拷贝 IP 层 (或者数据链路层）的包到 tcpcopy 进程
3. tcpcopy 修改包的目的及源地址 (源地址改成了一个不存在的网段的地址 192.168.60.x, 目标地址改成了目标机/测试机: 192.168.50.101 )，发给目标机/测试机
4. 拷贝的包到达目标测试机
5. 目标机/测试机的应用处理请求，并返回结果给辅助机 (通过路由规则发送到辅助机, 判断 目标地址在 192.168.60.x, 发到辅助机)
6. 返回结果在辅助机的数据链路层被截获，drop 响应的 body，copy 返回的 ip header；
7. 辅助机将响应 header 发送给线上机器的 tcpcopy 进程。

<https://www.cnblogs.com/gnivor/p/12845145.html>  
<https://github.com/session-replay-tools/tcpcopy>  
<https://blog.csdn.net/wangbin579/article/details/8949315>

### tcpcopoy

><https://github.com/session-replay-tools/tcpcopy>

### goreplay

><https://github.com/buger/goreplay>

### tcpcopy 架构漫谈

><https://blog.csdn.net/wangbin579/article/details/8949315>
><https://segmentfault.com/a/1190000039285429>
><https://github.com/buger/goreplay>

### 流量复制方案对比：Tcpcopy vs Goreplay

><https://segmentfault.com/a/1190000039285429>

## 其它工具

几款流量复制工具：

gor: <https://github.com/buger/goreplay>
tcpreplay: <https://github.com/appneta/tcpreplay>
tcpcopy: <https://github.com/session-replay-tools/tcpcopy>
Nginx模块ngx_http_mirror_module，在Nginx 1.13.4中开始引入，使用前请检查nginx版本

### goreplay

Goreplay 只能复制http流量 goreplay的pro版支持tcp，每年980刀

### tcpreplay

c 语言实现
<https://github.com/appneta/tcpreplay>

### tcpcopy

c 语言实现
<https://github.com/session-replay-tools/tcpcopy>

<https://winway.github.io/2017/10/17/tcpcopy-introduce/>
