---
title: Debian KVM WinXP
author: wiloon
type: post
date: 2011-12-03T09:11:53+00:00
url: /?p=1698
bot_views:
  - 3
views:
  - 8
categories:
  - Linux
  - VM
tags:
  - KVM

---
宿主机:

OS: Debian6/7

IP:192.168.1.100

网关:192.168.1.1

DNS:192.168.1.1

基于内核的虚拟机KVM(Kernel-based Virtual Machine)是linux平台上的全虚拟化解决方案

KVM需要包含虚拟化支持的x86硬件,intel VT或者AMD-V。KVM使用修改后的QEMU作为前端工具,QEMU通过/dev/kvm设备与KVM交互。自kernel版本2.6.20 KVM随主线内核一起发行。

**前提条件(prerequisite)**

可以使用KVM的前提条件是CPU支持虚拟化技术,Intel VT或者AMD-V
  
$egrep ‘(svm|vmx)’ /proc/cpuinfo
  
如果有输出则说明CPU支持硬件虚拟化,SVM(Secure Virtual Machine)是AMD CPU支持硬件虚拟化的标志,VMX是INTEL CPU支持硬件虚拟化的标志

[shell]
  
egrep &#8216;(svm|vmx)&#8217; /proc/cpuinfo
  
flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe nx constant\_tsc arch\_perfmon bts aperfmperf pni monitor vmx est tm2 xtpr pdcm
  
flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe nx constant\_tsc arch\_perfmon bts aperfmperf pni monitor vmx est tm2 xtpr pdcm
  
[/shell]

**安装**KVM****

[shell]
  
sudo apt-get install qemu-kvm
  
[/shell]

从squeeze开始KVM的包名改为qemu-kvm,kvm只是个占位dummy包

安装qemu-utils(ubuntu 10.04以上不需要这一步)

[shell]
  
sudo apt-get install qemu-utils
  
[/shell]

This package provides QEMU related utilities:
  
* qemu-img: QEMU disk image utility
  
* qemu-io: QEMU disk exerciser
  
* qemu-nbd: QEMU disk network block device server

**创建vdisk**

[shell]
  
sudo qemu-img create winxp.img 20G
  
[/shell]

回显

[shell]
  
Formatting &#8216;winxp.img&#8217;, fmt=raw size=10737418240
  
[/shell]

创建一个20G的raw格式的(默认)虚拟磁盘文件,更多参数见man qemu-img

虚拟机磁盘位置/home/wiloon/vm/winxp.img

分区格式:Ext4; (不要把img文件放在btrfs分区上,  磁盘性能会超级差)

**半虚拟化驱动Virtio**

Virtio是KVM/Linux的I/O虚拟化框架，以增强KVM的IO效率,是与其他虚拟化平台的半虚拟化(Paravirtualized)类似的东西,主要应用于磁盘设备和网络接口设备。主流的linux发行版已经默认支持Virtio，如果客户机是linux则无需其他设置，直接可以使用Virtio设备，但是如果客户机是windows，则需要在客户机安装Virtio设备驱动，甚至在windows开始安装之前需要提前加载块设备驱动。windows Virtio驱动可从这里下载<http://www.linux-kvm.com/> (磁盘驱动: virtio-win-1.1.16.vfd,网卡驱动: virtio-win-0.1-15.iso)

KVM主机端设置完毕后,开始安装客户机,我的客户端版本是Windows XP SP3 x32, 因为主机是32位的（IBMX60s／CPU L2400）客户机只能选32位。

因为要使用半虚拟化(Paravirtualized)驱动virtio,但是当前的Debian Stable版本也就是squeeze发行版的kvm并不支持从virtio驱动器启动(seabios 0.5.1-3),所以需要更新一下seabios,从Debian官方sid源下载seabios 0.6.3-2,然后手动安装该包<span style="color: #ff0000;">seabios_1.6.3-2_all.deb</span>

<http://packages.debian.org/sid/all/seabios/download>

<span style="color: #804040;">$sudo dpkg -i seabios_1.6.3-2_all.deb</span>

