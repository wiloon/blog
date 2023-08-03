---
title: openvpn
author: "-"
date: 2017-02-17T00:23:48+00:00
url: openvpn
categories:
  - network
tags:
  - VPN

---
## openvpn

### VPN, Virtual Private Network, 虚拟专用网络

OpenVPN 是一个基于 OpenSSL 库的应用层 VPN 实现, 最早由James Yonan编写

OpenVpn的技术核心是虚拟网卡,其次是SSL协议实现

虚拟网卡是使用网络底层编程技术实现的一个驱动软件,安装后在主机上多出现一个网卡,可以像其它网卡一样进行配置。服务程序可以在应用层打开虚拟网卡,如果应用软件 (如IE) 向虚拟网卡发送数据,则服务程序可以读取到该数据,如果服务程序写合适的数据到虚拟网卡,应用软件也可以接收得到。虚拟网卡在很多的操作系统下都有相应的实现,这也是OpenVpn能够跨平台一个很重要的理由.
  
在OpenVpn中,如果用户访问一个远程的虚拟地址 (属于虚拟网卡配用的地址系列,区别于真实地址) ,则操作系统会通过路由机制将数据包 (TUN模式) 或数据帧 (TAP模式) 发送到虚拟网卡上,服务程序接收该数据并进行相应的处理后,通过SOCKET从外网上发送出去,远程服务程序通过SOCKET从外网上接收数据,并进行相应的处理后,发送给虚拟网卡,则应用软件可以接收到,完成了一个单向传输的过程,反之亦然。

加密
OpenVPN使用OpenSSL库加密数据与控制信息: 它使用了OpenSSL的加密以及验证功能,意味着,它能够使用任何OpenSSL支持的算法。它提供了可选的数据包 HMAC 功能以提高连接的安全性。此外,OpenSSL的硬件加速也能提高它的性能。[1]

验证
  
OpenVPN提供了多种身份验证方式,
  
用以确认参与连接双方的身份,包括: 预享私钥,第三方证书以及用户名/密码组合。预享密钥最为简单,但同时它只能用于建立点对点的VPN；基于PKI的第三方证书提供了最完善的功能,但是需要额外的精力去维护一个PKI证书体系。 OpenVPN2.0后引入了用户名/口令组合的身份验证方式,它可以省略客户端证书,但是仍有一份服务器证书需要被用作加密。

网络
  
OpenVPN所有的通信都基于一个单一的IP端口,默认且推荐使用UDP协议通讯,同时TCP也被支持。OpenVPN连接能通过大多数的代理服务器,并且能够在NAT的环境中很好地工作。服务端具有向客户端"推送"某些网络配置信息的功能,这些信息包括: IP地址、路由设置等。OpenVPN提供了两种虚拟网络接口: 通用Tun/Tap驱动,通过它们,可以建立三层IP隧道,或者虚拟二层以太网,后者可以传送任何类型的二层以太网络数据。传送的数据可通过LZO算法压缩。IANA (Internet Assigned Numbers Authority) 指定给OpenVPN的官方端口为1194。OpenVPN 2.0以后版本每个进程可以同时管理数个并发的隧道。[1]
  
OpenVPN使用通用网络协议 (TCP与UDP) 的特点使它成为 IPsec 等协议的理想替代,尤其是在ISP (Internet service provider) 过滤某些特定VPN协议的情况下。[1]
  
在选择协议时候,需要注意2个加密隧道之间的网络状况,如有高延迟或者丢包较多的情况下,请选择TCP协议作为底层协议,UDP协议由于存在无连接和重传机制,导致要隧道上层的协议进行重传,效率非常低下。[1]

安全
  
OpenVPN与生俱来便具备了许多安全特性: 它在用户空间运行,无须对内核及网络协议栈作修改；初始完毕后以chroot方式运行,放弃root权限；使用mlockall以防止敏感数据交换到磁盘。[1]
  
OpenVPN通过PKCS#11支持硬件加密标识,如智能卡。

### install

```bash
#install
sudo pacman -S openvpn
apt-get install openvpn
```

### server

#### create keys

```bash
    pacman -S easy-rsa
```

#### use Elliptic curve instead of RSA

```bash
    # append line to /etc/easy-rsa/vars
    set_var EASYRSA_ALGO ec
    set_var EASYRSA_CURVE secp521r1
    set_var EASYRSA_DIGEST "sha512"
    set_var EASYRSA_NS_SUPPORT "yes"
```

