---
title: libvirt, virsh
author: "-"
date: 2012-04-24T02:48:24+00:00
url: virsh
categories:
  - vm
tags:
  - reprint
  - kvm


---
## libvirt, virsh

## archlinux

```bash
sudo pacman -S libvirt
systemctl status libvirtd
systemctl enable libvirtd --now

pacman -S dnsmasq dmidecode
virsh net-list --all
virsh net-start default
```

## vim /etc/libvirt/qemu.conf

```bash
user = "root"
group = "root"
```

## restart libvirtd

```bash
systemctl restart libvirtd

```

```bash
virt-install \
--name=foo --ram 2048 --vcpus=1 \
--disk path=/root/tmp/foo.raw,size=10,format=raw,bus=virtio \
--cdrom=/root/tmp/archlinux-2022.03.01-x86_64.iso \
--network network:default \
--graphics vnc,password=123456,port=5900,listen=0.0.0.0 \
--noautoconsole

# --connect qemu:///system    作用未知...
# --noautoconsole 禁止自动连接至虚拟机的控制台 安装不会自动代开virt-viewer来查看控制台已完成安装。这对远程使用SSH系统有用。
# --graphics vnc,listen=0.0.0.0 vnc 默认端口5900
```

## install vnc

```bash
pacman -S tigervnc 
vncviewer 10.1.10.2:1
```

## 参数

```
--name    #虚拟机名称
--ram     #分配给虚拟机的内存，单位MB
--vcpus   #分配给虚拟机的cpu个数
--cdrom   #指定CentOS镜像ISO文件路径
--disk    #指定虚拟机raw文件路径
  size    #虚拟机文件大小，单位GB
  bus     #虚拟机磁盘使用的总线类型，为了使虚拟机达到好的性能，这里使用virtio
  cache   #虚拟机磁盘的cache类型
--network bridge    #指定桥接网卡
   model            #网卡模式，这里也是使用性能更好的virtio
--graphics          #图形参数


```

## 命令

