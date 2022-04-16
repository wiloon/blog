---
title: raspberry pi openvpn docker
author: "-"
date: 2018-11-27T05:28:13+00:00
url: /?p=12939
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## raspberry pi openvpn docker
```bash
export  OVPN_DATA="ovpn-data"
docker volume create --name $OVPN_DATA
# volume默认位置: /var/lib/docker/volumes/ovpn-data

# gen config
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm mjenz/rpi-openvpn ovpn_genconfig -u udp://xxx.wiloon.com

# init pki
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm -it mjenz/rpi-openvpn ovpn_initpki

# start server
docker run -v $OVPN_DATA:/etc/openvpn -d -p 192.168.100.230:1194:1194/udp --cap-add=NET_ADMIN --name openvpn --restart=always mjenz/rpi-openvpn

#Generate a client certificate
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm -it mjenz/rpi-openvpn easyrsa build-client-full client0 nopass

# Retrieve the client configuration with embedded certificates
docker run -v $OVPN_DATA:/etc/openvpn --rm mjenz/rpi-openvpn ovpn_getclient client0 > client0.ovpn

docker run -v $OVPN_DATA:/etc/openvpn -p 1194:1194/udp --privileged -e DEBUG=1 mjenz/rpi-openvpn

```

https://github.com/mje-nz/rpi-docker-openvpn
  
https://github.com/kylemanna/docker-openvpn
  
http://blog.51cto.com/kisszero/1894076