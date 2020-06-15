---
title: shell exit退出状态代码
author: wiloon
type: post
date: 2019-01-07T06:03:34+00:00
url: /?p=13349
categories:
  - Uncategorized

---
https://blog.csdn.net/hongkangwl/article/details/16184883

Linux提供$?特殊变量来保存最后一条命令执行结束的退出状态。执行完一条命令后，立即执行echo$?，可以查看最后一条命令的退出状态值。

正常的情况下，命令成功执行完成的退出状态是0，如果非0，则命令执行有错。
  
该命令可以用于检查命令是否正确执行，比如在解压包的时候，检查解压包是否成功十分有效。

自定义退出状态码，可以在脚本中定义自己的退出状态代码，然后使用echo $?检查。

退出状态码最高是255，一般自定义的代码值为0~255，如果超出255，则返回该数值被256除了之后的余数。

退出状态代码：

0 命令成功完成

1通常的未知错误

2误用shell命令

126命令无法执行

127没有找到命令

128无效的退出参数

128+x使用Linux信号x的致命错误。

130使用Ctrl-C终止的命令

255规范外的退出状态

ubuntu下测试结果如下
  
wl@wl-MS-7673:/home/python$ date
  
2013年 11月 14日 星期四 19:12:45 CST
  
wl@wl-MS-7673:/home/python$ echo $?
  

  
wl@wl-MS-7673:/home/python$ kkllk
  
kkllk: command not found
  
wl@wl-MS-7673:/home/python$ echo $?
  
127
  
wl@wl-MS-7673:/home/python$ ls
  
hello.py hello.py~
  
wl@wl-MS-7673:/home/python$ vim a.c
  
wl@wl-MS-7673:/home/python$ ls
  
hello.py hello.py~
  
wl@wl-MS-7673:/home/python$ gedit a.c
  
wl@wl-MS-7673:/home/python$ ./hello.py
  
bash: ./hello.py: 权限不够
  
wl@wl-MS-7673:/home/python$ echo $?
  
126
  
wl@wl-MS-7673:/home/python$ date %t
  
date: 无效的日期"%t"
  
wl@wl-MS-7673:/home/python$ echo $?
  
1
  
wl@wl-MS-7673:/home/python$

root@wl-MS-7673:~# ls -sail test
  
790207 4 -rwxr&#8211;r&#8211; 1 root root 30 11月 14 19:25 test
  
root@wl-MS-7673:~# ./test
  
root@wl-MS-7673:~# echo $?
  
44
  
root@wl-MS-7673:~# cat test
  
#!/bin/bash
  
var=300
  
exit $var
  
root@wl-MS-7673:~#

* * *

作者：王伴农
  
来源：CSDN
  
原文：https://blog.csdn.net/hongkangwl/article/details/16184883
  
版权声明：本文为博主原创文章，转载请附上博文链接！