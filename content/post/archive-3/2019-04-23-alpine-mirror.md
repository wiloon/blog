---
title: alpine
author: wiloon
type: post
date: 2019-04-23T06:24:28+00:00
url: /?p=14227
categories:
  - Uncategorized

---
alpine mirror
  
vim /etc/apk/repositories
  
http://mirrors.ustc.edu.cn/

### alpine install telnet

```bash
apk update
apk add busybox-extras
busybox-extras telnet localhost 6900
```