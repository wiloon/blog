---
title: golang 读系统环境变量
author: lcf
date: 2012-10-29T03:18:33+00:00
url: golang-sys-env
categories:
  - Inbox
tags:
  - reprint
aliases:
  - /p4561/
  - /p6454/
  - /p6467/
---
## golang 读系统环境变量

http://studygolang.com/articles/3387

```go
os.Setenv("FOO", "1")
fmt.Println("FOO:", os.Getenv("FOO"))
```