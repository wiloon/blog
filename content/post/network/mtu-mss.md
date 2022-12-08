---
title: tcp MTU MSS
author: "-"
date: 2016-12-30T00:54:55+00:00
url: tcp/mtu/mss
categories:
  - network
tags:
  - reprint
---

## tcp MTU MSS

### MTU: Maxitum Transmission Unit 最大传输单元

由于以太网EthernetII最大的数据帧是1518Bytes这样, 刨去以太网帧的帧头 (DMAC目的地址MAC48bit=6Bytes+SMAC源MAC地址48bit=6Bytes+Type域2bytes) 14Bytes和帧尾CRC校验部分4Bytes (这个部门有时候大家也把它叫做FCS) ,那么剩下承载上层协议的地方也就是 Data 域最大就只能有1500Bytes. 这个值我们就把它称之为**MTU**。

以太网的MTU是1500,再减去PPP的包头包尾的开销 (8Bytes) ,就变成1492。

以太网和802.3对数据帧的长度都有一个限制,其最大值分别是1500字节和1492字节。链路层的这个特性称为MTU,即最大传输单元。不同类型网络的数帧长度大多数都有一个上限。如果IP层有一个数据报要传,而且数据帧的长度比链路层的MTU还大,那么IP层就需要进行分片( fragmentation),即把数据报分成干片,这样每一片就都小于MTU  
当同一个网络上的两台主机互相进行通信时,该网络的MTU是非常重要。但是如果两台主机之间的通信要通过多个网络,每个网络的链路层可能有不同的MTU,那么这时重要的不是两台主机所在网络的MTU的值,而是两台主机通信路径中的最小MTU,称为路径MTU( Path mtu,PMTU)。

两台主机之间的PMTU不一定是个常数,它取决于当时所选择的路径,而且路由选择也不一定是对称的(从A到B的路由可能与从B到A的路由不同),因此,PMTU在两个方向上不一定是一致的。
RFC1191描述了PMTU的发现机制,即确定路径MTU的方法。ICMP的不可到达错误采用的就是这种方法, traceroute程序也是用这种方法来确定到达目的节点的PMTU的

IP协议除了具有路由寻址功能外,另一个重要的功能就是IP数据报的分片处理。每个数据链路层能够确定发送的一个帧的最大长度称为最大传输单元。在Ethernet中,MTU为1500字节;在FDDI中,MTU为4352字节;在 IP over AMT中,MTU为9180字节。

### MSS: Maxitum Segment Size, 最大分段大小

MSS 就是 TCP 数据包每次能够传输的最大数据分段。 为了达到最佳的传输效能TCP协议在建立连接的时候通常要协商双方的 MSS 值, 这个值 TCP 协议在实现的时候往往用 MTU 值代替 (需要减去IP数据包包头的大小20Bytes和TCP数据段的包头20Bytes) 所以往往 MSS 为 1460。通讯双方会根据双方提供的MSS值的最小值确定为这次连接的最大MSS值。

先说说这MTU最大传输单元,这个最大传输单元实际上和链路层协议有着密切的关系,让我们先仔细回忆一下EthernetII帧的结构DMAC+SMAC+Type+Data+CRC。由于以太网传输电气方面的限制,每个以太网帧都有最小的大小64bytes,最大不能超过1518bytes,对于小于或者大于这个限制的以太网帧我们都可以视之为错误的数据帧,一般的以太网转发设备会丢弃这些数据帧。  
 (注: 小于64Bytes的数据帧一般是由于以太网冲突产生的"碎片"或者线路干扰或者坏的以太网接口产生的,对于大于1518Bytes的数据帧我们一般把它叫做Giant帧,这种一般是由于线路干扰或者坏的以太网口产生)

由于以太网EthernetII最大的数据帧是1518Bytes这样,刨去以太网帧的帧头 (DMAC目的MAC地址48bit=6Bytes+SMAC源MAC地址48bit=6Bytes+Type域2bytes) 14Bytes和帧尾CRC校验部分4Bytes (这个部门有时候大家也把它叫做FCS) ,那么剩下承载上层协议的地方也就是Data域最大就只能有1500Bytes这个值我们就把它称之为MTU。这个就是网络层协议非常关心的地方,因为网络层协议比如IP协议会根据这个值来决定是否把上层传下来的数据进行分片。就好比一个盒子没法装下一大块面包,我们需要把面包切成片,装在多个盒子里面一样的道理。

