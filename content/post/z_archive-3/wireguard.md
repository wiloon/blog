---
title: wireguard
author: "-"
date: 2022-07-31 13:54:01
url: wireguard
categories:
  - network
tags:
  - reprint
  - remix
  - VPN
  - Wireguard
---
## wireguard

wireguard default port: 51820

## install

### archlinux

archlinux 新版本的内核已经集成了 wireguard，不需要单独安装. 
已经集成了 wireguard 但是默认没加载, 需要配置一下启动的时候加载 wireguard 内核模块.

#### 手动加载模块

`sudo modprobe wireguard`

#### load kernel module at boot

```bash
vim /etc/modules-load.d/wireguard.conf

# content of wireguard.conf 
# load wireguard module at boot
wireguard
```

```bash
# 看看 wireguard 内核模块是不是已经加载了
lsmod | grep wireguard

pacman -Syu

# 安装 wireguard 管理工具, wireguard 集成进内核了, 但是管理工具还是要手动安装的
pacman -S wireguard-tools
```

### Debian

```bash
echo "deb http://deb.debian.org/debian/ unstable main" | sudo tee /etc/apt/sources.list.d/unstable-wireguard.list
printf 'Package: *\nPin: release a=unstable\nPin-Priority: 90\n' | sudo tee /etc/apt/preferences.d/limit-unstable
apt update
apt install wireguard
```

### macos

在 appstore 安装 wireguard  

## 生成密钥

peer A & peer B

```bash
# 同时生成私钥公钥
wg genkey | tee private.key | wg pubkey > public.key

# 单独生成私钥
wg genkey > private.key
chmod 600 private.key

# 单独生成公钥
wg pubkey < private.key > public.key

### optional, pre-shared key
wg genpsk > peer_A-peer_B.psk
```

### Peer A setup

假设 peer A 是服务端

#### 参数 allowed-ips

```bash
# 设置可以被路由到对端的 ip/段
allowed-ips

# 路由所有流量到对端
allowed-ips 0.0.0.0/0

# 路由指定 ip/段 到对端
allowed-ips 192.168.53.1/32

# 路由多个 ip/段 到对端
allowed-ips 192.168.53.1/32,192.168.50.0/24

# endpoint
对端的 ip 和端口
```

```bash
sudo ip link add dev wg0 type wireguard
sudo ip addr add 192.168.53.1/24 dev wg0
# 使用本端私钥
sudo wg set wg0 private-key ./private.key
sudo wg set wg0 listen-port 51900

# 做为服务端使用时，对端的 ip 和端口一般是动态的，所以不需要配置 endpoint
# PEER_B_PUBLIC_KEY = 对端公钥字符串
sudo wg set wg0 peer <PEER_B_PUBLIC_KEY> persistent-keepalive 25 allowed-ips 192.168.53.2/32
# 做为客户端时, 对端有确定的 IP 和端口时， 要配置对端的 endpoint
sudo wg set wg0 peer <PEER_B_PUBLIC_KEY> persistent-keepalive 25 allowed-ips 192.168.53.2/32  endpoint 192.168.50.115:9000

# set interface up
ip link set wg0 up
```

### peer B, client

```bash
sudo ip link add dev wg0 type wireguard
# ip 要改一下 ...
sudo ip addr add 192.168.53.2/24 dev wg0
sudo wg set wg0 private-key ./private.key

# 配置监听端口，监听 peer A 发起的连接请求，仅作为客户端使用时，可以不配置监听, 忽略此步骤
sudo wg set wg0 listen-port 9000 allowed-ips 0.0.0.0/0 peer_B

# allowed-ips 0.0.0.0/0 所有的 ip 包都 会被 发往 peer_A
# endpoint 对端的地址, ip 或域名
# PEER_A_PUBLIC_KEY 对端公钥
sudo wg set wg0 peer PEER_A_PUBLIC_KEY persistent-keepalive 25 allowed-ips 0.0.0.0/0 endpoint 192.168.50.215:9000
# set interface up
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

```bash
wg set wg0 peer PEER_A_PUBLIC_KEY remove
```

### 配置文件

```bash
/etc/wireguard/wg0.conf
```

#### 保存配置到文件

```bash
wg showconf wg0 > /etc/wireguard/wg0.conf
wg-quick up wg0
wg-quick down wg0
```

## systemd-networkd

```bash
systemd-networkd-wait-online.service
systemd-resolvconf  
openresolv
```

## ipv4 forward

>wiloon.com/ip-forward

### iptables, 设置 iptables 规则，客户端连接之后就能 Ping 通服务端局域网里的其它 ip 了

```bash
iptables -t filter -A FORWARD -i wg0 -j ACCEPT
# iptables -t nat    -A POSTROUTING -o <eth0> -j MASQUERADE
iptables -t nat    -A POSTROUTING -o ens18 -j MASQUERADE
iptables -t nat    -A POSTROUTING -o wlp1s0 -j MASQUERADE
```

## systemd-networkd, 用 systemd-networkd 配置 wireguard, 开机自动加载 wireguard 配置

```bash
vim /etc/systemd/network/99-wg0.network
```

```bash
[Match]
Name = wg0

