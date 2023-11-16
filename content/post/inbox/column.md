---
title: column command
author: "-"
date: 2018-03-25T02:09:57+00:00
url: /?p=12056
categories:
  - Inbox
tags:
  - reprint
---
## column command

```bash
ip route list |column -t
```

- -c 字符数 指定显示的列宽
- -s 分隔符 使用 -t 选项时, 指定分隔符 (允许指定多个分隔符)
- -t 判断输入行的列数来创建一个表。分隔符是使用在 -s 中指定的字符。如果没有指定分隔符, 默认是空格
- -x 更改排列顺序 (左→右) 。默认的顺序为 (上→下)

```bash
df -h |column -t
```

Filesystem Size Used Avail Use% Mounted on
  
/dev/vda1 7.9G 3.3G 4.3G 44% /
  
/dev/vdb1 50G 1.9G 45G 4% /data

[https://blog.csdn.net/bbs11111111/article/details/5975188](https://blog.csdn.net/bbs11111111/article/details/5975188)
  
[http://ask.apelearn.com/question/9933](http://ask.apelearn.com/question/9933)

[http://blog.csdn.net/robertsong2004/article/details/38796985](http://blog.csdn.net/robertsong2004/article/details/38796985)
