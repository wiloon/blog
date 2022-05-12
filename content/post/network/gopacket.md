---
title: gopacket, pcap, libpcap
author: "-"
date: 2011-12-25T05:23:13+00:00
url: gopacket
categories:
  - network
tags:$
  - reprint
---
## gopacket, pcap, libpcap
gopacket 是 google 出品的 抓取网络数据包的库

Windows 平台下有 Wireshark 抓包工具，其底层抓包库是 npcap (以前是 winpcap）；

Linux 平台下有 Tcpdump，其抓包库是 libpcap；

而 gopacket 库可以说是 libpcap 和 npcap 的 go 封装，提供了更方便的 go 语言操作接口。

```bash
# gopacket  依赖 pcap.h, 安装 libpcap-dev
sudo apt install libpcap-dev
sudo pacman -S libpcap

```

>https://zhuanlan.zhihu.com/p/361737169
>https://github.com/google/gopacket
>https://pkg.go.dev/github.com/google/gopacket?utm_source=godoc


### bpf filter

    dst host 192.168.50.10
