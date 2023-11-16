---
title: Mac OS X 中设置VPN静态路由
author: "-"
date: 2014-12-25T10:54:44+00:00
url: macos/route
categories:
  - Inbox
tags:
  - OS X

---
## Mac OS X 中设置 VPN 静态路由, macos route

```bash
sudo route -n add -net 192.168.5.4 -netmask 255.255.255.0 xxx.xxx.200.1
```

[https://blog.hackroad.com/apple/mac-os/7011.html](https://blog.hackroad.com/apple/mac-os/7011.html)

mac osx Lerpard 中, 使用内置的pptp client端拨号成功后,
  
所有的网络连接均走vpn路线,
  
这样校内的网站也走这个了,
  
导致速度缓慢, 校内连接终端等

解决方法是: 手动设置路由表, 以我的实际情况为例:
  
在windows下,我需要设置如下3条静态路由(首条0.0.0.0为default)

route -p add 0.0.0.0      mask 0.0.0.0       10.13.31.1   (我的校园网网关是这个)
route -p add 10.0.0.0     mask 255.0.0.0     10.13.31.1
route -p add 210.32.0.0   mask 255.255.240.0   10.13.31.1
route -p add 222.205.0.0 mask 255.255.128.0   10.13.31.1

在Mac OSX 中, 设置路由的命令稍有不同, 为:

route -n add defalut     10.13.31.1
route -n add   -net 10.0.0.0/8      10.13.31.1
route -n add -net 210.32.0.0/20   10.13.31.1
route -n add -net 222.205.0.0/17 10.13.31.1

或者用如下的比较明了的命令也可以:
  
例:route -n add -net   210.32.0.0 -netmask 255.255.240.0   10.13.31.1

在linux下的命令又不太一样, 如下:

route add default gw   10.13.31.1
route -n add   -net 10.0.0.0/8      gw 10.13.31.1
route -n add -net 210.32.0.0/20   gw 10.13.31.1
route -n add -net 222.205.0.0/17 gw   10.13.31.1

设置好如上静态路由, 就可以VPN内网外网访问无阻啦.
  
因为*nix的route命令没有 -p 选项(设置为静态路由),
  
重启后, 设置的3条路由又无效了, 必须重新运行命令,比较麻烦.
  
写成脚本, 每次开机运行下, 是一个方法.

Mac OSX 中可以设置成启动项, 每次开机自动运行, 方法是:
  
1. 在H:\Library\StartupItems\ 下新建一个目录, 比如命名为 SetRoutes
  
2. 在 SetRoutes目录下新建一个文本文件(比如命名为SetRoute),写上脚本程序如下:
  
============================================

        #!/bin/sh

# Set up static routing tables

# Roark Holz, Thursday, April 6, 2006

. /etc/rc.common

StartService ()
{
        ConsoleMessage "Adding Static Routing Tables"
        route -n add -net 10.0.0.0/8      10.13.31.1
        route -n add -net 210.32.0.0/20   10.13.31.1
        route -n add -net 222.205.0.0/17 10.13.31.1
}

StopService ()
{
        return 0
}

RestartService ()
{
        return 0
}

RunService "$1"

==================================================

注意更换其中的 route add 为你自己的命令.

3. 新建一个 StartupParameters.plist 文件, 指定命令参数,内容如下:
  
===================================

        {
        Description     = "Set static routing tables";
        Provides        = ("SetRoutes");
        Requires        = ("Network");
        OrderPreference = "None";
}

====================================

4. 修复磁盘权限, chmod 755 * 重启, OK!

以上在 Mac OSX 10.5.5 Leopard 中试验通过.
