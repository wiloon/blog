---
title: openwrt basic, opkg basic, ipk
author: "-"
date: 2022-08-11 08:27:40
url: openwrt
categories:
  - Network
lastmod: 2026-06-12T10:21:41+08:00
tags:
  - remix
  - AI-assisted
  - HomeLab
  - OpenWrt
  - Ansible
---
## openwrt basic, opkg basic, ipk

## commands

```bash
# 查看 openwrt 版本
cat /etc/openwrt_release

# 更新所有软件，包括 OpenWRT 内核、固件等
opkg list-upgradable | cut -f 1 -d ' ' | xargs opkg upgrade
```

### wan dns

在 wan 口设置里的“高级设置”选项里去掉"使用端局通告的DNS服务器"的勾选就可以使用自定义的DNS服务器

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

#### 手动指定上游 dns vi /etc/dnsmasq.conf

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

[https://downloads.openwrt.org/releases/19.07.6/targets/x86/](https://downloads.openwrt.org/releases/19.07.6/targets/x86/)

#### targets

- wndr4300, [https://downloads.openwrt.org/releases/22.03.5/targets/ath79/nand/openwrt-22.03.5-ath79-nand-netgear_wndr4300-squashfs-factory.img](https://downloads.openwrt.org/releases/22.03.5/targets/ath79/nand/openwrt-22.03.5-ath79-nand-netgear_wndr4300-squashfs-factory.img)

#### 64 (推荐使用)

64 用于现代 PC 硬件 (大约在 2007 年以后的产品), 它是为具有 64 位功能的计算机而构建的, 并支持现代 CPU 功能。除非有充分的理由,否则请选择此选项。

### Generic  

仅适用于32位硬件 (旧硬件或某些Atom处理器) ,应为i586 Linux体系结构,将在Pentium 4及更高版本上运行。仅当您的硬件无法运行64位版本时才使用此功能。

### Legacy

用于奔腾4之前的非常旧的PC硬件,在Linux体系结构支持中称为i386。它会错过许多现代硬件上想要/需要的功能,例如多核支持以及对超过1GB RAM的支持,但实际上会在较旧的硬件上运行,而其他版本则不会。

### Geode

是为Geode SoC定制的自定义旧版目标,Geode SoC仍在许多 (老化的) 网络设备中使用,例如PCEngines的较旧Alix板

### x86/64/

### openwrt-24.10.0-x86-64-generic-ext4-combined-efi (推荐使用)

generic-ext4-combined-efi.img.gz:

- 这个镜像包含了对 UEFI (统一可扩展固件接口) 启动支持的配置。UEFI 是 BIOS 的现代替代品，提供更加强大的启动和系统管理功能。
- 设备使用这个镜像可以在支持 UEFI 启动的硬件上启动。这通常包括现代的个人电脑和一些新型号的嵌入式设备。
  
#### combined-ext4.img.gz

包含 vmlinuz rootfs (ext4), 引导信息以及相关分区信息的 img, 一般是两个分区, 可以把它看成是硬盘镜像, 直接 dd 到某个磁盘
此磁盘映像使用单个读写 ext4 分区, 没有只读 squashfs 根文件系统, 因此可以扩大分区。故障安全模式或出厂重置等功能将不可用, 因为它们需要只读的 squashfs 分区才能起作用。

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

### openwrt 安装证书

openwrt 里访问 使用 let's encrypt 签发的证书站点报错:  

x509: certificate signed by unknown authority

安装最新的 ca-certificates 包也解决不了, 可能是因为 ca-certificates 里也没有 let's encrypt 的根证书。
浏览器访问站点手动导出证书后放到这个目录下解决。

```bash
vim /etc/ssl/certs/foo.crt
```

[https://blog.csdn.net/xushx_bigbear/article/details/47746285](https://blog.csdn.net/xushx_bigbear/article/details/47746285)
  
[https://blog.csdn.net/lee244868149/article/details/57076615](https://blog.csdn.net/lee244868149/article/details/57076615)

### openwrt lan 改网段

[https://www.cnblogs.com/double-win/p/3841017.html](https://www.cnblogs.com/double-win/p/3841017.html)

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

```bash
sed -i 's_downloads.openwrt.org_mirrors.tuna.tsinghua.edu.cn/openwrt_' /etc/opkg/distfeeds.conf
```

### build

clone [https://github.com/openwrt/openwrt.git](https://github.com/openwrt/openwrt.git)

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
opkg list  # 获取软件列表
opkg update # 更新可以获取的软件包列表
opkg upgrade # 对已经安装的软件包升级
opkg install xxx.ipk # 安装本地的软件包
opkg remove xxx
```

### 自定义防火墙规则

```bash
    /etc/firewall.user
```

### 系统防火墙规则

```bash
    /etc/config/firewall
```

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

```bash
logread          # 查看内存 ring buffer 中的所有日志
logread -f       # 实时跟踪日志（类似 tail -f）
logread | grep pppoe   # 过滤关键词
```

> **注意**：OpenWrt 默认只用内存 ring buffer（`log_size` 默认 128KB），日志仅保留几小时，重启后全部清空，无法回溯历史故障。

### 远程 syslog 转发

OpenWrt 使用 **BusyBox syslogd**（不是 rsyslog/syslog-ng），支持将日志实时转发到远端 syslog server。

远程转发本身是 **syslog 协议（RFC 3164）的标准功能**，但 OpenWrt 的配置方式是通过 **UCI** 完成的（BusyBox syslogd 没有 `/etc/rsyslog.conf`，参数由 UCI `system` 配置段控制）：

```bash
# 配置远端 syslog server
uci set system.@system[0].log_ip='192.168.50.100'   # 远端 IP
uci set system.@system[0].log_port='5140'            # 远端端口（默认 514）
uci set system.@system[0].log_proto='udp'            # 协议：udp 或 tcp
uci commit system
service log restart
```

也可以直接编辑 `/etc/config/system`：

```text
config system
    option log_ip    '192.168.50.100'
    option log_port  '5140'
    option log_proto 'udp'
```

配置后 OpenWrt 会将新产生的日志实时推送到远端，对本机内存 ring buffer 没有影响（两者并行）。典型用途：将日志推到集群里的 Grafana Alloy → Loki，实现持久化存储。

### 启动脚本位置

```bash
/etc/rc.d
```

### openwrt 添加开机运行脚本, start script

openwrt 系统启动的时候执行

openwrt 添加开机运行脚本
进入 /etc/init.d/ 目录创建脚本 test

```bash
vim test
```

在 /etc/init.d/test 中按照以下格式编写 shell 脚本

```bash
#!/bin/sh /etc/rc.common
START=99
STOP=15

start() {
    ip rule add fwmark 2 table 200
}
```

START 的值决定这个脚本的启动顺序, 这里为 99
start() 里执行增加的功能脚步或者写脚本启动自己的程序
3.给脚本添加可执行权限

```bash
chmod +x test
```

#### 创建一个软链接

```bash
/etc/init.d/test enable
```

## send email

opkg 默认不提供 sendmail, 替代的包是 msmtp

```bash
opkg install msmtp
```

### msmtp config, /etc/msmtprc

```bash
vim /etc/msmtprc
```

```bash
account default
host smtp.163.com          #163 的 smtp 服务器地址
from username@163.com      #要从哪个邮箱发出
auth login                 #这里如果使用on的话会报 "msmtp: cannot use a secure authentication method"错误
tls off
user uername@163.com       #邮箱用户名
password passwd0           #邮箱密码，这里可是明文的，文件权限 600，网易邮箱填写第三方客户端授权码
logfile /var/log/mmlog
```

[https://www.cnblogs.com/jjzd/p/6341478.html](https://www.cnblogs.com/jjzd/p/6341478.html)

### send email test

```bash
ln -s /usr/bin/msmtp /usr/sbin/sendmail
# mail to: wiloon.wy@gmail.com
echo -e "Subject: Hello!\n\nHello, world!" |sendmail wiloon.wy@gmail.com

```

[https://wiki.openwrt.org/zh-cn/doc/techref/opkg](https://wiki.openwrt.org/zh-cn/doc/techref/opkg)  
[https://blog.csdn.net/whatday/article/details/78920494](https://blog.csdn.net/whatday/article/details/78920494)  
[https://wiki.openwrt.org/doc/techref/odhcpd](https://wiki.openwrt.org/doc/techref/odhcpd)  
[https://openwrt.proxy.ustclug.org/](https://openwrt.proxy.ustclug.org/)  
[https://mirrors.ustc.edu.cn/help/lede.html](https://mirrors.ustc.edu.cn/help/lede.html)  
[https://openwrt.org/](https://openwrt.org/)
[https://hub.docker.com/u/openwrtorg](https://hub.docker.com/u/openwrtorg)
[https://hub.docker.com/r/openwrtorg/rootfs](https://hub.docker.com/r/openwrtorg/rootfs)
[https://openwrt.club/93.html](https://openwrt.club/93.html)
[https://openwrt.org/docs/techref/initscripts](https://openwrt.org/docs/techref/initscripts)
[https://blog.csdn.net/weixin_42512245/article/details/88602272](https://blog.csdn.net/weixin_42512245/article/details/88602272)

## Ansible 管理 OpenWrt

### Python 依赖

Ansible 有两种方式管理 OpenWrt：

**方式一：只用 `raw` 模块（无需 Python）**

`ansible.builtin.raw` 直接通过 SSH 执行 shell 命令，不依赖远端 Python 环境，适合简单的配置读取和命令执行。

**方式二：使用标准 Ansible 模块（需要最小化 Python）**

如果要用 `copy`、`template`、`lineinfile` 等模块，需要在 OpenWrt 上安装最小化 Python，不需要安装全量 `python3`：

```bash
opkg update
opkg install python3-base python3-codecs python3-openssl
```

- `python3-base` — Python 解释器，Ansible 模块运行的基础
- `python3-codecs` — 字符编码，Ansible JSON 通信必需
- `python3-openssl` — SSL 支持，安全连接必需

全量 `python3` 包含大量用不到的标准库（XML、email、数据库等），在 OpenWrt 的有限存储上没必要安装。

### inventory 配置

```ini
[openwrt]
192.168.50.1 ansible_user=root
```

### 使用 raw 模块备份配置示例

```yaml
- name: Backup OpenWrt configuration
  hosts: openwrt
  gather_facts: false
  tasks:
    - name: Read /etc/config/dhcp
      ansible.builtin.raw: cat /etc/config/dhcp
      register: dhcp_config
      changed_when: false

    - name: Save dhcp config locally
      ansible.builtin.copy:
        content: "{{ dhcp_config.stdout }}"
        dest: "./config/dhcp"
        mode: "0644"
      delegate_to: localhost
```