当两台远程PC互联的时候,它们的数据需要穿过很多的路由器和各种各样的网络媒介才能到达对端,网络中不同媒介的MTU各不相同,就好比一长段的水管,由不同粗细的水管组成 (MTU不同 :)) 通过这段水管最大水量就要由中间最细的水管决定。

对于网络层的上层协议而言 (我们以TCP/IP协议族为例) 它们对水管粗细不在意它们认为这个是网络层的事情。网络层IP协议会检查每个从上层协议下来的数据包的大小,并根据本机MTU的大小决定是否作"分片"处理。分片最大的坏处就是降低了传输性能,本来一次可以搞定的事情,分成多次搞定,所以在网络层更高一层 (就是传输层) 的实现中往往会对此加以注意！有些高层因为某些原因就会要求我这个面包不能切片,我要完整地面包,所以会在IP数据包包头里面加上一个标签: DF (Donot Fragment) 。这样当这个IP数据包在一大段网络 (水管里面) 传输的时候,如果遇到MTU小于IP数据包的情况,转发设备就会根据要求丢弃这个数据包。然后返回一个错误信息给发送者。这样往往会造成某些通讯上的问题,不过幸运的是大部分网络链路都是MTU1500或者大于1500。

对于UDP协议而言,这个协议本身是无连接的协议,对数据包的到达顺序以及是否正确到达不甚关心,所以一般UDP应用对分片没有特殊要求。

对于TCP协议而言就不一样了,这个协议是面向连接的协议,对于TCP协议而言它非常在意数据包的到达顺序以及是否传输中有错误发生。所以有些TCP应用对分片有要求-不能分片 (DF) 。

### PPPoE

花开两朵,各表一枝,说完MTU的故事我们该讲讲今天的第二个猪脚 PPPoE所谓PPPoE就是在以太网上面跑PPP协议,有人奇怪了,PPP协议和Ethernet不都是链路层协议吗？怎么一个链路层跑到另外一个链路层上面去了,难道升级成网络层协议了不成。其实这是个误区: 就是某层协议只能承载更上一层协议。
  
为什么会产生这种奇怪的需求呢？这是因为随着宽带接入 (这种宽带接入一般为Cable Modem或者xDSL或者以太网的接入) 由于以太网缺乏认证计费机制而传统运营商是通过PPP协议来对拨号等接入服务进行认证计费的,所以就出了这么一个怪胎: PPPoE。 (有关PPPoE的详细介绍参见V大以及本站其他成员的一些介绍文章,我就不啰里啰唆的了)

PPPoE带来了好处,也带来了一些坏处,比如: 二次封装耗费资源,降低了传输效能等等,这些坏处俺也不多说了,最大的坏处就是PPPoE导致MTU变小了以太网的MTU是1500,再减去PPP的包头包尾的开销 (8Bytes) ,就变成1492。

如果两台主机之间的某段网络使用了PPPoE那么就会导致某些不能分片的应用无法通讯。

这个时候就需要我们调整一下主机的MTU,通过降低主机的MTU,这样我们就能够顺利地进行通讯了。

当然对于TCP应用而言还有另外的解决方案。马上请出今天第三位猪脚: MSS。

### MSS: Maxitum Segment Size 最大分段大小

MSS最大传输大小的缩写,是TCP协议里面的一个概念。MSS就是TCP数据包每次能够传输的最大数据分段。为了达到最佳的传输效能TCP协议在建立连接的时候通常要协商双方的MSS值,这个值TCP协议在实现的时候往往用MTU值代替 (需要减去IP数据包包头的大小20Bytes和TCP数据段的包头20Bytes) 所以往往MSS为1460。通讯双方会根据双方提供的MSS值得最小值确定为这次连接的最大MSS值。

我们回过头来看前言里面的那个问题,我们试想一下,如果我们在中间路由器上把每次TCP连接的最大MSS进行调整这样使得通过PPPoE链路的最大MSS值加上数据包头包尾不会超过PPPoE的MTU大小1492这样就不会造成无法通讯的问题。

所以上面的问题可以通过ip tcp adjust-mss 1452来解决。

