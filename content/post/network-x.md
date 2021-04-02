+++
author = "w1100n"
date = "2021-02-17 13:32:57" 
title = "network, x"

+++
### Dnat VS Redirect VS Tproxy
#### Dnat
Dnat 通过iptable nat表变更目标IP和PORT，需要修改数据包，走IPTABLE需要过内核。
#### Redirect
REDIRECT 其实是 DNAT 的一种特殊形式,只变更目标端口，这种场景下只有两台机器通讯。
REDIRECT 把数据包的目标 IP 改成了 127.0.0.1，端口改成了--to-ports 参数指定的本地端口，这样本机的透明代理程序就能处理这个包，应用能通过内核的状态信息拿到被改写之前的目标 IP 和端口号，具体参考  
https://unix.stackexchange.com/questions/166692/how-does-a-transparent-socks-proxy-know-which-destination-ip-to-use

#### TPROXY
https://www.jianshu.com/p/76cea3ef249d

TPROXY开启TCP/IP IP_TRANSPARENT标志，数据在两个SOCKTS间复制, 这种场景不走kernel,不需要开启ip_forward,不需要开启connection_tracking。  
TPROXY比REDIRECT新的特性，它能做到不修改数据包，应用只需一点改动就能实现REDIRECT所有的功能，内核文档里有如下说明：

    TPROXY (Transparent proxying) often involves "intercepting" traffic on a router. This is
    usually done with the iptables REDIRECT target; however, there are serious
    limitations of that method. One of the major issues is that it actually
    modifies the packets to change the destination address -- which might not be
    acceptable in certain situations. (Think of proxying UDP for example: you won't
    be able to find out the original destination address. Even in case of TCP
    getting the original destination address is racy.)

从这段说明里似乎 UDP 并没有内核状态来记录更改前的 IP 地址，这与这篇博客所说所说的有些矛盾，我目前的理解还是 UDP 在内核没有状态记录。TPROXY得以实现归结为三个要点：

将流量重定向到本地路由
路由规则定义去向
代理程序监听，通过特殊的参数可以响应非本机的 IP(因为包的目的地址没改嘛)

### 安装依赖 
    opkg install sudo iptables-mod-tproxy iptables-mod-extra libopenssl ca-certificates

### 创建用户
```bash
    grep -qw x_tproxy /etc/passwd || echo "x_tproxy:x:0:23333:::" >> /etc/passwd
    sudo -u x_tproxy id # 检查用户是否添加成功
```

### 服务启动脚本 /etc/init.d/xxxx
```bash
#!/bin/sh /etc/rc.common

USE_PROCD=1

START=99
STOP=99

# SERVICE_DAEMONIZE=1
# SERVICE_WRITE_PID=1

CONF=/etc/xxxx/config.json
EXEC=/usr/bin/xxxx

start_service() {
  procd_open_instance
  procd_set_param command $EXEC --config $CONF
  procd_set_param file $CONF
  procd_set_param limits nofile="1000000 1000000"
  procd_set_param user x_tproxy
  procd_close_instance
}

start() {
        service_start $EXEC
}

stop() {
        service_stop $EXEC
}

reload() {
        service_reload $EXEC
}
```
### firewall rule /etc/firewall.user
```bash
ip rule add fwmark 1 table 100 # 如果mark 为1 则参考路由表100 将数据送出
ip route add local 0.0.0.0/0 dev lo table 100 # 把所有的流量发到本地

# 创建链 chain0
iptables -t mangle -N chain0
# 所有目标地址在网关所在网段的请求直连
iptables -t mangle -A chain0 -d 127.0.0.0/24 -j RETURN
iptables -t mangle -A chain0 -d 192.168.1.0/24 -j RETURN
iptables -t mangle -A chain0 -d 192.168.50.0/24 -j RETURN
iptables -t mangle -A chain0 -d 192.168.96.0/24 -j RETURN
iptables -t mangle -A chain0 -d 192.168.97.0/24 -j RETURN
# 目标地址为组播IP的请求直连
iptables -t mangle -A chain0 -d 224.0.0.0/4 -j RETURN
iptables -t mangle -A chain0 -d 255.255.255.255/32 -j RETURN
# 给 TCP 打标记 1，转发至 12345 端口, 数据包内部的dst等信息不变
iptables -t mangle -A chain0 -p tcp -j TPROXY --on-port 12345 --tproxy-mark 1
# udp
iptables -t mangle -A chain0 -p udp -j TPROXY --on-port 12345 --tproxy-mark 1
iptables -t mangle -A PREROUTING -j chain0

iptables -t mangle -N chain1
iptables -t mangle -A chain1 -m owner --gid-owner 23333 -j RETURN
iptables -t mangle -A chain1 -d 127.0.0.0/24 -j RETURN
iptables -t mangle -A chain1 -d 192.168.1.0/24 -j RETURN
iptables -t mangle -A chain1 -d 192.168.50.0/24 -j RETURN
iptables -t mangle -A chain1 -d 192.168.96.0/24 -j RETURN
iptables -t mangle -A chain1 -d 192.168.97.0/24 -j RETURN
iptables -t mangle -A chain1 -d 224.0.0.0/4 -j RETURN
iptables -t mangle -A chain1 -d 255.255.255.255/32 -j RETURN
iptables -t mangle -A chain1 -j MARK --set-mark 1
iptables -t mangle -A OUTPUT -p tcp -j chain1
iptables -t mangle -A OUTPUT -p udp -j chain1

```

### disable chain0,1
    iptables -t mangle -D PREROUTING 1
    iptables -t mangle -D OUTPUT 2
    iptables -t mangle -D OUTPUT 1

### openwrt policy route config
https://openwrt.org/docs/guide-user/network/ip_rules

    config rule
        option mark   '0xFF'
        option in     'lan'
        option dest   '172.16.0.0/16'
        option lookup '100'
---

https://www.jianshu.com/p/91a084e91ed2