---
title: openwrt basic, opkg basic, ipk
author: "-"
date: 2018-07-26T05:04:27+00:00
url: openwrt
categories:
  - network
tags:
  - reprint
  - HomeLab
  - openwrt
---
## openwrt basic, opkg basic, ipk

### wan dns

在wan口设置里的“高级设置”选项里去掉"使用端局通告的DNS服务器"的勾选就可以使用自定义的DNS服务器

### ssh port

   vim /etc/init.d/dropbear

   validate_section_dropbear > port

### ssh public key

   vim /etc/dropbear/authorized_keys

### dns 配置

查看本机的 DNS 配置:

$ cat /etc/resolv.conf
search lan
nameserver 127.0.0.1
发现使用的是本机 DNS 服务器,即 dnsmasq。

查看 dnsmasq 配置:

$ cat /etc/dnsmasq.conf

#### 手动指定上游dns vi /etc/dnsmasq.conf

```bash
server=223.5.5.5
server=223.6.6.6
```

### openwrt 改IP

```bash
vi /etc/config/network
```

### opwnert init

```bash
opkg install coreutils-nohup
opkg install ipset
opkg remove dnsmasq
opkg install dnsmasq-full
```

### openwrt cron

```bash
/etc/init.d/cron start
/etc/init.d/cron enable
crontab -e
crontab -l
```

### x86, firmware download

<https://downloads.openwrt.org/releases/19.07.6/targets/x86/>

#### 64 (推荐使用)

64用于现代PC硬件 (大约在2007年以后的产品) ,它是为具有64位功能的计算机而构建的,并支持现代CPU功能。除非有充分的理由,否则请选择此选项。

### Generic  

仅适用于32位硬件 (旧硬件或某些Atom处理器) ,应为i586 Linux体系结构,将在Pentium 4及更高版本上运行。仅当您的硬件无法运行64位版本时才使用此功能。

### Legacy

用于奔腾4之前的非常旧的PC硬件,在Linux体系结构支持中称为i386。它会错过许多现代硬件上想要/需要的功能,例如多核支持以及对超过1GB RAM的支持,但实际上会在较旧的硬件上运行,而其他版本则不会。

### Geode

是为Geode SoC定制的自定义旧版目标,Geode SoC仍在许多 (老化的) 网络设备中使用,例如PCEngines的较旧Alix板

### x86/64/

#### combined-ext4.img.gz (推荐使用)

包含 vmlinuz rootfs (ext4), 引导信息以及相关分区信息的 img, 一般是两个分区, 可以把它看成是硬盘镜像, 直接 dd 到某个磁盘
此磁盘映像使用单个读写ext4分区, 没有只读 squashfs 根文件系统, 因此可以扩大分区。故障安全模式或出厂重置等功能将不可用, 因为它们需要只读的 squashfs 分区才能起作用。

#### Combined-squashfs.img.gz

该磁盘映像使用传统的OpenWrt布局,一个squashfs只读根文件系统和一个读写分区,在其中存储您安装的设置和软件包。由于此映像的组装方式,您只有230 兆MB的空间来存储其他程序包和配置,而Extroot不起作用。

#### rootfs-ext4.img.gz

rootfs分区镜像,可以直接dd到某个分区,或者mount -o到某个目录

#### rootfs-squashfs.img.gz

同上

#### vmlinuz

kernel

#### generic-rootfs.tar.gz

rootfs用gz打包后的文件

要让系统启动,需要引导器 (x86是使用grub,好比是路由中的uboot,当然uboot管的内容更多) 、kernel、rootfs三者。

### mirror

sed -i 's_downloads.openwrt.org_mirrors.tuna.tsinghua.edu.cn/openwrt_' /etc/opkg/distfeeds.conf

### 安装证书

openwrt 里访问 使用let's encrypt 签发的证书站点报错:  

    x509: certificate signed by unknown authority

安装最新的 ca-certificates 包也解决不了, 可能是因为 ca-certificates 里也没有 let's encrypt 的根证书。  
浏览器访问站点手动导出证书后放到这个目录下解决。

    vim vim /etc/ssl/certs/foo.crt
<https://blog.csdn.net/xushx_bigbear/article/details/47746285>
  
<https://blog.csdn.net/lee244868149/article/details/57076615>

### openwrt lan 改网段

<https://www.cnblogs.com/double-win/p/3841017.html>

```bash
  
vim /etc/config/network

config 'interface' 'lan' #LAN口,用于路由器子网设置
          
option 'ifname' 'eth0'
          
option 'type' 'bridge'
          
option 'proto' 'static'
          
option 'ipaddr' '192.168.99.1'
          
option 'netmask' '255.255.255.0'

```

### mirror

    sed -i 's_downloads.openwrt.org_mirrors.tuna.tsinghua.edu.cn/openwrt_' /etc/opkg/distfeeds.conf

### build

clone <https://github.com/openwrt/openwrt.git>
  
apt-get install make
  
binutils
  
gcc
  
g++

### odhcpd

odhcpd 是openwrt 默认的dhcp服务
  
配置文件: /etc/config/dhcp

### init script

```bash
vim /etc/init.d/foo

#!/bin/sh /etc/rc.common
# Example script
# Copyright (C) 2007 OpenWrt.org

START=10
STOP=15

start() {        
        echo start
        # commands to launch application
}                 

stop() {          
        echo stop
        # commands to kill application 
}
```

### opkg

opkg 工具 (一个 ipkg 变种) 是一个用来从本地软件仓库或互联网软件仓库上下载并安装 OpenWrt 软件包的轻量型软件包管理器。

```bash
opkg list # 获取软件列表
opkg update # 更新可以获取的软件包列表
opkg upgrade # 对已经安装的软件包升级
opkg install xxx.ipk # 安装本地的软件包
opkg remove xxx
```

### 自定义防火墙规则

    /etc/firewall.user

### 系统防火墙规则

    /etc/config/firewall

#### 端口转发

config redirect
        option dest_port '80'
        option src 'wan'
        option name 'bpa'
        option src_dport '8888'
        option target 'DNAT'
        option dest_ip '192.168.96.1'
        option dest 'lan'

### 查看日志

logread

### 启动脚本位置

    /etc/rc.d

### openwrt添加开机运行脚本

openwrt添加开机运行脚本
进入/etc/init.d/目录创建脚本test

    vim test

在/etc/init.d/test中按照以下格式编写shell脚本

    #!/bin/sh /etc/rc.common
    START=99
    STOP=15

    start() {
        ip rule add fwmark 2 table 200
    }

START的值决定这个脚本的启动顺序,这里为99
start()里执行增加的功能脚步或者写脚本启动自己的程序
3.给脚本添加可执行权限

    chmod +x test

#### 创建一个软链接

    /etc/init.d/test enable
---

<https://wiki.openwrt.org/zh-cn/doc/techref/opkg>  
<https://blog.csdn.net/whatday/article/details/78920494>  
<https://wiki.openwrt.org/doc/techref/odhcpd>  
<https://openwrt.proxy.ustclug.org/>  
<https://mirrors.ustc.edu.cn/help/lede.html>  
<https://openwrt.org/>
<https://hub.docker.com/u/openwrtorg>
<https://hub.docker.com/r/openwrtorg/rootfs>
<https://openwrt.club/93.html>
<https://openwrt.org/docs/techref/initscripts>
<https://blog.csdn.net/weixin_42512245/article/details/88602272>
