---
title: 'Android  sqlite3,not found'
author: "-"
type: post
date: 2014-08-07T03:08:29+00:00
url: /?p=6903
categories:
  - Uncategorized

---
# 'Android  sqlite3,not found'
http://panxq0809.iteye.com/blog/1264785

在Android开发中，使用 adb shell 下的 sqlite3 命令来查看操作SQLite数据库时，遇到了 [ sqlite3 : not found] 问题。
  
网上找了下问题的原因——模拟器或真机中的 /system/xbin 目录下少了sqlite3 这个文件。

解决方法，步骤如下: 
  
（1) 让/system文件夹可读写
  
#adb shell
  
# mount -o remount,rw -t yaffs2 /dev/block/mtdblock3 /system

（2) 导入所需的sqlite3文件到/system/xbin目录。
  
（可以新建个模拟器，从/system/xbin中导出sqlite3，即可得到sqlite3文件;或者从另外一个有sqlite3文件的机器中导出获得) 
  
# adb push sqlite3 /system/xbin

（3) 修改 sqlite3 权限
  
# chmod 4755 /system/xbin/sqlite3

（4) 设置 /system为只读文件
  
# mount -o remount,ro -t yaffs2 /dev/block/mtdblock3 /system

（5) 至此，就可以使用 sqlite3 命令来操作 SQLite 数据库了。