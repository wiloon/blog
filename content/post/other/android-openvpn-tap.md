---
title: 'Android  OpenVPN-TAP 模式/策略路由'
author: "-"
date: 2011-10-16T08:57:13+00:00
url: /?p=1066
categories:
  - Java

tags:
  - reprint
---
## 'Android  OpenVPN-TAP 模式/策略路由'

<http://blog.csdn.net/dog250/article/details/42046269>

在Android的OpenVPN Service的FAQ上，关于TAP模式有三问三答，最后回答的建议是: Support TAP via emulation。这也是我自己前几个月实现过的。要问为何Android自己不能提供对TAPmode的支持，似乎不关VPNService作者本人的事，其建议是:
  
If you really want to see tap-style tunnels supported in OpenVPN Connect, we would encourage you tocontact the Google Android team and ask that the VpnService API be extended to allow this. Without such changes to the VpnService API, it is not possible for non-root apps such as OpenVPN Connect to support tap-style tunnels.
  
这似乎是个圈，但是我们仔细想一下就会发现这个圈原来是这样:
  
1.Android平台在一个公共的层下面拥有多个完全不同的底层实现，包括Linux内核；
  
2.开放Android的root权限意味着用户可以触摸到任意的底层；
  
3.所有的公共集合，包括API以及功能必须不能基于底层来构建，root权限不能对所有普通用户开放；
  
4.必须有一个公共的层，用户的需求基于这个公共的层来实现
  
5.这个层就是Android平台。
  
另外，我们需要理解的是tun.ko驱动本身，它很短，它很简单。它能在你的Linux BOX上load成功的原因是因为你的Linux BOX实现了Ethernet，看看你的内核config文件，是不是有:
  
CONFIG_NET_ETHERNET=y
  
这一行呢？实际上，tun的TAP mode严重依赖这个内核编译选项。然而对于Android，由于其底层的Linux内核完全根据具体的device定制，你不能保证它一定会支持Ethernet。闲来无事可以看看<http://source.android.com/source/building-kernels.html>这个站点。

虽然大多数的Android设备都支持root用户使用TAP mode的tun驱动，但是这说明不了什么问题，你依然无法保证Ethernet的支持是必须的。上述的自环解释圈说明了，Android平台不应该基于root用户可以触摸的完全的组件来构建...

当然，在VPNService中你还是可以使用TAP mode的！答案在于将这个TAP mode也构建于Android平台之上，怎么做？Support TAP via emulation！我已经做好了一个，办法很简单，就是在OpenVPN中内置了一个ARP处理以及Ethernet封装/解封装模块，代码来自uIP。这不是重点，重点是，难道非得这么任性吗？为何TUN mode就是不可以？！同样来自Android的FAQ，以下的话可能会为TUN mode加上几分:
  
The configuration of the VPN tunnel consists of the IP address and the networks that should be routed over this interface. Especially, no peer partner address or gateway address is needed or required. Special routes to reach the VPN Server (for example added when using redirect-gateway) are not needed either. The application will consequently ignore these settings when importing a configuration. The app ensures with the VPNService API that the connection to the server is not routed through the VPN tunnel.
  
是的，正如你看到的，使用TUN mode的话会省去很多配置，你不再需要对端的虚拟网卡IP地址信息，隧道建立之后，配置路由时，你只需要指定路由出口而不必指出下一跳，事实上，由于TUN mode的虚拟网卡处于点对点模式(下一跳是隐含且明确的！)，而只有多路访问模式的网卡才需要解析下一跳。

进入本日志的第二个话题。Android 4.4+使用了策略路由机制来添加通过OpenVPN虚拟网卡的路由。之所以写这个是因为一段插曲...

大概一个多月前的某天，和同事一起去客户那里排查一个问题，过程中用adb登录到了Android的后台，启动VPN后，例行地运行了iproute2命令集(只要有这个工具，几乎可以解决98.7512%的问题)，然后就是iptables-save命令，惊奇地产生了挫败感，整个人瞬间凌乱...太混乱了，竟然有打IPMARK的规则，ip ru ls 竟然可以看到多出来的策略路由表，mark好像是0x3c什么的...我瞬间崩溃的原因是因为我意识到我还债的时候到了，在不由自主地骂了几句后，客户那边的人也跟着附和...从来没人动过这个系统，iproute2+iptables+mark的风格以及策略路由表的命名风格又和我的风格是如此类似，我承认了"这是我几个月前来的时候加的调试手段..."，其实我自己也不知道怎么回事...问题是我身边的人好像只有我会干出这种事，命名规则看起来又不像是厂商的手笔，那就一定是我干的！这是一个理所当然的推理。...那天还好算是把问题解决了。之后我就一直是回忆回忆回忆，什么时候干过那事呢？百思不得其解，直到碰到了又一个问题，我的另一个同事说Android 4.4的路由没法添加。当然，没法加路由意味着OpenVPN不能使用，这是一个很严重的问题。后来就是google+iproute2了，后来还真的发现了ip rule中有端倪，确实添加了新的路由表专门处理和OpenVPN的数据通道相关的数据包！于是google确认，发现了下面的文字:
  
Routing/Interface Configuration

The Routing and interface configuration is not done via traditional ifconfig/route commands but by using the VPNService API. This results in a different routing configuration than on other OSes.

The configuration of the VPN tunnel consists of the IP address and the networks that should be routed over this interface. Especially, no peer partner address or gateway address is needed or required. Special routes to reach the VPN Server (for example added when using redirect-gateway) are not needed either. The application will consequently ignore these settings when importing a configuration. The app ensures with the VPNService API that the connection to the server is not routed through the VPN tunnel.

The VPNService API does not allow specifying networks that should not be routed via the VPN. As a workaround the app tries to detect networks that should not be routed over tunnel (e.g. route x.x.x.x y.y.y.y net_gateway) and calculates a set of routes that excludes this routes to emulate the behaviour of other platforms. The log windows shows the configuration of the VPNService upon establishing a connection.

Behind the scenes: Android 4.4+ does use policy routing. Using route/ifconfig will not show the installed routes. Instead use ip rule, iptables -t mangle -L