当然问题也可以通过修改PC机的MTU来解决。

### TCP MSS

MSS (Maximum Segment Size, 最大报文长度), 是 TCP 协议定义的一个选项,MSS选项用于在TCP连接建立时,收发双方协商通信时每一个报文段所能承载的最大数据长度

一旦DF位置为一,(DF位为1的话则不允许分片) 将不允许中间设备对该报文进行分片,那么在遇到IP报文长度超过中间设备转发接口的MTU值时,该IP报文将会被中间设备丢弃。在丢弃之后,中间设备会向发送方发送ICMP差错报文。

一旦出现这种因DF位置一而引起丢包,如果客户端无法正常处理的话,将会导致业务应用出现异常,外在表现为页面无法打开、页面打开不全、某些大文件无法传输等等,这将严重影响业务的正常运行。
那么客户端如何处理这种状况呢？
TCP主要通过两种方式来应对:

1. 协商MSS,在交互之前避免分片的产生
2. 路径MTU发现 (PMTUD)

TCP在三次握手建立连接过程中,会在SYN报文中使用MSS (Maximum Segment Size) 选项功能,协商交互双方能够接收的最大段长MSS值。

MSS是传输层TCP协议范畴内的概念,顾名思义,其标识TCP能够承载的最大的应用数据段长度,因此,MSS=MTU-20字节TCP报头-20字节IP报头,那么在以太网环境下,MSS值一般就是1500-20-20=1460字节。
客户端与服务器端分别根据自己发包接口的MTU值计算出相应MSS值,并通过SYN报文告知对方,

通过在TCP连接之初,协商MSS值巧妙的解决了避免端系统分片的问题,但是在复杂的实际网络环境下,影响到IP报文分片的并不仅仅是发送方和接收方,还有路由器、防火墙等中间系统,假设在下图的网络环境下:

中间路径上的MTU问题,端系统并不知道,因此需要一个告知的机制,这个机制就是路径MTU发现 (PMTUD:  Path MTU Discovery ) ！

## PMTUD

说起PMTUD,我们必须在此回到上面讲到的ICMP需要分片但DF位置一差错报文,还记得那个ICMP差错报文中有一个字段是告知下一跳的MTU值的吗？PMTUD正是利用ICMP需要分片但DF位置一差错报文的这一特性来实现的。
发送方在接收到该差错报文后,会根据该报文给出的下一跳的MTU值计算适合传输的最大段长度,从而在后续的发送报文过程中,避免在中间路径被分片的情况产生。
这在端系统主要是通过在路由表里临时添加目的主机路由并将ICMP差错报文告知的下一跳MTU值跟该主机路由关联起来来实现。
PMTUD的确是个非常不错的机制,但是在复杂的实际网络环境中,有时候会失效,因为为了安全起见,有些网络管理员会在路由器、防火墙等中间设备上设置过滤ICMP报文的安全策略,这将导致ICMP差错报文被这些中间设备丢弃,无法达到发送方,从而引起PMTUD的失效, 网上有个宫一鸣前辈共享的案例——《错误的网络访问控制策略导致PMTUD 实现故障一例》,该案例正是说明这种情况绝好的例子,大家可以自行百度此文档学习参考。

值得一提的是PMTUD仅TCP支持,UDP并不支持PMTUD。

由于PMTUD可能存在ICMP差错报文被过滤的情况,很多中间设备的接口支持adjust tcp mss设置功能,思科路由器一般是在接口模式下使用命令"ip tcp adjust-mss 1400 "来做设置,其他的品牌产品的相关设置大家可在实际工作环境下自查相关品牌和产品的使用手册。

这个功能主要是通过由中间设备修改经过其转发的TCP SYN报文中的MSS值,让中间设备参与进TCP 三次握手时SYN报文的MSS协商来避免分片。

需要注意的是,该功能不像MTU值,只针对出接口,此功能一旦开启,其将针对该接口的收发双向有效。
我做一个简化环境下的工作过程图示以便于大家理解其工作过程:

### 后记
  
Cisco在IOS 12.2(4)T及以后的版本支持修改MSS大小的特性

Cisco的TCP Adjust MSS Feature:

The TCP MSS Adjustment feature enables the configuration of the
  
