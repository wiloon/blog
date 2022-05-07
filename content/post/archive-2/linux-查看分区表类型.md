---
title: linux 查看分区表类型
author: "-"
date: 2018-02-12T14:36:36+00:00
url: /?p=11878
categories:
  - Inbox
tags:
  - reprint
---
## linux 查看分区表类型
You can use parted -l to determine the type of partition table. Eg:

$ sudo parted -l
  
Model: ATA TOSHIBA THNSNS25 (scsi)
  
Disk /dev/sda: 256GB
  
Sector size (logical/physical): 512B/512B
  
Partition Table: msdos

Number Start End Size Type File system Flags
   
1 4194kB 32.2GB 32.2GB primary ext4 boot
   
2 32.2GB 256GB 224GB primary ext4

https://unix.stackexchange.com/questions/120221/gpt-or-mbr-how-do-i-know