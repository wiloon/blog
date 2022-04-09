---
title: wireguard
author: "-"
date: 2020-03-15T16:20:26+00:00
url: wireguard
categories:
  - network
tags:
  - reprint
  - remix
  - vpn
---
## wireguard

## install

### archlinux

archlinux 如果使用的是新版本的内核的话，就不需要单独安装 wireguard 了， wireguard 已经被集成进了内核。

```bash
pacman -Syu
# 安装 wireguard 管理工具
pacman -S wireguard-tools

lsmod | grep wireguard
sudo modprobe wireguard
```

### debian

```bash
echo "deb http://deb.debian.org/debian/ unstable main" | sudo tee /etc/apt/sources.list.d/unstable-wireguard.list
printf 'Package: *\nPin: release a=unstable\nPin-Priority: 90\n' | sudo tee /etc/apt/preferences.d/limit-unstable
apt update
apt install wireguard
```

### 生成密钥 peer A & peer B

```bash
# 生成私钥
wg genkey > peer_A.key
chmod 600 peer_A.key
# 生成公钥
wg pubkey < peer_A.key > peer_A.pub

# 同时生成私钥公钥
wg genkey | tee peer_A.key | wg pubkey > peer_A.pub

### optional, pre-shared key
wg genpsk > peer_A-peer_B.psk
```

### 参数

```bash
# 设置可以被路由到对端的ip/段
allowed-ips

# 路由所有流量到对端
allowed-ips 0.0.0.0/0

# 路由指定ip/段到对端
allowed-ips 192.168.53.1/32

# 路由多个ip/段到对端 
allowed-ips 192.168.53.1/32,192.168.50.0/24

# endpoint
对端的ip和端口
```

#### Peer A setup

```bash
sudo ip link add dev wg0 type wireguard
sudo ip addr add 192.168.53.1/24 dev wg0
sudo wg set wg0 private-key ./peer_A.key
sudo wg set wg0 listen-port 51900

# peer A 做为服务端使用时，peer_B 的ip 和端口一般是动态的，所以peer A 不配置 endpoint  
sudo wg set wg0 peer <PEER_B_PUBLIC_KEY> persistent-keepalive 25 allowed-ips 192.168.53.2/32
# peer b 有确定的端口和IP时， peer A 可以配置endpoint
sudo wg set wg0 peer <PEER_B_PUBLIC_KEY> persistent-keepalive 25 allowed-ips 192.168.53.2/32  endpoint 192.168.50.115:9000

### set interface up
ip link set wg0 up
```

### peer B

```bash
sudo ip link add dev wg0 type wireguard
# ip要改一下...
sudo ip addr add 192.168.53.2/24 dev wg0
sudo wg set wg0 private-key ./privatekey

# 配置监听端口，监听 peer A 发起的连接请求，仅作为客户端使用时，可以不配置监听, 忽略此步骤
sudo wg set wg0 listen-port 9000 allowed-ips 0.0.0.0/0 peer_B 

# 所有的ip包都 会被 发往 peer_A
# endpoint 对端的地址,ip或域名
# PEER_A_PUBLIC_KEY 对端公钥
sudo wg set wg0 peer PEER_A_PUBLIC_KEY persistent-keepalive 25 allowed-ips 0.0.0.0/0 endpoint 192.168.50.215:9000
sudo ip link set wg0 up
```

### 添加路由

```bash
# ipv4
ip route add 192.168.50.0/24 dev wg0
# ipv6
ip route add fd7b:d0bd:7a6e::/64 dev wg0
```

### remove peer

    wg set wg0 peer PEER_A_PUBLIC_KEY remove  

### 配置文件

    /etc/wireguard/wg0.conf

#### 保存配置到文件

    wg showconf wg0 > /etc/wireguard/wg0.conf
    wg-quick up wg0
    wg-quick down wg0

### systemd-networkd

    systemd-networkd-wait-online.service
    systemd-resolvconf  
    openresolv

### iptables, 设置iptables规则，客户端连接之后就能Ping通服务端局域网里的其它ip了。

    iptables -A FORWARD -i wg0 -j ACCEPT
    iptables -t nat -A POSTROUTING -o <eth0> -j MASQUERADE
    iptables -t nat -A POSTROUTING -o wlp1s0 -j MASQUERADE

### systemd-networkd, 用 systemd-networkd 配置 wireguard,开机自动加载 wireguard 配置

#### vim /etc/systemd/network/99-wg0.netdev

    [NetDev]
    Name = wg0
    Kind = wireguard
    Description = wireguard

    [WireGuard]
    ListenPort = 51900
    PrivateKey = private-key-0

    [WireGuardPeer]
    PublicKey = public-key-0
    AllowedIPs = 192.168.xx.xx/32 

    [WireGuardPeer]
    PublicKey = public-key-1
    AllowedIPs = 192.168.xx.xx/32 

