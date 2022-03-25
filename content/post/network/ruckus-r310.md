---
author: "-"
date: "2021-06-20 14:19:01" 
title: "Ruckus R310, 优科"

categories:
  - inbox
tags:
  - reprint
---
## "Ruckus R310, 优科"

### 默认用户名密码
    super/sp-admin


### 软件升级
https://support.ruckuswireless.com/software?filter=88#sort=relevancy&f:@source=[Software%20Downloads]&f:@commonproducts=[R310]  

https://support.ruckuswireless.com/software/2791-ruckus-solo-access-point-110-0-0-0-2014-ga-refresh2-software-release-r310  

Ruckus Solo Access Point 110.0.0.0.2014 (GA Refresh2) Software Release (R310)


操作前的准备
认识硬件
LED状态灯

我们拿一台 Ruckus 2942 AP 来讲解。这个型号已经停产,而且是单频 2.4GHz AP,但是 LED 灯的状态和含义都是相同的。真正的原因是我不想重新做图,懒。

OPT- 没用,永远不亮。有些新的型号已经取消了OPT灯
WLAN- 现在基本上都是双频AP,所以不再有WLAN灯,取而代之的是2.4G和5G灯。有以下几种状态 (胖AP只会出现前3种) : 
灭- 表示WLAN服务没有启用 (默认情况下WLAN服务是关闭的) 
橙色长亮- 表示WLAN服务已经开启,但是没有客户端连接到Radio
绿色长亮- 表示WLAN服务已经开启,并且已经有客户端连接到Radio
绿色慢闪- 表示AP是Mesh AP,WLAN服务已经开启,但是没有客户端连接到Radio
绿色快闪- 表示AP是Mesh AP,WLAN服务已经开启,并且已经有客户端连接到Radio
DIR- 控制器管理状态灯,有以下几种状态: 
灭- AP是胖AP,没有被控制器管理
绿色长亮- AP是瘦AP,并且已经和控制器同步
绿色快闪 AP是瘦AP,正在和控制器同步,或者正在更新固件
绿色慢闪 AP是瘦AP,正在寻找控制器 (如果一直处于这种状态,就要检查网络连通性) 
AIR- Mesh上行链路状态灯,有些型号的双频AP没有AIR灯,用5G灯来充当AIR灯的功能: 

灭- AP是Root AP,或者Mesh被禁用
绿色长亮- Mesh上行链路良好
绿色快闪- Mesh上行链路不佳 (此时需要检查干扰情况,或者调整AP的位置和间距) 
绿色慢闪- Mesh上行链路不存在,AP没有找到Root AP
红色 AP硬件损坏
NOTE1: Mesh技术介绍 http://baike.baidu.com/view/1215700.htm
NOTE2: AP都会有一个Reset按键,是一个凹陷的孔。先把AP加电,2-3秒钟之后,用曲别针之类的东西按住Reset键 6 秒钟再松手,AP就可以恢复出厂设置。为了避免Reset失败,最好按8秒再松手。
NOTE3: 有些型号的AP还会有一个soft reset,作用是重启AP。

启用浏览器的SSL功能
Ruckus采用HTTPS的方式对设备进行管理,所以浏览器需要开启SSL和TLS功能。设置–>Internet选项–>高级: 


IP地址,用户名和密码
AP的以太网端口默认情况下开启了DHCP Client功能,如果网内存在DHCP Server,AP会自动获取IP地址。如果AP获取不到IP地址,它的IP地址就是192.168.0.1。所以在配置胖AP的时候,要先让AP和电脑背靠背连接,配置完成之后再连接到局域网中,否则AP可能会获取一个你不知道的IP地址。

默认的AP管理员账号是super,密码是sp-admin
NOTE: 默认IP地址,用户名和密码写在AP背面的标签上

基本配置
配置界面
Status - 监控各个项目的配置和状态
Configuration - 配置菜单,所有的项目都在这个菜单中操作
Maintenance - 升级,重启,复位,排错等维护工作的操作域
Administration - 网络管理,日志,ping等管理内容

