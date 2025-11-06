---
title: IDEA无法启动,Failed to create JVM,error code -4
author: "-"
date: 2014-12-10T01:49:51+00:00
url: /?p=7107
categories:
  - Inbox
tags:
  - IDEA

---
## IDEA无法启动,Failed to create JVM,error code -4
http://blog.csdn.net/twlkyao/article/details/24534505

发生该错误的原因是因为IDEA需要使用的连续内存空间没有得到满足,解决方案: 

1.减小-Xmx和-XX:PermSize的值
  
切换到IDE_HOME\bin\目录下,找到<product>.exe.vmoptions文件,尝试减少-Xmx和-XX:PermSize的值,建议以100M为单位,直到IDEA可以启动。
  
2.开启64位模式
IDEA提供idea64.exe的启动器,该启动器使用64位的JDK (需要单独安装) 。
  
3.使用<product>.bat启动

使用<product>.bat替代.exe启动IDEA。
  
4.强制使用64位的JDK

.bat脚本默认使用32位的JDK (IDEA安装文件的jre 目录下) ,可以通过环境变量强制使用64位的JDK,变量的值取决于你使用的产品,IDEA_JDK for IntelliJ IDEA, WEBIDE_JDK for PhpStorm and WebStorm, PYCHARM_JDK for PyCharm, RUBYMINE_SDK for RubyMine. 参考选择合适的JDK。
  
5.卸载不常用的应用程序

通过卸载不常用的应用程序来减少应用分割程地址空间。
  
参考资料: 点击打开链接