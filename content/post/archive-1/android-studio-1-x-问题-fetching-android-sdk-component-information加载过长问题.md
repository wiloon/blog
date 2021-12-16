---
title: 'Android Studio 1.x  问题  Fetching android sdk component information加载过长问题'
author: "-"
date: 2015-02-04T01:29:04+00:00
url: /?p=7300
categories:
  - Uncategorized

---
## 'Android Studio 1.x  问题  Fetching android sdk component information加载过长问题'
**http://blog.csdn.net/zhongwcool/article/details/41939967**

**解决Fetching android sdk component information加载过长问题**

安装完成后,如果直接启动,Android Studio会去获取 android sdk 组件信息,这个过程相当慢,还经常加载失败,导致Android Studio启动不起开。解决办法就是不去获取android sdk 组件信息。方法如下: 
  
1) 进入刚安装的Android Studio目录下的bin目录。找到idea.properties文件,用文本编辑器打开。
  
2) 在idea.properties文件末尾添加一行: disable.android.first.run=true,然后保存文件。
  
3) 关闭Android Studio后重新启动,便可进入界面。

这是由cnblog的@sonyi提供的方案,可用。

其实是如果不做这个修改, Android Studio每次启动都会去检查更新。