---
title: 未找到文件 WFMLRSVCApp.ear
author: wiloon
type: post
date: 2015-07-07T02:15:02+00:00
url: /?p=8009
categories:
  - Uncategorized

---
http://www.cnblogs.com/zzuzys/p/3195885.html

在64位Windows 7 系统下安装Oracle Database 11g 的过程中，
  
出现提示：
  
“未找到文件D:\app\Administrator\product\11.2.0\dbhome\_1\owb\external\oc4j\_applications\applications\WFMLRSVCApp.ear”，

解决方法如下：
  
两个安装文件夹：win64\_11gR2\_database\_1of2和win64\_11gR2\_database\_2of2
  
首先将win64\_11gR2\_database\_2of2\database\stage\Components里文件复制到win64\_11gR2\_database\_1of2\stage\Components
  
而后运行win64\_11gR2\_database_1of2文件中的setup.exe

注意：再次运行的时候要将D:\app\Administrator\product\11.2.0\dbhome\_1\.......红色区域文件删除，也就是删除dbhome\_1文件夹。

否者安装到60%左右会出现文件移动错误！！