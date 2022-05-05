---
title: du command
author: "-"
date: 2011-12-24T01:34:26+00:00
url: du
categories:
  - Linux
tags:
  - reprint
---
## du command

disk usage

### 查看文件占用的磁盘空间

     du --block-size=1 sparse-file

### 查看各子目录大小 -d, --max-depth

    du -hd 1
    du -hd1
    du -h --max-depth=1
    du -hd1 --exclude=proc

### 参数

    # 排除文件或目录
    --exclude=foo

### 排序

    du -d1 |sort -rn

```bash
du -sh

du -s ./* | sort -rn
# 这是按字节排序
du -sh ./* | sort -rn
# 这是按兆 (M) 来排序

4.选出排在前面的10个 
du -s ./* | sort -rn | head

5.选出排在后面的10个 
du -s ./* | sort -rn | tail

说明: ./*也可以改成你想到达的任何目录 
如/usr/local/ 这个目录就可以写成 
/usr/local/*

```

-s, --summarize    
display only a total for each argument
  
-h, --human-readable
print sizes in human readable format (e.g., 1K 234M 2G)

du(disk usage)
  
功能说明: 显示磁盘空间的使用情况，统计目录 (或文件) 所占磁盘空间的大小。该命令的功能是逐级进入指定目录的每一个子目录并显示该目录占用文件系统数据块 (1024字节) 的情况。若没有给出指定目录，则对当前目录进行统计。

语法: du [-abcDhHklmsSx][-L <符号连接>][-X <文件>][–block-size][–exclude=<目录或文件>][–max-depth=<目录层数>][–help][–version][目录或文件]

补充说明: du会显示指定的目录或文件所占用的磁盘空间。

参数: 
  
    -a 或-all 递归地显示指定目录中各文件及子目录中各文件占用的数据块数。若既不指定-s，也不指定-a，则只显示Names中的每一个目录及其中的各子目录所占的磁盘块数。
    -b 或 -bytes 显示目录或文件大小时，以byte为单位。 (数据可能来自 inode)
    -c 或–total 除了显示个别目录或文件的大小外，同时也显示所有目录或文件的总和。
    -D 或–dereference-args 显示指定符号连接的源文件大小。
    -h 或 –human-readable 以K，M，G为单位，提高信息的可读性。 (数据可能来自 superblock , -h 和 -b 的数据源不一样)
  
-H 或–si 与-h参数相同，但是K，M，G是以1000为换算单位。
-k 或–kilobytes 以1024 bytes为单位。
  
-l 或–count-links 重复计算硬件连接的文件。  
-L <符号连接>或–dereference<符号连接> 显示选项中所指定符号连接的源文件大小。  
-m 或–megabytes 以1MB为单位。
  
-s 或–summarize 仅显示总计。
  
-S 或–separate-dirs 显示个别目录的大小时，并不含其子目录的大小。
  
-x 或–one-file-xystem 以一开始处理时的文件系统为准，若遇上其它不同的文件系统目录则略过。
  
-X <文件>或–exclude-from=<文件> 在<文件>指定目录或文件。
  
--exclude=<目录或文件> 略过指定的目录或文件。
  
–max-depth=<目录层数> 超过指定层数的目录后，予以忽略。
  
–help 显示帮助。
  
–version 显示版本信息。

* * *

https://blog.csdn.net/windone0109/article/details/4445518