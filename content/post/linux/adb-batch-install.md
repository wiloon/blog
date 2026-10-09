---
title: "Linux 下用 adb 为 Android 手机批量安装软件"
author: "-"
date: 2012-09-24T14:58:35+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: adb-batch-install
categories:
  - Linux
tags:
  - android
  - adb
  - remix
  - AI-assisted
aliases:
  - /linux下用adb为android手机批量安装软件/
---
## linux下用adb为android手机批量安装软件

通常大家安装软件都是从Andorid Market或者从网上下载到手机本地安装，这有两个问题，第一个情况碰到网速慢，那要急死，第二种情况是安装的太慢，如果软件多的话，手指累死，那么，就用adb安装吧，看我的操作情况:
  
首先把以前安装的软件备份到电脑，比如~/backup/，接着，打开电脑上的终端，取得root权限，
  
# cd adb
  
# ./adb start-server
  
打开另一个终端，默认用户权限
  
$ cd adb
  
$ sh install.sh  (-sh里面的内容如这样: ./adb install ~/backup/***.apk......，把你要装的软件都这样编辑，一行一个软件)
  
ok，等着吧，安装完，切换到第一个终端，执行
  
# ./adb kill-server
  
安全移除手机，看看手机上是不是已经显示你安装的软件了，呵呵

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `adb-batch-install.md`；title 改为「Linux 下用 adb 为 Android 手机批量安装软件」；url 改为 `adb-batch-install`；旧 url 加入 aliases | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
