---
title: linux iwconfig
author: "-"
date: 2012-01-01T06:05:56+00:00
url: /?p=2065
categories:
  - Linux
  - Network

tags:
  - reprint
---
## linux iwconfig
apt-get install wireless-tools

iwconfig wlan0 essid your essid iwconfig wlan0 key s:yourpass iwconfig wlan0 mode managed dhclient wlan0 iwconfig

是linux wireless extensions(lwe)的用户层配置工具之一。

lwe是linux下对无线网络配置的工具，包括内核的支持、用户层配置工具和驱动接口的支持三部 分。目前很多无线网卡都支持lwe，而且主流的linux发布版本，比如redhat linux、ubuntu linux都已经带了这个配置工具。

1. iwconfig 用法:

iwconfig interface [essid {nn|on|off}] [nwid {nn|on|off}] [mode {managed|ad-hoc|...} [freq n.nnnn[k|m|g]] [channel n] [ap {n|off|auto}] [sens n] [nick n] [rate {n|auto|fixed}] [rts {n|auto|fixed|off}] [frag {n|auto|fixed|off}] [enc {nnnn-nnnn|off}] [power {period n|timeout n}] [retry {limit n|lifetime n}] [txpower n {mw|dbm}] [commit]

说明: iwconfig是lwe最主要的工具，可以对无线网卡的大部分参数进行配置。 参数:  essid: 设置无线网卡的essid(extension service set id)。

通过essid来区分不同的无线网络，正常情况下只有相同essid的无线站点 才可以互相通讯，除非想监听无线网络。

其后的参数为双引号括起的essid字符串，或者是any/on/off，如果essid字符串中包含 any/no/off，则需要在前面加"–"。

示例: 

#iwconfig eth0 essid any

允许任何essid，也就是混杂模式

#iwconfig eth0 essid "my network"

设置essid为"my network"

#iwconfig eth0 essid — "any"

设置essid为"any" nwid: network id，只用于pre-802.11的无线网卡，802.11网卡利用essid和ap的mac地址来替换nwid，现在基本上不用设置。

示例: 

#iwconfig eth0 nwid ab34

#iwconfig eth0 nwid off nick: nickname，一些网卡需要设置该参数，但是802.11协议栈、mac都没有用到该参数，一般也不用设置。

示例: 

#iwconfig eth0 nickname "my linux node" mode: 

设置无线网卡的工作模式，可以是 ad-hoc: 不带ap的点对点无线网络 managed: 通过多个ap组成的网络，无线设备可以在这个网络中漫游 master: 设置该无线网卡为一个ap repeater: 设置为无线网络中继设备，可以转发网络包 secondary: 设置为备份的ap/repeater monitor: 监听模式 auto: 由无线网卡自动选择工作模式 示例: 

#iwconfig eth0 mode managed

#iwconfig eth0 mode ad-hoc freq/channel: 设置无线网卡的工作频率或者频道，小于1000的参数被认为是频道，大于10000的参数被认为是频率。频率单位为hz， 可以在数字后面附带k, m, g来改变数量级，比如2.4g。频道从1开始。使用lwlist工具可以查看无线网卡支持的频率 和频道。参数off/auto指示无线网络自动挑选频率。 注意: 如果是managed模式，ap会指示无线网卡的工作频率，因此该设置的参数会被忽略。ad-hoc模式下只使用该设定的频率 初始无线网络，如果加入已经存在的ad-hoc网络则会忽略该设置的频率参数。 示例: 