#### vim /etc/systemd/network/99-wg0.network

    [Match]
    Name = wg0

    [Network]
    Address = 192.168.53.1/32

    [Route]
    Gateway = 192.168.53.1
    Destination = 192.168.53.0/24

### config router, add port forward config

## client

### android client

安装wireguard
https://f-droid.org/en/packages/com.wireguard.android/  
点右下角的加号新建 连接  
输入连接名 
点击私钥后面的刷新按钮 新建一对密钥
把公钥发给对端, 在服务端执行wg set... 配置服务端

#### 客户端
局域网ip/address: 192.168.53.xx/32
端口/port: random
DNS servers: 192.168.50.1
listen port: random
mtu: auto

##### 添加节点/add peer
公钥:  服务端公钥
预共享密钥/pre-shared key (可以不填)
对端/endpoint: xxx.wiloon.com:51xxx
路由的ip地址: 0.0.0.0/0

### IOS client
1. Create from scratch
2. Name/名称: <foo>
3. Generate keypair/生成密钥对
4. 发送公钥到服务端
5. 配置 foo.netdev
6. Addresses/局域网IP地址: 192.168.54.x
7. Listen port/监听端口:自动
8. MTU: 1200
9. DNS: 192.168.50.1
10. Add peer/点击 添加节点
11. 节点配置:
12. Public key/公钥: <服务端/对端公钥>
13. Preshared key/预共享密钥: 不填
14. Endpoint/对端: foo.bar.com:12345
15. Allowed IPs/路由的IP地址(段): 0.0.0.0/0
16. Exclude private IPs: yes
17. 连接保活间隔(单位:秒): 不填

### chromeos > crostini

使用 android 版本的 wireguard
chromeos 从 google play 安装wireguard,连接成功后，vpn全局生效包括crostini里的linux也可以使用vpn通道

### win 11

- 新建空隧道
  - 名称: pingd
  - 公钥: 自动生成的本端公钥

```bash
[Interface]
PrivateKey = privateKey0
Address = 192.168.53.8/32
DNS = 192.168.50.1

[Peer]
PublicKey = publicKey0
AllowedIPs = 192.168.50.0/24, 192.168.53.0/24
Endpoint = foo.bar.com:51900
# endpoint 配置了域名的时候, wireguard 建立连接时会先把域名解析成ip,再建连接,断网重连的时候直接用上一次的ip重连, 用DDNS的情况, ip变了之后会导致重连失败.
```

---

### crostini
~~crostini 不支持wireguard 类型的网络设备， 不能直接使用wireguard, 需要安装tunsafe~~
~~<https://tunsafe.com/user-guide/linux>~~

### ~~tunsafe  安装~~
    /etc/wireguard/wg0.conf

    git clone https://github.com/TunSafe/TunSafe.git
    cd TunSafe
    sudo apt-get install clang-6.0
    make
    sudo make install
    sudo tunsafe start  TunSafe.conf
    sudo tunsafe start -d TunSafe.conf


#### ~~tunsafe 配置文件(废弃)~~ 

    [Interface]
    PrivateKey = <private_key>
    DNS = 192.168.50.1
    BlockDNS = true

    # 设置虚拟网卡的内网地址 (可选子网掩码) 
    Address = 192.168.53.3/24
    ;/l.4r5t3677777777
    [Peer]
    PublicKey = <public_key>

    # 目标地址是192.168.53.1 的会通过vpn发送到服务端
    AllowedIPs = 192.168.53.1/24

    # 所有ip包都 会发往 vpn服务端
    AllowedIPs = 0.0.0.0/0
    Endpoint = <server_ip0:server_port0>
    PersistentKeepalive = 25

### chromeos>crostini
chromeos从 google play 安装wireguard,连接成功后，vpn全局生效包括crostini里的linux也可以使用vpn通道
又ccighervkevururvkfggtlhrvtuclinuntecvikn
~~crostini 不支持wireguard 类型的网络设备， 不能直接使用wireguard, 需要安装tunsafe~~
~~<https://tunsafe.com/user-guide/linux>~~  
---

https://www.wireguard.com/install/
https://www.linode.com/docs/networking/vpn/set-up-wireguard-vpn-on-debian/
https://blog.mozcp.com/wireguard-usage/
https://mine260309.me/archives/1697
https://mine260309.me/archives/1697/embed#?secret=3eFM6gPGdn
https://wiki.debian.org/Wireguard
https://docs.linuxconsulting.mn.it/notes/setup-wireguard-vpn-on-debian9
https://github.com/wgredlong/WireGuard/blob/master/2.%E7%94%A8%20wg-quick%20%E8%B0%83%E7%94%A8%20wg0.conf%20%E7%AE%A1%E7%90%86%20WireGuard.md