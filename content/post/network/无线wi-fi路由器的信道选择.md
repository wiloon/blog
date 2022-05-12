---
title: 无线WI-FI路由器的信道选择
author: "-"
date: 2012-05-19T02:21:05+00:00
url: /?p=3156
categories:
  - Linux
  - Network
tags:
  - reprint
---
## 无线WI-FI路由器的信道选择

  
    http://blog.solrex.org/articles/wifi-channel-choosing.html
  

    
      很多人从来没有注意过路由器的 wifi 频道，以为只要笔记本电脑能连上，无线路由就没问题。但有个问题是很多移动设备不能支持全频道，其中即有功耗考虑，也有销售目标国家考虑。因此有条件时最好检测一下信噪比，选择一个最适合自己的频道，而不是让路由器启动时自己去选择。
    
  
  
    但接着又有朋友说: "求普及..."。参考 Avinash Kaushik 在他的网站统计博客"Occam's Razor"成立 5 周年时的感慨 (这篇文章很值得一读，very inspiring) ，我想即使我不是专家，分享一下自己知道的这点儿事也不错。
  
  
    切入正题，现在很多家庭都有了自己的无线 Wi-Fi 路由器，也有了各种接入互联网的移动设备: 笔记本、上网本、手机、平板电脑、电纸书、MID (已没落) 。很多移动设备联网时都会出现诡异问题，这篇文章仅仅关注其中一种诡异问题: 错误的信道 (Channel，也译为频道、频段) 配置导致无法联网或者信号较差。
  
  
    精确的技术知识我就不解释了，感兴趣的同学可以去读 Wikipedia Wi-Fi 或者 IEEE 802.11 等词条。下面主要说明为什么需要配置无线信道以及如何选择无线信道。
  
  
    为什么需要配置无线信道？
  
  
    相信大家都使用过收音机。使用收音机时，都有一个选台的问题，无论你是用旋钮、按键或者触摸，你总要选定某个台，才能收听该台的节目。无线路由也一样。你家里的无线路由器会广播一个 SSID (就是你看到的无线连接名) ，点击该连接，就会使你的电脑调制到该连接所在信道进行通信。
  
  
    但是使用收音机时，可能会有这样的问题: 1. 有些台根本收不到，比如你的收音机不是全波段的；2. 有些台杂音太大听不清，比如某些唢呐电台。同理到你的无线环境上，问题 1 转化为"笔记本电脑 (全波段收音机) 能连接无线路由器，但平板电脑 (非全波段收音机) 却无法连接"；问题 2 转化为"能连接到无线路由器，但干扰太多，达不到最大的网速 (这个网速指 Wi-Fi 连接速度，与 ADSL 网速无关) "。
  
  
    如果没有手动配置过，无线路由器会自动选择一个默认或者随机的信道进行广播和连接建立。在设备没有联网问题和周围没有别人使用时，这是 OK 的。
  
  
    但如果你周围的人家都有无线设备，且大家用的都是同一款运营商赠送的无线路由器 (或无线猫) 时，那么极有可能所有人都选择了同一个信道进行通信。这就会造成很大的信号干扰，这一般影响不到网速——除非你家用的 ADSL 大于 4M，但会造成家里两台设备之间数据传输速度极慢，例如用豌豆荚往手机上无线发送视频文件时。
  
  
    如果不巧的是你家无线路由器会随机选择信道，那么它极有可能选择到一个你设备不支持的信道。我就曾经遇到过爱国者某型号 MID 只支持信道 1-9 但无线路由器自己选择了信道 11 的情况，那是死活也连不上啊！移动设备出于降低功耗或其它考虑，不支持某些信道是很正常的；再加上不同国家对无线信道管制情况不同 (参见 List of WLAN Channels) ，其它国家的水货设备到了国内可能也会水土不服。
  
  
    幸运的是，你不能控制广播电台的波段，却可以控制自家无线路由器的无线信道。修改无线信道的方法请参考各路由器厂商的帮助文档，或者在网上寻求帮助。不过在修改之前，你还面临着，我该改到哪个信道呢？
  
  
    如何选择无线信道？
  
  
    首先，要选择自己通信设备都支持的信道。不过在此之前，首先确认所有设备都支持同一协议，比如你移动终端不支持 IEEE 802.11n，你非得在路由器上用 802.11n 协议，这就是找不自在了。这些知识要参考设备的手册，或者自己尝试。在 Linux 系统中，可以用 iwlist channel 列出移动终端支持的所有信道，比如 Kindle 支持的信道就是 (看到这里我基本可以肯定那哥们 Kindle 问题不是因为信道了，除非他用的是日本产路由器) : 
  
  [root@kindle root]# iwlist channel
lo        no frequency information.

wlan0     13 channels in total; available frequencies :
          Channel 01 : 2.412 GHz
          Channel 02 : 2.417 GHz
          Channel 03 : 2.422 GHz
          Channel 04 : 2.427 GHz
          Channel 05 : 2.432 GHz
          Channel 06 : 2.437 GHz
          Channel 07 : 2.442 GHz
          Channel 08 : 2.447 GHz
          Channel 09 : 2.452 GHz
          Channel 10 : 2.457 GHz
          Channel 11 : 2.462 GHz
          Channel 12 : 2.467 GHz
          Channel 13 : 2.472 GHz
          Current Frequency:2.412 GHz (Channel 1)
  
    其次，在干扰不能容忍情况下，再去选择干扰较少的信道。这个可以通过扫描周围信号强度比较高的 SSID 都在使用哪些信道，通过和信道列表图谱比较，选择可能干扰较小的信道进行尝试。RSSI 和 SNR 测试需要专门的知识和工具 (例如 Linux 下的 iwconfig) ，对普通人来说可能比较费力。
  
  [root@kindle root]# iwconfig     
lo        no wireless extensions.

wlan0     AR6000 802.11g  ESSID:"mosaic" 
          Mode:Managed  Frequency:2.412 GHz  Access Point: 00:23:EB:B7:E6:94  
          Bit Rate=54 Mb/s   Tx-Power=16 dBm   Sensitivity=0/3 
          Retry:on  
          Encryption key:off
          Power Management:off
          Link Quality:49/94  Signal level:-46 dBm  Noise level:-96 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:0   Missed beacon:0
  
    最后总结一下，随着移动终端的发展，越来越多的移动终端支持更全的信道，但总有那么个别的终端厂商比较变态。因此本文谈到内容仅仅是作为一个提醒，在解决无线连接问题时作一个参考
  
