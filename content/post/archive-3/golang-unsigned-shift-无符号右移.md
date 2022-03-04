---
title: 'golang  unsigned shift, 无符号右移'
author: "-"
date: 2020-02-11T09:06:44+00:00
url: /?p=15522
categories:
  - Uncategorized

tags:
  - reprint
---
## 'golang  unsigned shift, 无符号右移'
int32 转 uint32 再右移

https://stackoverflow.com/questions/33336336/go-perform-unsigned-shift-operation

```go
func Test10(t *testing.T) {
    x1 := -100
    result := uint32(x1) >> 2
    fmt.Println(result)
}

```