---
title: "pve + openwrt"
author: "-"
date: "2021-06-17 22:28:37"
url: ""
categories:
  - network
tags:
  - inbox
---
## "pve + openwrt"

### download openwrt image

下载 "combined-ext4.img.gz"  

```bash
curl -O https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
curl -O https://downloads.openwrt.org/releases/21.02.3/targets/x86/64/openwrt-21.02.3-x86-64-generic-ext4-combined-efi.img.gz
```

#### 创建虚拟机

1. 点击 "创建虚拟机"，填写虚拟机名称 (例如Openwrt), 选"高级"，勾选"开机自启动" (软路由必须随机启动) ，点击"下一步"。
2. CD/DVD选择"Do not use any media"，操作系统和版本默认即可，点击"下一步"。
3. 系统选项卡全部默认，点击"下一步"。
4. 硬盘不用改，之后会删除，然后用刚刚下载的 img 镜像创建虚拟磁盘。
5. CPU核心数量按需添加，一般双核足够了
6. 内存256MB以上都是够的，系统有富余就多加一点，一般不用超高2GB，点击"下一步"
7. PVE虚拟机可选网卡模型 (虚拟网卡) 有Intel E1000、VirtIO (半虚拟化) 、Realtek RTL8139和VMware vmxnet3四种。建议选用默认的VirtIO (半虚拟化) ，其性能和效率最高。
8. 分离不用的硬盘: 选择刚刚创建的"Openwrt"虚拟机 >  硬件 > Hard Disk(scsi0) > 点击"分离(Detach)"。
9. 删除不用的硬盘和光驱: 选中"未使用的磁盘0"，点击"删除"；再用同样的方法删除不用的光驱。

### upload

```f
    pve>local(xxx)>ISO Images>upload
```

### 添加启动盘

上传Openwrt镜像: 选择"pve"节点 > local存储空间 > 内容 > 点击上传 > 选择"openwrt.img"镜像 > 点击"上传"，openwrt镜像最好提前重命名一下，原来的太长了。

网上绝大多数教程都使用 WinSCP 或其他 FTP 工具把镜像上传到 root根目录，个人认为是多此一举，不妨看下 "local"和"local-lvm"存储空间的内容说明:

local: VZDump 备份文件, ISO镜像, 容器模板
local-lvm: 磁盘映像, 容器
其中 local-lvm 不能上传文件，只能用"qm importdisk"命令把镜像转换成虚拟磁盘并存储在里面 (或创建磁盘和磁盘映射) ，这样做比上传到 root根目录更便捷而且便于管理。

### 查看上传镜像的目录

点击网页下端的任务选项卡 > 双击最新的"数据拷贝"任务 > "target file"后面就是刚刚上传的镜像文件完整目录:

target file:  
/var/lib/vz/template/iso/openwrt.img  
/var/lib/vz/template/iso/openwrt-21.02.3-x86-64-generic-ext4-combined-efi.img  

### 把镜像转成虚拟磁盘并导入到虚拟机

选择"pve"节点 > shell > 输入以下命令并回车:

```bash
# 后面的参数‘102’是Openwrt虚拟机的编号
qm importdisk 102 /var/lib/vz/template/iso/openwrt.img local-lvm
qm importdisk 104 /var/lib/vz/template/iso/openwrt-21.02.3-x86-64-generic-ext4-combined-efi.img local-lvm
```

shell会显示vm-102-disk-0虚拟磁盘创建的进度，最后显示‘Successfully imported disk as 'unused0:local-lvm:vm-102-disk-0'就是添加成功了。

qm importdisk 是PVE导入磁盘到虚拟机的工具，后面的参数‘102’是Openwrt虚拟机的编号，‘/var/lib/vz/template/iso/openwrt.img’是刚才上传Openwrt镜像的完整目录，‘local-lvm’是PVE储存虚拟磁盘的存储空间。

导入成功后在‘Openwrt’虚拟机的"硬件"选项卡就能看到一个"未使用的磁盘0"，选中它点击编辑，弹出配置窗口，Bus/Device 选"sata"，最后点击添加。

切换到虚拟机的"选项"选项卡，双击"引导顺序"，第一引导项选"Disk ‘sata0’"。

### 添加虚拟网卡

PVE 安装完后系统只会创建一个虚拟网桥，前面创建虚拟机的时候添加的"vmbr0"对应openwrt软路由的"eth0网卡"，默认是软路由LAN口；所以还要创建一个"vmbr1"对应软路由的"eth1网卡"，用作软路由的WAN口:

选择"pve"节点 > 网络 > 创建 > Linux Bridge > 桥接名称填写"vmbr1" > 端口(Bridge Ports)填写其他未使用的网卡名称 > 最后点击"创建"。

### 添加虚拟网卡到虚拟机

选择"Openwrt"虚拟机 > 硬件 > 添加 > 网络设备 > 桥接选"vmbr1" > 网卡模型选"Virto" > 最后点击"添加"。

到此Openwrt/LEDE虚拟机软路由就创建完成了，在你面前的是一台崭新的功能丰富的高端有线路由器。

### Openwrt/LEDE设置

最后启动 openwrt 虚拟机，把电脑接到 PVE 实体机的 "enp2s0"网口 (vmbr1网桥对应的网口) ，如果设置都正确的话电脑将自动获取ip地址， (不行就手动指定电脑的IP:
192.168.1.xxx，子网掩码: 255.255.255.0 网关: 192.168.1.1 DNS: 114.114.114.14) ，就能访问192.168.1.1就能进入openwrt的登录页面

最后设置一下软路由的WAN 口拨号和LAN口地址连上光猫就能上网了，WAN口要自己选PPPOE，在这里设置: 网络 > 接口 > WAN >  编辑 > 基本设置 > 协议，选好保存再编辑就能输入宽带账号密码。

软路由的LAN口enp2s0网卡可以下接交换机、无线路由或AP，把网络共享出来。

openwrt-LEDE WAN口设置
LAN口要改一下IP地址，不要跟光猫的地址在同个网段，光猫一般是192.168.1.1，这里我改成192.168.0.1。

openwrt-LEDE LAN口设置
至此，PVE安装Openwrt/LEDE虚拟机软路由教程就结束了，软路由的优点是性能可以定制，性价比可以轻易碾压中高端物理路由器。

还有一个好处是有线和无线分离，有线部分将来容易扩展万兆或多千兆，无线部分可以用POE交换机带面板AP，也为将来无线部分换Wi-Fi 6做好准备。