maximum segment size (MSS) for transient packets that traverse a router,
  
specifically TCP segments in the SYN bit set, when Point to Point Protocol
  
over Ethernet (PPPoE) is being used in the network. PPPoE truncates the
  
Ethernet maximum transmission unit (MTU) 1492, and if the effective MTU
  
on the hosts (PCs) is not changed, the router in between the host and the
  
server can terminate the TCP sessions. The ip tcp adjust-mss command
  
specifies the MSS value . the intermediate router of the SYN packets to
  
avoid truncation.

附: MS文章-路径最大传输单元 (PMTU) 黑洞路由器
  
当路由器必须将 IP 包分段但又因 DF 标记设置为 1 而不能分段时,路由器可采用以下任一种方式:

发送符合 RFC 792 中最初定义的"ICMP Destination Unreachable-Fragmentation Needed and DF Set"消息,然后丢弃该包。
  
原始消息格式中不包含有关转发失败的链路的 IP MTU 的信息。

发送符合 RFC 1191 中重新定义的"ICMP Destination Unreachable-Fragmentation Needed and DF Set"消息,然后丢弃该包。此新消息格式包含一个 MTU 字段,可指出转发失败的链路的 IP MTU。
  
RFC 1191 定义了路径 MTU (PMTU) 发现,它使得成对的 TCP 对等方能够动态地发现二者之间路径的 IP MTU,从而发现该路径的 TCP MSS。一旦收到符合 RFC 1191 定义的"Destination Unreachable-Fragmentation Needed and DF Set"消息,TCP 就会将该连接的 MSS 调整为指定 IP MTU 减去 TCP 和 IP 报头的大小。这样,在该 TCP 连接上发送的后续包就不会超过最大大小,无需分段即可在该路径上传输。

直接丢弃包。
  
直接丢弃需分段但 DF 标记设置为 1 的包的路由器称为 PMTU 黑洞路由器。

PMTU 黑洞路由器会给 TCP 连接带来问题。例如,Microsoft® Windows® XP 和 Windows Server™2003 中的 TCP/IP 协议默认情况下会使用 PMTU 发现。TCP 会发送 DF 标记设置为 1 的数据段,并且在需要时,会根据符合 RFC 1191 定义的"ICMP Destination Unreachable-Fragmentation Needed and DF Set (ICMP Type 3 Code 4) "消息的回执 (其中包含 IP MTU) ,更改 TCP MSS 值。

在 TCP 三次握手期间交换的 TCP 数据段不会太大,因而不会被 PMTU 黑洞路由器丢弃。但是,一旦开始在连接上传输数据—假定基于协商的 MSS 确定的 PMTU 比实际 PMTU 大—TCP 数据段的大于实际 PMTU 的 IP 包就会被直接丢弃。
  
例如,您可以用 FTP 命令行工具成功地与 FTP 服务器建立连接并登录。但是,当您试图下载或者上载文件时,中间的 PMTU 黑洞路由器就会丢弃达到最大大小的 TCP 数据段,从而导致错误和文件传输失败。
  
您可以按照下面的语法使用 Ping 工具来检测 PMTU 黑洞路由器:
  
Pingdestination –f –l ICMPEchoPayloadSize

此处的 destination 可以是一个 IP 地址,也可以是一个可解析为 IP 地址的名称。

-f 选项可将 DF 标记设置为 1。

-l 选项指定 ICMP Echo 消息的有效负载的大小。

ICMPEchoPayloadSize 是 ICMP Echo 消息的有效负载的字节数。
  
要计算 ICMPEchoPayloadSize,可用您想发送的 IP 包的大小减去 28。这是因为,IP 报头的大小为 20 字节,而 ICMP Echo 消息的 ICMP 报头的大小为 8 字节。下图显示了二者的关系。

例如,要发送长度为 1500 字节的 ICMP Echo 消息,您应使用以下命令:
  
ping destination –f –l 1472
  
如果有 IP MTU 更小的中间链路,且路由器发送了"ICMP Destination Unreachable-Fragmentation Needed and DF Set"消息,则 Ping 工具会显示"Packet needs to be fragmented but DF set"消息。如果有 IP MTU 更小的中间链路,且 PMTU 黑洞路由器直接丢弃了包,则 Ping 工具会显示"Request timed out"消息。
  
