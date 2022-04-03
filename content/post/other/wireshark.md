---
title: Wireshark
author: "-"
date: 2011-10-22T15:04:44+00:00
url: wireshark
categories:
  - Network

tags:
  - reprint
---
## Wireshark
Wireshark (前称Ethereal) 是一个网络封包分析软件。网络封包分析软件的功能是撷取网络封包，并尽可能显示出最为详细的网络封包资料。

网络封包分析软件的功能可想像成 "电工技师使用电表来量测电流、电压、电阻" 的工作 - 只是将场景移植到网络上，并将电线替换成网络线。
在过去，网络封包分析软件是非常昂贵，或是专门属于营利用的软件。Ethereal的出现改变了这一切。在GNUGPL通用许可证的保障范围底下，使用者可以以免费的代价取得软件与其源代码，并拥有针对其源代码修改及客制化的权利。Ethereal是目前全世界最广泛的网络封包分析软件之一。

### 应用  
Wireshark使用目的以下是一些使用Wireshark目的的例子: 

    网络管理员使用Wireshark来检测网络问题，网络安全工程师使用Wireshark来检查资讯安全相关问题，开发者使用Wireshark来为新的通讯协定除错，普通使用者使用Wireshark来学习网络协定的相关知识当然，有的人也会"居心叵测"的用它来寻找一些敏感信息……
  
  
  
    Wireshark不是入侵侦测软件 (Intrusion DetectionSoftware,IDS) 。对于网络上的异常流量行为，Wireshark不会产生警示或是任何提示。然而，仔细分析Wireshark撷取的封包能够帮助使用者对于网络行为有更清楚的了解。Wireshark不会对网络封包产生内容的修改，它只会反映出目前流通的封包资讯。 Wireshark本身也不会送出封包至网络上。
 
### 发展简史
1997年底，GeraldCombs需要一个能够追踪网络流量的工具软件作为其工作上的辅助。因此他开始撰写Ethereal软件。Ethereal在经过几次中断开发的事件过后，终于在1998年7月释出其第一个版本v0.2.0。自此之后，Combs收到了来自全世界的修补程式、错误回报与鼓励信件。Ethereal的发展就此开始。不久之后，GilbertRamirez看到了这套软件的开发潜力并开始参予低阶程式的开发。1998年10月，来自NetworkAppliance公司的GuyHarris在寻找一套比tcpview (另外一套网络封包撷取程式) 更好的软件。于是他也开始参与Ethereal的开发工作。1998年底，一位在教授TCP/IP课程的讲师RichardSharpe，看到了这套软件的发展潜力，而后开始参与开发与加入新协定的功能。在当时，新的通讯协定的制定并不复杂，因此他开始在Ethereal上新增的封包撷取功能，几乎包含了当时所有通讯协定。
  
  
  
自此之后，数以千计的人开始参与Ethereal的开发，多半是因为希望能让Ethereal撷取特定的，尚未包含在Ethereal默认的网络协定的封包而参予新的开发。2006年6月，因为商标的问题，Ethereal更名为Wireshark。
- `[TCP ZeroWindow]`: 接收者向发送者发送的一种窗口警告，告诉发送者你的接收窗口已满，暂时停止发送。
- [TCP Window Full]: 服务端向客户端发送的一种窗口警告，表示已经发送到数据接收端的极限了。
- [TCP Window Update]: 缓冲区已释放为所示的大小，因此请恢复传输。

## wireshark 时序图

菜单>统计>TCP流图形>时间序列

## 窗口尺寸
菜单>统计>TCP流图形>窗口尺寸

>https://www.codenong.com/cs106112955/
