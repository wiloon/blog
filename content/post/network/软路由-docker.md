---
author: "-"
date: "2020-08-03 23:17:25" 
title: "软路由, docker"
categories:
  - inbox
tags:
  - reprint
---
## "软路由, docker"

### 

    docker network create -d macvlan \
        --subnet=192.168.50.0/24 --gateway=192.168.50.1 \
        -o parent=enp1s0 \
        -o macvlan_mode=bridge \
        macvlan

    docker network create -d macvlan \
        --subnet=192.168.254.0/24 --gateway=192.168.254.1 \
        --ipv6 --subnet=fe81::/16 --gateway=fe81::1 \
        -o parent=enp1s0 \
        -o macvlan_mode=bridge \
        dMACvWAN


### 导入镜像
    docker import  openwrt-19.07.2-x86-64-generic-rootfs.tar.gz openwrt:17.07.2

### docker run

    docker run -d \
        --network macvlan \
        --privileged \
        --name openwrt \
        openwrt:17.07.2 \
        /sbin/init