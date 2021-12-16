---
title: Android Log
author: "-"
date: 2014-07-31T08:34:42+00:00
url: /?p=6869
categories:
  - Uncategorized

---
## Android Log
http://blog.csdn.net/Android_Tutor/article/details/5081713

Android中级教程之--Log图文详解(Log.v,Log.d,Log.i,Log.w,Log.e)!
  
分类:  Android中级教程 2009-12-26 16:14 61927人阅读 评论(56) 收藏 举报
  
androidlayoutbuttonencodingeclipsebt
  
在Android群里，经常会有人问我,AndroidLog是怎么用的，今天我就把从网上以及SDK里东拼西凑过来，让大家先一睹为快，希望对大家入门AndroidLog有一定的帮助．

android.util.Log常用的方法有以下5个: Log.v() Log.d() Log.i() Log.w() 以及 Log.e() 。根据首字母对应VERBOSE，DEBUG,INFO, WARN，ERROR。

1、Log.v 的调试颜色为黑色的，任何消息都会输出，这里的v代表verbose啰嗦的意思，平时使用就是Log.v("","");

2、Log.d的输出颜色是蓝色的，仅输出debug调试的意思，但他会输出上层的信息，过滤起来可以通过DDMS的Logcat标签来选择.

3、Log.i的输出为绿色，一般提示性的消息information，它不会输出Log.v和Log.d的信息，但会显示i、w和e的信息

4、Log.w的意思为橙色，可以看作为warning警告，一般需要我们注意优化Android代码，同时选择它后还会输出Log.e的信息。

5、Log.e为红色，可以想到error错误，这里仅显示红色的错误信息，这些错误就需要我们认真的分析，查看栈的信息了。