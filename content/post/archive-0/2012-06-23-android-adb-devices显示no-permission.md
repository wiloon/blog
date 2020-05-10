---
title: Android adb devices显示no permission
author: wiloon
type: post
date: 2012-06-23T01:35:19+00:00
url: /?p=3627
categories:
  - Linux

---
<http://www.blogjava.net/brian/articles/316019.html>

在ubuntu(9.10)下执行adb devices命令, 返回的结果是:
  
List of devices attached
  
???????????? no permissions
  
这意味着,USB连接的设备是能够被识别的。Google之后，得知adb server需要以root的权限启动，于是有了如下命令:
  
brian@brian-laptop:~/Dev/Java/Android/android-sdk-linux_86/tools$ **./adb kill-server**
  
brian@brian-laptop:~/Dev/Java/Android/android-sdk-linux_86/tools$ **sudo ./adb start-server**
  
\* daemon not running. starting it now \*
  
\* daemon started successfully \*

第一条命令用来杀死当前正在运行的server, 第二条命令则以root的权限启动了新的server. 我们可以再次查看devices:
  
brian@brian-laptop:~/Dev/Java/Android/android-sdk-linux_86/tools$ **./adb devices**
  
List of devices attached
  
HT848KV04386 device

这次设备就被正确识别了。自然地, 像ddms之类的工具也能派上用场了。

如果你的机器不能识别，或不是Ubuntu环境，请参考官方文档:http://developer.android.com/guide/developing/device.html。