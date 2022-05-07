---
title: apktool之APK解压、打包
author: "-"
date: 2014-12-30T06:52:58+00:00
url: /?p=7157
categories:
  - Inbox
tags:
  - reprint
---
## apktool之APK解压、打包
http://blog.csdn.net/caszhao/article/details/6030425


博客分类:  java
  
apktoolandroidjava
  
简介: 
  
Android apktool是一个用来处理APK文件的工具,可以对APK进行反编译生成程序的源代码和图片、XML配置、语言资源等文件,也可以添加新的功能到APK文件中。用该工具来汉化Android软件然后重新打包发布是相当简单的。
  
1. 安装
  
1) .首先安装需要JAVA环境，先下载JDK/JRE，点击下载，已经有JAVA环境的可跳过此步

2) .到code.google上下载apktool.jar以及相关文件: http://code.google.com/p/android-apktool/downloads/list
  
点击下载apktool1.4.3.tar.bz2 和 apktool-install-windows-r04-brut1.tar.bz2

3) .解压apktool-install-windows-r04-brut1.tar.bz2到任意文件夹，然后解压apktool1.4.3.tar.bz2,把apktool.jar拷贝至apktool-install-windows-r04-brut1.tar.bz2解压所在的文件夹下，此时文件下有aapt.exe、apktool.bat及apktool.jar三个应用。

4) .点击开始菜单，运行，输入CMD回车，用cd命令转到刚刚解压的D:\My Documents\Desktop\apktool-install-windows-r04-brut1所在的文件夹，输入apktool，出现如下命令即说明安装成功 (以下信息，即apktool使用命令) 。

D:\My Documents\Desktop\apktool-install-windows-r04-brut1>apktool
  
Java代码 收藏代码
  
Apktool v1.4.3 - a tool for reengineering Android apk files
  
Copyright 2010 Ryszard Wi?niewski <brut.alll@gmail.com>
  
Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

Usage: apktool [-q|-quiet OR -v|-verbose] COMMAND [...]

COMMANDs are:

d[ecode] [OPTS] <file.apk> [<dir>]
  
Decode <file.apk> to <dir>.

OPTS:

-s, -no-src
  
Do not decode sources.
  
-r, -no-res
  
Do not decode resources.
  
-d, -debug
  
Decode in debug mode. Check project page for more info.
  
-f, -force
  
Force delete destination directory.
  
-t <tag>, -frame-tag <tag>
  
Try to use framework files tagged by <tag>.
  
-keep-broken-res
  
Use if there was an error and some resources were dropped, e.g.:
  
"Invalid config flags detected. Dropping resources", but you
  
want to decode them anyway, even with errors. You will have to
  
fix them manually before building.
  
b[uild] [OPTS] [] [<out_file>]
  
Build an apk from already decoded application located in .

It will automatically detect, whether files was changed and perform
  
needed steps only.

If you omit  then current directory will be used.
  
If you omit <out_file> then /dist/<name_of_original.apk>
  
will be used.

OPTS:

-f, -force-all
  
Skip changes detection and build all files.
  
-d, -debug
  
Build in debug mode. Check project page for more info.

if|install-framework <framework.apk> [<tag>]
  
Install framework file to your system.

For additional info, see: http://code.google.com/p/android-apktool/

2. 使用
  
1) .解压APK
  
D:\My Documents\Desktop\apktool-install-windows-r04-brut1>apktool d F:\document\APK\PushAd.apk F:\document\app
  
源文件: F:\document\APK\PushAd.apk
  
解压目录: F:\document\app
  
Java代码 收藏代码
  
I: Baksmaling...
  
I: Loading resource table...
  
I: Loaded.
  
I: Loading resource table from file: D:\My Documents\apktool\framework\1.apk
  
I: Loaded.
  
I: Decoding file-resources...
  
I: Decoding values*/* XMLs...
  
I: Done.
  
I: Copying assets and libs...
  
2) .打包APK
  
D:\My Documents\Desktop\apktool-install-windows-r04-brut1>apktool b F:\document\app F:\\document\\app.apk
  
源文件: F:\\document\\app
  
打包目录: F:\document\app.apk
  
Java代码 收藏代码
  
I: Checking whether sources has changed...
  
I: Smaling...
  
I: Checking whether resources has changed...
  
I: Building resources...
  
I: Building apk file...