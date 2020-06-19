---
title: 'golang  unsigned shift, 无符号右移'
author: wiloon
type: post
date: 2020-02-11T09:06:44+00:00
url: /?p=15522
categories:
  - Uncategorized

---
int32 转 uint32 再右移

https://stackoverflow.com/questions/33336336/go-perform-unsigned-shift-operation

```golang
func Test10(t *testing.T) {
    x1 := -100
    result := uint32(x1) >> 2
    fmt.Println(result)
}

```