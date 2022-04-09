---
title: centos8 kvm
author: "-"
date: 2013-11-10T11:25:12+00:00
url: /?p=5942
categories:
  - Uncategorized
tags:
  - KVM

---
## centos8 kvm

sudo yum update
sudo yum install @virt

After installation, verify that Kernel modules are loaded

lsmod | grep kvm

Also install useful tools for virtual machine management.

sudo dnf -y install libvirt-devel virt-top libguestfs-tools virt-install

osinfo-query os

```bash
virt-install \
--name roy-dev \
--ram 2048 \
--vcpus 2 \
--network network:default \
--os-type=fedora34 \
--disk path=/home/roy/vm.qcow2,format=qcow2,bus=virtio,cache=none,size=16 \
--graphics none \
--location=https://mirrors.163.com/fedora/releases/34/Server/x86_64/os/ \
--extra-args="console=tty0 console=ttyS0,115200"
```

>https://computingforgeeks.com/how-to-install-kvm-on-rhel-8/
>https://computingforgeeks.com/how-to-mount-vm-virtual-disk-on-kvm-hypervisor/



### static ip

# if you did not set HostName, set it like follows
[root@localhost ~]# hostnamectl set-hostname dlp.srv.world
# display devices
[root@localhost ~]# nmcli device
DEVICE  TYPE      STATE      CONNECTION
enp1s0  ethernet  connected  enp1s0
lo      loopback  unmanaged  --

# set IPv4 address
[root@localhost ~]# nmcli connection modify enp1s0 ipv4.addresses 10.0.0.30/24
# set gateway
[root@localhost ~]# nmcli connection modify enp1s0 ipv4.gateway 10.0.0.1
# set DNS
# if set multiple DNS, specify with space separated ⇒ ipv4.dns "10.0.0.10 10.0.0.11 10.0.0.12"
[root@localhost ~]# nmcli connection modify enp1s0 ipv4.dns 10.0.0.10
# set DNS search base (your domain name)
[root@localhost ~]# nmcli connection modify enp1s0 ipv4.dns-search srv.world
# set manual for static setting (it's [auto] for DHCP)
[root@localhost ~]# nmcli connection modify enp1s0 ipv4.method manual
# restart the interface to reload settings
[root@localhost ~]# nmcli connection down enp1s0; nmcli connection up enp1s0
Connection 'enp1s0' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/1)
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/2)

# confirm settings
[root@localhost ~]# nmcli device show enp1s0


## 禁用 selinux


>https://www.server-world.info/en/note?os=Fedora_34&p=initial_conf&f=3



---

使用 osinfo-query os 可以查询出 --os-variant 所有支持的参数，这样可以精确指定操作系统版本以便优化运行参数。

--graphics none 表示不使用VNC来访问VM的控制台，而是使用VM串口的字符控制台。

`--location 指定通过网络安装，如果使用本地iso安装，则使用 --cdrom /var/lib/libvirt/images/ubuntu-18.04.2-live-server-amd64.iso

只有通过网络安装才可以使用 --extra-args="console=tty0 console=ttyS0,115200" 以便能够通过串口控制台安装。也就是说，如果使用 iso镜像安装，则不能传递内核参数，否则提示报错:

ERROR    Kernel arguments are only supported with location or kernel installs.
要模拟UEFI，需要安装 ovmf 软件包，并使用参数 --boot uefi

root分区采用EXT4文件系统，占据整个磁盘

软件包只选择 OpenSSH server 以便保持最小化安装，后续clone出的镜像再按需安装

上述安装是通过 virsh console 连接到虚拟机的串口控制台实现的，安装完成后，需要 detach 断开串口控制台: CTRL+Shift+] ，这就可以返回host主机的控制台。


>https://cloud-atlas.readthedocs.io/zh_CN/latest/kvm/startup/create_vm.html

