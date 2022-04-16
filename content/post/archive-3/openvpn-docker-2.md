---
title: openvpn docker
author: "-"
date: 2019-04-29T15:23:57+00:00
url: /?p=14273
categories:
  - Network
tags:
  - reprint
  - VPN
  - Docker
---
## openvpn docker
```bash
export  OVPN_DATA="ovpn-data"
docker volume create --name $OVPN_DATA
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_genconfig -u udp://home.wiloon.com
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn ovpn_initpki
docker run -v $OVPN_DATA:/etc/openvpn -d -p 192.168.50.220:1194:1194/udp --cap-add=NET_ADMIN --name openvpn --restart=always kylemanna/openvpn
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn easyrsa build-client-full client0 nopass
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_getclient client0 > client0.ovpn

# Retrieve the client configuration with embedded certificates
docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/rpi-openvpn ovpn_getclient client0 > client0.ovpn

docker run -v $OVPN_DATA:/etc/openvpn -p 1194:1194/udp --privileged -e DEBUG=1 kylemanna/rpi-openvpn

```

```bash
server 192.168.255.0 255.255.255.0
verb 3
key /etc/openvpn/pki/private/xxxx.key
ca /etc/openvpn/pki/ca.crt
cert /etc/openvpn/pki/issued/xxx.crt
dh /etc/openvpn/pki/dh.pem
tls-auth /etc/openvpn/pki/ta.key
key-direction 0
keepalive 10 60
persist-key
persist-tun

proto udp
# Rely on Docker to do port mapping, internally always 1194
port 1194
dev tun0
status /tmp/openvpn-status.log

user nobody
group nogroup
comp-lzo no

### Route Configurations Below
route 192.168.254.0 255.255.255.0

### Push Configurations Below
push "block-outside-dns"
push "dhcp-option DNS 192.168.50.1"
push "comp-lzo no"

push "redirect-gateway def1 bypass-dhcp"
```