更改密码
Configuration–>Device可以更改AP的用户名和密码: 


更改AP的IP地址/设置PPPoE拨号
Configuration–>Internet可以更改AP的IP地址。作为胖AP,IP地址当然要static,不过你也可以让AP直接PPPoE拨号 (9.3以上的固件版本支持PPPoE) ,把它当路由器来用。


设置Radio
Configuration–>Radio 2.4G 或者 Radio 5G,分别设置2个频段的Radio参数。默认情况下,AP的信道是通过Channelfly自动选择的,那么在至少30分钟内,每隔几秒钟,AP都会自动切换一次信道——因为它要对所有的信道进行扫描评估。那么反应在客户端上面,就是ping丢包,AP吞吐量小。如果客户端网卡不支持802.11h,还会掉线。所以,如果你是工勘测试的话,还是手工指定一个Channel吧！


2.4GHz的频宽Channel Width不要设置成40MHz,5GHz的频宽最好也不要设置成80MHz,因为干扰会比较大。除非你有特殊的要求。

默认的国家代码Country Code是美国,这意味着AP的发射功率会比中国的国家标准大3个db,而且可用信道也不太一样。目前中国已经开放了5G频段,已经不再只是5.8G了,可用信道12个,比美国的标准还要多。如果你要开启5G,最好还是把国家代码改成china。更改国家代码后,AP会自动重启。

点击Advanced Settings右边的按钮,可以更改AP的发射功率,以1个db为步长向下调整: 


设置桥接模式的WLAN/SSID
设置好Radio的通用参数之后,就开始设置WLAN/SSID。2.4GHz的WLAN和5GHz的WLAN需要分别设置,但SSID的名称可以是一样的。前面已经讲过,默认情况下AP的WLAN服务是关闭的,需要手工开启,点选Wireless Availability右边的Enabled。

如下图所示,胖AP的每个Radio支持8个WLAN,双频AP一共支持16个WLAN。也就是说,你可以用双频AP发出16个SSID。


点击Rate Limiting右边的按钮,可以按每客户端做上行和下行限速。点击Access Control右边的按钮,可以创建L2 MAC访问控制列表。

关键的地方来了,设置包转发模式Packet Forward。默认的包转发模式是桥接Bridge,也就是说,把AP当作一个支持VLAN的2层交换机来用。Access VLAN右边的文本框中,填写这个SSID需要绑定的VLAN,相当于在交换机上配置access端口。默认是1,也就是把AP当作一个傻交换机来用,相当于你在交换机上啥也不做 (交换机端口默认就是access vlan 1) 。按照我的经验,很多人都对这个部分感到很困惑。如果要深入的讲,需要另写一篇长文。所以还是算了。

NOTE: 对于Ruckus设备,AC也好,AP也好,只要有设置 Access VLAN的地方,如果是1,就说明在上行端口不封装802.1q Tag；如果是大于1的任何数值,就说明在上行端口需要封装802.1q Tag

另外一个重要的地方是: 加密方式WPA Algorithm必须用AES,不能用TKIP,也不要用Auto。因为802.11n的标准中,没有定义TKIP。如果你选择了TKIP,那么AP最大的并发用户数就只有20(新的固件版本可以达到26),如果并发用户数超过了这个数量,无线客户端仍然可以连接SSID,仍然可以获取IP地址,但是——不能上网。跟用户的印象就是: AP死机了。但其实AP没死,只是它不再转发数据了。如果你选择了Auto,只要有1个客户端适配到了TKIP,那么和选择TKIP的现象是一样的。

设置DHCP Server
上面的例子都是用桥接模式,但同时,AP也可以当路由器用。一部分SSID是桥接,一部分SSID做路由。要设置路由模式,首先要设置DHCP Server,指定路由模式的3层接口,配置地址池。Configuration–>Local Subnets,如下图所示,AP最多支持4个3层路由接口: 

