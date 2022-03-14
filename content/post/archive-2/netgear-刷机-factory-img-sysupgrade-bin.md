---
title: 'netgear  刷机, factory.img, sysupgrade.bin'
author: "-"
date: 2018-10-28T02:49:31+00:00
url: /?p=12826
categories:
  - Uncategorized

tags:
  - reprint
---
## 'netgear  刷机, factory.img, sysupgrade.bin'
xxx-factory.img

1. 把网线连接路由器的LAN口 和 PC的网口
2. 路由器断电,用牙签或其他工具,捅路由器的reset口。
3. 开启设备电源开关,观察电源灯 (此时保持按住Restore Factory Settings按钮不要松手) ,直到电源灯由橙色闪烁状态变到绿色闪烁状态 (说明设备已经进入到了TFTP修复模式) 
    - R7800: 橙色闪烁变成白色闪烁。
4. 在win下面使用DOS命令,即:  tftp -i 192.168.1.1 put 文件名.img
5. 在mac下面,同样也是使用tftp命令。
    1.自己的ip改成192.168.1.10,网关即路由ip 192.168.1.1
    2.把 下好的 img 固件放到用户文件夹下
    3.打开终端,输入(binary的作用是改为二进制模式)>tftp>connect 192.168.1.1>binary>put 文件名.img完了之后路由器会闪灯后自动重启。

### linux
      tftp
      tftp> binary
      tftp> verbose
      tftp> put 192.168.1.1:openwrt.img

  6. 文件传送完毕后,等待80秒左右,设备会自动重启 (请耐心等待,切勿将路由器手动断电) 。至此,TFTP修复完成。
  7. 设备重启后,可手动断电,再重启。否则可能没有5G。这不是BUG,其他openwrt也是一样的
  8. 如果恢复过程中断或失败,重复上述步骤再做尝试。

https://www.netgear.com/support/product/WNDR4300.aspx
https://downloads.openwrt.org/releases/19.07.3/targets/ar71xx/nand/openwrt-19.07.3-ar71xx-nand-wndr4300-ubi-factory.img
https://downloads.openwrt.org/releases/17.01.4/targets/ar71xx/nand/lede-17.01.4-ar71xx-nand-wndr4300-squashfs-sysupgrade.tar