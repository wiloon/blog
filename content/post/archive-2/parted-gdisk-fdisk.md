---
title: mbr, gpt
author: "-"
date: 2018-05-10T06:15:35+00:00
url: /?p=12223
categories:
  - Uncategorized

tags:
  - reprint
---
## mbr, gpt
http://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_linux_039_fdisk_gdisk_parted.html

### 两种分区结构简介
  
#### MBR分区
硬盘主引导记录MBR由4个部分组成
主引导程序 (偏移地址0000H-0088H) ,它负责从活动分区中装载,并运行系统引导程序。
出错信息数据区,偏移地址0089H-00E1H为出错信息,00E2H-01BDH全为0字节。
分区表 (DPT,Disk Partition Table) 含4个分区项,偏移地
址01BEH-01FDH,每个分区表项长16个字节,共64字节为分区项1、分区项2、分区项3、分区项4
结束标志字,偏移地址01FE-01FF的2个字节值为结束标志55AA  

#### GPT分区
GPT:GUID (Globals Unique Identifiers)  partitiontable 支持128个分区,使用64位,支持8Z (512Byte/block ) 64Z  ( 4096Byte/block) 
使用128位UUID(Universally Unique Identifier) 表示磁盘和分区 GPT分区表自动备份在头和尾两份,并有CRC校验位
UEFI (统一扩展固件接口)硬件支持GPT,使操作系统启动