注意,这里的Access VLAN我填了30。其实,如果你只有1个SSID,这里填1也是可以的,但是这台AP的DHCP Server会影响到有线网络的其它主机,所以最好不要填1。

设置路由模式的WLAN/SSID
下面我用5G的Wireless9来创建一个路由模式的SSID。如下图,在Packet Forward下拉菜单中选择“Local Subnet NAT and Route to WAN”,下面就会自动出现Local Subnet菜单。然后在Local Subnet菜单中,绑定刚才建立的Local Subnet (即3层接口) 。


高级设置
设置802.1x
上面我们用2.4G的Wireless1创建了一个采用密钥认证的SSID,现在我们来用2.4G的Wireless2开启一个使用802.1x认证的SSID。前面的步骤都一样,注意Access VLAN我填写了20,和Wireless1的SSID不在同一VLAN。WPA Authentication选择802.1x,然后页面就会变成下面的样子,把Radius的IP地址,端口和共享密钥填进去就行了。


设置AP以太网端口
如果你只有1个SSID,或者所有的SSID的Access VLAN都是1,那么配置工作就结束了。但是,我们现在已经创建了3个SSID,其中2个桥接的SSID的VLAN都不一样,你肯定想到了一个词——Trunk。是的,因为AP的上行端口只有1个,它需要传输多个VLAN的数据,需要封装802.1q Tag。在Configuration–>Ethernet Ports进行设置: 

在较低版本的固件中,AP以太网端口默认就是Trunk口,不需要设置。但是最新的固件版本做出了改变,默认是Access口,你需要把它改成Trunk Port。

NOTE: 一般的Ruckus中高端AP都有2个以太网端口,你需要先看右边的AP图片,上面有端口号的标记,然后根据端口号码修改配置,不要搞错了。

设置交换机以太网端口
交换机连接AP的那个以太网端口同样要设置Trunk,但要注意的是,它还要设置Native VLAN/PVLAN。例如,我们之前创建了一个VLAN10的SSID,还创建了一个VLAN20的SSID。同时,AP本身还有一个管理IP在VLAN100。那么交换机端口需要做以下配置: 

Cisco交换机端口配置 (默认allow vlan all,建议配置vlan修剪) : 
interface ...
  switchport mode trunk
  switchport trunk native vlan 100
H3C交换机端口配置
interface ...
  port link-type trunk
  port trunk permit vlan 10,20
  port trunk pvid vlan 100
HP/Brocade交换机端口配置
vlan 100 untag ...
vlan 10 tag ...
vlan 20 tag ...
设置Portal网页认证/Hotspot/Wispr
设置Hotspot
Ruckus胖AP同样支持网页认证,Configuration–>Hotspot,设置Portal和Radius的各项参数: 


More Options可以设置一些认证的高级参数,例如MAC地址认证,宽限期 (在宽限期内,如果用户下线再上线,不需要重新认证) : 


Walled Garden围墙花园,设置用户在完成认证之前可以访问的网络资源。围墙花园必须设置,必须允许Radius Server和Portal Server的IP或域名,如果还有短信认证,还要允许短信网关的IP: 

在围墙花园中,可以添加域名,Host IP地址,还可以添加子网。在某些固件版本的AC中,可以添加0.0.0.0/0,如果你只是想弹个网页,不需要认证,这是个好办法。但是在新版本的胖AP中并不允许这样做。

Unrestricted Clients可以设置一些不需要认证的MAC地址,也就是白名单: 


在WLAN/SSID中应用Hotspot
现在我们来用5G Radio的Wireless10创建一个网页认证的SSID。在Hotspot Service下拉菜单中,选择我们刚才建立的Hotspot0 (胖AP只能创建1个Hotspot,所以菜单中只会存在1个Hotspot0),其它选项与普通的SSID没有区别。

NOTE1: 我在启用Hotspot的同时,选择了路由模式,当然你也可以选择桥接模式,这取决于你的网络结构。
NOTE2: 我在启用Hotspot的同时,还开启了WPA密钥认证,目的只是想让你知道这2种认证方式是可以同时激活的。通常情况下,如果启用了网页认证就不会再开启WPA——星巴克的WiFi也是没有密码的啊。

