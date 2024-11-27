---
title: linux test disk io
author: "-"
date: 2018-02-07T03:58:38+00:00
url: /?p=11826
categories:
  - Inbox
tags:
  - reprint
---
## linux test disk io
```bash
  
time dd if=/dev/zero of=test.dbf bs=8k count=300000 oflag=direct
  
```

http://blog.csdn.net/zqtsx/article/details/25487185