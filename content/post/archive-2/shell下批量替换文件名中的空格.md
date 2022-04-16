---
title: shell下批量替换文件名中的空格
author: "-"
date: 2017-09-22T14:00:29+00:00
url: /?p=11188
categories:
  - shell
tags:
  - reprint
  - shell
---
## shell下批量替换文件名中的空格
http://blog.csdn.net/dliyuedong/article/details/14229121

```bash
  
rename 's/ /_/g' *
  
rename 's/\(/_/g' *
  
```