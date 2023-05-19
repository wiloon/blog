---
title: 将cmd中命令输出保存为TXT文本文件
author: "-"
date: 2019-09-17T02:41:45+00:00
url: /?p=14926
categories:
  - windows
tags:
  - reprint
---
## 将cmd中命令输出保存为TXT文本文件

<https://www.cnblogs.com/hongten/archive/2013/03/27/hongten_windows_cms.html>

将cmd中命令输出保存为TXT文本文件
  
在网上看到一篇名为: "[转载]如何将cmd中命令输出保存为TXT文本文件"

例如: 将Ping命令的加长包输出到D盘的ping.txt文本文件。
  
1. 在D:目录下创建文本文件ping.txt (这步可以省略，偶尔提示无法创建文件时需要)
  
2. 在提示符下输入ping <www.idoo.org.ru> －t > D:ping.txt
  
3. 这时候发现D盘下面的ping.txt里面已经记录了所有的信息
  
备注:
  
只用">"是覆盖现有的结果，每一个命令结果会覆盖现有的txt文件，如果要保存很多命令结果的话，就需要建立不同文件名的txt文件。
  
那么有没有在一个更好的办法只用一个txt文件呢？答案是肯定的，要在同一个txt文件里面追加cmd命令结果，就要用">>"替换">" 就可以了.
