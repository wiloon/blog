---
title: tee
author: "-"
date: 2017-02-28T07:29:45+00:00
url: tee
categories:
  - Linux
tags:
  - reprint
---
## tee

```bash
tail -f foo.log |grep bar tee bar.log
```

命令说明: 双向重定向, 从标准输入读取数据, 输出到屏幕上, 同时保存成文件。
  
格式: tee [-a] file
  
参数说明:
  
-a: 以累加的方式, 将数据加入到 file 中。
  
例如: ls -al /home | tee ~/myfile | more,将ls命令的数据存一份到myfile中,同时屏幕也有输出数据。

我使用过的Linux命令之 tee - 重定向输出到多个文件
  
本文链接: <http://codingstandards.iteye.com/blog/833695>    (转载请注明链接)

用途说明
  
在执行Linux命令时,我们可以把输出重定向到文件中,比如 ls >a.txt,这时我们就不能看到输出了,如果我们既想把输出保存到文件中,又想在屏幕上看到输出内容,就可以使用tee命令了。tee命令读取标准输入,把这些内容同时输出到标准输出和 (多个) 文件中 (read from standard input and write to standard output and files. Copy standard input to each FILE, and also to standard output. If a FILE is -, copy again to standard output.) 。在info tee中说道: tee命令可以重定向标准输出到多个文件 (\`tee': Redirect output to multiple files. The \`tee' command copies standard input to standard output and also to any files given as arguments.  This is useful when you want not only to send some data down a pipe, but also to save a copy.) 。要注意的是: 在使用管道线时,前一个命令的标准错误输出不会被tee读取。

常用参数
  
格式: tee

只输出到标准输出,因为没有指定文件嘛。

格式: tee file

输出到标准输出的同时,保存到文件file中。如果文件不存在,则创建；如果已经存在,则覆盖之。 (If a file being written to does not already exist, it is created. If a file being written to already exists, the data it previously
  
contained is overwritten unless the \`-a' option is used.)

格式: tee -a file

输出到标准输出的同时,追加到文件file中。如果文件不存在,则创建；如果已经存在,就在末尾追加内容,而不是覆盖。

格式: tee -

输出到标准输出两次。 (A FILE of \`-' causes \`tee' to send another copy of input to standard output, but this is typically not that useful as the copies are interleaved.)

格式: tee file1 file2 -

输出到标准输出两次,同时保存到file1和file2中。

使用示例
  
示例一 tee命令与重定向的对比

[root@web ~]# seq 5 >1.txt
  
[root@web ~]# cat 1.txt
  
[root@web ~]# cat 1.txt >2.txt
  
[root@web ~]# cat 1.txt | tee 3.txt
  
[root@web ~]# cat 2.txt
  
[root@web ~]# cat 3.txt
  
[root@web ~]# cat 1.txt >>2.txt
  
[root@web ~]# cat 1.txt | tee -a 3.txt
  
[root@web ~]# cat 2.txt
  
[root@web ~]# cat 3.txt
  
[root@web ~]#

示例二 使用tee命令重复输出字符串

[root@web ~]# echo 12345 | tee
  
12345

[root@web ~]# echo 12345 | tee -
  
12345
  
12345
  
[root@web ~]# echo 12345 | tee - -
  
12345
  
12345
  
12345
  
[root@web ~]# echo 12345 | tee - - -
  
12345
  
12345
  
12345
  
12345
  
[root@web ~]# echo 12345 | tee - - - -
  
12345
  
12345
  
12345
  
12345
  
12345
  
[root@web ~]#

[root@web ~]# echo -n 12345 | tee

12345[root@web ~]# echo -n 12345 | tee -
  
1234512345[root@web ~]# echo -n 12345 | tee - -
  
123451234512345[root@web ~]# echo -n 12345 | tee - - -
  
12345123451234512345[root@web ~]# echo -n 12345 | tee - - - -
  
1234512345123451234512345[root@web ~]#

示例三 使用tee命令把标准错误输出也保存到文件

[root@web ~]# ls "*"
  
ls: *: 没有那个文件或目录
  
[root@web ~]# ls "*" | tee -
  
ls: *: 没有那个文件或目录
  
[root@web ~]# ls "*" | tee ls.txt
  
ls: *: 没有那个文件或目录
  
[root@web ~]# cat ls.txt
  
[root@web ~]# ls "*" 2>&1 | tee ls.txt
  
ls: *: 没有那个文件或目录
  
[root@web ~]# cat ls.txt
  
ls: *: 没有那个文件或目录
  
[root@web ~]#

问题思考
  
相关资料
  
【1】Linux公社   linux tee命令详解
  
【2】百度知道    linux tee 命令的详细使用, 越详细越好.
  
【3】脚本学习    linux tee命令: 将标准输出一分为二
  
【4】起航工作室  linux tee 命令详解

【5】5Linux教程   Linux tee command

PS: 2011.10.09 对此文件进行了编辑。
