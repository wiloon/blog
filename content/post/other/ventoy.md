---
author: "-"
date: "2021-02-11 17:41:09" 
title: ventoy, 安装盘, 多合一启动盘制作工具, 多个系统 Win/PE/Linux 镜像装在1个U盘里
url: ventoy
categories:
  - inbox
tags:
  - reprint
---
## ventoy, 安装盘, 多合一启动盘制作工具, 多个系统 Win/PE/Linux 镜像装在 1 个 U 盘里

ventoy 是一款国人开发的新一代多 ISO 启动引导程序，这款工具最大的优点就是无需格式化优盘，用户只需要将所需的 ISO 镜像文件拷贝至优盘中即可在Ventoy 界面中选择自己想要的 ISO 镜像文件。

## Ventoy 五大优势

- 广泛兼容：支持包括 Windows 10、Windows 8.1、Windows 7、WinPE 系统以及 Ubuntu 等多种 Linux 发行版。
- 无需格盘：该工具可以直接安装到U盘上且不需要将其他镜像刻录U盘，用户需要做的仅仅是将ISO复制到U盘中。
- 启动兼容：无差别支持Legacy BIOS 和UEFI模式，无论你的电脑主板使用什么模式Ventoy都可以自动检测识别。
- 大型文件：该工具也支持将超过4GB的镜像文件复制到U盘，这点很重要因为Windows 10 镜像文件已超过4GB。
- 其他优势：可并存多个操作系统镜像无需每次使用重新格盘刻录、启动过程中支持写保护、版本升级不丢失数据。

### commands

```bash
yay -S ventoy-bin
# 或者直接下载
download linux version: ventoy-1.0.35-linux.tar.gz
sudo ./Ventoy2Disk.sh -i /dev/sdx
# 复制各种 iso 到 /dev/sdb1
```

[https://www.ventoy.net/](https://www.ventoy.net/)

## winPE iso

[https://www.ventoy.net/en/distro_iso/winpe.html](https://www.ventoy.net/en/distro_iso/winpe.html)
