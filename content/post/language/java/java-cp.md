---
title: java -cp
author: "-"
date: 2012-04-17T13:24:22+00:00
url: /?p=2951
categories:
  - Java
tags:
  - reprint
---
## java cp

[http://quicker.iteye.com/blog/856722](http://quicker.iteye.com/blog/856722)

java -cp .;c:dir1lib.jar Test

-cp 和 -classpath 一样，是指定类运行所依赖其他类的路径，通常是类库，jar包之类，需要全路径到jar包，windows上分号";"分隔，linux上是冒号":"分隔。不支持通配符，需要列出所有jar包，用一点"."代表当前路径。

虽然现在都有 eclipse 之类的 IDE 了，但有时候后会手工编译和运行一些程序，很多人包括多年开发经验的人都不知道怎么在命令行参
  
数运行类。有点杯具……
  
使用范例:
  
java -cp ..libhsqldb.jar org.hsqldb.Server -database mydb
  
或
  
java -cp ../lib/hsqldb.jar org.hsqldb.Server -database.0 mydb -dbname.0 mydb

    -cp <class search path of directories and zip/jar files>