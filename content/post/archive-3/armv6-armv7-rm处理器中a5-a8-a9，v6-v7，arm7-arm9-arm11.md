---
title: armv6, armv7, rm处理器中a5 a8 a9，v6 v7，arm7 arm9 arm11
author: "-"
date: 2019-03-27T15:36:51+00:00
url: /?p=13967
categories:
  - Inbox
tags:
  - reprint
---
## armv6, armv7, rm处理器中a5 a8 a9，v6 v7，arm7 arm9 arm11
ARM是微处理器行业的一家知名企业，arm处理器以体积小和高性能的优势在嵌入式设备中广泛使用，几乎所有手机都是使用它的。

armv6, armv7, armv7s是ARM CPU的不同指令集，原则上是向下兼容的。如iPhone4S CPU支持armv7, 但它同时兼容armv6，只是使用armv6指令可能无法充分发挥它的特性。同理iPhone5 CPU支持armv7s，它虽然也兼容armv7，但是却无法进行相关的优化。

ARM处理器发展这么多年，有很多架构，很多不同的内核
  
架构有armv1 v2 v3 v4 v5 v6 v7
  
内核太多了，比如armv1对应的是arm1，armv5对应的arm9，armv6对应的arm11，armv7对应的cortex(比如A8 A9都属于cortex架构)
  
cortex-a8 cortex-a9 arm11 arm 9都是CPU构架。
  
在性能上cortex-a9 >cortex-a8>arm11。

arm11是ARM V6的构架，老的指令集，被淘汰的东西咯，性能不如ARM V7构架的CPU。

cortex-a8 是第一款基于 ARM V7指令集的CPU，比V6先进了，V6的不支持在线FLASH播放。即使能安装插件也不能完整的支持FLASH播放，性能上不行，即使破解了播不出来。A8完美支持FLASH的！

cortex-a8 是目前的主流CPU，中高端机上的，尤其是高端机的稳定产品，中低端都用V6构架的CPU，比如MSM 7227 ，别看800Hz的频率，其实是上一代的，不如同频率的7230的性能的四分之一。

cortex-a9多核处理器，对MPCore的优化，向高性能的发展，未来的主流，现在的双核手机CPU都是这个构架

目前最好的是cortex-A9构架的CPU是高端的主流CPU，比如NV的双核，德州仪器的双核很多都是用的A9构架，A8是目前的中高端的主流，一般A8构架的双核CPU不多，几乎没有。

https://blog.csdn.net/maochengtao/article/details/9951131