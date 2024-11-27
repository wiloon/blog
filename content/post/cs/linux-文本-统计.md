---
title: linux 文本 统计
author: "-"
date: 2015-10-28T06:09:58+00:00
url: /?p=8439
categories:
  - Inbox
tags:
  - reprint
---
## linux 文本, 字符 统计

```bash
# 统计一个目录下所有 .md 文件的字符数
find content/post -name '*.md' -exec wc -w '{}' \; > /tmp/foo.txt
awk '{sum+=$1} END {print sum}' /tmp/foo.txt

# 另外一种统计, 数字好像不太对, 有时间再研究一下.
ls -lR content/post |grep '\.md'|wc -w

```

### 用 grep -c 来统计匹配的行数
  
grep -c 的作用类似grep | wc -l,不同的是,如果是查找多个文件,grep -c会统计每个文件匹配的行数,每行一个文件的列出来,而 wc -l 则列出总的统计数字。
  
另外grep -c 要比 grep | wc -l快一点。

grep -c night restart.07014

返回2

没有

返回0


>http://blog.csdn.net/xuejiayue1105/article/details/1483940
