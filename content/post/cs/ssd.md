---
title: SSD
author: "-"
date: 2019-04-14T02:04:41+00:00
url: ssd
categories:
  - Hardware
tags:
  - reprint
---
## SSD

### TRIM

```bash
#检查 SSD 是否支持 TRIM
lsblk --discard
# 或者用 hdparm
sudo pacman -S hdparm
sudo hdparm -I /dev/sda | grep TRIM
```

Linux 文件系统对于删除操作，只标记为未使用，实际并没有清零，底层存储如 SSD 和传统机械磁盘并不知道哪些数据块可用，哪些数据块可以 Erase。所以对于非空的 page，SSD 在写入前必须先进行一次 Erase，则写入过程为 read-erase-modify-write: 将整个 block 的内容读取到 cache 中，整个 block 从 SSD 中 Erase, 要覆写的 page 写入到 cache 的 block 中，将 cache 中更新的 block 写入闪存介质，这个现象称之为写入放大( write amplification)。

SSD中提供了一个TRIM命令，操作系统在删除文件时可以通过向SSD发送TRIM命令告诉它哪些数据块中的数据已经不再使用了。SSD在收到TRIM命令后，通常会在定期的垃圾收集操作中重新组织这些区块，为将来写入数据做好准备，不过每一款SSD在底层对TRIM命令的执行机制都不尽相同，但无论如何，通过TRIM能够显著改善SSD的性能和寿命。

[https://www.guokr.com/blog/483475/](https://www.guokr.com/blog/483475/)

[https://zhuanlan.zhihu.com/p/34683444](https://zhuanlan.zhihu.com/p/34683444)

## SSD 检测工具

## Crystal Dick Info

## Crystal Disk Mark

## Samsung_Magician_Installer_Official_7.0.1.630

[https://semiconductor.samsung.com/consumer-storage/support/tools/](https://semiconductor.samsung.com/consumer-storage/support/tools/)