---
author: "-"
date: "2020-11-06 16:37:13" 
title: "tcp dump, wireshark"
categories:
  - inbox
tags:
  - reprint
---
## "tcp dump, wireshark"

### TCP segment of a reassembled PDU

关于"TCP segment of a reassembled PDU"

标签: TCP segment of a reaPDUreassembled PDU

[http://blog.csdn.net/dog250/article/details/51809566](http://blog.csdn.net/dog250/article/details/51809566)

版权声明: 本文为博主原创,无版权,未经博主允许可以随意转载,无需注明出处,随意修改或保持可作为原创！

为什么大家看到这个以后总是会往MSS,TSO上联系呢？也许第一个解释这个的人是个高手,而且以MSS/MTU/TSO的观点解释了这个问题,还有一种可能就是TSO等技术让人觉得太牛逼,毕竟是底层硬件机制吧,抓包机制又是作用于网卡层面的,所以很自然会觉得TSO会有关联。

事实上,这个跟TSO没有关系！跟MSS有一定的关系但不是全部因果关系,在阐述"TCP segment of a reassembled PDU"之前,先把TSO理清再说。当有人问题"这个包会不会被TSO分段"这类问题时,只要看该TCP数据包的长度,拿它跟MTU比较,如果数据长度更长,则就是TSO。

那么,"TCP segment of a reassembled PDU"究竟是什么呢？答案是,这要向上看,这个跟应用层有关,而与底层关系不大！我用Wireshark的抓包例子来解释这个问题。首先看一个抓包,我们以网络测试工具baidu为例,抓取一个访问其服务器[https://14.215.177.38/的一个HTTPS](https://14.215.177.38/的一个HTTPS)连接的包:

网上很多人在解释这个"TCP segment of a reassembled PDU"的时候(基本都是转载),都说什么"ACK了同一笔数据就会是reassembled PDU","同一个GET请求的response"云云...但是很显然,上述我抓包的截图中,402到405号包都有ACK了同一个序列号,但是为什么只有一个"TCP segment of a reassembled PDU"呢？？在没有标识reassembled PDU的数据包中,另外标识了TLSv1.2的协议原语。此时,我来做一个动作,按下"Ctrl-Shift-E"组合键,事实上就是点击"分析"菜单,进入"已启用的协议"界面:

反选SSL协议,不再识别SSL协议之后,我们再看402到405号数据包:

没有了"TCP segment of a reassembled PDU"这些,除了没有这些"修饰语"之外,其它的协议层面的数据完全和之前识别SSL协议的时候相符合。我们的结论是,关掉了对SSL协议的识别,就没有了reassembled PDU的修饰,这恰恰是因为SSL协议让Wireshark知道403号包是一个reassembled PDU！如果你不知道这是个SSL协议,你就无法判断出这是不是一个reassembled PDU！

是的,这就是原因。接下来,为什么SSL协议就能识别这是一个reassembled PDU呢？这就要看你对SSL协议是否理解了,起码我是懂的,在握手阶段,Server Hello和Server的Certificate是背靠背发送的,也就是说它们是连着发给Client的,一个Server Hello,外加一个证书,一起发给Client,接下来就是不那么根本但很显然的事情了,如果这些包的总和足够小或者链路的MTU足够大,能够一次性发送过去的话,那当然好,如果不能,很显然要拆成几个分段发送了,如果中间的那个分段不能被SSL协议的原语识别,那么就会被标识成reassembled PDU,这就是为什么404,405号数据包都是连续发送的,但是却未被识别为reassembled PDU,因为SSL协议知道它们是Certificate消息和Server Key Exchange消息。

现在明白了吗？我特意没有用HTTP协议去解释这个而是选择了用SSL协议,目的就是想让大家明白,并不是针对同一个GET请求的同一笔回应会被标识为reassembled PDU！而是完全靠着应用层协议原语来识别协议消息。如果你的Wireshark被配置成不识别任何协议,比如不识别HTTP协议,SSL协议,那也就不会出现reassembled PDU了,因为Wireshark不知道到底是不是！实际上Wireshark支持你去自定义你自己的协议插件,你可以试一下,自己开发一个简单的协议,就算你的TCP数据段总和没有超过一个MSS,比如你的socket每发100字节就sleep 10秒,并且TCP socket没有设置Nagle算法,那么虽然每个段只有100字节,远没有到一个MSS,也会有reassembled PDU的标识！

本质上来讲,reassembled PDU要向上看,而不是去考虑什么底层的MTU,TSO什么的。Wireshark根据它能识别的应用层协议,告诉你哪些数据是属于一个应用层消息的。就这么简单。

作者: 守望者_1065
链接: [https://www.jianshu.com/p/d4d1d76c3956](https://www.jianshu.com/p/d4d1d76c3956)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

### PDU (Protocol Data Unit) 协议数据单元

协议数据单元PDU (Protocol Data Unit) 是指对等层次之间传递的数据单位。协议数据单元(Protocol Data Unit )物理层的 PDU是数据位 (bit) ,数据链路层的 PDU是数据帧 (frame) ,网络层的PDU是数据包 (packet) ,传输层的 PDU是数据段 (segment) ,其他更高层次的PDU是数据 (data) 。

在分层网络结构,例如在开放式系统互联(OSI)模型中,在传输系统的每一层都将建立协议数据单元(PDU)。PDU包含来自上层的信息,以及当前层的实体附加的信息。然后,这个PDU被传送到下一较低的层。物理层实际以一种编帧的位流形式传输这些PDU,但是由协议栈的较高层建造这些PDU。接收系统自下而上传送这些分组通过协议栈,并在协议栈的每一层分离出PDU中的相关信息。重要的一点是,每一层附加到PDU上的信息,是指定给另一个系统的同等层的。这就是对等层如何进行一次通信会话协调的。通过从传输层段剥离报头,执行协议数据检测以确定作为传输层段的部分数据的协议段的数据,以及执行标志验证和剥离,从而处理数据段。还提供用于处理数据段的技术,其中接收到协议数据单元的报头部分。利用所接收的报头部分来确定将储存在应用空间中的数据的字节数。而且,利用所接收的报头部分来确定下一个协议数据单元的下一个报头部分。然后,发出窥视命令以获得下一个报头部分。另外提供用于利用所储存的部分循环冗余校验摘要和剩余数据来执行循环冗余校验的技术。

MAC (Media Access Control) 层与 LLC (Logic Link Control) 层的区别

LLC子层实现数据链路层与硬件无关的功能,比如流量控制、差错恢复等 (LLC子层负责向其上层提供服务)
较低的MAC子层提供LLC和物理层之间的接口。 (MAC子层的主要功能包括数据帧的封装/卸装,帧的寻址和识别,帧的接收与发送,链路的管理,帧的差错控制等。MAC子层的存在屏蔽了不同物理链路种类的差异性)
 (一) MAC 子层作用
MAC子层负责把物理层的"0"、"1"比特流组建成帧,并通过帧尾部的错误校验信息进行错误校验；提供对共享介质的访问方法,包括以太网的带冲突检测的载波侦听多路访问 (CSMA/CD) 、令牌环 (Token Ring) 、光纤分布式数据接口 (FDDI) 等 。
MAC子层分配单独的局域网地址,就是通常所说的MAC地址 (物理地址) 。MAC子层将目标计算机的物理地址添加到数据帧上,当此数据帧传递到对端的MAC子层后,它检查该地址是否与自己的地址相匹配,如果帧中的地址与自己的地址不匹配,就将这一帧抛弃；如果相匹配,就将它发送到上一层中

 (二) LLC子层的主要功能包括:

传输可靠性保障和控制；
数据包的分段与重组；
数据包的顺序传输。
LLC子层提供三种服务:

1. 无确认无连接的服务。这是数据包类型的服务。
2. 连接方式的服务。这种服务类似于HDLC提供的服务。
3. 有确认无连接的服务。提供有确认的数据包,但不建立连接。

LLC子层维护一张以DSAP为索引的函数列表,每接收到一个数据包,以DSAP为索引调用相应的函数,该函数把数据包挂到相应接收队列。

作者: 赛亚人之神
链接: [https://www.jianshu.com/p/7af3c034929e](https://www.jianshu.com/p/7af3c034929e)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

[TCP Spurious Retransmission]

- TCP虚假重传

发送端认为发送的package已经丢失了,所以重传了,尽管此时接收端已经发送了对这些包的确认。

指实际上并没有超时,但看起来超时了,导致虚假超时重传的原因有很多种:

 (1) 对于部分移动网络,当网络发生切换时会导致网络延时突增

 (2) 当网络的可用带宽突然变小时,网络rtt会出现突增的情况,这会导致虚假超时重传

 (3) 网络丢包 (原始和重传的包都有可能丢包) 会导致虚假重传超时。

[Reassembly error, protocol TCP: New fragment overlaps old data (retransmission?)]
-重新组装错误,协议TCP:新片段与旧数据重叠(重新传输?)
[Reassembly error, protocol TCP: New fragment overlaps old data (retransmission?)] 说明有部分的tcp段出现了重传。

### 网络抓包、分析、重放
[https://my.oschina.net/u/4258573/blog/3327617](https://my.oschina.net/u/4258573/blog/3327617)
