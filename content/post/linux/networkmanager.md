---
author: "-"
date: 2026-02-18T11:53:33+08:00
title: "network manager"
url: networkmanager
categories:
  - inbox
tags:
  - reprint
  - remix
  - AI-assisted
---
## "network manager"

```bash
sudo pacman -S networkmanager
sudo systemctl status NetworkManager.service
sudo systemctl start NetworkManager.service
sudo systemctl restart NetworkManager.service
sudo pacman -S nm-connection-editor
sudo pacman -S network-manager-applet

nmcli device
nmcli connection
nmcli c delete
```

### System policy prevents control of network connections

System policy prevents control of network connections
System policy prevents modification of network settings for all users<

vim /usr/share/polkit-1/actions/org.freedesktop.NetworkManager.policy

Open /usr/share/polkit-1/actions/org.freedesktop.NetworkManager.policy with root/sudo privileges and search for the following line:

System policy prevents modification of network settings for all users
A few lines below that should be this:

auth_admin_keep</allow_active>
Change it to:

yes</allow_active>
Save the file and restart your computer.

设置取值有:
no
Not authorized.
yes
Authorized.
auth_self
Authentication by the owner of the session that the client originates from is required.

auth_admin

Authentication by an administrative user is required.

auth_self_keep

Like auth_self but the authorization is kept for a brief period (e.g. five minutes).

auth_admin_keep

Like auth_admin but the authorization is kept for a brief period (e.g. five minutes).

典型的场景是把allow_active的设置从auth_admin (root密码) 改成auth_self (当前用户密码) 或者yes (不要密码) 。

### 配置文件

```bash
/etc/NetworkManager/NetworkManager.conf
/etc/NetworkManager/system-connections
```

### network manager + openvpn 多个默认路由的问题

IPv4 Settings->Routes and checking "Use this connection only for resources on its network".
[https://www.debuntu.org/how-to-network-manager-openvpn-overwrites-default-route/](https://www.debuntu.org/how-to-network-manager-openvpn-overwrites-default-route/)

### DNS

```bash
vim /etc/NetworkManager/NetworkManager.conf

# add following lines
[main]
dns=systemd-resolved

```

使用 systemd-resolved, networkmanager 会把 /etc/resolv.conf 设置成 127.0.0.1:53, 当然 systemd-resolved  要配置成 DNSStubListener=yes 开启本地的 53 端口, 这样 dns 请求就交给 systemd-resolved 处理了.

[https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/configuring-the-order-of-dns-servers_configuring-and-managing-networking](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/configuring-the-order-of-dns-servers_configuring-and-managing-networking)

## 禁用 NetworkManager，改用 systemd-networkd（Arch Linux）

```bash
# 停止并禁用 NetworkManager
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager

# 启用并启动 systemd-networkd
sudo systemctl enable --now systemd-networkd

# 启用并启动 systemd-resolved（可选，用于 DNS 解析）
sudo systemctl enable --now systemd-resolved

# 将 /etc/resolv.conf 指向 systemd-resolved 的存根
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

配置网络接口，在 `/etc/systemd/network/` 目录下创建 `.network` 文件，例如有线接口 DHCP 配置：

```ini
# /etc/systemd/network/20-wired.network
[Match]
Name=en*

[Network]
DHCP=yes
```

静态 IP 示例：

```ini
# /etc/systemd/network/20-wired.network
[Match]
Name=enp3s0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=1.1.1.1
```

创建配置后重启服务：

```bash
sudo systemctl restart systemd-networkd
```
