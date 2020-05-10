---
title: failed to allocate direct memory
author: wiloon
type: post
date: 2018-03-23T07:46:52+00:00
url: /?p=12037
categories:
  - Uncategorized

---
failed to allocate 1024 byte(s) of direct memory (used: xxx, max: xxx)

https://netty.io/news/2016/06/07/4-0-37-Final.html
  
https://github.com/netty/netty/pull/5314

System.setProperty(&#8220;io.netty.maxDirectMemory&#8221;, &#8220;0&#8221;);

// Here is how the system property is used:
          
//
          
// * < 0 &#8211; Don&#8217;t use cleaner, and inherit max direct memory from java. In this case the
          
// &#8220;practical max direct memory&#8221; would be 2 * max memory as defined by the JDK.
          
// * == 0 &#8211; Use cleaner, Netty will not enforce max memory, and instead will defer to JDK.
          
// * > 0 &#8211; Don&#8217;t use cleaner. This will limit Netty&#8217;s total direct memory
          
// (note: that JDK&#8217;s direct memory limit is independent of this).
          
long maxDirectMemory = SystemPropertyUtil.getLong(&#8220;io.netty.maxDirectMemory&#8221;, -1);