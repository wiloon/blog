---
title: linux iwconfig
author: w1100n
type: post
date: 2012-01-01T06:05:56+00:00
url: /?p=2065
categories:
  - Linux
  - Network

---
apt-get install wireless-tools

iwconfig wlan0 essid your essid iwconfig wlan0 key s:yourpass iwconfig wlan0 mode managed dhclient wlan0 iwconfig

是linux wireless extensions(lwe)的用户层配置工具之一。

lwe是linux下对无线网络配置的工具，包括内核的支持、用户层配置工具和驱动接口的支持三部 分。目前很多无线网卡都支持lwe，而且主流的linux发布版本，比如redhat linux、ubuntu linux都已经带了这个配置工具。

1、iwconfig 用法:

iwconfig interface [essid {nn|on|off}] [nwid {nn|on|off}] [mode {managed|ad-hoc|...} [freq n.nnnn[k|m|g]] [channel n] [ap {n|off|auto}] [sens n] [nick n] [rate {n|auto|fixed}] [rts {n|auto|fixed|off}] [frag {n|auto|fixed|off}] [enc {nnnn-nnnn|off}] [power {period n|timeout n}] [retry {limit n|lifetime n}] [txpower n {mw|dbm}] [commit]

说明：iwconfig是lwe最主要的工具，可以对无线网卡的大部分参数进行配置。 参数： essid：设置无线网卡的essid(extension service set id)。

通过essid来区分不同的无线网络，正常情况下只有相同essid的无线站点 才可以互相通讯，除非想监听无线网络。

其后的参数为双引号括起的essid字符串，或者是any/on/off，如果essid字符串中包含 any/no/off，则需要在前面加"–"。

示例：

#iwconfig eth0 essid any

允许任何essid，也就是混杂模式

#iwconfig eth0 essid "my network"

设置essid为"my network"

#iwconfig eth0 essid — "any"

设置essid为"any" nwid: network id，只用于pre-802.11的无线网卡，802.11网卡利用essid和ap的mac地址来替换nwid，现在基本上不用设置。

示例：

#iwconfig eth0 nwid ab34

#iwconfig eth0 nwid off nick: nickname，一些网卡需要设置该参数，但是802.11协议栈、mac都没有用到该参数，一般也不用设置。

示例：

#iwconfig eth0 nickname "my linux node" mode：

设置无线网卡的工作模式，可以是 ad-hoc：不带ap的点对点无线网络 managed：通过多个ap组成的网络，无线设备可以在这个网络中漫游 master：设置该无线网卡为一个ap repeater：设置为无线网络中继设备，可以转发网络包 secondary：设置为备份的ap/repeater monitor：监听模式 auto：由无线网卡自动选择工作模式 示例：

#iwconfig eth0 mode managed

#iwconfig eth0 mode ad-hoc freq/channel：设置无线网卡的工作频率或者频道，小于1000的参数被认为是频道，大于10000的参数被认为是频率。频率单位为hz， 可以在数字后面附带k, m, g来改变数量级，比如2.4g。频道从1开始。使用lwlist工具可以查看无线网卡支持的频率 和频道。参数off/auto指示无线网络自动挑选频率。 注意：如果是managed模式，ap会指示无线网卡的工作频率，因此该设置的参数会被忽略。ad-hoc模式下只使用该设定的频率 初始无线网络，如果加入已经存在的ad-hoc网络则会忽略该设置的频率参数。 示例：

#iwconfig eth0 freq 2422000000 #iwconfig eth0 freq 2.422g #iwconfig eth0 channel 3 #iwconfig eth0 channel auto ap：连接到指定的ap或者无线网络，后面的参数可以是ap的mac地址，也可以是iwlist scan出来的标识符。如果是ad-hoc，则连接到 一个已经存在的ad-hoc网络。使用off参数让无线网卡不改变当前已连接的ap下进入自动模式。any/auto参数，无线网卡自动选择 最好的ap。 注意：如果无线信号低到一定程度，无线网络会进入自动选择ap模式。 示例： #iwconfig eth0 ap 00:60:1d:01:23:45 #iwconfig eth0 ap any #iwconfig eth0 ap off rate/bit：如果无线网卡支持多速率，则可以通过该命令设置工作的速率。小于1000的参数由具体的无线网卡驱动定义，一般是传输速 率的索引值，大于1000的为速率，单位bps，可以在数字后面附带k, m, g来指定数量级。auto参数让无线网卡自动选择速率 fixed参数让无线网卡不使用自动速率模式。 示例： #iwconfig eth0 rate 11m #iwconfig eth0 rate auto #iwconfig eth0 rate 5.5m auto //自动选择5.5m以下的速率 txpower：如果无线网卡支持多发射功率设定，则使用该参数设定发射，单位为dbm，如果指定为w（毫瓦），只转换公式为： dbm=30+log(w)。参数on/off可以打开和关闭发射单元，auto和fixed指定无线是否自动选择发射功率。 示例： #iwconfig eth0 txpower 15 #iwconfig eth0 txpower 30mw #iwconfig eth0 txpower auto #iwconfig eth0 txpower off sens：设置接收灵敏度的下限，在该下限之下，无线网卡认为该无线网络信号太差，不同的网卡会采取不同的措施，一些现代的无线网卡 会自动选择新的ap。正的参数为raw data，直接传给无线网卡驱动处理，一般认为是百分比。负值表示dbm值。 示例： #iwconfig eth0 sens -80 #iwconfig eth0 sens 2 retry：设置无线网卡的重传机制。limit 'value' 指定最大重传次数；lifetime 'value'指定最长重试时间，单位为秒，可以附带m和u来 指定单位为毫秒和微秒。如果无线网卡支持自动模式，则在limit和lifetime之前还可以附加min和max来指定上下限值。 示例： #iwconfig eth0 retry 16 #iwconfig eth0 retry lifetime 300m #iwconfig eth0 retry min limit 8 rts：指定rts/cts握手方式，使用rts/cts握手会增加额外开销，但如果无线网络中有隐藏无线节点或者有很多无线节点时可以提高性能。 后面的参数指定一个使用该机制的最小包的大小，如果该值等于最大包大小，则相当于禁止使用该机制。可以使用auto/off/fixed 参数。 示例： #iwconfig eth0 rts 250 #iwconfig eth0 rts off frag：设置发送数据包的分片大小。设置分片会增加额外开销，但在噪声环境下可以提高数据包的到达率。一般情况下该参数小于最大包 大小，有些支持burst模式的无线网卡可以设置大于最大包大小的值来允许burst模式。还可以使用auto/fixed/off参数。 示例： #iwconfig eth0 frag 512 #iwconfig eth0 frag off key/enc[ryption]：设置无线网卡使用的加密密钥，此处为设置wep模式的加密key，如果要使用wpa，需要wpa_supplicant工具包。 密钥参数可以是 xxxx-xxxx-xxxx-xxxx 或者 xxxxxxxx 格式的十六进制数值，也可以是s:xxxxxx的ascii字符。如果在密钥参数之前加了[index]，则只是设置该索引值对应的密钥，并不改变当前的密钥。直接指定[index]值可以设置当前使用哪一个密钥。指定on/off可以控制是否使用加密模式。open/restricted指定加密模式，取决于不同的无线网卡，大多数无线网卡的open模式不使用加密且允许接收没有加密的数据包，restricted模式使用加密。可以使用多个key参数，但只有最后一个生效。 wep密钥可以是40bit，用10个十六进制数字或者5个ascii字符表示，也可以是128bit，用26个十六进制数字或者13个ascii字符表 示。 示例： #iwconfig eth0 key 0123-4567-89 #iwconfig eth0 key [3] 0123-4567-89 #iwconfig eth0 key s:password [2] #iwconfig eth0 key [2] #iwconfig eth0 key open #iwconfig eth0 key off #iwconfig eth0 key restricted [3] 0123456789 #iwconfig eth0 key 01-23 key 45-67 [4] key [4] power：设置无线网卡的电源管理模式。period 'value' 指定唤醒的周期，timeout 'value'指定进入休眠的等待时间，这两个参数之前可以 加min和max修饰，这些值的单位为秒，可以附加m和u来指定毫秒和微秒。off/on参数指定是否允许电源管理，all/unicast/multicast 指定允许唤醒的数据包类型。 示例： #iwconfig eth0 power period 2 #iwconfig eth0 power 500m unicast #iwconfig eth0 power timeout 300u all #iwconfig eth0 power off #iwconfig eth0 power min period 2 power max period 4 commit：提交所有的参数修改给无线网卡驱动。有些无线网卡驱动会先缓存无线网卡参数修，使用这个命令来让无线网卡的参数修改生效。不过一 般不需