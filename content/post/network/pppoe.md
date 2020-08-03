+++
author = "w1100n"
date = "2020-08-02 11:58:43" 
title = "pppoe"

+++

PPP: Point-to-Point Protocol，链路层协议。用户实现点对点的通讯。
PPPoE的工作过程分成两个阶段，即发现阶段(Discorvery)和PPP会话阶段。

发现阶段(Discovery Stage)的具体过程如下：
1. 用户主机用广播的方式发出PADI (PPPOE Active Discovery Initiatio) 包，准备去获得所有可连接的接入设备（获得其MAC地址）；
2. 接入设备收到PADI包后，返回PADO (PPPOE Active Discovery Offer) 作为回应；
3. 用户主机从收到的多个PADO包中，根据其名称类型名或者服务名，选择一个合适的接入设备，然后发送PADR (PPPOE Active Discovery Request) 包，另外如果一个用户主机在发出PADI后在规定时间内没有收到PADO，则会重发PADI；
4. 接入设备收到PADR包后，返回PAS (PPPOE Active Discovery Session-confirmation) 包，其中包含了一个唯一session ID，双方进入PPP会话阶段。

PPP会话阶段，即在session建立后的通讯阶段。
另外，无论是用户主机还是接入设备可随时发起PADT包，中止通讯。
与PPPoE相对应的获得地址和认证的是DHCP，但普通家庭用户很少直接使用DHCP方式接入互联网（这里说的DHCP不是自家路由器上的DHCP，而是互联网运营商的DHCP）。PPPoE和DHCP的区别是：前者需要身份验证才能上网，后者什么都不需要，直接接上网线即可。当然了，具体获得IP地址的方式还有很多。

作者：北极
链接：https://www.zhihu.com/question/25847423/answer/31563282
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

https://blog.csdn.net/xinyuan510214/article/details/51361853
https://juejin.im/post/6844903991889887245