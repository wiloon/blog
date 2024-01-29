---
title: 统计文件行数, 文件数
author: "-"
date: 2016-05-15T05:01:30+00:00
url: /?p=8996
categories:
  - inbox
tags:
  - reprint
---
## 统计文件行数, 文件数
Linux下有三个命令: ls、grep、wc。通过这三个命令的组合可以统计目录下文件及文件夹的个数。

统计当前目录下文件的个数 (不包括目录) 
    ls -l | grep "^-" | wc -l
统计当前目录下文件的个数 (包括子目录) 
    ls -lR| grep "^-" | wc -l
查看某目录下文件夹(目录)的个数 (包括子目录) 
    ls -lR | grep "^d" | wc -l

### 统计.md文件个数
    ls -lR|grep "^-.*.md"|wc -l


语法: wc [选项] 文件…

说明: 该命令统计给定文件中的字节数、字数、行数。如果没有给出文件名,则从标准输入读取。wc同时也给出所有指定文件的总统计数。字是由空格字符区分开的最大字符串。

该命令各选项含义如下: 

- c 统计字节数。
- l 统计行数。
- w 统计字数。

这些选项可以组合使用。

输出列的顺序和数目不受选项的顺序和数目的影响。

总是按下述顺序显示并且每项最多一列。

行数、字数、字节数、文件名

如果命令行中没有文件名,则输出中不出现文件名。

例如: 

`$ wc - lcw file1 file2

4 33 file1

7 52 file2

11 11 85 total`

举例分析: 

### 统计文件数量
```
  find demo/ -name "*.js" |wc -l
  find ~/projects/wiloon.com/content -name "*.md" |wc -l
```

2.统计demo目录下所有js文件代码行数: 

```
  find demo/ -name "*.js" |xargs cat|wc -l 或 wc -l `find ./ -name "*.js"`|tail -n1
```

3.统计demo目录下所有js文件代码行数,过滤了空行: 

```
  find /demo -name "*.js" |xargs cat|grep -v ^$|wc -l
```

http://www.cnblogs.com/fullhouse/archive/2011/07/17/2108786.html