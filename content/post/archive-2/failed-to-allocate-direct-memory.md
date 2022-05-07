---
title: failed to allocate direct memory
author: "-"
date: 2018-03-23T07:46:52+00:00
url: /?p=12037
categories:
  - Inbox
tags:
  - reprint
---
## failed to allocate direct memory
failed to allocate 1024 byte(s) of direct memory (used: xxx, max: xxx)

https://netty.io/news/2016/06/07/4-0-37-Final.html
  
https://github.com/netty/netty/pull/5314

System.setProperty("io.netty.maxDirectMemory", "0");

// Here is how the system property is used:
          
//
          
// * < 0 - Don't use cleaner, and inherit max direct memory from java. In this case the
          
// "practical max direct memory" would be 2 * max memory as defined by the JDK.
          
// * == 0 - Use cleaner, Netty will not enforce max memory, and instead will defer to JDK.
          
// * > 0 - Don't use cleaner. This will limit Netty's total direct memory
          
// (note: that JDK's direct memory limit is independent of this).
          
long maxDirectMemory = SystemPropertyUtil.getLong("io.netty.maxDirectMemory", -1);