Debian 7 seabios 版本是1.7.0-1。

查看seabios版本：/usr/share/doc/seabios/changelog.Debian.gz

**KVM核心参数 <http://www.wiloon.com/wordpress/?p=1711>**

sudo apt-get install seabios

sudo apt-get install ebtables

**安装windows XP SP3 x32客户机**

首先从<http://www.linux-kvm.com/>下载[virtio for windows驱动][1],使用如下脚本启动虚拟安装

[shell]
  
#!/bin/sh
  
sudo kvm -bios /usr/share/seabios/bios.bin \
  
-smp 2 \
  
-m 1024 \
  
-rtc base=localtime,clock=host \
  
-boot order=d \
  
-net nic,model=virtio,macaddr=52-54-00-12-34-02 \
  
-net tap,ifname=tap0,script=no,downscript=no \
  
-drive file=/home/wiloon/vm/winxp.img,if=virtio,index=0,media=disk,format=raw,cache=writeback \
  
-drive file=/media/M\_DEV/Tools/win/system/windows\_xp\_professional\_SP3_x86.iso,index=2,media=cdrom \
  
-fda /home/wiloon/tools/kvm/virtio-win-1.1.16.vfd
  
[/shell]

安装开始后记得按F6安装磁盘的virtio驱动

安装网卡驱动

[shell]
  
#!/bin/sh
  
sudo kvm -bios /usr/share/seabios/bios.bin \
  
-smp 1 \
  
-m 512 \
  
-rtc base=localtime,clock=host \
  
-boot order=d -net nic,model=virtio,macaddr=52-54-00-12-34-02 \
  
-net tap,ifname=tap0,script=no,downscript=no \
  
-drive file=/home/wiloon/vm/winxp.img,if=virtio,index=0,media=disk,format=raw,cache=writeback \
  
-drive file=/home/wiloon/tools/kvm/virtio-win-0.1-15.iso,index=2,media=cdrom
  
[/shell]

网桥配置:

&nbsp;

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-nat分割线

虚拟机能过nat方式访问外网

[shell]
  
#创建一个名为tap0的虚拟网卡（就象第一块网卡通常称为eth0），拥有者是用户USERNAME。不过这里的拥有者不是指创建的设备文件/dev/net /tun的拥有者，
  
有些应用可能需要对/dev/net/tun拥有写权限，需要另行处理，一个简单的办法就是把该用户加入uml-net用户组。
  
sudo tunctl -t tap0 -u USERNAME
  
[/shell]

这里的username 可以用当用户

[shell]
  
sudo ifconfig tap0 172.16.0.1 up
  
[/shell]

设置tap0的ip,启动tap0

[shell]

sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE

[/shell]

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-桥接</pre> 

安装uml-utilities和bridge-utils和,这两个工具分别含有tunctl和brctl命令

**1. 是否加载tun模块？**
  
lsmod | grep tun

**2. 检查/dev/net/tun的权限**
  
ls -l /dev/net/tun

**3. 检查/etc/qemu-ifup的权限**
  
当前用户需要有可执行权限

**4. 检查是否已经安装bridge-utils软件包**
  
rpm -qa | grep bridge 来查询，如果没有就请安装bridge-utils包，主要是脚本中一般需要用到brctl这个命令的。

[shell]
  
#eth0
  
auto eth0
  
iface eth0 inet manual
  
address 192.168.1.192
  
netmask 255.255.255.0
  
gateway 192.168.1.1

#tap0, for the vm
  
auto tap0
  
iface tap0 inet manual
  
tunctl_user youeusername

#wlan0
  
auto wlan0
  
iface wlan0 inet dhcp
  
wpa-ssid "XXXX"
  
wpa-psk "XXXX"

#br0
  
auto br0
  
iface br0 inet dhcp
  
bridge_ports wlan0 tap0
  
bridge_fd 9
  
bridge_hello 2
  
bridge_maxage 12
  
bridge_stp off
  
[/shell]

bridge_ports wlan0 tap0,此处将主机的bonding接口wlan0, tap0加入网络桥.

