---
title: easy-rsa
author: "-"
date: 2018-11-03T09:51:13+00:00
url: /?p=12853
categories:
  - Inbox
tags:
  - reprint
---
## easy-rsa

```bash
#debian
apt-get install easy-rsa
mkdir /etc/openvpn
cp -r /usr/share/easy-rsa /etc/openvpn/
cd /etc/easy-rsa
vim vars
./clean-all
./build-ca
./build-key-server server0
./build-key client0

#---
pacman -S easy-rsa
cd /etc/easy-rsa
export EASYRSA=$(pwd)
easyrsa init-pki
easyrsa build-ca

scp /etc/easy-rsa/pki/ca.crt foo@hostname-of-openvpn-server:/tmp/ca.crt

#OpenVPN server machine
mv /tmp/ca.crt /etc/openvpn/server/
chown root:root /etc/openvpn/server/ca.crt


```

[https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-debian-8](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-debian-8)
