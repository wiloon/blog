---
title: Golang 命名规范
author: "-"
date: 2012-04-07T10:55:18+00:00
url: /?p=2833
categories:
  - Linux
  - Network

tags:
  - reprint
---
## Golang 命名规范

## 变量命名

和结构体类似，变量名称一般遵循驼峰法，首字母根据访问控制原则大写或者小写，但遇到特有名词时，需要遵循以下规则：

如果变量为私有，且特有名词为首个单词，则使用小写，如 appService；

若变量类型为 bool 类型，则名称应以 Has, Is, Can 或 Allow 开头。

```go
var isExist bool
var hasConflict bool
var canManage bool
```

>https://zhuanlan.zhihu.com/p/216001587


## golang 文件名 命名规则
project name: -
  
package: lowercase
  
file name: _
  
https://stackoverflow.com/questions/25161774/what-are-conventions-for-filenames-in-go

https://golang.org/doc/effective_go.html#package-names