要找出包含 PMTU 黑洞路由器的路径的有效 IP MTU,请使用 Ping 工具,同时不断增大 Echo 消息的有效负载的大小。因为典型子网的最小 IP MTU 是 576 字节,因此开始时可将 ICMP Echo 消息的有效负载设置为 548 字节,然后每次递增 100 字节,直到找到有效 PMTU。
  
例如,如果 ping 10.0.0.10 -f -l 972 命令显示"Reply from 10.0.0.10",而命令 ping 10.0.0.10 -f -l 973 显示"Request timed out",则 IP 地址为 10.0.0.10 的节点的有效 PMTU 为 1000 字节 (972+28)。

PMTU 黑洞路由器的解决方案和工作方法
  
1. 配置中间路由器以支持路由器端 PMTU 发现
  
解决专用 Intranet 中的 PMTU 黑洞路由器问题的最简单的方法,是将您的所有路由器配置为支持路由器端 RFC 1191,并支持发送 ICMP Destination Unreachable-Fragmentation Needed and DF Set 消息 (其中带有转发失败的链路的 IP MTU) 。这与将路由器配置为支持主机端 RFC 1191 是有区别的,后者的路由器会对自己的 TCP 连接使用 PMTU 发现。
  
在 Internet 上进行通信时,通常不太可能将 Internet 路由器配置为支持路由器端 PMTU 发现。在这种情况下,您可以使用以下各节介绍的工作方法。
  
3. 确定最佳 IP MTU 并通过 MTU 注册表设置来设置该值
  
启用 PMTU 黑洞路由器检测的替代方法,是根据本文前面部分的介绍使用 Ping 工具确定所有相关路径的 PMTU 值,然后使用注册表设置手动配置发送接口的 IP MTU。
  
该方法通过不停发送 DF 标记设置为 1,大小又不会导致 PMTU 黑洞路由器将其直接丢弃的 IP 包来避开 PMTU 黑洞路由器。手动指定 IP MTU 意味着所有通信量 (包括本地子网通信量和不包含 PMTU 黑洞路由器的路径上的通信量) 都将使用较小的 IP MTU。
  
确定有效的 PMTU 后,您可以通过以下步骤手动指定 TCP/IP 接口的 IP MTU:

1. 打开 Network Connections 文件夹,记下 LAN 连接的名称,如"Local Area Connection"。
2. 单击开始,单击"运行",键入"regedit.exe",然后单击"确定"。
3. 使用注册表编辑器工具的树图 (左边窗格) 打开如下键: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control \Network\{4D36E972-E325-11CE-BFC1-08002BE10318}
4. 此键下面是与已安装的 LAN 连接相关联的全局唯一标识符 (GUID) 的一个或多个键。这些 GUID 键中的每一个都有一个 Connection 子键。打开每个 GUID\Connection 键,寻找值与第一步中记下的 LAN 连接的名称匹配的 Name 设置。
5. 如果找到包含与 LAN 连接匹配的 Name 设置的 GUID\Connection 键,请写下或记下该 GUID 值。
6. 使用注册表编辑器的树视图打开如下键: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip \Parameters\Interfaces\GUID
7. 右键单击树视图中的"GUID"键,指向"新建",然后单击"双字节值"。
8. 在注册表编辑器工具的内容窗格 (右窗格) 中,为新注册表设置的值键入 MTU,然后按 ENTER。
9. 在内容窗格中,双击新的 MTU 设置,并在"编辑双字节值"对话框中选择"十进制",然后在"数值数据"中键入有效 MTU 值。
10. 单击"确定"。关闭注册表编辑器工具。
11. 重新启动计算机使 MTU 设置生效。

网络故障举例: [转自华为3COM全球服务论坛]

现象描述:
  
组网:
  
PC－AR2831－AR2880－CISCO设备组成的核心网－SERVER
  
网络运行MPLS VPN;AR2880为PE;AR2831为CE,PE、CE间运行OSPF,多CE配置；路由器各接口MTU、TCP MSS值采用默认设置
  
AR2880: Version 3.30, Release 0008
  
AR2831: Version 3.30, Release 0008
  
现象1:
  
