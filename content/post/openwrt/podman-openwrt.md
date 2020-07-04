---
title: "podman openwrt"
date: 2020-05-03T11:59:36Z
---

https://openwrt.org/
https://hub.docker.com/u/openwrtorg
https://hub.docker.com/r/openwrtorg/rootfs
```bash
podman run -it --name openwrt --hostname openwrt openwrtorg/rootfs:x86-64 /bin/sh
```

### openwrt mirror
https://mirrors.tuna.tsinghua.edu.cn/help/openwrt/
sed -i 's_downloads.openwrt.org_mirrors.tuna.tsinghua.edu.cn/openwrt_' /etc/opkg/distfeeds.conf

### 宿主机配置
#### 打开网卡混杂模式
```bash
ip link set enp1s0 promisc on
```

#### 网络
/etc/network/interfaces 不是systemd-networkd的配置文件，如果使用systemd-networkd要把 /etc/network/interfaces 备份删除。

```bash
podman network create --subnet=192.168.50.0/24 --gateway=192.168.50.1 --macvlan=enp1s0 mac1
cat /etc/cni/net.d/mac1.conflist
```

```bash
podman run -itd --name c1 --ip=192.168.50.99 --network mac1 busybox
```