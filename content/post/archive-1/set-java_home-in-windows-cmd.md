---
title: Set JAVA_HOME in windows cmd
author: "-"
date: 2014-12-29T07:21:19+00:00
url: /?p=7137
categories:
  - Inbox
tags:
  - Windows

---
## Set JAVA_HOME in windows cmd

http://kooyee.iteye.com/blog/525068

set JAVA_HOME=jrepath
  
set PATH=%JAVA_HOME%\bin;%PATH%
  
注意这里没有引号。
  
这样就不需要在我的电脑属性中修改java_home了,以及重启命令行了。
  
对于程序会用到多个jre 会比较有用。

linux 修改 JAVA_HOME如下
  
export JAVA_HOME=jrepath
  
export PATH=$JAVA_HOME\bin;$PATH

如果需要永久修改 则 在.bashrc文件中加入上面的两句话就可以了。