AR2880路由器的以太口MTU使用缺省设置时,使用的OA系统(BS架构)部分流程无法运行,上网发邮件时附件无法粘贴；但是在cisco设备上,同样的组网没有发现问题；
  
现象2:
  
将AR2880路由器的以太口MTU改为512测试,邮件附件可以粘贴,但OA主页打开后无内容,刷新不了；将AR2880路由器的以太口MTU改为1200测试,邮件附件可以粘贴,OA主页可以正常显示,但是点击OA系统的"起草公文"无页面弹出,正常状况下应弹出新建公文页面；

告警信息:
  
无
  
原因分析:
  
原因分析:
  
可能是应用软件问题；可能是MTU 、TCP MSS值协商配置问题；
  
具体分析:
  
1. 接口MTU、TCP MSS采用缺省值1500时,无法贴附件；
  
这是因为应用了三层MPLS VPN技术,增加了8bit的标签,MTU值协商出现问题。
  
AR28XX路由器默认在接口上自动分片,所以在普通的应用中采用默认值不会影响业务。但路由器接口上收到一个报文长度大于本接口MTU值的报文,如果该报文被强制打上不分片的标记,将丢弃报文,并返回一个ICMP差错报文 (type 3,code 4) ,通知报文发起者丢弃原因。报文发起者将发送比较小的报文。通过多次上述报文协商,将得到对于某一个固定路径上的最小Mtu值,这个过程叫做Mtu Discovery ,通过MTU Discovery来确定报文路径上最小可通过的MTU；如果两个设备相连,没有MTU Discovery功能并且MTU值不一致,将可能导致丢弃报文。只有把双方设备的Mtu为对端设备MRU的最小值,才能正常通信。由于某些组网考虑到网络安全问题和性能,往往会把ICMP报文过滤掉,引起Mtu Discovery不能正常运行；应用软件由于程序算法问题或根本没有相应协商功能,也会导致了部分应用异常。
  
2. 更改接口MTU值以后,仍然有部分业务不正常；
  
这是因为TCP MSS值协商的问题。
  
MSS值的计算方法是: MSS=MTU-IP-TCP (如果有其他pppoe、加密报文头的话也同样减去) ,也就是说MSS值其实就是TCP所承载的净载荷的长度。由于AR28XX接口缺省的MTU是1500字节,故一般要求加密报文头+链路层开销+IP头 (20-60字节) +TCP报文 (20字节) 小于1500字节,即TCP分片配置1200左右比较适合。缺省情况下,TCP报文不分片。因此TCP MSS不匹配也会引起部分应用异常。

处理过程:
  
本例中通过修改路由器接口MTU、TCP MSS值,解决问题。
  
具体报文mtu 、tcp mss大小要根据具体应用,按经验值进行尝试,选择最佳值；其中MTU值的选择可以通过ping命令设置不分片来进行测试；TCP MSS值的选择则可以通过MTU减去相应其它加密、链路层开销、IP头、TCP头等字节计算。
  
具体过程如下:
  
1. 本例中使用cisco路由器时相关应用正常。初步估计是mtu值问题,但是对普通应用AR28系列路由器会自动分片,不会影响业务。测试发现在client上ping大包的时候,如果不设置不允许分片,业务正常。看来客户应用中做了不允许分片的设置或其它原因mtu协商错误。更改路由器接口mtu为1500-8＝1492以后,业务正常。
  
2. 更改接口mtu以后,其它部分业务还不正常。分析原因是tcp mss值的问题。减小tcp mss值8字节1460-8＝1452,但是还有部分业务不正常。询问软件集成商,得到答复部分软件中使用了加密技术。而且不同的应用加密强度不同。
  
3. 逐步调整路由器接口的tcp mss值,减到到1200以后,所有业务测试通过。

命令说明:
  
1. mtu命令用来设置以太网接口的MTU (最大传输单元) ,undo mtu命令用来恢复MTU的缺省值。缺省的MTU为1500。使用mtu命令改变接口最大传输单元MTU后,需要先对接口执行shutdown命令,再执行undo shutdown命令将接口重启,以保证设置的MTU生效。
  
2. tcp mss命令用来配置TCP报文分片,undo tcp mss命令用来取消TCP报文分片。

个人总结:

MTU=MSS+IP header+TCP header+链路层开销+加密报文头 (某些程序加密强度不一样)

