---
title: test for a specific port from Linux,  shell>telnet  >netcat > Socat
author: "-"
date: 2017-12-16T06:59:25+00:00
url: /?p=11601
categories:
  - Inbox
tags:
  - reprint
---
## test for a specific port from Linux,  shell>telnet> netcat> socat

### 使用 Telnet验证端口的连通性

打开命令行模式。具体方法,请参考打开命令或 Shell 提示符 (2076587) (Opening a command or shell prompt (1003892))。
  
在命令行窗口键入:

```bash
# telnet server port
telnet 192.168.50.1 22
```

其中 server 是服务器的主机名或IP地址,port 是您想要连接的端口号。

按回车。
  
注: 要离开 Telnet 应用程序,请键入 Ctrl + ],然后键入 quit。

<https://kb.vmware.com/s/article/2020963>

### socat

```bash
# test tcp port
socat - TCP4:192.168.1.15:22,connect-timeout=2

# test udp port
#set up a server listening on UDP port 48772
socat UDP-RECV:48772 STDOUT

# test udp port
socat - UDP:localhost:48772
```

## shell

```bash
echo >/dev/tcp/192.168.1.15/22

```

## nc

telnet 只能测试 tcp端口, 测试udp端口需要用nc

```bash
# centos
yum install nc

nc -lvu 0.0.0.0  124
nc -vuz host 124
```

<http://www.oschina.net/news/48357/socat-1-7-2-3>

socat是一個netcat(nc)的替代產品,可以稱得上nc++。socat的特點就是在兩個流之間建立一個雙向的 通道。socat的地址類型很 多,有ip, tcp, udp, ipv6, pipe,exec,system,open,proxy,openssl,等等

<http://blog.csdn.net/zhu_xun/article/details/16885333>

Telnet有"标准输入文件结束符(standard input EOF)"问题,
  
所以需要在脚本中延迟计算以便等待网络输出结束。这就是netcat持续运行直
  
到连接被关闭的主要原因。Telnet也不能传输任意的二进制数据,因为一些特
  
定的字符会被解释为Telnet的参数而被从数据流中去除。Telnet还将它的一些
  
诊断信息显示到标准输出上,而NetCat会将这信息与它的输出分开以不改变真
  
实数据的传输,除非你要求它这么做。当然了,Telnet也不能监听端口,也不
  
能使用UDP。 NetCat没有这些限制,比Telnet更小巧和快捷,而且还有一些其
  
它的功能。

NetCat的一些主要功能:

*支持连出和连入(outbound and inbound connection),TCP和UDP,任意源和目的端口
  
*全部DNS正向/反向检查,给出恰当的警告
  
*使用任何源端口
  
*使用任何本地设置的网络资源地址
  
*内建端口扫描功能,带有随机数发生器
  
*内建loose source-routing功能
  
*可能标准输入读取命令行参数
  
*慢发送模式,每N秒发送一行
  
*以16进制显示传送或接收的数据
  
*允许其它程序服务建立连接,可选
  
*对Telnet应答,可选

Use Netcat - not Telnet - to test network connectivity
  
<http://www.terminalinflection.com/use-netcat-not-telnet-to-test-network-connectivity/embed/#?secret=xAPNTA4aj2>

Stop using telnet and start using netcat
  
<https://scottlinux.com/2013/12/19/stop-using-telnet-and-start-using-netcat/embed/#?secret=mR1NgJH6y2>
  
<https://stackoverflow.com/questions/47844060/how-to-test-a-remote-port-is-reachable-with-socat>
