---
title: Android SharedPreferences
author: "-"
type: post
date: 2014-08-29T06:14:34+00:00
url: /?p=6966
categories:
  - Uncategorized

---
1.概述。SharePreferences是用来存储一些简单配置信息的一种机制，使用Map数据结构来存储数据，以键值对的方式存储，采用了XML格式将数据存储到设备中。例如保存登录用户的用户名和密码。只能在同一个包内使用，不能在不同的包之间使用，其实也就是说只能在创建它的应用中使用，其他应用无法使用。

创建的存储文件保存在/data/data/<package name>/shares_prefs文件夹下。

http://blog.csdn.net/zuolongsnail/article/details/6556703

http://xusaomaiss.iteye.com/blog/378524