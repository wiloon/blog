---
title: golang rand, 随机数
author: "-"
date: 2017-07-27T07:14:38+00:00
url: go/rand
categories:
  - Go
tags:
  - reprint
---
## golang 随机数

<http://www.cnblogs.com/baiyuxiong/p/4545032.html>
  
math/rand 包用于生成随机数。

```go
package main

import "fmt"
import "math/rand"

func main() {
    fmt.Println(rand.Intn(100)) // 产生0-100的随机整数
    fmt.Println(rand.Float32()) 
    fmt.Println(rand.Float64()) // 产生0.0-1.0的随机浮点数
    
    s1 := rand.NewSource(42) // 用指定值创建一个随机数种子
    r1 := rand.New(s1)
    fmt.Print(r1.Intn(100), ",")
    fmt.Print(r1.Intn(100))
    fmt.Println()
    
    s2 := rand.NewSource(42) // 同前面一样的种子
    r2 := rand.New(s2)
    fmt.Print(r2.Intn(100), ",")
    fmt.Print(r2.Intn(100))
    fmt.Println()
}

func GenRandomBytes(size int) (randomBytes []byte) {
    rand.Seed(time.Now().UnixNano())
    randomBytes = make([]byte, size)
    rand.Read(randomBytes)
    return randomBytes
}
```

返回结果:

```r
81
0.9405090880450124
5,87
5,87
```

多次重复执行上述代码,返回的结果仍然是一样的。所以为了使得调用的随机数不相同,就需要使用NewSource来提供一个随机的种子。比如:

s2 := rand.NewSource(time.Now().Unix())

如果在同一次执行中多次调用,返回的结果是不一样的:

比如这个代码:

复制代码
  
```go
package main

import "fmt"
  
import "math/rand"

func main() {
  fmt.Println(rand.Intn(100))
  fmt.Println(rand.Intn(100))
  fmt.Println(rand.Intn(100))
  fmt.Println(rand.Intn(100))
}
```

### 随机数 bytes

```go
package main

import (
    "fmt"
    "math/rand"
)

func main() {
    bytes := make([]byte, 5)
    rand.Read(bytes)
    fmt.Println(bytes)
}
```
