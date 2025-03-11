---
title: Android APK反编译
author: "-"
date: 2014-12-30T02:19:52+00:00
url: /?p=7141
categories:
  - Inbox
tags:
  - reprint
---
## Android APK反编译

[http://blog.csdn.net/ithomer/article/details/6727581](http://blog.csdn.net/ithomer/article/details/6727581)

这段时间在学Android应用开发，在想既然是用Java开发的应该很好反编译从而得到源代码吧，google了一下，确实很简单，以下是我的实践过程。

在此郑重声明，贴出来的目的不是为了去破解人家的软件，完全是一种学习的态度，不过好像通过这种方式也可以去汉化一些外国软件。
  
本文Android反编译教程，测试环境:

Win7 Ultimate x64

Ubuntu 12.04 x86_x64

反编译工具包 下载  (2012-10-10更新)
  
一、Apk反编译得到Java源代码
  
下载上述反编译工具包，打开apk2java目录下的dex2jar-0.0.9.9文件夹，内含apk反编译成java源码工具，以及源码查看工具。

apk反编译工具dex2jar，是将apk中的classes.dex转化成jar文件

源码查看工具jdgui，是一个反编译工具，可以直接查看反编译后的jar包源代码
  
dex2jar 和 jdgui 最新版本下载，分别见google code:

dex2jar (google code)

jdgui (google code) ，最新版本请见 官方
  
具体步骤:

首先将apk文件后缀改为zip并解压，得到其中的classes.dex，它就是java文件编译再通过dx工具打包而成的，将classes.dex复制到dex2jar.bat所在目录dex2jar-0.0.9.9文件夹。

在命令行下定位到dex2jar.bat所在目录，运行

dex2jar.bat    classes.dex

生成

classes_dex2jar.jar
  
然后，进入jdgui文件夹双击jd-gui.exe，打开上面生成的jar包classes_dex2jar.jar，即可看到源代码了，如下图:

HelloAndroid源码在反编译前后的对照如下:

二、apk反编译生成程序的源代码和图片、XML配置、语言资源等文件

如果是汉化软件，这将特别有用

首先还是要下载上述反编译工具包，其中最新的apktool，请到google code下载

apktool (google code)
  
具体步骤:

下载上述反编译工具包，打开apk2java目录下的apktool1.4.1文件夹，内含三个文件: aapt.exe，apktool.bat，apktool.jar

注: 里面的apktool_bk.jar是备份的老版本，最好用最新的apktool.jar
  
在命令行下定位到apktool.bat文件夹，输入以下命令: apktool.bat  d  -f   abc123.apk   abc123，如下图:

上图中，apktool.bat 命令行解释: apktool.bat   d  -f    [apk文件 ]   [输出文件夹]
  
反编译的文件如下 (AndroidManifest.xml为例) :

将反编译完的文件重新打包成apk，很简单，输入apktool.bat   b    abc123 (你编译出来文件夹) 即可，命令如下:

打包apk后的文件在目录C:\HelloAndroid下，生成了两个文件夹:

build

dist

其中，打包生成的HelloAndroid.apk，在上面的dist文件夹下，Ok
  
三、 图形化反编译apk

上述步骤一、二讲述了命令行反编译apk，现在提供一种图形化反编译工具: Androidfby

首先，下载上述反编译工具包，打开Androidfby目录，双击Android反编译工具.exe，就可以浏览打开要反编译的apk

本文反编译工具包整理历史版本:
  
Android反编译工具包 (升级)    (2012-10-10)

Android反编译工具  (2012-08-21)
  
android反编译工具  (2011-08-28)
  
本博客反编译方法，仅供参考学习使用，禁止用于非法和商业等用途，谢谢！
