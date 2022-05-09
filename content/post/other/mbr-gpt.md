---
title: mbr gpt
author: "-"
date: 2015-04-21T13:30:02+00:00
url: /?p=7472
categories:
  - Inbox
tags:
  - reprint
---
## mbr gpt

http://www.rodsbooks.com/linux-fs-code/

硬盘分区表扫盲: MBR和GPT表,你在用哪一样？
  
2013-11-12 15:11:22来源: IT之家 原创作者: 阿象责编: 阿象人气: 7253 评论: 24
  
自从2007年Vista操作系统推出以后,各大硬件厂商对于硬件开发速度明显加快,其中对于硬盘的速度和容量,从最早的5400转,160G容量,提升到现在的7200转甚至万转机械盘,容量也先后出现上TB级别的。单硬盘都出现4Tb容量。

由于磁盘容量越来越大,传统的MBR分区表 (主引导记录) 已经不能满足大容量磁盘的需求。传统的MBR分区表只能识别磁盘前面的2.2TB左右的空间,对于后面的多余空间只能浪费掉了,而对于单盘4TB的磁盘,只能利用一半的容量。因此,才有了GPT (全局唯一标识分区表) 。

除此以外,MBR分区表只能支持4个主分区或者3主分区+1扩展分区 (包含随意数目的逻辑分区) ,而GPT在Windows下面可以支持多达128个主分区。

下面IT之家也给大家分享下MBR和GPT的详细区别。

MBR分区表: 

在传统硬盘分区模式中,引导扇区是每个分区 (Partition) 的第一扇区,而主引导扇区是硬盘的第一扇区。它由三个部分组成,主引导记录MBR、硬盘分区表DPT和硬盘有效标志。在总共512字节的主引导扇区里MBR占446个字节,第二部分是Partition table区 (分区表) ,即DPT,占64个字节,硬盘中分区有多少以及每一分区的大小都记在其中。第三部分是magic number,占2个字节,固定为55AA。

一个扇区的硬盘主引导记录MBR由4个部分组成。

•主引导程序 (偏移地址0000H-0088H) ,它负责从活动分区中装载,并运行系统引导程序。

•出错信息数据区,偏移地址0089H-00E1H为出错信息,00E2H-01BDH全为0字节。

•分区表 (DPT,Disk Partition Table) 含4个分区项,偏移地址01BEH-01FDH,每个分区表项长16个字节,共64字节为分区项1、分区项2、分区项3、分区项4。

•结束标志字,偏移地址01FE-01FF的2个字节值为结束标志55AA,如果该标志错误系统就不能启动。

GPT分区表: 

GPT的分区信息是在分区中,而不象MBR一样在主引导扇区,为保护GPT不受MBR类磁盘管理软件的危害,GPT在主引导扇区建立了一个保护分区 (Protective MBR) 的MBR分区表 (此分区并不必要) ,这种分区的类型标识为0xEE,这个保护分区的大小在Windows下为128MB,Mac OS X下为200MB,在Window磁盘管理器里名为GPT保护分区,可让MBR类磁盘管理软件把GPT看成一个未知格式的分区,而不是错误地当成一个未分区的磁盘。

另外,为了保护分区表,GPT的分区信息在每个分区的头部和尾部各保存了一份,以便分区表丢失以后进行恢复。

对于基于x86/64的Windows想要从GPT磁盘启动,主板的芯片组必须支持UEFI (这是强制性的,但是如果仅把GPT用作数据盘则无此限制) ,例如Win8/Win8.1原生支持从UEFI引导的GPT分区表上启动,大多数预装Win8系统的电脑也逐渐采用了GPT分区表。至于如何判断主板芯片组是否支持UEFI,一般可以查阅主板说明书或者厂商的网址,也可以通过查看BIOS设置里面是否有UEFI字样。


### /dev/sda contains GPT signatures
 
fixparts /dev/sdc
http://www.rodsbooks.com/fixparts/
http://www.rodsbooks.com/gdisk/gdisk.html
https://forums.kali.org/showthread.php?18265-dev-sda-contains-GPT-signatures

