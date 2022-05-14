---
author: "-"
date: "2020-07-17 17:13:21" 
title: "network manager"
categories:
  - inbox
tags:
  - reprint
---
## "network manager"

    sudo pacman -S networkmanager
    sudo systemctl start NetworkManager.service
    sudo pacman -S nm-connection-editor
    sudo pacman -S network-manager-applet

    nmcli device
    nmcli connection
    nmcli c delete


### System policy prevents control of network connections
System policy prevents control of network connections
System policy prevents modification of network settings for all users<

vim /usr/share/polkit-1/actions/org.freedesktop.NetworkManager.policy

Open /usr/share/polkit-1/actions/org.freedesktop.NetworkManager.policy with root/sudo privileges and search for the following line:

<message>System policy prevents modification of network settings for all users</message>
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

    /etc/NetworkManager/system-connections

### network manager + openvpn 多个默认路由的问题
IPv4 Settings->Routes and checking "Use this connection only for resources on its network".
https://www.debuntu.org/how-to-network-manager-openvpn-overwrites-default-route/