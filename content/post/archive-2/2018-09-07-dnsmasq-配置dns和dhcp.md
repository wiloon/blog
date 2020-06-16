---
title: 'dnsmasq  配置'
author: wiloon
type: post
date: 2018-09-07T02:42:31+00:00
url: /?p=12638
categories:
  - Uncategorized

---
```bash
docker run \
    --name dnsmasq \
    -d \
    -p 30053:53/udp \
    -p 35380:8080 \
    -v dnsmasq-config:/etc/dnsmasq.conf \
    --log-opt "max-size=100m" \
    -e "HTTP_USER=foo" \
    -e "HTTP_PASS=bar" \
    --restart always \
    jpillora/dnsmasq
```

```bash
mkdir /etc/dnsmasq.d
echo 'conf-dir=/etc/dnsmasq.d' &gt;&gt; /etc/dnsmasq.conf
```

### docker

```bash
docker run \
-d \
--name dnsmasq \
--cap-add=NET_ADMIN \
-p 53:53/udp \
-v /etc/localtime:/etc/localtime:ro \
-v dnsmasq-config:/etc/dnsmasq.d \
--restart=always \
andyshinn/dnsmasq

```

http://debugo.com/dnsmasq/

DNSmasq是一个小巧且方便地用于配置DNS和DHCP的工具，适用于小型网络。它提供了DNS功能和可选择的DHCP功能可以取代dhcpd(DHCPD服务配置)和bind等服务，配置起来更简单，更适用于虚拟化和大数据环境的部署。

dhcp服务
  
其中一些关键的配置如下,配置文件/etc/dnsmasq.conf 中的注释已经给出了非常详细的解释。

```bash
vim /etc/dnsmasq.conf

# 配置上游服务器地址
# resolv-file配置Dnsmasq额外的上游的DNS服务器，如果不开启就使用Linux主机默认的/etc/resolv.conf里的nameserver。

# 通过下面的选项指定其他文件来管理上游的DNS服务器
resolv-file=/etc/resolv.dnsmasq.conf


# 服务监听的网络接口地址
# If you want dnsmasq to listen for DHCP and DNS requests only on
# specified interfaces (and the loopback) give the name of the
# interface (eg eth0) here.
# Repeat the line for more than one interface.
#interface=
# Or you can specify which interface _not_ to listen on
#except-interface=
# Or which to listen on by address (remember to include 127.0.0.1 if
# you use this.)
listen-address=192.168.97.1,127.0.0.1

# dhcp动态分配的地址范围
# Uncomment this to enable the integrated DHCP server, you need
# to supply the range of addresses available for lease and optionally a lease time
dhcp-range=192.168.97.10,192.168.97.20,48h

# dhcp服务的静态绑定
# Always set the name and ipaddr of the host with hardware address
# dhcp-host=00:0C:29:5E:F2:6F,192.168.1.201
# dhcp-host=00:0C:29:5E:F2:6F,192.168.1.201,infinite    无限租期
dhcp-host=00:0C:29:5E:F2:6F,192.168.97.201,os02
dhcp-host=00:0C:29:15:63:CF,192.168.97.202,os03
```

```bash
vim /etc/resolv.dnsmasq.conf
nameserver 223.5.5.5
nameserver 223.6.6.6
```

https://www.hi-linux.com/posts/30947.html#%E9%85%8D%E7%BD%AE%E4%B8%8A%E6%B8%B8%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%9C%B0%E5%9D%80
  
http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html