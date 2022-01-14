---
title: MTU, MSS
author: "-"
date: 2017-05-22T08:35:54+00:00
url: /?p=10333
categories:
  - Uncategorized

---
## MTU, MSS
http://blog.crhan.com/2014/05/mtu-and-mss/

MTU 到底是怎么来的
  
MTU, 是 Maximum Transmission Unit 的缩写, 根据 Wikipedia 的定义, MTU 指的是在 Network Layer (因处 OSI 第三层, 后以 L3 代替)上传输的最大数据报单元, 而 MTU 的大小一般由 Link Layer (因处 OSI 第二层, 后以 L2 代替) 设备决定. 比如生活中使用最广泛的以太网(Ethernet, IEEE 802.3)的帧大小是 1518 字节, 根据 Ethernet Frame 的定义, L2 Frame 由 14 字节 Header 和 4 字节 Trailer 组成, 所以 L3 层(也就是 IP 层)最多只能填充 1500 字节大小, 这就是 MTU 的由来.

802.3 Ethernet MTU
  
+-----+----+------+---+------+
  
| Dest MAC(6) | Src MAC(6) | Eth Type/Len(2) | Payload | CRC Trailer(4) |
  
+-----+----+------+---+------+
  
所以说, 当使用 Ethernet 介质时确定只能传最大 1518 字节的帧后, 减去 18 字节的 L2 头和尾, 留给 IP 层的就只有 1500 字节了.

PS: 标准文档中中所说的 LLC 层因为在实际应用中基本不存在, 所以 802.3 标准 MTU 是 1492, 但是实际使用中的 MTU 是 1500.
  
L2, L3 示意图
  
+-----------+
  
| IP Layer(1500) |
  
+-----------+
  
| Link Layer(1518) |
  
+-----------+
  
PPPoE MTU
  
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
  
+-----------+
  
| Link Layer(1522) |
  
+-----------+
  
TCP MSS
  
MSS (Maximum Segment Size)是 TCP Layer (L4) 的属性, MSS 指的是 TCP payload 的长度. 当在 MTU 1500 的网络上传输时, MSS 为 1460 (即 1500 减去 20 字节 IP 头, 20 字节 TCP 头).

为什么 L3 有 MTU 后 L4 还要 MSS 呢?
  
MTU 和 MSS 的功能其实基本一致, 都可以根据对应的包大小进行分片, 但实现的效果却不太一样.

L3 (IP) 提供的是一个不可靠的传输方式, 如果任何一个包在传输的过程中丢失了, L3 是无法发现的, 需要靠上层应用来保证. 就是说如果一个大 IP 包分片后传输, 丢了任何一个部分都无法组合出完整的 IP 包, 即是上层应用发现了传输失败, 也无法做到仅重传丢失的分片, 只能把 IP 包整个重传. 那 IP 包越大的话重传的代价也就越高.

L4 (TCP) 提供的是一个可靠的传输方式, 与 L3 不同的是, TCP 自身实现了重传机制, 丢了任何一片数据报都能单独重传, 所以 TCP 为了高效传输, 是需要极力避免被 L3 分片的, 所以就有了 MSS 标志, 并且 MSS 的值就是根据 MTU 计算得出, 既避免了 L3 上的分片, 又保证的最大的传输效率.

参考资料:
  
RFC 1042: A Standard for the Transmission of IP Datagrams over IEEE 802 Networks
  
RFC 1122: Requirements for Internet Hosts - Communication Layers
  
RFC 879: The TCP Maximum Segment Size and Related Topics