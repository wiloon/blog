---
title: rename
author: "-"
date: 2017-09-30T04:10:48+00:00
url: rename
categories:
  - Inbox
tags:
  - reprint
---
## rename

## 重命名 rename

```bash
  
#files
  
copy-sys-log-01
  
copy-sys-log-02

rename copy-sys-log-0 copy-app-log-0 copy-sys-log-0*

7000
  
7001
  
7002

rename 700 node-700 700*

node-7000
  
node-7001
  
node-7002
  
```

### rename + 正则

```bash
rename 's/\d{4}-\d{2}-\d{2}-//' *.md
```

### 批量重命名

```bash
find . -name '*.md' -exec rename 's/\d{4}-\d{2}-\d{2}-//' {} \;
```

<http://www.cnblogs.com/longdouhzt/archive/2012/04/30/2477282.html>
  
<http://blog.51cto.com/jiemian/1846951>
