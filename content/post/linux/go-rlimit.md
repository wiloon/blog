---
title: go rlimit
author: "-"
date: 2012-01-17T07:47:08+00:00
url: /?p=2148
categories:
  - Linux
tags:
  - reprint
---
## go rlimit

```bash
package main

import (
    "fmt"
    "syscall"
)

func main() {
    var rLimit syscall.Rlimit
    err := syscall.Getrlimit(syscall.RLIMIT_NOFILE, &rLimit)
    if err != nil {
        fmt.Println("Error Getting Rlimit ", err)
    }
    fmt.Println(rLimit)
    rLimit.Max = 999999
    rLimit.Cur = 999999
    err = syscall.Setrlimit(syscall.RLIMIT_NOFILE, &rLimit)
    if err != nil {
        fmt.Println("Error Setting Rlimit ", err)
    }
    err = syscall.Getrlimit(syscall.RLIMIT_NOFILE, &rLimit)
    if err != nil {
        fmt.Println("Error Getting Rlimit ", err)
    }
    fmt.Println("Rlimit Final", rLimit)
}

```