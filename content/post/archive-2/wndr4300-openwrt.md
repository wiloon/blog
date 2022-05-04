---
title: 'WNDR4300 openwrt'
author: "-"
date: 2016-01-09T04:08:41+00:00
url: /?p=8660
categories:
  - network
tags:
  - reprint
---
## 'WNDR4300 openwrt'

https://wiki.openwrt.org/zh-cn/toh/netgear/wndr4300
  
WNDR4300
  
Flash容量: 128 MiB NAND
  
RAM: 128 MiB
  
mips, not mipsle
  
go build ... GOMIPS=softfloat

WNDR4300有两种固件,一种为 ...ubi-factory.img 格式,一种为 ...squashfs-sysupgrade.tar 格式。 其中 img 格式只能用 tftp 的方法刷入。而 tar 只能通过已刷了Openwrt的WEB端进行刷入。
https://downloads.openwrt.org/releases/19.07.3/targets/ar71xx/nand/openwrt-19.07.3-ar71xx-nand-wndr4300-ubi-factory.img
https://downloads.openwrt.org/releases/17.01.4/targets/ar71xx/nand/lede-17.01.4-ar71xx-nand-wndr4300-squashfs-sysupgrade.tar

```bash
opkg update
opkg install libopenssl
opkg list_installed
```

下载img文件
http://downloads.openwrt.org/chaos_calmer/15.05/ar71xx/nand/openwrt-15.05-ar71xx-nand-wndr4300-ubi-factory.img

进路由器界面,找到『固件升级』,然后上传这个包点确定。路由器就会自动刷成 openwrt 固件,等待它重启后再连路由器就大功告成了。
  
下载升级包: http://downloads.openwrt.org/chaos_calmer/15.05/ar71xx/nand/openwrt-15.05-ar71xx-nand-wndr4300-squashfs-sysupgrade.tar稍后在 openwrt 系统里给升级。
  
基础设置
  
新的 openwrt 固件默认是不开 wifi 的,所以第一次你得用网线连上路由器,进去后应试能看到 luci 界面,这里会让你输入密码,用户名默认是 root,此时密码还是个空的,随便输一个回车进回界面,

先设置一密码吧,直接点 luci 界面上面的警告条后进入密码设置界面,输入一个你自己的密码,顺便把下面的 远程ssh给勾上。
  
让你的路由器连上网,按顶部菜单栏进入net-interface选择你的接口,通常是 WAN 口,点旁边的 eidt,然后选择 ppope,点切换,然后输入你的宽带帐号和密码,然后应用。 此时你的路由已经能上网了。
  

---

https://wiki.openwrt.org/zh-cn/toh/netgear/wndr4300
  
http://dlmao.com/wndr4300-%E6%8A%98%E8%85%BE-openwrt-%E8%AE%B0.html
  
http://dlmao.com/wndr4300-zhe-teng-openwrt-ji-zhong-ji-xiu-zheng-ban.html
  
https://bigeagle.me/2016/02/ipset-policy-routing/

https://php-rmcr7.rhcloud.com/openwrt-fq/

https://php-rmcr7.rhcloud.com/openwrt-fq/embed/#?secret=xcThHfkyLS  
https://cokebar.info/archives/948  

https://cokebar.info/archives/948/embed#?secret=k8dinHiD9m
https://forum.archive.openwrt.org/viewtopic.php?id=16599