---
title: debian 修改无线网卡的信道
author: "-"
date: 2012-05-19T02:37:05+00:00
url: /?p=3160
categories:
  - Linux
  - Network
tags:$
  - reprint
---
## debian 修改无线网卡的信道
查看无线网卡支持的信道

```bash
  
sudo iwlist channel
  
```

```bash
  
#这个是我的thinkpad x60s, !!!不支持channel 12,13,14,
  
#最后面有列出当前信道Current Frequency=xxx
  
lo no frequency information.

eth0 no frequency information.

wlan0 24 channels in total; available frequencies :
            
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
            
Channel 36 : 5.18 GHz
            
Channel 40 : 5.2 GHz
            
Channel 44 : 5.22 GHz
            
Channel 48 : 5.24 GHz
            
Channel 52 : 5.26 GHz
            
Channel 56 : 5.28 GHz
            
Channel 60 : 5.3 GHz
            
Channel 64 : 5.32 GHz
            
Channel 149 : 5.745 GHz
            
Channel 153 : 5.765 GHz
            
Channel 157 : 5.785 GHz
            
Channel 161 : 5.805 GHz
            
Channel 165 : 5.825 GHz
            
Current Frequency=2.462 GHz (Channel 11)

tap0 no frequency information.

```

修改当前信道
  
```bash
  
sudo iwconfig wlan0 channel xx
  
```
  
xx: 改成你想要的信道,要跟无线路由器设置的信道相同!

参考来源:http://www.ehow.com/how_5443932_change-wireless-card-channel-linux.html
  
http://blog.solrex.org/articles/wifi-channel-choosing.html