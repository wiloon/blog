---
title: clonezill
author: "-"
date: 2019-03-15T05:23:40+00:00
url: clonezill
categories:
  - CS
tags:
  - reprint
  - remix
---
## clonezill

download clonezill iso from https://clonezilla.org/downloads.php

install balenaEtcher

```Bash
dd bs=1M conv=fdatasync if=./clonezilla-live-3.2.0-5-amd64.iso of=/dev/sdx
```

```
start clonezilla
device-image
nfs_server
dhcp
nfs4
192.168.50.227
/backup_xxxx/
beginner
save parts
```


## clonezill

https://clonezilla.org/

https://clonezilla.org/liveusb.php#macos-setup

1. Download the `Clonezilla` Live iso file.
2. Insert a USB flash drive on the Mac machine.
3. Erase it using the standard Mac Disk Utility (exFAT works fine).
4. Download `balenaEtcher` for macOS, then follow its document to burn the image to the USB flash drive.
5. Eject the USB drive.

Thanks to Hans Palm for providing this info.

### 备份硬盘

https://minipc.netlify.app/posts/3390c071/

1. Clonezilla GNU GRUB
2. Clonezilla live (VGA 800*600)
3. zh_CN.UTF8 Chinese
4. keyboard: Keep
5. start clonezilla
6. device-image
7. local_dev
8. 插入移动硬盘
9. 屏幕上会打印出当前连接的存储设备, 能看到系统盘 nvme01 和移动硬盘
10. ctrl-c
11. 选择保存镜像文件的分区, 选移动硬盘上的空闲分区 sdb1
12. 检查文件系统, 因为要备份的是windows所以选择 no-fsck
13. 选择保存镜像的目录, 默认选中的是根目录, 选好之后选择 Done
14. 看一下屏幕上打印的挂载状态, 没有问题的话按回车
15. 模式选择: Beginner
16. savedisk: 备份整个目标硬盘
17. 输入镜像名
18. 选择要备份的硬盘: nvme0n1
19. 压缩方式: z9p (默认)
20. 因为目标盘是 windows, 所以跳过 fsdk: -sfsck
21. 检查保存的镜像
22. 不加密 -senc
23. 操作完成要执行的动作 -p choose
24. 按 y 执行
