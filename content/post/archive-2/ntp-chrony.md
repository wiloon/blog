---
title: ntp, chrony, 时钟服务, 时钟同步
author: "-"
date: 2017-07-20T00:57:34+00:00
url: ntp
categories:
  - Linux
tags:
  - reprint
---
## ntp, chrony

NTP，是 Net Time Protocol的缩写，意即网络时间协议。

## systemd-timesyncd

systemd-timesyncd 是一个用于跨网络同步系统时钟的守护服务。它实现了一个 SNTP 客户端。与NTP的复杂实现相比，这个服务简单的多，它只专注于从远程服务器查询然后同步到本地时钟。

## chrony install

```bash
# install chrony - arch
sudo pacman -S chrony

# for centos
yum install chrony

# ubuntu
apt install chrony
```

## chrony 配置

`#` 号和 `!` 号都代表注释

```bash
# pacman
vim  /etc/chrony.conf
# ubuntu 
vim  /etc/chrony/chrony.conf
```

```bash
# 中国ntp服务
server 0.cn.pool.ntp.org iburst
server 1.cn.pool.ntp.org iburst
server 2.cn.pool.ntp.org iburst
server 3.cn.pool.ntp.org iburst

# 北美
north-america.pool.ntp.org

# 日本国立信息通信技术研究所, 此为一层（Stratum 1）NTP服务器。 支持IPv6
ntp.nict.jp
```

```bash
# chronyd service
systemctl status chronyd
systemctl start chronyd
systemctl --now enable chronyd

## 查看 ntp_servers 状态
chronyc sources -v

# 查看时间差
chronyc -n tracking

# 立即校准系统时间, 需要root权限
sudo chronyc makestep

# systemd-timesyncd.service is in conflict with chronyd
systemctl disable systemd-timesyncd.service

## 查看 ntp_sync 状态
chronyc sourcestats -v

## 查看 ntp_servers 是否在线
chronyc activity -v

## 查看 ntp 详细信息
chronyc tracking -v

可以通过运行 chronyc 命令来修改设置,命令如下: 
accheck - 检查NTP访问是否对特定主机可用
add server - 手动添加一台新的NTP服务器。
clients - 在客户端报告已访问到服务器
delete - 手动移除NTP服务器或对等服务器
settime - 手动设置守护进程时间
```

<http://www.361way.com/rhel7-chrony/4778.html>
<http://www.361way.com/rhel7-chrony/4778.html/embed#?secret=M7IADqld6f>
<https://www.zfl9.com/chrony.html>

## chronyc sources结果显示

^? controller .......
这表示时间同步服务器不可到达。
经以下步骤成功排除错误，供参考
在控制节点
1.检查controller节点服务器的时间同步服务是否开启成功
systemctl status chronyd.service
根据提示信息排查配置文件 /etc/chrony.conf中的错误，重点排查
allow 允许连接同步服务的主机

## ntp

```bash
sudo pacman -S ntp

systemctl status ntpd
sudo systemctl start ntpd.service
sudo systemctl enable ntpd.service

vim /etc/ntp.conf
server time.wiloon.com iburst

#check ntp status
ntpq -p

```

```bash
# 查看ntp状态
ntpq -p
ntpq -4p
```

chrony的优势
  
Chrony 的优势包括:

更快的同步只需要数分钟而非数小时时间,从而最大程度减少了时间和频率误差,这对于并非全天 24 小时运行的台式计算机或系统而言非常有用。
  
能够更好地响应时钟频率的快速变化,这对于具备不稳定时钟的虚拟机或导致时钟频率发生变化的节能技术而言非常有用。
  
在初始同步后,它不会停止时钟,以防对需要系统时间保持单调的应用程序造成影响。
  
在应对临时非对称延迟时 (例如,在大规模下载造成链接饱和时) 提供了更好的稳定性。
  
无需对服务器进行定期轮询,因此具备间歇性网络连接的系统仍然可以快速同步时钟。

### ntpdate 网络校时

ntpdate
  
-u 指定使用无特权的端口发送数据包。 当在一个对特权端口的输入流量进行阻拦的防火墙后是很有益的, 并希望在防火墙之外和主机同步。防火墙是一个系统或者计算机,它控制从外网对专用网的访问。

<https://chrony.tuxfamily.org/documentation.html>
  
<https://wiki.archlinux.org/index.php/Network_Time_Protocol_daemon>
<https://www.ntppool.org/en/use.html>

## NTP层级关系词

NTP 时钟以层次模型组织。层级中的每层被称为一个 stratum（阶层）。stratum 的概念说明了一台机器到授权的时间源有多少 NTP 跳。

01

Stratum 0 由没有时间漂移的时钟组成，例如原子时钟。这种时钟不能在网络上直接使用。Stratum N (N > 1) 层服务器从 Stratum N-1 层服务器同步时间。Stratum N 时钟能通过网络和彼此互联。

NTP 支持多达 15 个 stratum 的层级。Stratum 16 被认为是未同步的，不能使用的。

stratum 1:
这一层是计算机，它们的系统时间和连接其上的 stratum 0 设备保持同步，误差在几个微秒。
本层计算机可能与其他同层的计算机对等相连，以进行完整性检查和备份。它们也被称为主要（primary）时间服务器。

这一层对互联网是不可见的，虽然它们是部署在互联网上的。

它们率属于美国海军天文台。 参看 https://tycho.usno.navy.mil/

作者：zhaoxg_cat
链接：https://www.jianshu.com/p/8096c0477230
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

1.4 Stratum
Stratum 是 NTP 中表示时间服务器层级的术语。基准时钟（refclock，Reference Clock）是 Stratum 0；直接连接到基准时钟的服务器是 Stratum 1；连接到 Stratum N 服务器的客户端是 Stratum N+1。N 的数值越大，距离基准时钟越远，也就越不精准。N 的最大值是 16，表示该设备未同步且不可达。大多数公共时间服务器是 Stratum 1 或 Stratum 2。

<https://zhuanlan.zhihu.com/p/257335659>


## htpdate

NTP uses UDP port 123

NTP service is using UDP protocol to sync the time. So HTTP/TCP proxy may not work for it. Alternative to accepted answer, there is a good htpdate tool to sync time behind proxy.

A cron job example:

```bash
* 3 * * * /usr/bin/htpdate -s -P <PROXY_HOST>:<PROXY__PORT> www.linux.org www.freebsd.org

```

## How to use ntpdate behind a proxy

<https://superuser.com/questions/307158/how-to-use-ntpdate-behind-a-proxy>

## archlinux ntp

```bash
timedatectl status
# System clock synchronized: yes
```
