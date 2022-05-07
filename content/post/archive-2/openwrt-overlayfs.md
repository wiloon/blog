---
title: R7800, Build custom Netgear R7800 firmware for a larger flash size/root space
author: "-"
date: 2018-04-05T15:47:18+00:00
url: /?p=12113
categories:
  - Inbox
tags:
  - reprint
---
## R7800, Build custom Netgear R7800 firmware for a larger flash size/root space
```bash
  
sudo apt-get install subversion g++ zlib1g-dev build-essential git python rsync man-db
  
sudo apt-get install libncurses5-dev gawk gettext unzip file libssl-dev wget

git clone https://github.com/openwrt/openwrt.git openwrt
  
cd openwrt
  
git fetch -all -tags -prune
  
git checkout tags/v17.01.2

./scripts/feeds update -a
  
wget https://downloads.lede-project.org/releases/17.01.4/targets/ipq806x/generic/config.seed -O config.seed
  
rm -rf .config*
  
mv config.seed .config

#Edit the following file with your favorite editor:
  
target/linux/ipq806x/files/arch/arm/boot/dts/qcom-ipq8065-r7800.dts

#for R7800:
  
#1. DON'T TOUCH kernel and ubi. and I won't touch reserve neither.
  
#2. Remove netgear section. it contains, actually, nothing useful, if you want to use lede.
  
#3. extend ubi partition to the end of original netgear partition.

# luci support
  
./scripts/feeds update packages luci
  
./scripts/feeds install -a -p luci

# make menuconfig 不要用root账号
  
make menuconfig #set "Target System", "Subtarget", "Target Profile";
  
make defconfig #恢复默认配置

# 选了dnsmasq-full就不要选dnsmasq了, 编译的时候会冲突
  
Base system> dnsmasq-full>Build with IPset support.

#调试用的, 选用。
  
kernel modules>Netfilter Extensions>kmod-ipt-debug
  
Administration>syslog-ng

# make -j8 V=s不要用root账号
  
make -j8 V=s #(build OpenWRT with console logging, you can see where build failed.).

编译出来的img到这找:  bin/targets/ipq806x/generic/lede-17.01.4-ipq806x-R7800-squashfs-factory.img

sudo ip link set enp0s31f6 up
  
sudo ip addr add 192.168.1.11/24 broadcast 192.168.1.255 dev enp0s31f6

tftp -v -m binary 192.168.1.1 -c put lede-17.01.4-ipq806x-R7800-squashfs-factory.img

```

https://forum.lede-project.org/t/netgear-r7800-only-19mb-flash-available/1115
  
https://forum.lede-project.org/t/tutorial-build-custom-netgear-r7800-firmware-for-a-larger-flash-size-root-space/5989
  
https://kb.netgear.com/22688/How-to-upload-firmware-to-a-NETGEAR-router-using-TFTP

http://www.right.com.cn/forum/thread-144853-1-1.html

```bash
  
cat /proc/mtd
  
```