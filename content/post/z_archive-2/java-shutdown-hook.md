---
title: java shutdown hook
author: "-"
date: 2015-12-30T07:16:53+00:00
url: /?p=8610
categories:
  - Inbox
tags:
  - reprint
---
## java shutdown hook
在线上Java程序中经常遇到进程程挂掉,一些状态没有正确的保存下来,这时候就需要在JVM关掉的时候执行一些清理现场的代码。Java中得ShutdownHook提供了比较好的方案。
  
JDK在1.3之后提供了Java Runtime.addShutdownHook(Thread hook)方法,可以注册一个JVM关闭的钩子,这个钩子可以在以下几种场景被调用: 

1) 程序正常退出
  
2) 使用System.exit()
  
3) 终端使用Ctrl+C触发的中断
  
4) 系统关闭
  
5) 使用Kill pid命令干掉进程
  
注: 在使用kill -9 pid是不会JVM注册的钩子不会被调用。

http://blog.csdn.net/hemingwang0902/article/details/6207682

http://www.cnblogs.com/nexiyi/p/java_add_ShutdownHook.html