[Network]
# wg0 网卡的 IP
Address = 192.168.53.1/32

[Route]
#配置路由表 目标地址是 192.168.53.0/24 发到 网关 192.168.53.1
Gateway = 192.168.53.1
Destination = 192.168.53.0/24
```

```bash
vim /etc/systemd/network/99-wg0.netdev
```

```bash
[NetDev]
Name = wg0
Kind = wireguard
Description = wireguard

[WireGuard]
ListenPort = 51900
# 本端私钥
PrivateKey = private-key-0

# 对端 A
[WireGuardPeer]
# 对端 A 公钥
PublicKey = public-key-0
# allowed-ips, 对端 A IP
AllowedIPs = 192.168.xx.xx/32

# 对端 B
[WireGuardPeer]
PublicKey = public-key-1
AllowedIPs = 192.168.xx.xx/32
```

#### restart to enable

```bash
systemctl restart systemd-networkd
```

### config router, add port forward config

## client

### android client

安装 wireguard
[https://f-droid.org/en/packages/com.wireguard.android/](https://f-droid.org/en/packages/com.wireguard.android/)  
点右下角的加号新建 连接  
输入连接名
点击私钥后面的刷新按钮 新建一对密钥
把公钥发给对端, 在服务端执行 wg set... 配置服务端

#### 客户端

局域网ip/address: 192.168.53.xx/32
监听端口/port: random
DNS servers: 192.168.50.1
listen port: random
mtu: auto

##### 添加节点/add peer

公钥: 服务端公钥
预共享密钥/pre-shared key (可以不填)
对端/endpoint: xxx.wiloon.com:51xxx
路由的ip地址: 0.0.0.0/0

### iOS client

1. Create from scratch
2. Name/名称: `<foo>`
3. Generate keypair/生成密钥对
4. 发送公钥到服务端
5. 配置 foo.netdev
6. Addresses/局域网IP地址: 192.168.54.x
7. Listen port/监听端口: 自动/Automatic
8. MTU: 1200
9. DNS: 192.168.50.1
10. Add peer/点击 添加节点 (配置对端)
11. 节点配置:
12. Public key/公钥: <服务端/对端公钥> (对端提供)
13. Preshared key/预共享密钥: 两端配置成一样的, 我一般不填
14. Endpoint/对端: foo.bar.com:12345
15. Allowed IPs/路由的IP地址(段): 0.0.0.0/0
16. Exclude private IPs: yes
17. 连接保活间隔(单位:秒): 不填

### chromeos > crostini

使用 android 版本的 wireguard
chromeos 从 google play 安装wireguard,连接成功后，vpn全局生效包括crostini里的linux也可以使用vpn通道

## windows

- 新建空隧道
  - 名称: pingd
  - 公钥: 自动生成的本端公钥

```bash
[Interface]
# 自动生成的私钥
PrivateKey = privateKey0
# 本端地址, 跟对端配置填成一样的
Address = 192.168.53.8/32
# DNS 可选字段, 配置之后 DNS 请求会发到这个地址
DNS = 192.168.50.1

[Peer]
# publicKey0: 服务端公钥, 对端公钥
PublicKey = publicKey0
AllowedIPs = 192.168.50.0/24, 192.168.53.0/24
# endpoint 配置了域名的时候, wireguard 建立连接时会先把域名解析成ip,再建连接,断网重连的时候直接用上一次的ip重连, 用DDNS的情况, ip变了之后会导致重连失败.
Endpoint = foo.bar.com:51900
# keep alive
PersistentKeepalive = 25
```

## network manager + wireguard

在 network manager 图标上点右键> edit connections...> add a new connection> choose a connection type> wireguard> create

- interface name: wg0
- private key: input private key

peers> Add>

- public key: `<public key>`
- allowed ips: 192.168.53.0/24

[https://www.xmodulo.com/wireguard-vpn-network-manager-gui.html](https://www.xmodulo.com/wireguard-vpn-network-manager-gui.html)

## openwrt wireguard

```bash
opkg update
opkg install luci-i18n-wireguard-zh-cn

