---
title: opkg command, openwrt
author: w1100n
type: post
date: 2018-03-24T02:00:02+00:00
url: /?p=12043

---

opkg 工具 (一个 ipkg 变种) 是一个用来从本地软件仓库或互联网软件仓库上下载并安装 OpenWrt 软件包的轻量型软件包管理器。

```bash
opkg list # 获取软件列表
opkg update # 更新可以获取的软件包列表
opkg upgrade # 对已经安装的软件包升级
opkg install # 安装指定的软件包

opkg install xxx.ipk
opkg remove xxx
```

https://wiki.openwrt.org/zh-cn/doc/techref/opkg

https://blog.csdn.net/whatday/article/details/78920494