MTU,对UDP和TCP报文都检测,当超过时,如果报文DF=0 ,就进行分段,如果DF=1,就丢弃,同时返回RFC 792定义的ICMP Type3 Code 4 (ICMP Destination Unreachable-Fragmentation Needed and DF Set) 或 RFC 1191定义的ICMP包 (包含转发失败链路的MTU) ,主机收到后会调节MSS以适应,后续包不会分片就可进行传输。如果两端之间某Router 配置了ACL ,deny掉所有的ICMP,那就无法收到咯。

MSS其实就是TCP报文payload大小。一般的应用软件,当客户端和服务器端在建立TCP连接的时候需要根据实际传输的报文大小来协商TCP的窗口大小MSS。Tcp连接成功后会进行两次滑动窗口的协商,一次是pc与server,一次是与网关,然后在两次协商里选择一个较小的值作为窗口来发送报文。

当协商出来的MSS比较大时,加上IP header+TCP header+链路层开销+加密报文头后,就有可能大于MTU,当DF=1时,就会丢弃掉。

正如     所说: "对于UDP协议而言,这个协议本身是无连接的协议,对数据包的到达顺序以及是否正确到达不甚关心,所以一般UDP应用对分片没有特殊要求。"所以在路由器上进行ip tcp mss命令只对tcp packet检测就够了。

再提供一个案例: MSN是使用https方式登陆的,有时会有突发大报文,而且DF位是设置为1的。虽然目前大部分出现的故障现象都是: 不能发送附件；不能打开网页等。都是在PPPoE中发生的。但就算源和目的网络的MTU都是1500,但是由于中间经过的节点链路可能存在不同,可能少于1500。或者在传输过程中的某个路由器设置了较小的MTU。而往往配置路由器或交换机时,习惯禁止了所有的ICMP信息,这样的话那路由器就无法返回ICMP 3/4的包给源主机了。 RFC 2923  (TCP Problems with Path MTU Discovery) 。

所以,有时候出现的故障,不止要调试MTU值,还要调试MSS值,才能使所有应用正常
  
其实碰到此问题时,最好是借助Sniffer抓包分析 (不过奇怪,锐捷NBR1000无法抓到ICMP Type 3 Code 4的包,所以无法抓包提供分析图,好可惜！是路由器不支持还是其他原因,以后有机会考证)

附: Sniffer抓包协助理解分片过程以及DF

上图是: Ping –l 2000 [url]www.163.com[/url]
  
首先看IP header,More fragments位为1,向对方通告此数据包为多帧发送 (分段) ,total lengt=1300bytes (1280bytes+IP报头20bytes) 。再看ICMP处,可以看到分了两个包,大小分别为1280bytes和728bytes,2008 bytes of reassembled data指明重组后的数据为2008bytes (icmp包头8bytes,数据2000bytes) 。然后看DLC部分,指明了以太类型0800 (IP) ,帧大小为1314bytes (ICMP的1280bytes+IP报头20bytes+帧14bytes)

再接着看下一个帧。首先看到DLC部分写着了帧大小为762bytes,IP部分,continuation of frame 17 ,第17个帧的后续。Fragment offset 分段偏移量为1280bytes (第一个包的大小) 。至此,第一个icmp echo包全部发送完毕。

ping –f –l 1200 [url]www.163.com[/url]
  
