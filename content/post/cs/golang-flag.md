---
title: golang flag 获取命令行参数
author: "-"
date: 2016-07-01T07:00:04+00:00
url: /?p=9093
categories:
  - Inbox
tags:
  - Go

---
## golang flag 获取命令行参数

```java
flag.String("port", ":8080", "http listen port")
```

像flag.Int、flag.Bool、flag.String这样的函数格式都是一样的,第一个参数表示参数名称,第二个参数表示默认值,第三个参数表示使用说明和描述。flag.StringVar这样的函数第一个参数换成了变量地址,后面的参数和flag.String是一样的。

flag.Parse()

解析函数将会在碰到第一个非 flag 命令行参数时停止,非flag命令行参数是指不满足命令行语法的参数,如命令行参数为cmd -flag=true abc 则第一个非 flag 命令行参数为 "abc"

使用flag来操作命令行参数,支持的格式如下:

```bash
-id=1
--id=1
-id 1
--id 1
```

```go
package main
import (
"flag"
"fmt"
)

func main() {
    ok := flag.Bool("ok", false, "is ok")
    id := flag.Int("id", 0, "id")
    port := flag.String("port", ":8080", "http listen port")
    var name string
    flag.StringVar(&name, "name", "123", "name")

    flag.Parse()

    fmt.Println("ok:", *ok)
    fmt.Println("id:", *id)
    fmt.Println("port:", *port)
    fmt.Println("name:", name)
}
```

还是非常方便的。

执行一下:

$ go run flag.go -id=2 -name="golang"
  
ok: false
  
id: 2
  
port: :8080
  
name: golang

使用-h参数可以查看使用帮助:

$ go run flag.go -h
  
-id=0: id
  
-name="123″: name
  
-ok=false: is ok
  
-port=":8080″: http listen port

[http://www.01happy.com/golang-command-line-arguments/](http://www.01happy.com/golang-command-line-arguments/)
  
[http://faberliu.github.io/2014/11/12/Golang-flag%E5%8C%85%E4%BD%BF%E7%94%A8%E8%AF%A6%E8%A7%A3-%E4%B8%80/](http://faberliu.github.io/2014/11/12/Golang-flag%E5%8C%85%E4%BD%BF%E7%94%A8%E8%AF%A6%E8%A7%A3-%E4%B8%80/)
