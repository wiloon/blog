---
title: A cycle was detected in the build path of project
author: "-"
date: 2015-08-10T04:11:39+00:00
url: /?p=8091
categories:
  - Uncategorized
tags:
  - Java

---
## A cycle was detected in the build path of project
解决Eclipse中Java工程间循环引用而报错的问题
  
如果我们的项目包含多个工程 (project) ,而它们之间又是循环引用的关系,那么Eclipse在编译时会抛出如下一个错误信息: 
  
"A cycle was detected in the build path of project: XXX"
  
解决方法非常简单: 
  
Eclipse Menu -> Window -> Preferences... -> Java -> Compiler -> Building -> Building path problems -> Circular dependencies -> 将Error改成Warning

http://blog.csdn.net/kcai678/article/details/4668993