```bash
virt-install --osinfo list
virsh list                                  # 查看活动虚拟机状态
virsh list --all                            # 查看所有虚拟机状态, 包括已经关闭的
virsh start <虚拟机名称>                     # 启动一个之前已经定义define过的虚拟机（domain)
virsh shutdown <虚拟机名称>                  # 关闭虚拟机,类似虚拟机内执行关机
virsh destroy <虚拟机名称>                   # 强制关闭虚拟机，类似于断电
virsh undefine <虚拟机名称>                  # 对于运行中的持久性虚拟机，将状态转换为暂时的，关机后virsh无法感知其存在
                                            # 对于非活动的虚拟机，undefine后virsh将无法感知其存在
                                            # undefine后磁盘依然存在，只是删除虚拟机的配置文件/etc/libvirt/qemu
virsh undefine <虚拟机名称> --remove-all-storage    # 删除虚拟机并删除所有磁盘文件
virsh define <虚拟机xml文件>                 # 从xml文件定义define新的domain，不会自动启动
virsh dumpxml <虚拟机名称>                   # 查看虚拟机xml文件

virsh help                                  # 查看帮助信息
virsh version                               # 查看qemu版本
virsh help <特定命令>                       # 查看特定命令帮助信息
virsh <特定命令> --help                     # 查看特定命令帮助信息
virsh nodeinfo                              # 查看宿主机信息
virsh uri                                  # 查看当前主机hyperviso的连接路径；
virsh connect <hypervisor uri>             # 连接到特定hypervisor,默认qemu:///system
virsh sysinfo                               # 查看hypervisro信息


virsh reboot <虚拟机名称>                    # 重启虚拟机

virsh suspend <虚拟机名称>                   # 挂起虚拟机，将当前状态保存在内存中
virsh resume <虚拟机名称>                    # 恢复虚拟机挂起状态，从内存中恢复虚拟机状态
virsh save <虚拟机名称> <img镜像文件名>        # 暂停虚拟机，将虚拟机状态保存在磁盘镜像文件中
virsh restore <img镜像文件名>             　　#重新载入暂停的虚拟机
virsh autostart <虚拟机名称>                 # 虚拟机随着物理机启动自动启动
virsh autostart <虚拟机名称> --disable       # 禁止开机启动
virsh dominfo <虚拟机名称>                   # 查看虚拟机domain信息
virsh domblklist <虚拟机名称>                # 列出虚拟机所有块存储设备
virsh console <虚拟机名称>                   # 控制台连接虚拟机

virsh edit <虚拟机名称>                      # 编辑虚拟机xml文件
virsh managedsave <虚拟机名称>               # 保存状态save并关闭虚拟机，下次启动会恢复到之前保存的状态
virsh start <虚拟机名称>                     # 启动并恢复managedsave保存的状态
virsh reset <虚拟机名称>                     # 对虚拟机执行强制重启，类似重置电源按钮
virsh create <虚拟机xml文件>                 # 从xml文件中创建domain，创建完成后会自动启动；
                                            # 一个xml对应一个domain虚拟机






virsh snapshot-create-as <虚拟机名称> --name <快照名称>   # 从命令行创建快照
virsh snapshot-create <虚拟机名称>                       # 从xml文件创建快照
virsh snapshot-list <虚拟机名称>                         # 查看虚拟机快照列表
virsh snapshot-parent <虚拟机名称> --current             # 查看当前快照的上一级快照
virsh snapshot-edit <虚拟机名称> --snapshotname <快照名>    # 编辑快照
virsh snapshot-revert <虚拟机名称> --snapshotname <快照名>  # 恢复快照
virsh snapshot-delete <虚拟机名称> --snapshotname <快照名>  # 删除快照

virsh setvcpus <虚拟机名称> 4 --maximum --config # 设置最大vcpu数（只能用--config，下次运行生效）
virsh setvcpus <虚拟机名称> 4 --config           # 下次启动使用vcpu数
virsh vcpuinfo <虚拟机名称>                      # 查看vcpu信息
virsh vcpupin <虚拟机名称>                       # 查询域 vcpu亲和性,即vcpu和物理cpu之间关系
virsh maxvcpus                                 # 显示本机vcpu最大值

virsh setmaxmem <虚拟机名称> [--size] 2G --current  # 设置最大内存限制值
virsh setmem <虚拟机名称> [--size] 2G --current     # 设置内存分配


virsh domblklist cirros                         # 查看虚拟机的存储块设备

创建磁盘文件
#qcow2是文件类型，test1-add1.qcow2是磁盘文件，5G是大小
qemu-img create -f qcow2 /var/lib/libvirt/images/test1-add1.qcow2 5G
qemu-img info <虚拟机镜像>           # 查看镜像信息


virt-install <命令行>  # 通过命令行指定来创建虚拟机

virsh attach-disk <虚拟机名称> 
virsh attach-device <虚拟机名称> /etc/libvirt/qemu/test2-add.xml --persistent        # 从XML文件附加设备
virsh detach-device <虚拟机名称> /etc/libvirt/qemu/test2-add.xml --persistent        # 卸载设备   

```

><https://linux.die.net/man/1/virt-install>

### 虚拟机改名

```bash
cd /etc/libvirt/qemu
virsh dumpxml  kvm_client00 > kvm_00.xml
vim kvm_00.xml
virsh undefine foo
virsh define /etc/libvirt/qemukvm_00.xml 
```

><http://www.cnblogs.com/5201351/p/4464350.html>

## 调整内存

```bash
virsh shutdown vm0
sudo virsh setmaxmem vm0 16G
virsh start vm0
virsh setmem vm0 16G

```

————————————————
版权声明：本文为CSDN博主「tom马」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/mshxuyi/article/details/98305715>

## centos6

```bash
virt-install \
--name=centos6 --ram 2048 --vcpus=2 \
--disk path=/home/michael/centos6.raw,size=20,format=raw,bus=virtio \
--cdrom=/home/michael/CentOS-6.10-x86_64-minimal.iso \
--network network:default \
--graphics vnc,port=5901,listen=0.0.0.0 \
--noautoconsole

```
