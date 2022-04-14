---
title: hostapd
author: "-"
date: 2013-12-01T11:58:10+00:00
url: /?p=6001

categories:
  - inbox
tags:
  - reprint
---
## hostapd

主页: <http://w1.fi/hostapd/>

hostapd是一个_IEEE 802.11的AP和IEEE 802.1X/WPA/WPA2/EAP/RADIUS验证器_.此页面用于怎么在linux系统下使用它.其他操作系统请参考hostapd主页

就Linux而言,老版本只能使用以下3个包
- HostAP
- madwifi
- prism54

所有新的基于mac80211的驱动实现AP功能被hostapd's **nl80211** 驱动支持

The mac80211 子系统将所有的master模式已经移到用户空间.通过hostapd去处理客户端验证,设置加密密钥,建立密钥转化策略,以及无线公共部分的其他方面. 由此,老的使用'iwconfig <wireless interface> mode master'的方法已经不能使用了. 用户空间程序像hostapd目前使用netlink (the nl80211 driver)去创建master mode接口实现通信,monitor mode接口实现接收和发送管理框架

## 获得hostapd {#Getting_hostapd}

### Using your distributions hostapd {#Using_your_distributions_hostapd}

在编译和安装你的拷贝之前尝试发行版本是很明智的.这将让你以后的干礼轻松,如果你的版本大于0.6.8或更新,你通过简单配置hostapd-minimal.conf文件来进行测试:

#change wlan0 to your wireless device
interface=wlan0
driver=nl80211
ssid=test
channel=1

如果上述配置出现以下错误:

hostapd $ sudo hostapd ./hostapd-minimal.conf
Configuration file: ./hostapd-minimal.conf
Line 2: invalid/unknown driver 'nl80211'
1 errors found in configuration file './hostapd-minimal.conf'

那就意味着你的hostapd不支持nl80211,你将需要按以下操作编译。如果正常,你可以跳转到配置hostapd章节

### 下载和编译hostpad {#Download_and_compile_hostapd}

_使用基于nl80211的hostapd需要你有至少libnl-1.0 pre8或更新的 genl版本,nl80211依赖Generic Netlink. 大多数发行版都自带有这个或者更新的.在fedora或其它开发包和安装包分开发行版编译 _时,你需要libnl-devel 包

_使用下面命令在线获取hostapd:_

git clone git://w1.fi/srv/git/hostap.git
cd hostap/hostapd

也可以使用下面的命令

wget http://w1.fi/releases/hostapd-x.y.z.tar.gz
tar xzvf hostapd-x.y.z.tar.gz
cd hostapd-x.y.z/hostapd

然后,我们需要在编译时配置enable nl80211支持.复制defconfig为.config,并编辑它.另外这里还有一些其他选项你可以开启支持,如果你的硬件支持,你可以开启802.11n支持. 大多数其他的加密类型和特性在大多数应用程序是不需要的,因此你可以自行考虑是否开启支持.

cp defconfig .config
vi .config

找到如下行:

#CONFIG_DRIVER_NL80211=y

取消'#'.同样根据你的要求配置其他选项.基本上,只要配置这行就足够让hostapd运行WPA/WPA2 验证和加密

编译:

make

如果出现以下错误:

driver_nl80211.c:21:31: warning: netlink/genl/genl.h: No such file or directory
driver_nl80211.c:22:33: warning: netlink/genl/family.h: No such file or directory
driver_nl80211.c:23:31: warning: netlink/genl/ctrl.h: No such file or directory
driver_nl80211.c:24:25: warning: netlink/msg.h: No such file or directory
driver_nl80211.c:25:26: warning: netlink/attr.h: No such file or directory

你需要安装或更新libnl0.6.8或更新.如果成功,尝试配置.

hostapd # ./hostapd ./hostapd-minimal.conf
Configuration file: ./hostapd-minimal.conf
Using interface wlan1 with hwaddr 00:0d:0b:cf:04:40 and ssid 'test'

如果像例子那样的显示,就可以配置hostapd. 如果出现其他错误,重新上述编译.如果出现以下错误:

Hardware does not support configured mode
wlan0: IEEE 802.11 Hardware does not support configured mode (2)
Could not select hw_mode and channel. (-2)
wlan0: Unable to setup interface.
rmdir[ctrl_interface]: No such file or directory

说明你设置了硬件不支持的hw_mode (a, b or g).


## 配置hostapd {#Configuring_hostapd}


### Establishing Baseline for Configuration {#Establishing_Baseline_for_Configuration}

配置之前,你需要了解客户端的能力.不是所有的设备都支持所有的你实现的方法,因此基准配置需被确定 . 你也需要了解你所在地区的channel上有最少的其他APs.当选择哪个channel使用,需要记住的是在20MHz内,channels和其他channels将会重叠 .

例如,你需要确定以下:

Encryption: wpa-psk + tkip
Wireless Mode: g
Normal for an environment that has to support semi legacy devices, that don't support ccmp or wpa2
Encryption: wpa2-psk + ccmp
Wireless Mode: g+n
Normal for an environment that has only up to date hardware and software
Encryption: wep
Wireless Mode: b
This is the works case scenario, as wep is broken and can be trivially cracked.  Don't consider this as anything more than keeping casual free loaders out.

一旦你确定的基准,你便可以开始编辑hostapd.conf:

Common Options: options that you will probably want to set
Additional Options: options that are likely useful to at least know you have
Extra Options: options that you aren't likely to need for most setups

