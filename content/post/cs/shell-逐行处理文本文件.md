---
title: Shell 逐行处理文本文件
author: "-"
date: 2018-08-28T10:58:20+00:00
url: /?p=12599
categories:
  - shell
tags:
  - reprint
---
## Shell 逐行处理文本文件， shell 读文件

[https://www.cnblogs.com/dwdxdy/archive/2012/07/25/2608816.html](https://www.cnblogs.com/dwdxdy/archive/2012/07/25/2608816.html)

## read命令

read命令接收标准输入,或其他文件描述符的输入,得到输入后,read命令将数据放入一个标准变量中．

用read读取文件时,每次调用read命令都会读取文件中的"一行"文本．

当文件没有可读的行时, read命令将以非零状态退出．

```bash
#!/bin/bash
cat data.dat | while read line; do
    echo "File:${line}"
done

while read line; do
    echo "File:${line}"
done <data.dat
```
  
2.使用awk命令完成

awk是一种优良的文本处理工具,提供了极其强大的功能．

利用awk读取文件中的每行数据,并且可以对每行数据做一些处理,还可以单独处理每行数据里的每列数据．

1 cat data.dat | awk '{print $0}'
  
2 cat data.dat | awk 'for(i=2;i<NF;i++) {printf $i} printf "\n"}'
  
第1行代码输出data.dat里的每行数据,第2代码输出每行中从第2列之后的数据．

如果是单纯的数据或文本文件的按行读取和显示的话,使用awk命令比较方便．

3.使用for var in file 命令完成

for var in file表示变量var在file中循环取值．取值的分隔符由$IFS确定．

复制代码
  
1 for line in $(cat data.dat)
  
2 do
  
3 echo "File:${line}"
  
4 done
  
6 for line in `cat data.dat`
  
7 do
  
8 echo "File:${line}"
  
9 done
  
复制代码
  
如果输入文本每行中没有空格,则line在输入文本中按换行符分隔符循环取值．

如果输入文本中包括空格或制表符,则不是换行读取,line在输入文本中按空格分隔符或制表符或换行符特环取值．

可以通过把IFS设置为换行符来达到逐行读取的功能．

IFS的默认值为: 空白(包括: 空格,制表符,换行符)．