将youeusername改为你登陆主机的用户名

手动配置网络之后就不再需要随系统启动的network manager. 可以在sysv-rc-conf里把network manager 禁用掉.<http://www.wiloon.com/wordpress/?p=2278>

使用桥接网络,客户机必须使用主机的一个tap设备将客户机的网络接口连接到主机的网络桥,tap设备可以用两种方式来设置

一种是静态方式，直接把tap设备的配置写道/etc/network/interfaces文件中，并将tap接口加入网络桥.
  
增加更多的tap接口依次类推

被桥接的网卡会开启混杂模式!!,据说无线网卡没有对应的&#8221;混杂模式&#8221;一说&#8230;&#8230;,但是流量监控还是能看到其它计算机的流量.

如果启动tap0时报错:tap0: ERROR while getting interface flags: No such device, 安装uml-utilities, 并重启系统.

设置ebtables&#8230;

[shell]
  
sudo ebtables -t nat -A POSTROUTING -o wlan0 -j snat &#8211;to-src 00:1b:77:05:aa:4f &#8211;snat-arp &#8211;snat-target ACCEPT
  
sudo ebtables -t nat -A PREROUTING -p IPv4 -i wlan0 &#8211;ip-dst 192.168.1.199 -j dnat &#8211;to-dst 52:54:00:12:34:02 &#8211;dnat-target ACCEPT
  
sudo ebtables -t nat -A PREROUTING -p ARP -i wlan0 &#8211;arp-ip-dst 192.168.1.199 -j dnat &#8211;to-dst 52:54:00:12:34:02 &#8211;dnat-target ACCEPT
  
[/shell]

#00:1b:77:05:aa:4f 无线网卡也是网桥的物理地址.
  
#192.168.1.199 虚拟机的IP.
  
#52:54:00:12:34:02 虚拟机的物理地址.

&#8212;

  1. 桥接后，br0的IP就是宿主机的IP，而虚拟机的IP需要在虚拟机内设定。至于是动态IP还是静态IP，需要根据使用者的需要来设定。因为虚拟 机桥接接入局域网以后，虚拟机就相当于是局域网内的一台实体计算机，与宿主机平行，所以IP的设定要谨慎一些。如果宿主机是静态IP，而虚拟机是动态 IP，那么请确保局域网内有一台DHCP服务器来分配IP。
  2. 设定虚拟机IP的时候，请不要跟br0的IP相同，否则会造成IP冲突，导致宿主机或虚拟机不能连接网络。
  3. 如果出现虚拟机、宿主机和网关能够互相ping通，但虚拟机不能浏览网络等情况，请检查虚拟机的DNS设置。如果出现宿主机或虚拟机断开网络，请检查桥接网络中网桥是否连接好，网关是否设置好.

&nbsp;

启动虚拟机

[shell]

sudo kvm \
  
-bios /usr/share/seabios/bios.bin \
  
-smp 2 -m 2048 \
  
-rtc base=localtime,clock=host \
  
-boot order=c \
  
-net nic,model=virtio,macaddr=52-54-00-12-34-02 \
  
-net tap,ifname=tap0,script=no,downscript=no \
  
-drive file=/home/wiloon/vm/winxp.img,if=virtio,index=0,media=disk,format=raw,cache=writeback

-k en-us -vnc :1

-usb -usbdevice tablet

[/shell]

设置虚拟机的ip:172.16.0.2, 网关172.16.0.1, dns:192.168.1.1

kvm 参数:<http://www.wiloon.com/wordpress/?p=1711>

参考来源:

<http://openwares.net/linux/debian_kvm.html>
  
<http://wiki.debian.org/BridgeNetworkConnections>

<http://forum.ubuntu.org.cn/viewtopic.php?f=65&t=120857&sid=034b1df18a2235d164079b8229fcb92a>

<http://8366.iteye.com/blog/1002397>

<http://blog.shouxi.name/post/28615112175/kvm-on-nox-linux>

 [1]: http://alt.fedoraproject.org/pub/alt/virtio-win/latest/images/bin/