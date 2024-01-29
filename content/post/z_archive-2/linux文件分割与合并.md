---
title: Linux split, 文件分割与合并
author: "-"
date: 2017-09-01T05:13:51+00:00
url: /?p=11083
categories:
  - Inbox
tags:
  - reprint
---
## Linux split, 文件分割与合并
```bash
  
# -l 按行分割
  
# -d numeric suffixes
  
split -l 300 -d large_file.txt new_file_prefix
  
```

inux文件分割与合并: split & cat

Linux下文件分割可以通过split命令来实现,而用cat进行文件合并。而分割可以指定按行数分割和安大小分割两种模式。Linux下文件合并可以通过cat命令来实现,非常简单。
  
在Linux下用split进行文件分割: 
  
模式一: 指定分割后文件行数
  
对与txt文本文件,可以通过指定分割后文件的行数来进行文件分割。
  
命令: 
  
split -l 300 large_file.txt new_file_prefix
  
模式二: 指定分割后文件大小
  
对于可执行文件等二进制文件,则不能通过文件行数来进行文件分割,此时我们可以指定分割大小来分隔文件。
  
命令: 
  
split -b 10m large_file.bin new_file_prefix
  
对二进制文件我们同样也可以按文件大小来分隔。
  
在Linux下用cat进行文件合并: 
  
命令: 
  
cat small_files* > large_file
  
Linx文件分割命令英文释义: 
  
-, read standard input.

Mandatory arguments to long options are mandatory for short options too.

-a, -suffix-length=N

use suffixes of length N (default 2)

-b, -bytes=SIZE

put SIZE bytes per output file

-C, -line-bytes=SIZE

put at most SIZE bytes of lines per output file

-d, -numeric-suffixes

use numeric suffixes instead of alphabetic

-l, -lines=NUMBER

put NUMBER lines per output file

http://os.51cto.com/art/201104/255359.htm