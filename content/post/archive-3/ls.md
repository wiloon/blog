---
title: ls command
author: "-"
date: 2022-11-17 13:21:20
url: ls
categories:
  - Linux
tags:
  - reprint
  - remix
---
## ls command

- ls 默认列出当前目录的内容, ls 是 list 的缩写
- ls 命令默认会按照文件名字母序排序

```bash
find $PWD | xargs ls -ld
ls -lrth

# -l 默认按文件名排序
ls -l 

# 只列出目录
ls -d foo*
ls -dl foo*    
ls -l | grep ^d

# 子目录所有文件
ls -lR|grep ^-
ls -lR|grep ^-|awk '{print $9}'

# 列出重复的行
ls -lR|grep ^-|awk '{print $9}'|sort|uniq -d
```

## 参数

- -i 打印出文件的 inode
- -R 列出所有子目录
- -L 当文件是软链接时, 直接显示被链接的文件的信息
- -l 除文件名称外，亦将文件型态、权限、拥有者、文件大小等资讯详细列出
- -t 选项，将首先按照文件的最后修改时间排序 (时间越新越靠前) ，之后再按字母顺序排
- -T 结合 -l 可将时间显示为 hh:mi:ss 的形式，但不会按时间排序，因而不会影响默认字母排序
- -S 按文件大小排序，越大越靠前
- -u 结合 -l 选项可以看到每个文件最后被访问的时间，并且也会按该时间排序

以上影响排序的选项如果结合 -r 选项一起使用，则按相反顺序排列

<https://www.iteye.com/blog/wxl24life-2041310>

## 通配符和正则表达式

<https://www.cnblogs.com/lixuwu/p/7816335.html>
