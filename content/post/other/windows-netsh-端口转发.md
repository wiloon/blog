---
title: windows netsh 端口转发
author: "-"
date: 2015-06-13T04:55:12+00:00
url: /?p=7813
categories:
  - Inbox
tags:
  - Network

---
## windows netsh 端口转发

[http://aofengblog.blog.163.com/blog/static/631702120148573851740/](http://aofengblog.blog.163.com/blog/static/631702120148573851740/)

在windows上用netsh动态配置端口转发

下载LOFTER客户端

使用多个虚拟机，将开发环境和工作沟通环境分开 (即时通，办公系统都只能在windows下使用…) ，将开发环境的服务提供给外部访问时，需要在主机上通过代理配置数据转发。

VirtualBox提供了端口转发的功能，可以将主机中的端口转发至指定IP的虚拟机中的端口，支持TCP协议和UDP协议。但有一个缺点: 需要重启虚拟主机才生效。

其实在Windows中，如果想做端口转发，可以使用Windows自身携带的服务:netsh，使用netsh interface portproxy指令，新增和修改配置信息后，即时生效，并且重启系统后配置信息仍然存在，非常方便。适用于WindowsXP、Windows7，其他的版本还没有试过，支持IPv4和IPv6，但是只支持TCP协议。
  
新增端口转发
  
1. 命令
  
netsh interface portproxy add v4tov4 - 添加通过 IPv4 的 IPv4 和代理连接到的侦听项目。
  
netsh interface portproxy add v4tov6 - 添加通过 IPv6 的 IPv4 和代理连接到的侦听项目。
  
netsh interface portproxy add v6tov4 - 添加通过 IPv4 的 IPv6 和代理连接到的侦听项目。
  
netsh interface portproxy add v6tov6 - 添加通过 IPv6 的 IPv6 和代理连接到的侦听项目。
  
2. 命令语法
  
以netsh interface portproxy add v4tov4为例，其语法格式如下:

netsh interface portproxy add v4tov4 [listenport=]<integer>|<servicename>
  
[connectaddress=]<IPv4 address>|<hostname>
  
[[connectport=]<integer>|<servicename>]
  
[[listenaddress=]<IPv4 address>|<hostname>]
  
[[protocol=]tcp]

参数:
  
标记            值
  
listenport      - IPv4 侦听端口。
  
connectaddress  - IPv4 连接地址。
  
connectport     - IPv4 连接端口。
  
listenaddress   - IPv4 侦听地址。
  
protocol        - 使用的协议。现在只支持 TCP。
  
说明: 添加通过 IPv4 的 IPv4 和代理连接到的侦听项目。
  
3. 使用示例
  
netsh interface portproxy add v4tov4 listenport=8080 connectaddress=192.168.56.101 connectport=8080
  
将本地的8080端口的数据转发至192.168.56.101上的8080端口。

netsh interface portproxy add v4tov4 listenport=9090 connectaddress=192.168.56.101 connectport=9090
  
将本地的9090端口的数据转发至192.168.56.101上的9090端口。
  
显示所有的端口转发配置信息
  
1. 命令
  
netsh interface portproxy show all - 显示所有端口代理参数。
  
netsh interface portproxy show v4tov4 - 显示 IPv4 代理连接到另一个 IPv4 端口的参数。
  
netsh interface portproxy show v4tov6 - 显示 IPv4 代理连接到 IPv6 的参数。
  
netsh interface portproxy show v6tov4 - 显示 IPv6 代理连接到 IPv4 的参数。
  
netsh interface portproxy show v6tov6 - 显示 IPv6 代理连接到另一个 IPv6 端口的参数。

2. 使用示例
  
netsh interface portproxy show all
  
控制台显示如下信息:
  
侦听 ipv4:                 连接到 ipv4:
  
地址            端口        地址            端口
  
----- ----  ----- ----
  
* 8080        192.168.56.101  8080
  
* 9090        192.168.56.101  9080
  
修改端口转发配置
  
1. 命令
  
netsh interface portproxy set v4tov4     - 更新通过 IPv4 的 IPv4 和代理连接到的侦听项目。
  
netsh interface portproxy set v4tov6     - 更新通过 IPv6 的 IPv4 和代理连接到的侦听项目。
  
netsh interface portproxy set v6tov4     - 更新通过 IPv4 的 IPv6 和代理连接到的侦听项目。
  
netsh interface portproxy set v6tov6     - 更新通过 IPv6 的 IPv6 和代理连接到的侦听项目。
  
2. 命令语法
  
以netsh interface portproxy set v4tov4为例，其语法格式如下:

netsh interface portproxy set v4tov4 [listenport=]<integer>|<servicename>
  
[connectaddress=]<IPv4 address>|<hostname>
  
[[connectport=]<integer>|<servicename>]
  
[[listenaddress=]<IPv4 address>|<hostname>]
  
[[protocol=]tcp]

参数:
  
标记            值
  
listenport      - IPv4 侦听端口。
  
connectaddress  - IPv4 连接地址。
  
connectport     - IPv4 连接端口。
  
listenaddress   - IPv4 侦听地址。
  
protocol        - 使用的协议。现在只支持 TCP。
  
说明: 更新通过 IPv4 的 IPv4 和代理连接到的侦听项目。
  
3. 使用示例
  
netsh interface portproxy set v4tov4 listenport=9090 connectaddress=192.168.56.101 connectport=9080
  
将本地9090端口改成转发至192.168.56.101的9080端口中。

删除端口转发配置
  
1. 命令
  
netsh interface portproxy delete v4tov4  - 删除通过 IPv4 的 IPv4 和代理连接到的侦听项目。
  
netsh interface portproxy delete v4tov6  - 删除通过 IPv6 的 IPv4 和代理连接到的侦听项目。
  
netsh interface portproxy delete v6tov4  - 删除通过 IPv4 的 IPv6 和代理连接到的侦听项目。
  
netsh interface portproxy delete v6tov6  - 删除通过 IPv6 的 IPv6 和代理连接到的侦听项目。
  
2. 命令语法
  
以netsh interface portproxy delete v4tov4为例，其语法格式如下:

netsh interface portproxy delete v4tov4 [listenport=]<integer>|<servicename>
  
[[listenaddress=]<IPv4 address>|<hostname>]
  
[[protocol=]tcp]

参数:
  
标记             值
  
listenport     - 要侦听的 IPv4 端口。
  
listenport     - 要侦听的 IPv4 地址。
  
protocol       - 要使用的协议。当前仅支持 TCP。
  
注释: 删除要侦听的 IPv4 的项并通过 Ipv4 代理连接。
  
3. 使用示例
  
netsh interface portproxy delete v4tov4 listenport=9090

删除本地端口9090的端口转发配置。

<正文结束>

文章声明

作者: 傲风(aofengblog@163.com)       编写时间: 2014年09月05日

网址: [http://aofengblog.blog.163.com](http://aofengblog.blog.163.com)

作者保留所有权利，转载请保留文章全部内容或者说明原作者和转载地址！
