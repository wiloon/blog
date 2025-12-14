---
title: netcat
author: "-"
date: 2025-12-05T08:30:00+08:00
url: netcat
categories:
  - Network
tags:
  - reprint
  - remix
  - AI-assisted
---
## netcat

## check if netcat is installed

```bash
# check if netcat is available
which nc

# or try to get the version/help
nc -h

# or check if it's installed via package manager
pacman -Qs netcat
```

## check remote UDP port

```bash
# send UDP packet to remote host and check if port is listening
echo "test" | nc -u -w 1 remote_host port

# use -v for verbose output, -z for scan mode
nc -vuz remote_host port

# if port is closed, you may receive ICMP port unreachable response
# if port is open but service doesn't respond, it's hard to determine the status
```

**参数说明：**

- `-u` : 使用 UDP 协议而不是默认的 TCP
- `-w 1` : 设置超时时间为 1 秒，超时后自动退出
- `-v` : verbose 模式，显示详细的连接信息
- `-z` : 扫描模式，只检查端口是否开放，不发送数据
- `-n` : 不进行 DNS 解析，直接使用 IP 地址

**如何判断 UDP 端口是否在监听：**

```bash
# 方法1: 使用 -v 参数查看详细信息
echo "test" | nc -vu -w 1 remote_host port

# 方法2: 检查命令返回值
echo "test" | nc -u -w 1 remote_host port
echo $?  # 返回 0 通常表示连接成功，非0表示失败

# 方法3: 使用 timeout 和 verbose 模式
timeout 2 nc -vu remote_host port
```

**判断规则：**

- **有明确错误消息**（如 "Connection refused" 或 "port unreachable"）→ 端口**未监听**
- **无任何输出，命令超时退出** → 可能端口**正在监听**，但服务不响应
- **收到响应数据** → 端口**正在监听**且服务正常响应

**最可靠的判断方法：**

1. 使用 `-v` 参数查看详细输出
2. 检查命令的退出码 `$?`
3. 如果可能，向 UDP 服务发送它能识别的特定格式数据

**注意事项：**

- UDP 是无连接协议，没有 TCP 的三次握手过程
- 如果端口开放但服务不响应，无法准确判断端口状态
- 防火墙可能会丢弃 ICMP 错误消息，导致误判
- UDP 端口扫描的可靠性相对较低

## test syslog service

```bash
# syslog 默认使用 UDP 514 端口
# 发送标准 syslog 格式的消息
echo "<134>$(date '+%b %d %H:%M:%S') $(hostname) test: test message" | nc -u -w 1 remote_host 514

# 或者使用更简单的格式
echo "<14>Test syslog message" | nc -u -w 1 remote_host 514

# 使用 logger 命令测试（推荐）
logger -n remote_host -P 514 -p local0.info "test message"

# 使用 nc 的 verbose 模式查看详细信息
echo "<134>Test" | nc -vu -w 1 remote_host 514
```

**syslog 消息格式说明：**

- `<134>` 是优先级（Priority）= Facility * 8 + Severity
  - Facility 16 (local0) * 8 + Severity 6 (info) = 134
- `<14>` = Facility 1 (user) * 8 + Severity 6 (info) = 14

**syslog 服务特点：**

- syslog 通常不会向客户端返回响应
- 如果端口在监听，消息会被接收但没有回应
- 需要在服务端查看日志文件确认消息是否被接收
- 可以使用 `-v` 参数查看连接状态，但无法通过响应判断消息是否被处理

## commands

```Bash
# install gnu-netcat
pacman -S gnu-netcat
# listen on udp port
nc -vv -ul -p 1234
```

NetCat是一个非常简单的Unix工具,可以读、写TCP或UDP网络连接(network connection)。它被设计成一个可靠的后端(back-end) 工具,
通过与其他工具结合和重定向,你可以在脚本中以多种方式使用它。同时,它又是一个功能丰富的网络调试和开发工具,
因为它可以建立你可能用到的几乎任何类型的连接,以及一些非常有意思的内建功能。NetCat,它的实际可运行的名字叫nc
  
NetCat还可以当服务器使用,监听任意指定端口的连接请求(inbound connection),并可做同样的读写操作。除了较小限制外,
它实际并不关心自己以"客户端"模式还是"服务器"模式运行,它都会来回运送全部数据。在任何一种模式下,都可以设置一个非活动时间来强行关闭连接。
它还可以通过UDP来完成这些功能,因此它就象一个telnet那样的UDP程序,用来测试你的UDP服务器。正如它的"U"所指的,
UDP跟TCP相比是一种不可靠的数据传输,一些系统在使用UDP 传送大量数据时会遇到麻烦,但它还有一些用途。

你可能会问"为什么不用telnet来连接任意的端口"？问题提得好(valid),这儿有一些理由。Telnet有"标准输入文件结束符(standard input EOF)"问题,
所以需要在脚本中延迟计算以便等待网络输出结束。这就是netcat持续运行直到连接被关闭的主要原因。Telnet也不能传输任意的二进制数据,
因为一些特定的字符会被解释为Telnet的参数而被从数据流中去除。Telnet还将它的一些诊断信息显示到标准输出上,
而NC会将这信息与它的输出分开以不改变真实数据的传输,除非你要求它这么做。当然了,Telnet也不能监听端口,也不能使用UDP。 
NC没有这些限制,比Telnet更小巧和快捷,而且还有一些其它的功能。

NC所做的就是在两台电脑之间建立链接并返回两个数据流,在这之后所能做的事就看你的想像力了。你能建立一个服务器,传输文件,
与朋友聊天,传输流媒体或者用它作为其它协议的独立客户端。

传输文本信息

首先需要其中一台服务器打开一个端口,然后进行tcp连接,第一台服务器去侦听某个端口时使用nc -l 通过-p指定端口号,客户端:nc -nv 1.1.1.1 4444

```bash
  
nc -l -p 3333 {开通3333端口}
  
netstat -pantu | grep 3333 {查看3333端口是否已经开通}
  
nc -nv 192.168.14.23 333
  
```

http://www.jianshu.com/p/af6766e428ec