-f命令: 将数据报DF (don't fragment) 位设置为1 (不能分段)
  
本文出自 "我是木头" 博客,请务必保留此出处<http://infotech.blog.51cto.com/391844/123859>
<http://infotech.blog.51cto.com/>
<https://zhuanlan.zhihu.com/p/139537936>

## MTU, MSS

><http://blog.crhan.com/2014/05/mtu-and-mss/>

MTU 到底是怎么来的
  
MTU, 是 Maximum Transmission Unit 的缩写, 根据 Wikipedia 的定义, MTU 指的是在 Network Layer (因处 OSI 第三层, 后以 L3 代替) 上传输的最大数据报单元, 而 MTU 的大小一般由 Link Layer (因处 OSI 第二层, 后以 L2 代替) 设备决定. 比如生活中使用最广泛的以太网(Ethernet, IEEE 802.3)的帧大小是 1518 字节, 根据 Ethernet Frame 的定义, L2 Frame 由 14 字节 Header 和 4 字节 Trailer 组成, 所以 L3 层(也就是 IP 层)最多只能填充 1500 字节大小, 这就是 MTU 的由来.

## 802.3 Ethernet MTU
  
    +-------------+------------+-----------------+---------+----------------+
    | Dest MAC(6) | Src MAC(6) | Eth Type/Len(2) | Payload | CRC Trailer(4) |
    +-------------+------------+-----------------+---------+----------------+

所以说, 当使用 Ethernet 介质时确定只能传最大 1518 字节的帧后, 减去 18 字节的 L2 头和尾, 留给 IP 层的就只有 1500 字节了.

PS: 标准文档中中所说的 LLC 层因为在实际应用中基本不存在, 所以 802.3 标准 MTU 是 1492, 但是实际使用中的 MTU 是 1500.
  
L2, L3 示意图
  
+-----------+
| IP Layer(1500) |
+-----------+
| Link Layer(1518) |
+-----------+
  
## PPPoE MTU
  
另一个典型的 MTU 是拨号上网( PPPoE )的 1492 字节, 通过以太网接入的 PPPoE 的封包结构上会在 L2 和 L3 之间插入两层, 一层 PPP 协议和一层 PPPoE 协议. 但是因为传输的底层仍然使用的是以太网, 所以上层包大小仍然受 L2 大小限制. MTU 这样算, Link Layer 长 1518 字节, 所以 PPPoE Layer 最长 1500 字节, 然后 PPPoE 头占用 6 字节, PPP 头占用 2 字节, 所以留给 IP 层的最大空间就剩下了 1492 字节:

+-----------+
| IP Layer(1492) |
+-----------+
| PPP Layer(1494) |
+-----------+
| PPPoE Layer(1500) |
+-----------+
| Link Layer(1518) |
+-----------+
  
VLAN(802.1Q) MTU
  
VLAN (IEEE 802.1Q) 的实现是在 L2 头部扩展了一个 4 字节大小的字段, 分别是 2 字节协议识别码(TPID)和 2 字节的控制信息(TCI), 这导致了 L2 的头和尾加起来的长度变成了 22 字节, 所以 L3 的 MTU 就被压缩到了 1496 字节:

+-----------+
| IP Layer(1496) |
+-----------+
| Link Layer(1518) |
+-----------+
  
然而在 802.3ac 标准之后的以太网帧大小则扩展到了 1522 字节, 也就是说在这个标准下的 Ethernet, MTU 也可以设定成 1500 字节了.

+-----------+
| IP Layer(1500) |
+----------+
| Link Layer(1522) |
+-----------+
  
## TCP MSS
  
MSS (Maximum Segment Size) 是 TCP Layer (L4) 的属性, MSS 指的是 TCP payload 的长度. 当在 MTU 1500 的网络上传输时, MSS 为 1460 (即 1500 减去 20 字节 IP 头, 20 字节 TCP 头).

为什么 L3 有 MTU 后 L4 还要 MSS 呢?
  
MTU 和 MSS 的功能其实基本一致, 都可以根据对应的包大小进行分片, 但实现的效果却不太一样.

L3 (IP) 提供的是一个不可靠的传输方式, 如果任何一个包在传输的过程中丢失了, L3 是无法发现的, 需要靠上层应用来保证. 就是说如果一个大 IP 包分片后传输, 丢了任何一个部分都无法组合出完整的 IP 包, 即是上层应用发现了传输失败, 也无法做到仅重传丢失的分片, 只能把 IP 包整个重传. 那 IP 包越大的话重传的代价也就越高.

L4 (TCP) 提供的是一个可靠的传输方式, 与 L3 不同的是, TCP 自身实现了重传机制, 丢了任何一片数据报都能单独重传, 所以 TCP 为了高效传输, 是需要极力避免被 L3 分片的, 所以就有了 MSS 标志, 并且 MSS 的值就是根据 MTU 计算得出, 既避免了 L3 上的分片, 又保证的最大的传输效率.

>RFC 1042: A Standard for the Transmission of IP Datagrams over IEEE 802 Networks
>RFC 1122: Requirements for Internet Hosts - Communication Layers
>RFC 879: The TCP Maximum Segment Size and Related Topics
