---
title: apktool APK解压、打包
author: wiloon
type: post
date: 2014-09-24T01:24:35+00:00
url: /?p=6990
categories:
  - Uncategorized

---
[shell]

keytool -genkey -alias JFrench.keystore -keyalg RSA -validity 1000000 -keystore JFrench.keystore

jarsigner -verbose -keystore E:\projects\keystore\JFrench.keystore -s ignedjar JFrench_signed.apk foo.apk JFrench.keystore

[/shell]

&nbsp;

&nbsp;

http://showlike.iteye.com/blog/1686103

http://blog.csdn.net/jesusjzp/article/details/7922451