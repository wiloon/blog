---
title: RedHat Enterprise Linux 网络配置
author: "-"
date: 2012-03-13T14:59:40+00:00
url: /?p=2554
categories:
  - Linux
  - Network
tags:
  - RedHat

---
## RedHat Enterprise Linux 网络配置
一、$/sbin/ifconfig //显示ifconfig命令查看网络接口的信息
  

  
#ifconfig eth0 //显示指定接口的信息
  

  
#ifconfig -a //显示所有接口的信息 (无论是否活跃) 
  

  
#ifconfig eth0 192.168.0.2 netmask 255.255.255.0
  

  
//临时修改接口IP地址 (无需重启接口) 
  

  
二、$/sbin/route //显示当前Linux主机中的路由表信息
  

  
1. #route del default gw 192.168.0.1
  

  
//临时删除默认网关192.168.0.1
  

  
2. #route add default gw 192.168.0.1
  

  
//临时添加默认网关192.168.0.1
  

  
3. #route add -net 192.168.1.0/24 gw 192.168.0.254
  

  
//临时添加一条静态路由
  

  
/*\*本文中提及临时操作的地方，即主机重启后该操作将失效，如果希望每次系统重启后自动添加静态路由条目，则可以将该语句写入/etc/rc.d/rc.local中。\**/
  

  
三、#ping //测试与其他主机的网络连接
  

  
1. #ping -c 4 192.168.0.1 //指定发出ICMP包个数
  

  
四、#traceroute //测试当前主机到目的著急的网络连接
  

  
五、#hostname //查看当前主机的主机名
  

  
1. #hostname linsrv //临时修改当前主机名
  

  
六、#nslookup //测试DNS域名解析
  

  
>server //显示当前DNS服务器
  
>server 192.168.0.1 //临时指定DNS服务器地址
  

  
七、#dhclient //为当前主机申请网络配置信息
  

  
八、#netconfig //通过向导在字符界面下修改网络配置信息
  

  
九、#/etc/init.d/network restart //重启网络服务
  

  
1. #/etc/init.d/network stop //停止网络服务
  

  
2. #/etc/init.d/network start //启动网络服务
  

  
/*\*无论是通过netconfig，还是通过修改配置文件的方式修改了网络配置信息，都需要重启network服务才能生效\**/
  

  
十、#service network start //启动网络服务
  

  
1. #service network stop //停止网络服务
  

  
2. #service network restart //重启网络服务
  

  
3. #service network status //查看网络服务状态
  

  
/*\*在RHEL4中可以通过service命令来管理大多数服务的启动、停止、重启以及查看其工作状态等\**/
  

  
十一、#chkconfig ——list | grep network //查看某服务的自动启动级别
  

  
1. #chkconfig ——level 35 network off //设置在级别35不自动启动某服务
  

  
2. #chkconfig ——level 3 network on //设置在级别3自动启动某服务
  

  
十二、ntsysv //通过向导在字符界面下修改服务的自启动选项
  

  
十三、#vi /etc/sysconfig/network-scripts/eth0 //编辑指定网络接口配置文件
  

  
DEVICE=eth0 //指定接口名称
  

  
ONBOOT=yes //系统启动时加载
  

  
BOOTPROTO=static //IP地址静态配置，若该值为"dhcp"则为动态获得
  

  
IPADDR=192.168.0.1 //设置IP地址
  

  
NETMASK=255.255.255.0 //设置子网掩码
  

  
GATEWAY=192.168.0.254 //设置默认网关
  

  
/*\*注意: 设置之后必须要重启network服务或者重启接口 (#ifdown eth0；ifup eth0) ，才能生效。\**/
  

  
十四、#vi /etc/sysconfig/network //通过配置文件修改主机名
  

  
NETWORKING=yes
  

  
HOSTNAME=localhost.localdomain //修改该值作为主机名，如: rhel.lpwr.net
  

  
//该配置修改后，要重启系统方能生效
  

  
十五、#vi /etc/hosts //设置本地DNS解析文件
  

  
127.0.0.1 localhost.localdomain localhost //该行强烈建议保留
  

  
192.168.0.1 rhel.lpwr.net rhel //必须有三个字段: IP、FQDN、HOSTNAME
  

  
十六、#vi /etc/resolv.conf //指定当前主机的DNS服务器，最多可指定三个
  

  
search lpwr.net //设置当前主机的默认查找域
  

  
nameserver 192.168.0.100 //指定首选DNS服务器
  

  
nameserver 172.16.254.2
  

  
nameserver 202.106.0.20
  
