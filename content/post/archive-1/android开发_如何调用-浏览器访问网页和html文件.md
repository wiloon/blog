---
title: Android开发_如何调用 浏览器访问网页和Html文件
author: "-"
date: 2015-01-12T08:48:27+00:00
url: /?p=7228
categories:
  - Uncategorized

tags:
  - reprint
---
## Android开发_如何调用 浏览器访问网页和Html文件
http://blog.csdn.net/mengweiqi33/article/details/7679467
  
分类:  Android学习笔记2012-06-20 13:41 5291人阅读 评论(0) 收藏 举报
  
浏览器androidhtmlurlfilescheme
  
一、启动android默认浏览器


Intent intent= new Intent();
  
intent.setAction("android.intent.action.VIEW");
  
Uri content_url = Uri.parse("http://www.cnblogs.com");
  
intent.setData(content_url);
  
startActivity(intent);

这样子，android就可以调用起手机默认的浏览器访问。


二、指定相应的浏览器访问
  
1. 指定android自带的浏览器访问

 ( "com.android.browser": packagename   ；"com.android.browser.BrowserActivity": 启动主activity) 
  
Intent intent= new Intent();
  
intent.setAction("android.intent.action.VIEW");
  
Uri content_url = Uri.parse("http://www.cnblogs.com");
  
intent.setData(content_url);
  
intent.setClassName("com.android.browser","com.android.browser.BrowserActivity");
  
startActivity(intent);

2. 启动其他浏览器 (当然该浏览器必须安装在机器上) 
  
只要修改以下相应的packagename 和 主启动activity即可调用其他浏览器


intent.setClassName("com.android.browser","com.android.browser.BrowserActivity");

uc浏览器": "com.uc.browser", "com.uc.browser.ActivityUpdate"

opera    : "com.opera.mini.android", "com.opera.mini.android.Browser"
  
qq浏览器: "com.tencent.mtt", "com.tencent.mtt.MainActivity"


三、打开本地html文件

打开本地的html文件的时候，一定要指定某个浏览器，而不能采用方式一来浏览，具体示例代码如下


Intent intent= new Intent();
  
intent.setAction("android.intent.action.VIEW");
  
Uri content_url = Uri.parse("content://com.android.htmlfileprovider/sdcard/help.html");
  
intent.setData(content_url);
  
intent.setClassName("com.android.browser","com.android.browser.BrowserActivity");
  
startActivity(intent);
  
关键点是调用了"content"这个filter。

以前有在win32编程的朋友，可能会觉得用这种形式"file://sccard/help.html"是否可以，可以很肯定的跟你说，默认的浏览器设置是没有对"file"这个进行解析的，如果要让你的默认android浏览器有这个功能需要自己到android源码修改manifest.xml文件，然后自己编译浏览器代码生成相应的apk包来重新在机器上安装。

大体的步骤如下: 

1. 打开 packages/apps/Browser/AndroidManifest.xml文件把加到相应的<intent-filter>后面就可以了


<intent-filter>
  

  
<category android:name="android.intent.category.DEFAULT" />
  
<category android:name="android.intent.category.BROWSABLE" />
  
<data android:scheme="file" />
  
</intent-filter>
  
2. 重新编译打包，安装，这样子，新的浏览器就支持"file"这个形式了
  
有兴趣的可以去试试。