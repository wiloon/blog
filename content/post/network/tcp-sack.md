---
author: "-"
date: "2020-11-07 23:41:33" 
title: "tcp sack"
categories:
  - inbox
tags:
  - reprint
---
## "tcp sack"
https://blog.csdn.net/wdscq1234/article/details/52503315

TCP-IP详解: SACK选项 (Selective Acknowledgment) 
 
引入理由
在文章TCP-IP详解: 超时重传机制中,有介绍到快速重传和超时重传都会面临到一个重传什么包的问题,因为发送端也不清楚丢失包后面传送的数据是否有成功的送到。主要原因还是对于TCP的确认系统,不是特别的好处理这种不连续确认的状况了,只有低于ACK number的片段都被收到才有进行ACK,out-of-order的片段只能是等待,同时,这个时间窗口是无法向右移动的。

举个例子: 

1. 服务发送4个片段给客户端,seg1(seq=1,len=80),seg2(seq=81,len=120), seg3(seq=201,len=160),seg4(seq=361,len=140)

2. 服务器收到seg1和seg2的ACK = 201,所以此时seg1 seg2变成发送并已经确认范畴的数据包,被移除滑动窗口,此时服务器又可以多发80+120 byte数据

3. 假设seg3由于某些原因丢失,这个时候服务器仍然可以像客户端发送数据,但是服务器会等待seg3的ACK,否则窗口无法滑动,卡主了

4. seg3丢失了,即使后面的seg4收到了,客户端也无法告知服务器已经收到了seg4,试想一下,如果窗口也够大,服务器可以继续持续发送更多的片段,那么这些片段被客户端接收,只能存放到队列中,无法进行确认

正式因为后续OUT-OF-ORDER的报文段的发送状况也不清楚,所以Server也不是特别清楚要如何去处理这种状况,不过一般来说只能有2中状况: 

1. 只重传超时的数据包,这种方法是最常想到的,比较实用与后面的数据包都能够正常接收的状况,只重传超时的数据包,但是如果比较坏的情况下,丢失了很多封包呢？  那就需要一个一个的等待超时了,很浪费时间。

2. 重传这个片段以及之后的所有包,这种方法在最坏的状况下,看起来效率还是挺高的,但是如果只有一个包丢失,就去重传后面所有接受到的包,流量浪费也是很严重的。

总之对于上面阐述的问题,没有想到一个好的思路来解。但是RFC2018提供了一个SACK的方法,有效的解决这个问题


SACK(Selective Acknowledgment)
SACK是一个TCP的选项,来允许TCP单独确认非连续的片段,用于告知真正丢失的包,只重传丢失的片段。要使用SACK,2个设备必须同时支持SACK才可以,建立连接的时候需要使用SACK Permitted的option,如果允许,后续的传输过程中TCP segment中的可以携带SACK option,这个option内容包含一系列的非连续的没有确认的数据的seq range,这些

SYN包中SACK Permitted 选项,双方都支持才对



SACK option格式

Kind 5  Length  剩下的都是没有确认的segment的range了 比如说segment 501-600 没有被确认,那么Left Edge of 1st Block = 501,Right Edge of 1st Block = 600,TCP的选项不能超过40个字节,所以边界不能超过4组。


可以看下实际的tcpdump抓包中的SACK option,如下图,使用tcp.option.sack进行过滤,可以看到这个SACK option只有一个片段,接收并没有进行确认,范围是18761~20101


再来将上面的例子

客户端收到seg4的时候,发送seg3的ACK 会产生一个SACK的option (361~500) ,Server收到这个ACK后,就知道seg3丢失了,但是seg4已经收到了但是并没有确认,所以就只会重传seg3


SACK的产生,RFC2018
SACK通常是由数据接收方产生,如果在connection建立的时候,SYN包中有SACK-Permitted 的选项为true,同时自身也支持SACK,那么可以在接收异常的时候,产生SACK option. 如果要发送,SACK中需要携带接收队列中所有没有被确认的数据段信息。

如果接收方选择发送带有SACK的ACK,需要遵循如下规则: 

1. 第一个block需要指出是哪一个segment触发SACK option ,我认为就是谁乱序了,才会导致SACK

2. 尽可能多的把所有的block填满

3. SACK 要报告最近接收的不连续的数据块

接收端的行为: 

1. 数据没有被确认前,都会保持在滑动窗口内

2. 每一个数据包都有一个SACKed的标志,对于已经标示的segment,重新发送的时候会忽略

3. 如果SACK丢失,超时重传之后,重置所有数据包SACKed 标志


D-SACK RFC2883
D-SACK主要是使用了SACK来告诉发送方有哪些数据被重复接收了,如果是D-SACK,那么SACK option的第一个block代表被重复发送的序列片段

需要注意的点: 

1. D-SACK仅仅是接收端报告一个重复的连续的片段

2. 每个重复的连续片段只能在一个block中

3.  重复片段的序列号

4. 第二个block指的是data没有被确认的

分析一下RFC2883的例子: 

1. Reproting a Duplicate Segment

如下图:  发送端发送seg1和seg2,但是接收端的ACK都被drop掉了,超时重传seg1,然后接收端就发了一个D-SACK,告诉发送端3000~3499重复接收,需要接收4000的。


2. 报告OUT-OF-ORDER段和重传段

从图中可以看出seg4 out-of-order会触发SACK,说明已经收到但是没有确认的数据,但是这个丢掉了,通过发送方又重传了seg1,然后接收方此时会生成D-SACK,block1中存放了dup的segment,block2中存放了收到但没有确认的segment


还有比较多的例子,详细的可以参考 RFC2883。

总起来说D-SACK还是带了诸多的好处,能否让发送方了解是ACK丢了还是发送的数据包丢了,重复发送就说明是ACK丢了呗,同时也能够掌握网络上的一些事情,比如out-of-order,超时重传等,这样了解了网络,才能更好的做流控。

