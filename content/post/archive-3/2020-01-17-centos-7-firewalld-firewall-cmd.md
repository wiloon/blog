---
title: 'CentOS 7  firewalld,  firewall-cmd'
author: wiloon
type: post
date: 2020-01-17T08:34:39+00:00
url: /?p=15384
categories:
  - Uncategorized

---
```bash# 查看版本
[root@osboxes java]# firewall-cmd --version
0.3.9
# 查看状态
[root@osboxes java]# systemctl status firewalld.service
OR
[root@osboxes java]# firewall-cmd --state
running
# 获取启用的zone
[root@osboxes java]# firewall-cmd --get-active-zones
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

# 阻止某个IP（123.57.22.204）连接：

firewall-cmd --permanent --add-rich-rule="rule family=ipv4 source address=123.57.22.204 reject"
```