---
title: golang bytes.buffer
author: "-"
date: 2019-03-21T02:43:54+00:00
url: go/bytes-buffer
categories:
  - Go
tags:
  - reprint
---
## golang bytes.buffer

```go
buf := bytes.NewBuffer([]byte{})
```

bytes.buffer 是一个缓冲 byte 类型的缓冲器，这个缓冲器里存放着都是 byte  
A buffer is a variable-sized buffer of bytes with Read and Write methods. The zero value for Buffer is an empty buffer ready to use.

## 创建 Buffer 缓冲器

```go
var b bytes.Buffer         // 定义一个 Buffer 变量，不用初始化
b.Writer([]byte("Hello ")) // 可以直接使用

b1 := new(bytes.Buffer)   //直接使用 new 初始化，可以直接使用

// 其它两种定义方式
func NewBuffer(buf []byte) *Buffer
func NewBufferString(s string) *Buffer
```

### NewBufferString
  
还可以用 bytes.NewBufferString("hello") 来建立一个内容是 hello 的缓冲器

```go
buf1:=bytes.NewBufferString("hello")
buf2:=bytes.NewBuffer([]byte("hello"))
buf3:=bytes.NewBuffer([]byte{"h","e","l","l","o"})
// 以上三者等效
buf4:=bytes.NewBufferString("")
buf5:=bytes.NewBuffer([]byte{})
// 以上两者等效
```

如果 buffer 在 new 的时候是空的也没关系，因为可以用 Write 来写入，写在尾部

## 写入到缓冲器 (缓冲器变大) 使用 Write 方法，将一个 byte 类型的 slice 放到缓冲器的尾部

`func (b *Buffer) Write(p []byte) (n int, err error)`

```go
package main

import (
    "bytes"
    "fmt"
)

func main() {
    var buffer bytes.Buffer
    for i := 0; i < 1000; i++ {
        buffer.WriteString("a")
    }
    fmt.Println(buffer.String())
}
```

[https://my.oschina.net/u/943306/blog/127981](https://my.oschina.net/u/943306/blog/127981)

### bytes.Buffer, io.Writer

```go
import "bufio"
import "bytes"

func main() {
    var b bytes.Buffer
    foo := bufio.NewWriter(&b)
}
```

>[https://www.kancloud.cn/digest/batu-go/153538](https://www.kancloud.cn/digest/batu-go/153538)
