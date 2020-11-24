---
title: linux test disk io
author: w1100n
type: post
date: 2018-02-07T03:58:38+00:00
url: /?p=11826
categories:
  - Uncategorized

---
```bash
  
time dd if=/dev/zero of=test.dbf bs=8k count=300000 oflag=direct
  
```

http://blog.csdn.net/zqtsx/article/details/25487185