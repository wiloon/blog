---
title: r7800 openwrt
author: "-"
date: 2018-03-22T16:08:42+00:00
url: /?p=12034
categories:
  - network
tags:
  - reprint
  - HomeLab
---
## r7800 openwrt

在ubuntu上安装如下软件包:
  
gcc, g++, binutils, bzip2, flex, python, perl, make,find, grep, diff, unzip, gawk, getopt, subversion, libz-dev and libc 头文件
  
sudo apt-get updatesudo apt-get install gcc g++ build-essential subversion git-core libncurses5-dev zlib1g-dev gawk flex quilt libssl-dev xsltproc libxml-parser-perl mercurial bzr ecj cvs unzip
  
选择编译目标
  
make menuconfig Target System (Qualcomm Atheros IPQ806X) ->
  
Target Profile (Netgear Nighthawk X4S R7800) -> 退出保存
  
编译固件
  
make V=s -j4
  
编译完成后
  
ubuntu:~/kunteng-lede$ ls bin/targets/ipq806x/generic/config.seed
  
lede-ipq806x-R7800-squashfs-sysupgrade.tar lede-ipq806x-vmlinux.elflede-ipq806x-device-r7800.manifest
  
lede-ipq806x-squashfs-root.img
  
packageslede-ipq806x-R7800-squashfs-factory.img lede-ipq806x-ubifs-root.img
  
sha256sums其中lede-ipq806x-R7800-squashfs-factory.img即为R7800的工厂固件, lede-ipq806x-R7800-squashfs-sysupgrade.tar为升级固件

download <https://downloads.openwrt.org/releases/17.01.4/targets/bcm53xx/generic/lede-sdk-17.01.4-bcm53xx_gcc-5.4.0_musl-1.1.16_eabi.Linux-x86_64.tar.xz>
  
cd openwrt
  
./scripts/feeds update -a
  
./scripts/feeds install dnsmasq
  
make menuconfig

<https://wiki.openwrt.org/doc/howto/buildroot.exigence>

<https://wiki.openwrt.org/doc/howto/obtain.firmware.sdk>

<https://www.reddit.com/r/openwrt/comments/74mgvd/need_help_to_build_custom_dnsmasq_package_for/?ref_source=embed&ref=share>

<https://wikidevi.com/wiki/Netgear_R7800>
<http://www.right.com.cn/forum/thread-144853-1-1.html>
<http://www.expreview.com/47447-2.html>
<https://forum.openwrt.org/viewtopic.php?id=68795>
<https://blog.wanjie.info/2016/12/openwrt-or-lede-image-builder/>
<https://wikidevi.com/wiki/Netgear_R7000>
<https://openwrt.org/meta/infobox/broadcom_wifi>
<https://openwrt.org/inbox/unsupported_features>
<https://downloads.openwrt.org/releases/17.01.4/targets/bcm53xx/generic/>
