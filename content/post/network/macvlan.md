
---
title: "macvlan"
date: 2020-05-04T19:17:36Z
categories:
  - inbox
tags:
  - reprint
---
## "macvlan"

https://cizixs.com/2017/02/14/network-virtualization-macvlan/

macvlan 是 linux kernel 比较新的特性,可以通过以下方法判断当前系统是否支持: 

    modprobe macvlan
    lsmod | grep macvlan
    macvlan 19046 0

macvlan 允许你在主机的一个网络接口上配置多个虚拟的网络接口,这些网络 interface 有自己独立的 mac 地址,也可以配置上 ip 地址进行通信。macvlan 下的虚拟机或者容器网络和主机在同一个网段中,共享同一个广播域。macvlan 和 bridge 比较相似,但因为它省去了 bridge 的存在,所以配置和调试起来比较简单,而且效率也相对高。除此之外,macvlan 自身也完美支持 VLAN。

### 四种模式
- private mode: 过滤掉所有来自其他 macvlan 接口的报文,因此不同 macvlan 接口之间无法互相通信
- vepa(Virtual Ethernet Port Aggregator) mode:  需要主接口连接的交换机支持 VEPA/802.1Qbg 特性。所有发送出去的报文都会经过交换机,交换机作为再发送到对应的目标地址 (即使目标地址就是主机上的其他 macvlan 接口) ,也就是 hairpin mode 模式,这个模式用在交互机上需要做过滤、统计等功能的场景。
- bridge mode: 通过虚拟的交换机讲主接口的所有 macvlan 接口连接在一起,这样的话,不同 macvlan 接口之间能够直接通信,不需要将报文发送到主机之外。这个模式下,主机外是看不到主机上 macvlan interface 之间通信的报文的。
- passthru mode: 暂时没有搞清楚这个模式要解决的问题

VEPA 和 passthru 模式下,两个 macvlan 接口之间的通信会经过主接口两次: 第一次是发出的时候,第二次是返回的时候。这样会影响物理接口的宽带,也限制了不同 macvlan 接口之间通信的速度。如果多个 macvlan 接口之间通信比较频繁,对于性能的影响会比较明显。

private 模式下,所有的 macvlan 接口都不能互相通信,对性能影响最小。

bridge 模式下,数据报文是通过内存直接转发的,因此效率会高一些,但是会造成 CPU 额外的计算量。

NOTE: 如果要手动分配 mac 地址,请注意本地的 mac 地址最高位字节的低位第二个 bit 必须是 1。比如 02:xx:xx:xx:xx:xx。

## macvlan
https://cizixs.com/2017/02/14/network-virtualization-macvlan/
  
macvlan是 linux kernel 比较新的特性,可以通过以下方法判断当前系统是否支持: 

    modprobe macvlan
    lsmod | grep macvlan
    macvlan 19046 0
  
如果第一个命令报错,或者第二个命令没有返回,则说明当前系统不支持 macvlan,需要升级系统或者升级内核。

macvlan 允许你在主机的一个网络接口上配置多个虚拟的网络接口,这些网络 interface 有自己独立的 mac 地址,也可以配置上 ip 地址进行通信。macvlan 下的虚拟机或者容器网络和主机在同一个网段中,共享同一个广播域。macvlan 和 bridge 比较相似,但因为它省去了 bridge 的存在,所以配置和调试起来比较简单,而且效率也相对高。除此之外,macvlan 自身也完美支持 VLAN。

如果希望容器或者虚拟机放在主机相同的网络中,享受已经存在网络栈的各种优势,可以考虑 macvlan。

### 各个 linux 发行版对 macvlan 的支持
  
macvlan 对kernel 版本依赖: Linux kernel v3.9–3.19 and 4.0+。几个重要发行版支持情况: 

- ubuntu: >= saucy(13.10)
- RHEL(Red Hat Enterprise Linux): >= 7.0(3.10.0)
- Fedora: >=19(3.9)
- Debian: >=8(3.16)
  
各个发行版的 kernel 都可以自行手动升级,具体操作可以参考官方提供的文档。 
以上版本信息参考了这些资料: 

List of ubuntu versions with corresponding linux kernel version
  
Red Hat Enterprise Linux Release Dates
  
### 四种模式
  
- private mode: 过滤掉所有来自其他 macvlan 接口的报文,因此不同 macvlan 接口之间无法互相通信
- vepa(Virtual Ethernet Port Aggregator) mode:  需要主接口连接的交换机支持 VEPA/802.1Qbg 特性。所有发送出去的报文都会经过交换机,交换机作为再发送到对应的目标地址 (即使目标地址就是主机上的其他 macvlan 接口) ,也就是 hairpin mode 模式,这个模式用在交互机上需要做过滤、统计等功能的场景。
- bridge mode: 通过虚拟的交换机将主接口的所有 macvlan 接口连接在一起,这样的话,不同 macvlan 接口之间能够直接通信,不需要将报文发送到主机之外。这个模式下,主机外是看不到主机上 macvlan interface 之间通信的报文的。
- passthru mode: 暂时没有搞清楚这个模式要解决的问题
  
VEPA 和 passthru 模式下,两个 macvlan 接口之间的通信会经过主接口两次: 第一次是发出的时候,第二次是返回的时候。这样会影响物理接口的带宽,也限制了不同 macvlan 接口之间通信的速度。如果多个 macvlan 接口之间通信比较频繁,对于性能的影响会比较明显。

private 模式下,所有的 macvlan 接口都不能互相通信,对性能影响最小。  
bridge 模式下,数据报文是通过内存直接转发的,因此效率会高一些,但是会造成 CPU 额外的计算量。  
NOTE: 如果要手动分配 mac 地址,请注意本地的 mac 地址最高位字节的低位第二个 bit 必须是 1。比如 02:xx:xx:xx:xx:xx。

### 创建macvlan
    ip link add link enp0s8 mac1 type macvlan
    ip addr add 192.168.8.120/24 dev mac1  
    ip link set mac1 up

### podman run
    podman run -itd --name c1 --ip=192.168.50.99 --network mac1 busybox