AP维护工作
升级AP固件
Maintenance–>Upgrade,选择Local本地升级,点击浏览按钮选择固件,最后Perform Upgrade即可。AP升级之后会自动重启。

NOTE: 9.5以前的版本,如果通过网页升级AP,有可能会失败。不过这个Bug已经被修复,所以我就不用介绍怎样通过CLI升级AP了。

Ruckus AP固件平台介绍
Ruckus AP是胖瘦一体的,而且还是多平台的。通过更换固件在不同的平台间切换。请看下图,3.x.x.x.x的版本号是SCG/SZ平台的固件 (不支持胖AP) ,9.x.x.x.x的版本号是ZD平台的固件 (支持胖AP) ,100.x.x.x.x是ZD/SCG/SZ通用的固件 (支持胖AP) ,200.x.x.x.x是Unleash (25台AP以内不需要控制器,可以自组网) 平台的固件。


重启/Reset AP
除了长按8秒Reset,还可以通过网页对AP进行复位操作。Maintenance–>Reboot/Reset:


收集AP的Support info用于排错
如果你的无线网络出现了问题,只要AP的管理页面能够进得去,就必须提供support info给售后。Maintenance–>Support info: 

选择Save to Local Computer,然后把supportinfo.txt文件保存下来。supportinfo里面包括Log,所以不需要单独保存日志文件。

AP管理操作
设置网管功能
Maintenance–>Management。默认情况下AP的Telnet端口是关闭的,可以在这里Enable。

还记得我说过的,Ruckus AP是胖瘦一体的吗？你辛辛苦苦把胖AP设置好了,结果这时候管理VLAN内出现了一台AC,你就只能眼睁睁看着这台胖AP自动变成一台瘦AP。为了避免这种事情的发生,需要在这里把Controller Discovery Agent设置成Disable,关闭控制器自动发现功能。

如果你的瘦AP和胖AP跨三层或者跨广域网组网,可以将Set Controller Address设置成Enable,手工指定AC的域名或地址。但是DHCP Option43是更好的方法。


如果你有FlexMaster网管,可以在这里指定FM的URL。但DHCP Option43是更好的方法。

使用Ping和Traceroute进行网络诊断
Administration–>Diagnostics,可以使用Ping和Traceroute工具对网络的连通性进行诊断: 


设置Syslog
AP的内存有限,只能保存很短时间的syslog。如果有条件,最好能把日志保存到Syslog Server上面。Maintenance–>Log: 


使用SpeedFlex测试网络
Ruckus提供了一个免费的App用于测试无线网络的吞吐量——SpeedFlex。如果你使用iOS的设备,可以直接在iTunes中搜索下载安装。如果你使用Android设备就比较麻烦,必须在GooglePlay中下载安装。但是,你懂的。。。

不过呢,我从墙外把最新版本的apk拖下来了,你可以点击这里下载,不需要Root手机。

使用方法也很简单: 
1. 点击右上角的齿轮图标,设置IP地址和参数
2. 点击右上角的对号图标,完成设置
3. 按Start开始测试

NOTE: AP的IP地址可以是管理IP,也可以是Local Subnet三层接口地址,但必须和手机的IP地址处于同一VLAN。

扩展: AP不能做胖AP了？
有时候,当你拿到一台Ruckus的AP,却发现Configuration菜单下面没有Wireless或者Radio的配置选项,Reset AP也还是没有。你可能认为AP坏了,其实并没有。在Ruckus Support网站注册一个帐号,下载100.x.x.x.x版本的固件,升级AP,你就可以配置Radio了。
————————————————
版权声明: 本文为CSDN博主「然后咧」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/chenghit/article/details/50364883

---

https://blog.csdn.net/chenghit/article/details/50364883  
https://post.smzdm.com/p/ax08q0r3/  
