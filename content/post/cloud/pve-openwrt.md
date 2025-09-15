---
title: pve + openwrt
author: "-"
date: "2021-06-17 22:28:37"
url: ""
categories:
  - network
tags:
  - inbox
  - openwrt
---
## pve + openwrt

局域网网段: 192.168.50.0/24
pve 宿主机 ip: 192.168.50.6
软路由 ip: 192.168.50.1

### download openwrt image

下载 "ext4-combined-efi"  

```bash
curl -O https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
curl -O https://downloads.openwrt.org/releases/21.02.3/targets/x86/64/openwrt-21.02.3-x86-64-generic-ext4-combined-efi.img.gz
curl -O https://downloads.openwrt.org/releases/24.10.0/targets/x86/64/openwrt-24.10.0-x86-64-generic-ext4-combined-efi.img.gz
```

### upload image to pve

```bash
# 解压出 .img 文件
gunzip openwrt-19.07.7-x86-64-combined-ext4.img.gz
```

把 openwrt-24.10.0-x86-64-generic-ext4-combined-efi.img 上传到 pve local
pve>local(xxx)>ISO Images>upload

#### 创建虚拟机

1. 点击 "创建虚拟机(Create VM)", 填写虚拟机名称 (例如 openwrt-24-10), 选"高级"，勾选"开机自启动" (软路由必须开机启动) ，点击"下一步"。
2. OS: CD/DVD 选择 "Do not use any media"(不要去选择刚才上传的镜像)，点击"下一步"。
3. System: 系统选项卡全部默认，点击"下一步"。
4. Disk: 硬盘不用改，之后会删除，会用上一步下载的 .img 镜像创建虚拟磁盘。
5. CPU 核心数量按需添加，一般双核足够了
6. 内存 256MB 以上都是够的，系统有富余就多加一点，一般不用超过 2GB，点击"下一步"
7. Network: PVE 虚拟机可选网卡模型 (虚拟网卡) 有 Intel E1000、VirtIO (半虚拟化) 、Realtek RTL8139和VMware vmxnet3四种。建议选用默认的 VirtIO (半虚拟化) ，其性能和效率最高。
8. 分离不用的硬盘: 选择刚刚创建的虚拟机 >  硬件(Hardware) > Hard Disk(scsi0) > 点击"分离(Detach)", 然后它会变成 unused disk。
9. 删除不用的硬盘和光驱: 选中"Unused disk 0"，点击"删除"；再用同样的方法删除不用的光驱。

### 添加启动盘

上传 Openwrt 镜像: 选择"pve"节点 > local存储空间 > 内容 > 点击上传 > 选择"openwrt-24.10.0-x86-64-generic-ext4-combined-efi.img"镜像 > 点击"上传"。

### 查看上传镜像的目录

点击网页下端的任务选项卡 > 双击最新的"数据拷贝"任务 > "target file" 后面就是刚刚上传的镜像文件完整路径:

target file:  
/var/lib/vz/template/iso/openwrt-24.10.0-x86-64-generic-ext4-combined-efi.img

### 把镜像转成虚拟磁盘并导入到虚拟机

选择"pve"节点 > shell > 输入以下命令并回车:

```bash
# 后面的参数 100 是 Openwrt 虚拟机的编号
qm importdisk 100 /var/lib/vz/template/iso/openwrt-24.10.0-x86-64-generic-ext4-combined-efi.img local-lvm
```

shell 会显示 vm-100-disk-0 虚拟磁盘创建的进度，最后显示 ‘Successfully imported disk as 'unused0:local-lvm:vm-100-disk-0' 就是添加成功了。

qm importdisk 是 PVE 导入磁盘到虚拟机的工具，后面的参数‘100’是Openwrt虚拟机的编号，
‘/var/lib/vz/template/iso/openwrt-24.10.0-x86-64-generic-ext4-combined-efi.img’ 是刚才上传Openwrt镜像的完整目录，
‘local-lvm’ 是PVE储存虚拟磁盘的存储空间。

