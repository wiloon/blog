---
title: 'netgear 刷机, factory.img, sysupgrade.bin, openwrt'
author: "-"
date: 2018-10-28T02:49:31+00:00
url: netgear
categories:
  - Router
tags:
  - reprint
  - remix
  - openwrt
---
## 'netgear  刷机, factory.img, sysupgrade.bin, openwrt'

xxx-factory.img

- 把网线连接路由器的 LAN 口 和 PC 的网口
- 路由器断电, 用牙签或其他工具, 捅路由器的 reset 口
- 开启设备电源开关, 观察电源灯 (此时保持按住 reset/ Restore Factory Settings 按钮不要松手), 直到电源灯由橙色闪烁状态变到绿色闪烁状态(wndr4300) (说明设备已经进入到了TFTP修复模式)
  - R7800: 电源灯从橙色闪烁变成白色闪烁。
- 在 win 下面使用命令, `tftp -i 192.168.1.1 put image0.img`
- 在 mac 下面, 同样也是使用 tftp 命令。
  - 自己的 ip 改成192.168.1.10, 网关即路由 ip 192.168.1.1
  - 把下好的 img 固件放到用户文件夹下
  - 打开终端, 输入 (binary的作用是改为二进制模式)>tftp> connect 192.168.1.1>binary>put 文件名.img完了之后路由器会闪灯后自动重启。

### linux

```bash
tftp
(to) 192.168.1.1
tftp> binary
tftp> verbose
tftp> put openwrt0.img
tftp> quit
```

- 文件传送完毕后,等待 80 秒左右, 设备会自动重启 (请耐心等待, 切勿将路由器手动断电)。至此, TFTP 修复完成。
- 设备重启后, 可手动断电, 再重启。否则可能没有5G。这不是BUG,其他openwrt也是一样的
- 如果恢复过程中断或失败, 重复上述步骤再做尝试。

[https://www.netgear.com/support/product/WNDR4300.aspx](https://www.netgear.com/support/product/WNDR4300.aspx)

[https://downloads.openwrt.org/releases/19.07.3/targets/ar71xx/nand/openwrt-19.07.3-ar71xx-nand-wndr4300-ubi-factory.img](https://downloads.openwrt.org/releases/19.07.3/targets/ar71xx/nand/openwrt-19.07.3-ar71xx-nand-wndr4300-ubi-factory.img)

[https://downloads.openwrt.org/releases/17.01.4/targets/ar71xx/nand/lede-17.01.4-ar71xx-nand-wndr4300-squashfs-sysupgrade.tar](https://downloads.openwrt.org/releases/17.01.4/targets/ar71xx/nand/lede-17.01.4-ar71xx-nand-wndr4300-squashfs-sysupgrade.tar)
