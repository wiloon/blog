---
title: kill a process in one line using bash
author: w1100n
type: post
date: 2018-08-25T09:01:59+00:00
url: /?p=12563
categories:
  - Uncategorized

---
https://stackoverflow.com/questions/3510673/find-and-kill-a-process-in-one-line-using-bash-and-regex

```bash
  
kill $(ps -ef|grep process-foo|grep -v grep |awk '{print $2}')
  
```