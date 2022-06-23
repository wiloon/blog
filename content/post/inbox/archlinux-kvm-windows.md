---
title: archlinux kvm windows
author: "-"
date: 2016-02-01T08:05:51+00:00
url: /?p=8723
categories:
  - inbox
tags:
  - reprint
---
## archlinux kvm windows

- 创建虚拟磁盘
- 安装windows虚拟机
- 配置网络

### check if cpu suport kvm

```bash
egrep --color=auto 'vmx|svm|0xc0f' /proc/cpuinfo
zgrep CONFIG_KVM /proc/config.gz
zgrep VIRTIO /proc/config.gz
lsmod | grep kvm
lsmod | grep virtio
```

### install qemu

```bash
sudo pacman -Sy
sudo pacman -S qemu libvirt

# 可选项
sudo pacman -S samba
### 安装virtio
yay -S virtio-win
```

### 创建磁盘文件

```bash
qemu-img create -f raw win10.raw 30G

# 如果磁盘文件所在分区为btrfs文件系统,在创建磁盘文件之前先在外层目录禁用COW。
chattr +C /path/to/qemu-img/

```

### 安装 win10

```bash
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-m 2048 \
-boot d \
-drive file=/home/wiloon/vm/win10.raw,format=raw,if=virtio,index=1 \
-drive file=/home/wiloon/vm/Win10_1511_English_x64.iso,format=raw,index=2,media=cdrom \
-fda /usr/share/virtio/virtio-win_x86_64.vfd
```

### 如果遇到 -fda read-only 的问题, 去修改一下权限

qemu-system-x86_64: Initialization of device isa-fdc failed: Could not reopen file: Permission denied
qemu-system-x86_64: Initialization of device isa-fdc failed: Block node is read-only

```bash
chmod 777 /usr/share/virtio/virtio-win_x86_64.vfd
```

### 配置网络

#### ip forward

<https://blog.wiloon.com/?p=13701>

#### 创建tap

<https://blog.wiloon.com/?p=13281>

#### config nat, nftables 实现, 跟下面的iptables实现二选一

<https://blog.wiloon.com/?p=8681>

#### 用 iptables 实现的 nat

```bash
sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE
```

### start win10

第一次启动要挂载virtio-win_x86_64.vfd,启动之后到win里面安装网卡驱动。

```bash
#start kvm with virtio net (install eth)
qemu-system-x86_64 \
 -enable-kvm \
 -cpu host \
 -m 2048 \
 -boot c \
 -drive file=/home/wiloon/vm/win10.raw,format=raw,if=virtio,index=1 \
 -fda /usr/share/virtio/virtio-win_x86_64.vfd \
 -netdev tap,ifname=tap0,id=hostnet0,script=no,downscript=no \
 -device virtio-net,netdev=hostnet0,id=net0,mac=52:54:3e:a5:fb:68 \
```

```bash
#User-mode networking
#port forward, net device driver, specified mac addr
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-m 4096 \
-boot d \
-drive file=/mnt/workspace/apps/vm/kvm/win7.qcow2,if=virtio,index=1 \
-drive file=/usr/share/virtio/virtio-win.iso,index=2,media=cdrom \
-net user,hostfwd=tcp::10022-:3389,net=192.168.76.0/24,dhcpstart=192.168.76.9 \
-net nic,macaddr=52:54:00:12:34:03
```

Make sure that each virtual machine has a unique link-level address, but it should always start with 52:54:.

<https://blog.csdn.net/liqiangxo/article/details/62443481>
  
<https://wiki.archlinux.org/index.php/KVM#How_to_use_KVM>
  
<https://wiki.archlinux.org/index.php/Internet_sharing>
  
<https://wiki.archlinux.org/index.php/QEMU#Installing_virtio_drivers>

## linux virtual machine manager

virt-manager