#### easy-rsa

    cd /etc/easy-rsa
    export EASYRSA=$(pwd)
    export EASYRSA_VARS_FILE=/etc/easy-rsa/vars
    easyrsa init-pki
    easyrsa build-ca
    # new ca certificate file: /etc/easy-rsa/pki/ca.crt
    scp /etc/easy-rsa/pki/ca.crt foo@hostname-of-openvpn-server:/tmp/ca.crt
    mv /tmp/ca.crt /etc/openvpn/server/
    chown root:openvpn /etc/openvpn/server/ca.crt

    # install easy-rsa on openvpn server
    pacman -S easy-rsa
    easyrsa init-pki
    easyrsa gen-req pingd nopass
    cp /etc/easy-rsa/pki/private/pingd.key /etc/openvpn/server/
    openvpn --genkey secret /etc/openvpn/server/ta.key

    # The server and client(s) certificates need to be signed by the CA then transferred back to the OpenVPN server/client(s).

    cp /etc/easy-rsa/pki/reqs/*.req /tmp
    scp /tmp/*.req foo@hostname-of-CA:/tmp

    # on ca server
    cd /etc/easy-rsa
    easyrsa import-req /tmp/servername.req servername
    easyrsa sign-req server servername
    scp /etc/easy-rsa/pki/issued/*.crt foo@hostname-of-openvpn_server:/tmp

    mv /tmp/servername.crt /etc/openvpn/server/
    chown root:openvpn /etc/openvpn/server/servername.crt

### client

    pacman -S easy-rsa

#### use Elliptic curve instead of RSA

    ...

#### easy-rsa

    cd /etc/easy-rsa
    export EASYRSA=$(pwd)
    export EASYRSA_VARS_FILE=/etc/easy-rsa/vars
    easyrsa init-pki
    easyrsa gen-req client1 nopass

    # sign the certificates
    cp /etc/easy-rsa/pki/reqs/*.req /tmp

    # cd /etc/easy-rsa
    # easyrsa import-req /tmp/servername.req servername
    # easyrsa import-req /tmp/client1.req client1
    # easyrsa sign-req server servername
    # easyrsa sign-req client client1

### config

“＃”前缀是指定的注释标签。openvpn网站上的示例广泛使用'＃'注释。另外,分号 ';' 用于注释掉单行或单项。

### sample

    /usr/share/openvpn/examples/server.conf
    cp /usr/share/openvpn/examples/server.conf /etc/openvpn/server/pingd.conf
    # 服端配置文件名跟systemd 启动命令里的服务名要一致

### server

```bash
# local 服务端监听的ip地址, 默认0.0.0.0
local 0.0.0.0

# 服务端口
port 1194

# 协议,tcp, udp
proto udp
#tap, tun 采用路由模式,不过使用的却是tap
dev tun
# Certificate Authority, 验证客户端证书是否合法, 以下路径可以使用相对路径或绝对路径
ca /etc/openvpn/server/ca.crt

# server端证书
cert /etc/openvpn/server/server.crt
# 服务端私钥
key /etc/openvpn/server/server.key
# Diffie-Hellman, 即使密钥使用了椭圆算法, 这个dh也要配置, 是的, 配置了不起作用,但是也要配置,否则启动openvpn的时候会报错,看官方说法, 我理解是防呆设计,万一使用了不是椭圆算法的密钥也能保证安全性
dh /etc/openvpn/server/dh.pem
# 网络拓扑结构, 默认的net30已经不建议使用,启动会报warn
topology subnet

# 设定server端虚拟出来的网段
server 192.168.55.0 255.255.255.0

# 在此文件中维护客户端与虚拟IP地址之间的关联记录
# 如果OpenVPN重启,重新连接的客户端可以被分配到先前分配的虚拟IP地址
ifconfig-pool-persist /etc/openvpn/server/ipp.txt

# 推送路由信息到客户端,以允许客户端能够连接到服务器后的其他私有子网
# 即允许客户端访问VPN服务器可访问的其他局域网
# 记住,这些私有子网还需要将OpenVPN客户端地址池 (10.8.0.0/255.255.255.0) 路由回到OpenVPN服务器
push "route 192.168.55.0 255.255.255.0"

#Nat后面使用VPN,如果长时间不通信,NAT session 可能会失效,导致vpn连接丢失。#所有keepalive提供一个类似ping的机制,每10秒通过vpn的control通道ping对方,
#如果120秒无法ping通,则认为丢失,并重启vpn,重新连接。
keepalive 10 120
# tls-auth, server mode, key-direction 0
tls-auth /etc/openvpn/pki/ta.key 0
# 或者单独配置 key-direction
;key-direction 0

# 选择一个密码加密算法,该配置项也必须复制到每个客户端配置文件中
# 注意,v2.4客户端/服务器将自动以TLS模式协商AES-256-GCM,请参阅手册中的ncp-cipher选项
cipher AES-256-GCM

# 在VPN链接上启用压缩并将选项推送到客户端 (仅适用于v2.4 +) 
compress lz4-v2
push "compress lz4-v2"

#通过keepalive检测超时后,重新启动vpn,不重新读取keys,保留第一次使用的keys
persist-key
#通过keepalive检测超时后,重新启动vpn,一直保持tun或tap设备是linkup的,否则网络连接会先linkdown然后linkup
persist-tun

# 输出一个简短的状态文件,用于显示当前的连接状态,该文件每分钟都会清空并重写一次
;status openvpn-status.log

# 默认情况下,日志消息将写入syslog(在Windows系统中,如果以服务方式运行,日志消息将写入OpenVPN安装目录的log文件夹中)
# 可以使用log或者log-append来改变这种默认设置
# "log"方式在每次启动时都会清空之前的日志文件
# "log-append"是在之前的日志内容后进行追加
# 你可以使用两种方式之一(不要同时使用)
;log         openvpn.log
;log-append  openvpn.log

# 设置日志文件冗余级别(0~9)。
# 0 表示静默运行,只记录致命错误。
# 4 表示合理的常规用法。
# 5 和 6 可以帮助调试连接错误。
# 9 表示极度冗余,输出非常详细的日志信息。
verb 4

# 忽略过多的重复信息
# 相同类别的信息只有前20条会输出到日志文件中
;mute 20

# 通知客户端,当服务器重新启动时,可以自动重新连接
# 只能是UDP协议使用,TCP使用的话不能启动服务
# 测试需要push到客户端才有效果
;explicit-exit-notify 1
push "explicit-exit-notify 1"

;push "block-outside-dns"         # Block access to any other DNS, is a Windows specific option

#定义客户端的DNS服务器地址
;push "dhcp-options DNS 192.168.228.1"

# 允许客户端重定向穿越VPN到外网, 对应客户端配置redirect-gateway def1
;push "redirect-gateway def1 bypass-dhcp"
```

## client

```bash
# 指定这是一个客户端,这将从服务器获取某些配置文件指令
client
dev tun
# 指定连接的服务器是采用TCP还是UDP协议
# 使用与服务器上相同的设置
proto udp

# 指定服务器的主机名(或IP)以及端口号
# 如果有多个VPN服务器,为了实现负载均衡,可以设置多个remote指令
remote my-server-1 1194
# 启用该指令,与服务器连接中断后将自动重新连接,
# 这在网络不稳定的情况下(例如: 笔记本电脑无线网络)非常有用
resolv-retry infinite
# 大多数客户端不需要绑定本机特定的端口号
nobind
# 持久化选项可以尽量避免访问在重启时由于用户权限降低而无法访问的某些资源
persist-key
# 无线网络通常会产生大量的重复数据包
# 设置此标识将忽略掉重复数据包的警告信息
mute-replay-warnings

# SSL/TLS参数配置
# 更多描述信息请参考服务器端配置文件
# 最好为每个客户端单独分配.crt/.key文件对
# 单个CA证书可以供所有客户端使用
ca ca.crt
cert client.crt
key client.key

# 通过检查证书具有正确的密钥使用设置来验证服务器证书
# 这是防止此处讨论的潜在攻击的重要预防措施: 
#  http://openvpn.net/howto.html#mitm
# 要使用此功能,EasyRSA生成服务器证书的时候进行相关设置
remote-cert-tls server

# 如果在服务器上使用tls-auth密钥,那么每个客户端也必须拥有密钥
tls-auth ta.key 1
# 或者单独配置 key-direction
;key-direction 1

# 选择一个加密算法,服务器使用的算法选项,也必须在这里指定它
# 注意,v2.4客户端/服务器将自动以TLS模式协商AES-256-GCM。
# 另请参阅手册中的ncp-cipher选项
cipher AES-256-GCM

redirect-gateway def1 #使客户端中所有流量经过VPN

compress lz4-v2
push "compress lz4-v2"：openvpn 2.4版本的vpn才能设置此选项。表示服务端启用lz4的压缩功能，传输数据给客户端时会压缩数据包，Push后在客户端也配置启用lz4的压缩功能，向服务端发数据时也会压缩。如果是2.4版本以下的老版本，则使用用comp-lzo指令
comp-lzo：启用lzo数据压缩格式。此指令用于低于2.4版本的老版本。且如果服务端配置了该指令，客户端也必须要配置
```

### start server

```bash
    chown openvpn:openvpn /etc/openvpn/server/*.*
    openvpn /etc/openvpn/server/pingd.conf
    systemctl start openvpn-server@pingd.service
    systemctl status  openvpn-server@pingd
```

### start client

    openvpn /etc/openvpn/server/client.conf

### OpenVPN 合并证书到配置文件中

删除或者注释以下几行内容:
ca ca.crt改为: #ca ca.crt
cert client.crt改为: #cert client.crt
key client.key改为: #key client.key
tls-auth ta.key 1改为: #tls-auth ta.key 1

在最后面添加以下内容

```r
    <ca>
    ca.crt 文件内容
    </ca>
    <cert>
    client.crt 文件内容
    </cert>
    <key>
    client.key 文件内容
    </key>
    key-direction 1
    <tls-auth>
    ta.key 文件内容
    </tls-auth>
```

### server端配置转发

```bash
url: ip-forward

iptables -t nat -A POSTROUTING -o wlp1s0 -j MASQUERADE
```

><https://wiki.archlinux.org/title/Easy-RSA>  
<https://wiki.archlinux.org/index.php/OpenVPN>  
<https://baike.baidu.com/item/OpenVPN/10718662?fr=aladdin>  

<https://www.xiaobo.li/notes/archives/1151>
