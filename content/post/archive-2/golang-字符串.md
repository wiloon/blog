---
title: golang 字符串/string
author: "-"
date: 2017-02-17T01:13:08+00:00
url: go/string
categories:
  - Go
tags:
  - reprint
---
## golang 字符串/string

## 判断字符串开头

```go
import (
    "fmt"
    "strings"
)

func main() {
    myString := "www.topgoer.com"
    // Option 1: (Recommended)
    if strings.HasPrefix(myString, "www") {
        fmt.Println("Hello to you too")
    } else {
        fmt.Println("Goodbye")
    }
}

```

### go, string, join

```go
func main() {
    // 将字符串数组 拼接成 字符串
    // 参数: 要拼接的数组,拼接的内容
    str := strings.Join([]string{`你好`, `世界`}, `,`)

    // 输出拼接好的字符串
    println(str)
}


package main
 
import "strings"
 
func main(){
    a := "hahaha"
    b := "hehehe"
    c := strings.Join([]string{a,b},",")
    println(c)

```

### 字符串截取

```go
s := "abcdefg"
s = string([]byte(s)[:3])
fmt.Println(s) //得到 "abc"

s := "abcdefg"
s = string([]byte(s)[3:])
fmt.Println(s) //得到 "efg"

s := "12121211122"
first3 := s[0:3]
last3  := s[len(s)-3:]
```

### 字符串比较

```go
fmt.Println("go"=="go")
fmt.Println("GO"=="go")

fmt.Println(strings.Compare("GO","go"))
fmt.Println(strings.Compare("go","go"))

fmt.Println(strings.EqualFold("GO","go"))
```

Compare函数,区分大小写,比自建方法"=="的速度要快

### 测试字符串是否为空

```go
if len(mystring) > 0 { }
if mystring != "" { }
```

### 字符串连接

```bash
s = fmt.Sprintf("%s[%s]", s, v)

```

### 格式化 补0

```go
func main() {
    log.Println(fmt.Sprintf("%013d", 1))
}
```

substring
  
str := "hello world"
  
fmt.Print(str[0:5])
  
运行的时候将会输出

hello

split
  
strings.Split

<http://www.cnblogs.com/modprobe/p/4302681.html>

go语言中的字符串的比较: 相等
  
<https://www.crifan.com/go_language_string_compare_equal/embed/#?secret=u61L06fdZP>
  
<http://blog.csdn.net/oqqyuan1234567890/article/details/59110219>