```

### 配置

Network> interface> add new interface>Name: wg0> protocol: wireguard vpn> create interface

- general settings
  - private key: click "generate new key pair"
  - public key: click "generate new key pair"
  - ip address: 192.168.53.12
- peers> add peer
  - description: description0
  - 公钥: peer publick0
  - 允许的IP: 192.168.53.0/24
  - Route Allowed IPs: yes
  - endpoint host: xxx.xxx.xxx.xxx
  - endpoint port: 51900
  - persistent keep alive: 60

### openwrt 定时检查连接, 重启 wireguard

wireguard 只会在连接初始化的时候解析一次, 如果 ddns, 在 ip 更新 之后, wireguard 不会重连, 以下脚本定时检测连接, 有问题就重启 wireguard.

```bash
#!/bin/sh
# modified from https://openwrt.org/docs/guide-user/base-system/cron
# modified to use logger for global logging instead of scriptlogfile & added infinite reboot protection for reboot
# Prepare vars
DATE=$(date +%Y-%m-%d" "%H:%M:%S)
#logFile="/persistlogs/syslog"

# Ping and reboot if needed

#YOUR WIREGUARD PEER
CHECKHOSTNAME="192.168.53.1"

notification_email="wiloon.wy@gmail.com"
VPNINTERFACE="wg0"

ping -c3 $CHECKHOSTNAME

if [ $? -eq 0 ]; then
    echo "ok"
    logger $(echo "${DATE} - $0: OK - $VPNINTERFACE UP AND RUNNING")
else
    echo "RESTART wgvpn0 Interface"
    logger $(echo "${DATE} - $0: NO VPN CONNECTION RESTART $VPNINTERFACE INTERFACE...")
    # Note: To avoid infinite reboot loop, wait 70 seconds and touch a file in /etc
    ifdown $VPNINTERFACE
    ifup $VPNINTERFACE
    echo Subject: $0: VPN $VPNINTERFACE has been restarted | sendmail -v "$notification_email"
fi
```

[https://forum.openwrt.org/t/restart-wireguard-via-cli/51935/10](https://forum.openwrt.org/t/restart-wireguard-via-cli/51935/10)

---

[https://www.whosneo.com/wireguard-openwrt-ipv6/](https://www.whosneo.com/wireguard-openwrt-ipv6/)

### crostini

~~crostini 不支持wireguard 类型的网络设备， 不能直接使用wireguard, 需要安装tunsafe~~
~~[https://tunsafe.com/user-guide/linux](https://tunsafe.com/user-guide/linux)~~

### ~~tunsafe  安装~~

```bash
    /etc/wireguard/wg0.conf

    git clone https://github.com/TunSafe/TunSafe.git
    cd TunSafe
    sudo apt-get install clang-6.0
    make
    sudo make install
    sudo tunsafe start  TunSafe.conf
    sudo tunsafe start -d TunSafe.conf
```

#### ~~tunsafe 配置文件(废弃)~~

```bash
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
```

### chromeos>crostini

chromeos从 google play 安装wireguard,连接成功后，vpn全局生效包括crostini里的linux也可以使用vpn通道

又ccighervkevururvkfggtlhrvtuclinuntecvikn

~~crostini 不支持wireguard 类型的网络设备， 不能直接使用wireguard, 需要安装tunsafe~~

~~[https://tunsafe.com/user-guide/linux](https://tunsafe.com/user-guide/linux)~~

---

[https://www.wireguard.com/install/](https://www.wireguard.com/install/)
[https://www.linode.com/docs/networking/vpn/set-up-wireguard-vpn-on-debian/](https://www.linode.com/docs/networking/vpn/set-up-wireguard-vpn-on-debian/)
[https://blog.mozcp.com/wireguard-usage/](https://blog.mozcp.com/wireguard-usage/)
[https://mine260309.me/archives/1697](https://mine260309.me/archives/1697)
[https://mine260309.me/archives/1697/embed#?secret=3eFM6gPGdn](https://mine260309.me/archives/1697/embed#?secret=3eFM6gPGdn)
[https://wiki.debian.org/Wireguard](https://wiki.debian.org/Wireguard)
[https://docs.linuxconsulting.mn.it/notes/setup-wireguard-vpn-on-debian9](https://docs.linuxconsulting.mn.it/notes/setup-wireguard-vpn-on-debian9)
[https://github.com/wgredlong/WireGuard/blob/master/2.%E7%94%A8%20wg-quick%20%E8%B0%83%E7%94%A8%20wg0.conf%20%E7%AE%A1%E7%90%86%20WireGuard.md](https://github.com/wgredlong/WireGuard/blob/master/2.%E7%94%A8%20wg-quick%20%E8%B0%83%E7%94%A8%20wg0.conf%20%E7%AE%A1%E7%90%86%20WireGuard.md)
