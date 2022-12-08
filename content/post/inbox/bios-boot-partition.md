---
title: bios boot partition
author: "-"
date: 2018-02-12T15:33:04+00:00
url: /?p=11881
categories:
  - Inbox
tags:
  - reprint
---
## bios boot partition

https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks/zh-cn

```bash
  
(parted)mkpart primary 1 3
  
(parted)name 1 grub
  
(parted)set 1 bios_grub on
  
(parted)print
  
```

https://www.cnblogs.com/f-ck-need-u/p/7084627.html
  
BIOS boot partition是一个分区,gnu grub[译注1]用它来引导基于legacy bios但启动设备上却包含GPT格式分区表时的操作系统。这种结构有时候被称为BIOS/GPT启动[译注2]。

下图非原文内容,是本人提供,用于直观地感受bios boot分区。

Bios boot分区是必要的,因为GPT使用紧跟在MBR后面的扇区来保存实际的分区表,但在传统的MBR分区架构中,这些扇区并没有特殊的作用,这样的结果是没有足够的可用空闲空间来存储stage2这段boot loader。MBR中也存储了boot loader,但MBR无法存储超过512字节的内容,所以MBR中的这段boot loader被当作stage1使用,它的主要作用是加载功能更多更复杂的stage2这段boot loader,stage2可以从文件系统读取和载入操作系统内核。

当使用了BIOS boot分区,该分区将包含stage2的boot loader程序,例如grub2文件,而stage1的boot loader代码仍保留在MBR中。使用bios boot分区不是解决基于传统bios但使用了gpt格式磁盘问题的唯一方法,但是复杂的boot loader如grub2无法将无法完全符合MBR中的398-446字节的区域,因此它们需要一个辅助的存储空间。在MBR磁盘上,一般使用紧跟在MBR后的扇区空间来存储这些复杂的boot loader,这些扇区空间就是大众所熟知的"MBR gap"。而在GPT磁盘上,由于没有与MBR gap等效的未使用空间,所以单独使用一个bios boot分区来分配这样的空间,以存储复杂的boot loader。

BIOS boot分区的GUID可以是"21686148-6449-6E6F-744E-656564454649"。在基于BIOS的平台下的GPT中,BIOS boot分区有点类似于EFI平台下的EFI系统分区,EFI系统分区使用UEFI保存文件系统和文件,而用于BIOS平台的BIOS boot分区则不使用文件系统来保存代码(见上面的图,在bios boot分区上是没有创建文件系统的)。

bios boot分区的大小非常小,可以小到只有31kB(由于第一个扇区是mbr,所以bios boot的内容从第2扇区到第63扇区),但是由于未来boot loader可能会扩展,所以建议bios boot分区设置为1M大小,而且很多磁盘分区工具都使用1MB分区对齐策略,这样MBR到第一个分区之间会保留一些空闲空间。

在Example 2中,grub 2在bios boot分区中存储它的core.img。

[译注1]gnu grub: 现在使用的grub都是gnu山寨出来的grub,原始的grub早已消失在历史中。

[译注2]: 也就是bios MBR和gpt混用的模式。

转载请注明出处: http://www.cnblogs.com/f-ck-need-u/p/7084627.html