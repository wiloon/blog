---
title: 按日期删除文件
author: "-"
date: 2018-10-26T09:28:49+00:00
url: delete-by-date
categories:
  - Linux
tags:
  - find

---
## 按日期删除文件

```bash
# 列出30天前的日志
find /data/logs -mtime +30 -type f -name "*.*"
# 删除30天前的日志
find /data/logs -mtime +30 -type f -name "*.*" -exec rm -f {} \;

# 删除3天前的所有以".log"结尾的文件
find /文件路径 -name "*.log" -mtime +2 -exec rm {} \;
```

### 说明

  1. 文件路径是目标文件所在路径
  2. -name 设定目标文件名,建议采用,否则可能误删其他文件；
  3. -ctime 文件最后一次修改时间,后面只能用整数,单位为天,同时, 还有 atime, mtime(修改时间), amin, cmin, mmin 等时间参数可选, 具体请查看帮助
     + -mtime: File's data was last modified n_24 hours ago.
     + -mtime +10: 查找10天前的文件,这里用数字代表天数,+30表示查找30天前的文件
  4. 时间说明如下图 (随手画的,大概是这个意思) ,所以删除三天前的文件要用+2
  5. -exec 表示需要执行的命令,{} 代表 find 找到的内容, "\;" 是固定写法表示结束 -exec

所以例子的"-exec rm {} \;" 就表示对find找到的符合条件的文件执行删除操作

---

https://blog.csdn.net/liujianfei526/article/details/52433039  
https://www.linuxidc.com/Linux/2013-06/85613.htm  

