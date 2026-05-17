---
title: golang WebAssembly
author: "-"
date: 2019-05-10T10:19:33+00:00
url: golang-webassembly
categories:
  - Inbox
tags:
  - reprint
aliases:
  - /p9287/
  - /p9903/
  - /p12719/
  - /p13910/
  - /p14254/
  - /p14322/
  - /p15099/
  - /p15113/
  - /p15626/
  - /p15683/
---
## golang WebAssembly

[https://github.com/golang/go/wiki/WebAssembly](https://github.com/golang/go/wiki/WebAssembly)
  
[https://tutorialedge.net/golang/go-webassembly-tutorial/](https://tutorialedge.net/golang/go-webassembly-tutorial/)

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, WebAssembly!")
}
```

```bash
gOOS=js GOARCH=wasm go build -o main.wasm
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" .
go get -u github.com/shurcooL/goexec
goexec 'http.ListenAndServe(":8080", http.FileServer(http.Dir(".")))'

```
