---
title: Linux Testdisk
author: "-"
date: 2012-05-01T11:11:34+00:00
url: /?p=3074
categories:
  - Hardware
  - Linux
tags:
  - reprint
---
## Linux Testdisk
linux下超帅的分区表修复软件.以前用过n多的windows的分区表修复软件，没想到linux中有这么好用这么方便的修复软件，速度那叫一个快啊。。没有见到这个分区表修复软件以前我都白活了。。。。。
  
        好了，这个软件叫testdisk.很帅的。。
  
  
    如果你是使用修复光碟,就下载一个这个软件到电脑中,如果是恢复usb的disk直接
  
  
    #sudo apt-get install testdisk
  
  
    使用的话先sudo testdisk
  
  
      1.选择Create来进行分析
  
  
    Use arrow keys to select, then press Enter key:
 [ Create ]  Create a new log file
 [ Append ]  Append information to log file
 [ No Log ]  Don't record anything
  
  
    2.然后选择testdisk中你要修复的硬盘，回车
  
  
    Select a media (use Arrow keys, then press Enter):
 Disk /dev/sda - 160 GB / 149 GiB - ATA HITACHI HTS54251
 Disk /dev/sdb - 3272 MB / 3121 MiB - SM324BC USB DISK
     3.选择testdisk修复的平台,我们是Intel的，所以选择他
  
  
    Please select the partition table type, press Enter when done.
 [Intel  ]  Intel/PC partition
 [EFI GPT]  EFI GPT partition map (Mac i386, some x86_64...)
 [Mac    ]  Apple partition map
 [None   ]  Non partitioned media
 [Sun    ]  Sun Solaris partition
 [XBox   ]  XBox partition
 [Return ]  Return to disk selection
  
  
    4.使用testdisk分析,现在选择Analyse进行分析
  
  
    [ Analyse  ]  Analyse current partition structure and search for lost partitions
 [ Advanced ]  Filesystem Utils
 [ Geometry ]  Change disk geometry
 [ Options  ]  Modify options
 [ MBR Code ]  Write TestDisk MBR code to first sector
 [ Delete   ]  Delete all data in the partition table
 [ Quit     ]  Return to disk selection
  
  
     5.见到了没，基本所有的分区都出来了,直接回车就好了,默认直接回车是快速扫描.
  
  
    *=Primary bootable  P=Primary  L=Logical  E=Extended  D=Deleted
 [Quick Search]  [ Backup ]
  
  
    然后因为没用vista,所以选择n。
  
  
    Should TestDisk search for partition created under Vista ? [Y/N] (answer Yes if
 unsure)
 N
  
  
        6.进入,见到你的表区表了吧。
  
  
    Disk /dev/sda - 160 GB / 149 GiB - CHS 19457 255 63
 Partition               Start        End    Size in sectors
 * HPFS - NTFS              0   1  1  1567 254 63   25189857
 L FAT32 LBA             1568   2  1  5097 254 63   56709324 [NO NAME]
 L Linux Swap            5098   1  1  5221 254 63    1991997
 L Linux                 5222   1  1  7298 254 63   33366942
 L Linux                 7299   1  1 19456 254 63  195318207
  
  
    Structure: Ok.  Use Up/Down Arrow keys to select partition.
 Use Left/Right Arrow keys to CHANGE partition characteristics:
 *=Primary bootable  P=Primary  L=Logical  E=Extended  D=Deleted
 Keys A: add partition, L: load backup, T: change type, P: list files,
 Enter: to continue
 NTFS, 12 GB / 12 GiB
 你还可以按p进入一下，看看文件是不是你想要的那些，然后下面会显示文件系统多大,什么系统.
  
  
    我进入到这个地方时，基本找出来了，不需要在修改什么了，如果和你的分区不一样,那可能还需要使用Deeper search的功能.我的成功修复了，所以直接按write直接进行写到分区表中修复.
  
