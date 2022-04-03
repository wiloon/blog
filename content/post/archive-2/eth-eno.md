---
title: 网卡命名规则
author: "-"
date: 2017-12-20T09:04:09+00:00
url: /?p=11646
categories:
  - network

tags:
  - reprint
---
## 网卡命名规则
起因：自己装了最新版本的ubunt发行版，今天发现无法上网，在解决联网故障时发现网卡不再是传统的eth0的方式，本机显示为eno1。奇了个怪了，纳了个闷了，google一探究竟！
查看本机ubuntu版本命令：
cat etc/issue
为什么改名呢？参考Predictable Network Interface Names

可预测的网络接口命名
自从 v197 systemd/udev 开始，系统可以为本地的Ethernet、WLAN和WWAN接口自动地分配可预测的、稳定的网络接口名称。该规范脱离了传统的命名机制（eth0,eth1,wlan0等），但是修复了许多问题。
原因
在传统的网络接口命名规则下，是由内核简单地从eth0开始为可被驱动探索到的设备分配名字（eht0,eth1…）。由于这些驱动不能够被现在技术所预测，意味着多个网络接口都可以被分配名为“eth0”、“eth1”这样的名字，这种方式存在一种隐患，就是一种接口可能是以“eth0”启动，但是结束时就变成了“eth1”.不可预测的命名规则存在着严重的安全威胁。
为了修复这个问题，许多方案被提出和实现。很长一段时间，udev都是根据Mac地址来分配永久了“ethX”名字。这导致了很多问题：这需要一个可写的但是通常不允许的root目录；由于系统的无边界性，当root一个OS镜像的时候可能会改变镜像的配置信息；许多系统的Mac地址并不是固定的。其中最大的问题是用户空间和系统内核对设备命名的冲突。
另一种解决方案就是“biosdevname”，该方案通过找到固件中固定的拓扑信息然后利用它们分配固定的接口。这个命名机制同/dev/*/by-path/ symlinks的方式很相似。大多数情况下，biosdevname 从底层的内核设备定位机制中分离了出来。
最后，许多观点迟滞根据用户选择的名字对接口重新命名，切断同Mac和物理位置的联系。这是一个非常好的选择，但是存在一个隐藏的问题就是用户获得了选择和分配这些名字的权利。
我们相信由“biosdevname”机制已领的泛化机制是一个很好的选择。基于固件、拓扑和位置信息分配固定的名字有一个巨大的优势，名字是全自动地、可预测的，即使硬件添加或删除也不影响。
V197添加了什么
systemd 197为许多命名策略新增了许多本地化的支持到 systemd/udevd 并实现了一个类似于“biosdevname”的机制。五种网络接口的命名机制通过udev得到了支持：
1、Names incorporating Firmware/BIOS provided index numbers for on-board devices (example: eno1)
2、Names incorporating Firmware/BIOS provided PCI Express hotplug slot index numbers (example: ens1)
3、Names incorporating physical/geographical location of the connector of the hardware (example: enp2s0)
4、Names incorporating the interfaces's MAC address (example: enx78e7d1ea46da)
5、Classic, unpredictable kernel-native ethX naming (example: eth0)
1
2
3
4
5
6
默认情况下，如果固件信息是可用有效的 systemd v197 基于1策略命名接口，如果固件信息是可用有效的跳到2，如果可用跳到3，其他情况下跳到5。策略4默认不能用，不过如果用户选择时依旧有效。
这种合并的策略作为最新的一种手段，意味着，如果系统已经安装了biosdevname，该命名机制优先执行。如果用户在内核中加入了udev规则，改变了内核设备的名字，这种方式同样优先执行。另外，启发特殊的命名机制也起作用。

优势
1、稳定的接口名字
2、硬件的增删不影响接口名字
3、内核或驱动加载改变的时候不影响接口名字
4、替换网卡不会改变接口的名字
5、无需用户配置，名字可自动设定
6、接口名字可预测
7、无状态操作，改变硬件配置不会影响名字
8、网络接口命名方式更加贴近symlinks的命方式
9、对x86架构无约束，适用于多种架构



>https://blog.csdn.net/u010558281/article/details/68488791

