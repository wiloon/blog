---
title: journal, journalctl, syslog
author: "-"
date: 2017-11-24T09:34:51+00:00
url: journal
categories:
  - Linux
tags:
  - remix
  - reprint
---
## journal, journalctl, syslog

```bash
# -u 指定 unit
journalctl -u file-server
```

Arch Linux 启用 systemd 后, 很多服务都被替换掉了, 当然syslog 也不例外, 被 Systemd Journal 所替代。

systemd 拥有强大的处理与系统日志记录功能。在使用其它工具时,日志往往被分散在整套系统当中,由不同的守护进程及进程负责处理,这意味着我们很难跨越多种应用程序对其内容进行解读。

相比之下,systemd尝试提供一套集中化管理方案,从而统一打理全部内核及用户级进程的日志信息。这套系统能够收集并管理日志内容,而这也就是我们所熟知的journal。

Journal的实现归功于journald守护进程,其负责处理由内核、initrd以及服务等产生的信息

journal config
  
/etc/systemd/journald.conf
  
SystemMaxUse=1024M

### journald unit log, max size of journal log

```bash
    sudo journalctl -b -u systemd-journald
```

### customiz journal size

```bash
    /etc/systemd/journald.conf
    SystemMaxUse=50M
```

```bash
# 最近一次重新引导后收集到的日志
journalctl -b

sudo journalctl /usr/lib/systemd/systemd -b

# 查看系统上全部来自Nginx单元的日志
journalctl -u nginx.service
journalctl -u nginx.service --since today
journalctl -u nginx.service --since "2018-06-11 12:00:00"
journalctl --since "2015-01-10" --until "2015-01-11 03:00"
journalctl --since "2020-11-02 00:00" --until "2020-11-02 10:00"
journalctl --since "2020-11-02 00:00" --until "2020-11-02 10:00" | grep -v write

# 检查当前journal使用磁盘量
journalctl --disk-usage

journalctl --vacuum-time=2d

#如果使用–vacuum-size 选项,则可硬性指定日志的总体体积,意味着其会不断删除旧有记录直到所占容量符合要求
sudo journalctl --vacuum-size=1G

# 修改配置文件之后需要重启
systemctl restart systemd-journald.service

#检查journal是否运行正常以及日志文件是否完整无损坏
journalctl --verify

# 显示特定时间区间内的日志
journalctl --since=yesterday
journalctl --since=2012-10-15 --until="2011-10-16 23:59:59"

显示特定程序的所有消息:

# journalctl /usr/lib/systemd/systemd
显示特定进程的所有消息:

# journalctl _PID=1
显示与指定用户相关的日志: 

# journalctl _UID=70
# journalctl _UID=70 _UID=71

# 指定日志文件占据的最大空间
sudo journalctl --vacuum-size=1G

# 指定日志文件保存多久
$ sudo journalctl --vacuum-time=1years

```

大家可以配置自己的服务器以限定journal所能占用的最高容量。要实现这一点,我们需要编辑/etc/systemd/journald.conf文件。

以下条目可用于限定journal体积的膨胀速度:

SystemMaxUse=: 指定journal所能使用的最高持久存储容量。
  
SystemKeepFree=: 指定journal在添加新条目时需要保留的剩余空间。
  
SystemMaxFileSize=: 控制单一journal文件大小,符合要求方可被转为持久存储。
  
RuntimeMaxUse=: 指定易失性存储中的最大可用磁盘容量 (/run文件系统之内) 。
  
RuntimeKeepFree=: 指定向易失性存储内写入数据时为其它应用保留的空间量 (/run文件系统之内) 。
  
RuntimeMaxFileSize=: 指定单一journal文件可占用的最大易失性存储容量 (/run文件系统之内) 。

分发
  
systemd journal本身未提供日志分发功能。

常见的解决方案,做好单机日志的存储配置之后,通过rsync、btsync等工具收集同步日志至某中心节点进行分析处理。
  
另外在systemd-193添加了systemd-journal-gatewayd.service,服务器开启此服务之后,将监听本地19531端口,其他机器可通过HTTP或JSON协议访问服务器得到后者日志,详细介绍(登录验证等)请查看systemd-journal-gatewayd.service。
  
注: systemd-212引入了 systemd-journal-remote >systemd-journal-remote is a command to receive serialized journal events and store them to the journal.
  
<https://huataihuang.gitbooks.io/cloud-atlas/os/linux/redhat/system_administration/systemd/systemd_clear_journalctl.html>
  
<http://fangpeishi.com/systemd_chapter4.html>
  
<http://blog.csdn.net/zstack_org/article/details/56274966>
