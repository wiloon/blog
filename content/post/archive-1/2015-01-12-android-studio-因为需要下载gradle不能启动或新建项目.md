---
title: Android Studio 因为需要下载gradle不能启动或新建项目
author: wiloon
type: post
date: 2015-01-12T03:53:40+00:00
url: /?p=7217
categories:
  - Uncategorized

---
http://blog.csdn.net/likebamboo/article/details/19474893
  
分类： android 工具介绍2014-02-19 10:00 3201人阅读 评论(1) 收藏 举报
  
android studiogradle启动不了新建项目

目录(?)[+]

对于android studio 0.3.x 及以下的版本，安装或启动过程出现任何问题可以查看这篇博客。http://www.cnblogs.com/timeng/archive/2013/05/17/3084185.html 。
  
对于android studio 0.4.x 的版本， 安装了android studio 之后，按照上文所述的那篇博文下载安装gradle，配置环境变量， 启动android studio，新建项目，发现还是新建不了，界面一直停在 【"building ' 项目名' gradle project info"】:


其实这时候android studio 还是在下载 gradle ,但是由于被墙的原因, gradle 下载不了，所以建立不了项目。这时候我们只能在 任务管理器 中关闭android studio。

解决方案是：
  
1. Windows XP ：

打开 C:\Documents and Settings\<用户名>\.gradle\wrapper\dists\  。

Windows 7 ：

打开 C:\Users\<用户名>\.gradle\wrapper\dists 。

2. 你会看到这个目录下有个 gradle-x.xx-all 的文件夹， 这就是我们要手动下载的gradle版本，如果 x.xx 是1.9 ，那我们就要手动下载 1.9 版本，如果是1.10， 我们就要手动下载gradle 1.10 版本。下载地址是 http://www.gradle.org/downloads , 当然你也可以在 这里 下载。

3. 下载完相应版本的gradle之后，将下载的.zip文件(也可以解压)复制到上述的gradle-x.xx-all 文件夹下。

4. 重启Android Studio，新建项目，一切已经OK。当然第一次启动会比较慢。