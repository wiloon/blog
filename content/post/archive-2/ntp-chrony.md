---
title: ntp, chrony
author: "-"
date: 2017-07-20T00:57:34+00:00
url: ntp
categories:
  - inbox
tags:
  - reprint
---
## ntp, chrony

### chrony install

```bash
# install chrony - arch
sudo pacman -S chrony

# for centos
yum install chrony

# ubuntu
apt install chrony
```

### chrony 配置

```bash
# 号和！号都 代表注释

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

可以通过运行chronyc命令来修改设置,命令如下: 
accheck - 检查NTP访问是否对特定主机可用
add server - 手动添加一台新的NTP服务器。
clients - 在客户端报告已访问到服务器
delete - 手动移除NTP服务器或对等服务器
settime - 手动设置守护进程时间
```

<http://www.361way.com/rhel7-chrony/4778.html>
<http://www.361way.com/rhel7-chrony/4778.html/embed#?secret=M7IADqld6f>
<https://www.zfl9.com/chrony.html>

### ntp

```bash
sudo pacman -S ntp

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

### ntpdate网络校时

ntpdate
  
-u 指定使用无特权的端口发送数据包。 当在一个对特权端口的输入流量进行阻拦的防火墙后是很有益的, 并希望在防火墙之外和主机同步。防火墙是一个系统或者计算机,它控制从外网对专用网的访问。

<https://chrony.tuxfamily.org/documentation.html>
  
<https://wiki.archlinux.org/index.php/Network_Time_Protocol_daemon>
<https://www.ntppool.org/en/use.html>
