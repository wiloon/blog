---
title: linux下用adb为android手机批量安装软件
author: "-"
date: 2012-09-24T14:58:35+00:00
url: /?p=4235
categories:
  - Linux

tags:
  - reprint
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
  
安全移除手机，看看手机上是不是已经显示你安装的软件了，呵呵</wbr>
