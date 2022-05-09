---
title: 'CentOS firewalld, firewall-cmd'
author: "-"
date: 2020-01-17T08:34:39+00:00
url: /?p=15384
categories:
  - Inbox
tags:
  - reprint
---
## 'CentOS firewalld, firewall-cmd'

Firewalld 使用区域和服务的概念。根据您将要配置的区域和服务，您可以控制允许或阻止与系统之间的流量。
可以使用 firewall-cmd 命令行实用程序配置和管理 Firewalld  。
在 CentOS 8 中， nftables 替代了 iptables，作为 firewalld 守护程序的默认防火墙后端。

防火墙区域
区域是预定义的规则集，用于指定计算机连接到的网络的信任级别。您可以将网络接口和源分配给区域。

以下是 FirewallD 提供的区域，根据区域的信任级别从不信任到信任: 

drop: 删除所有传入连接，而无任何通知。仅允许传出连接。
block: 拒绝所有传入连接，并带有一条 icmp-host-prohibited 消息 IPv4 和一条 icmp6-adm-prohibited 关于 IPv6n  的消息。仅允许传出连接。
public: 用于不受信任的公共区域。您不信任网络上的其他计算机，但是可以允许选择的传入连接。
external: 用于在系统充当网关或路由器时启用 NAT 伪装的外部网络。仅允许选择的传入连接。
internal: 当系统充当网关或路由器时，用于内部网络。网络上的其他系统通常是受信任的。仅允许选择的传入连接。
dmz: 用于非军事区中访问网络其余部分的计算机。仅允许选择的传入连接。
work: 用于工作机。网络上的其他计算机通常是受信任的。仅允许选择的传入连接。
home: 用于家用机器。网络上的其他计算机通常是受信任的。仅允许选择的传入连接。
Trusted: 接受所有网络连接。信任网络中的所有计算机。

```bash
# 启动守护程序
systemctl start firewalld --now
# 查看版本
firewall-cmd --version
# 查看状态
systemctl status firewalld.service
# OR
firewall-cmd --state
# 查看默认区域
firewall-cmd --get-default-zone
# 
firewall-cmd --zone=public --list-ports
firewall-cmd --zone=public --add-port=8080/tcp
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --remove-port=8080/tcp

```
### 防火墙区域
默认的区域设置为 public ，并且所有网络接口都分配给该区域，当然您可以根据自己的需要修改默认区域。
默认区域是用于所有未明确分配给另一个区域的区域。
您可以通过键入以下内容查看默认区域: 

    sudo firewall-cmd --get-default-zone
    获取所有可用区域的列表，请输入: 
    sudo firewall-cmd --get-zones
    查看活动区域和分配给它们的网络接口，请执行以下操作: 
    sudo firewall-cmd --get-active-zones
    打印区域配置设置: 
    sudo firewall-cmd --zone=public --list-all
    检查所有可用区域的配置，请输入: 
    sudo firewall-cmd --list-all-zones

### 更改区域目标
target 为未指定的传入流量定义区域的默认行为。它可以设置为下列选项之一:  default ， ACCEPT ， REJECT ，和 DROP 。
要设置区域的目标，请使用 --zone 选项指定区域，并使用选项指定目标 --set-target 。
例如，要将 public 区域的目标更改为 DROP 您将运行: 
    sudo firewall-cmd --zone=public --set-target=DROP

仅对当前会话(运行时配置)允许公共区域中的接口允许传入的 HTTP 通信(端口 80) ，请输入: 

sudo firewall-cmd --zone=public --add-service=http

如果要在重新启动后将端口 80 保持打开状态，则需要再次键入相同的命令，但这一次带有 --permanent 标志: 

sudo firewall-cmd --permanent --zone=public --add-service=http

使用 --list-services 和 --permanent 标记一起验证您的更改: 

sudo firewall-cmd --permanent --zone=public --list-services

要为当前会话在公共区域中打开 8080 端口，请运行: 

sudo firewall-cmd --zone=public --add-port=8080/tcp
该协议可以是 tcp ， udp ， sctp ，或 dccp 。

验证更改: 
sudo firewall-cmd --zone=public --list-ports

```bash
# 获取启用的zone
firewall-cmd --get-active-zones
public
  interfaces: eno16777984

# 查看指定区域中开放的端口和服务
firewall-cmd --zone=public --list-all

# 不要忘记 --permanent 
[root@osboxes java]# firewall-cmd --zone=public --add-port=8080/tcp --permanent
# OR 添加一个地址段
[root@osboxes java]# firewall-cmd --zone=public --add-port=5060-5061/udp --permanent
success
# 需要reload后才启用, 热加载
[root@osboxes java]# firewall-cmd --reload
# OR 冷加载
[root@osboxes java]# firewall-cmd --complete-reload
success
# 能看到新端口已经添加
[root@osboxes java]# firewall-cmd --zone=public --list-all
public (default, active)
  interfaces: eno16777984
  sources:
  services: dhcpv6-client mdns ssh
  ports: 8080/tcp
  masquerade: no
  forward-ports:
  icmp-blocks:
  rich rules: 
# 删除一个端口
firewall-cmd --permanent --zone=public --remove-port=8080/tcp
firewall-cmd --permanent --zone=public --remove-port=8080/udp

# 阻止某个IP (123.57.22.204) 连接: 

firewall-cmd --permanent --add-rich-rule="rule family=ipv4 source address=123.57.22.204 reject"
```