### Common Options {#Common_Options}

使用nl80211的最基本的配置选项在hostapd-minimal.conf已经提供,此配置不使用加密,不在意频段,在现实中不会这样.

首先,我们将设置无线接口,然后无线环境,最后加密.

#### Wireless Interface {#Wireless_Interface}

设置概要:

  * interface:告诉hostapd使用的无线接口
  * bridge: 网络桥接口
  * driver: nl80211

如果你只有一个无线接口,并准备用它来桥接有线接口,一个例子如下:

interface=wlan0
bridge=br0
driver=nl80211

#### Wireless Environment {#Wireless_Environment}

设置概要:

  * ssid: 设置名字(SSID = service set identifier) ,老版本(iwconfig)叫"_essid_".
  * hw_mode: 设置操作mode,channels.有效的值取决于硬件,通常:a, b, g
  * channel:设置hostapd操作的channel.

ssid很容易配置..

hw_mode需要你的硬件支持.'g'大多数都支持, 并向前兼容802.11b..

channel应该与其他AP被选择在 20mhz (4 channels)之外,或者每边10mhz (2 channels).这就意味着一个在channel 3的一个AP将干涉channel 1或者channel 5的AP.选择一个channel.通常用户的APs默认channel 6, 因此你使用channel 1或channel 11大多数情况下最佳. channels也依赖于本地规则.

例如:

ssid=MyNetwork
hw_mode=g
channel=1

802.11n 设置概要

802.11n在上述构建中添加了额外的功能 如果你的硬件不支持802.11n,或者你不打算用它,可以忽略

  * ieee80211n: 设置1开启802.11n,0禁用
  * ht_capab: 你设备的802.11n特性清单

可以使用 'iw list'查看你设备的能力

例如:

wme_enabled=1
ieee80211n=1
ht_capab=[HT40+][SHORT-GI-40][DSSS_CCK-40]


### Authentication and Encryption {#Authentication_and_Encryption}

hostapd有大量的验证和加密选项. 以下介绍基本的加密wep/wpa/wpa2和其他选项.

设置概要:

  * macaddr_acl: MAC地址过滤. .
  * auth_algs: 加密字段, (1) 打开授权,(2) 共享授权(wep)(3).
  * ignore_broadcast_ssid: 开启或禁用广播ssid.
  * wpa: 类似auth_algs.first bit允许wpa1 (1), 第二位允许wpa2 (2), 都允许(3)
  * wpa_psk/wpa_passphrase: These establish what the pre-shared key will be for wpa authentication.
  * wpa_key_mgmt: This controls what key management algorithms a client can authenticate with.
  * wpa_pairwise: This controls wpa's data encryption
  * rsn_pairwise: This controls wpa2's data encryption

First, scratch macaddr_acl and ignore_broadcast_ssid from your priorities as they only enhance security (and even then, only slightly). Also, WEP has been effectively broken now, so unless you HAVE to support wep, scratch that from your list. This just leaves wpa/wpa2. Per the draft standard, wpa2 is required for 802.11n, and as there are known attacks on wpa now, wpa2 is the recommended authentication and encryption suite to use. Fortunately, you can have both enabled at once. If Windows clients are going to be connecting, you should leave ccmp encryption out of the wpa_pairwise option, as some windows drivers have problems with systems that enable it.

A good starting point for a wpa & wpa2 enabled access point is:

macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=3
wpa_passphrase=YourPassPhrase
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

If, alternately, you just want to support wpa2, you could use something like:

macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=YourPassPhrase
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

That should be all of the settings that you'll need to change for a basic, secure, access point using hostapd with an AP enabled mac80211 driver.


### Additional Options {#Additional_Options}


### Extra Options {#Extra_Options}


#### Dynamic VLAN tagging {#Dynamic_VLAN_tagging}

hostapd can be configured to move STAs into separate VLANs based on RADIUS tunnel attributes (as specified in RFC3580, <http://tools.ietf.org/html/rfc3580#section-3.31>):


Tunnel-Type=VLAN (13)
Tunnel-Medium-Type=802
Tunnel-Private-Group-ID=VLANID

To enable dynamic VLAN tagging the following options in hostapd.conf need to be set:

dynamic_vlan=1
vlan_file=/etc/hostapd.vlan

A value of 0 disables dynamic VLAN tagging, a value of 1 allows dynamic VLAN tagging and a value of 2 will reject the authentication if the RADIUS server does not provide the appropriate tunnel attributes.

Furthermore, hostapd needs to know how the VLAN interfaces should be named, this is done through an additional config file as specified in vlan_file.

Example /etc/hostapd.vlan:

1       wlan0.1
*       wlan0.#

This will create a wlan0.1 interface on top of wlan0 and move all STAs with the RADIUS supplied vlantag 1 to that interface. The second entry is used to dynamically create VLAN interfaces on top of wlan0, hostapd will create an interface wlan0.vlantag for each different vlantag as supplied by the RADIUS server. For example, if a STA associates and the RADIUS server attributes contain the vlantag 100 hostapd will create a wlan0.100 interface and map the STA to this new interface.

 [1]: http://linuxwireless.org/en/users/Drivers/hostap
 [2]: http://linuxwireless.org/en/users/Drivers/madwifi
 [3]: http://linuxwireless.org/en/users/Drivers/prism54
 [4]: http://linuxwireless.org/en/developers/Documentation/nl80211