导入成功后在 ‘Openwrt’ 虚拟机的"硬件"选项卡就能看到一个"未使用的磁盘0(Unused Disk 0)"，选中它点击编辑，弹出配置窗口，Bus/Device 选"sata"，最后点击添加。

切换到虚拟机的 "Options" 选项卡，双击 "Boot Order"，第一引导项选 "Disk ‘sata0’"。

### 添加虚拟网卡

PVE 安装完后系统只会创建一个虚拟网桥，前面创建虚拟机的时候添加的 "vmbr0" 对应 openwrt 软路由的 "eth0网卡"(创建 openwrt 虚拟机的时候插着网线的网卡)，默认是软路由 LAN 口；所以还要创建一个"vmbr1"对应软路由的"eth1网卡"，用作软路由的 WAN 口:

选择 "pve"节点(pve 节点的名字, 比如: n100) > 网络(Network) > 创建(Create) > Linux Bridge > 桥接名称填写"vmbr1" > 端口(Bridge Ports)填写其他未使用的网卡名称(比如: enp2s0) > 最后点击"创建"。

新创建的网桥状态是 Active = No

然后点击 Apply Configuration, 看到网桥状态变成 Active = Yes, 就是成功了.

### 添加虚拟网卡到虚拟机

选择 Openwrt 虚拟机 > 硬件 > 添加 > 网络设备 > 桥接选"vmbr1" > 网卡模型选"Virto" > 最后点击"添加"。

到此 Openwrt 虚拟机软路由就创建完成了。

### 把其它网口都绑到 vmbr0 上

选择 pve 节点> network> vmbr0 (路由器里 lan 对应的网卡)> 把其它网口也加到 bridge ports 里, 用空格分隔

### Openwrt 设置

启动虚拟机, 虚拟机控制台修改 openwrt 的 vr-lan ip

```bash
vim /etc/config/network
# 把 192.168.1.1 改成, 比如: 192.168.50.1, 重启 openwrt, 用浏览器就能访问 openwrt的 web ui 了.
```

openwrt web ui

设置密码
创建 wan interface: network>interface>add new interface
name: wan0
protocol: pppoe
device: 选择上面添加的虚拟网卡 eth1

---

最后启动 openwrt 虚拟机，把电脑接到 PVE 实体机的 "enp2s0" 网口 (vmbr1网桥对应的网口) ，如果设置都正确的话电脑将自动获取 ip 地址， (不行就手动指定电脑的IP:
192.168.1.xxx，子网掩码: 255.255.255.0 网关: 192.168.1.1 DNS: 114.114.114.14) ，就能访问192.168.1.1就能进入openwrt的登录页面

最后设置一下软路由的 WAN 口拨号和 LA N口地址连上光猫就能上网了，WAN口要自己选PPPOE，在这里设置: 网络 > 接口 > WAN >  编辑 > 基本设置 > 协议，选好保存再编辑就能输入宽带账号密码。

软路由的LAN口enp2s0网卡可以下接交换机、无线路由或AP，把网络共享出来。

openwrt-LEDE WAN口设置
LAN口要改一下IP地址，不要跟光猫的地址在同个网段，光猫一般是192.168.1.1，这里我改成192.168.0.1。

openwrt-LEDE LAN口设置
至此，PVE安装Openwrt/LEDE虚拟机软路由教程就结束了，软路由的优点是性能可以定制，性价比可以轻易碾压中高端物理路由器。

还有一个好处是有线和无线分离，有线部分将来容易扩展万兆或多千兆，无线部分可以用POE交换机带面板AP，也为将来无线部分换Wi-Fi 6做好准备。

## openwrt 路由设置 

protocol: PPPoE
bring up on boot: true
PAP/CHAP username: user_0
PAP/CHAP password: password_0
