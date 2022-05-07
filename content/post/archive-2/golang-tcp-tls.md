---
title: golang tcp tls
author: "-"
date: 2019-01-05T04:39:54+00:00
url: /?p=13322
categories:
  - Inbox
tags:
  - reprint
---
## golang tcp tls
https://colobu.com/2016/06/07/simple-golang-tls-examples/

### 生成TLS证书

<http://blog.wiloon.com/?p=12962>

#### server

```go
package main

import (
    "bufio"
    "crypto/tls"
    "log"
    "net"
)

func main() {
    cert, err := tls.LoadX509KeyPair("certs/server.pem", "certs/server.key")
    if err != nil {
        log.Println(err)
        return
    }
    config := &tls.Config{Certificates: []tls.Certificate{cert}}

    address := ":8443"

    log.Println("listening: ", address)
    ln, err := tls.Listen("tcp", address, config)
    if err != nil {
        log.Println(err)
        return
    }
    defer ln.Close()

    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Println(err)
            continue
        }
        go handleConn(conn)
    }
}
func handleConn(conn net.Conn) {
    defer conn.Close()
    r := bufio.NewReader(conn)
    for {
        msg, err := r.ReadString('\n')
        if err != nil {
            log.Println(err)
            return
        }
        println(msg)
        n, err := conn.Write([]byte("world\n"))
        if err != nil {
            log.Println(n, err)
            return
        }
    }
}

```

#### client

```go
package main

import (
    "crypto/tls"
    "log"
)

func main() {
    conf := &tls.Config{
        InsecureSkipVerify: true,
    }
    conn, err := tls.Dial("tcp", "127.0.0.1:8443", conf)
    if err != nil {
        log.Println(err)
        return
    }
    defer conn.Close()
    n, err := conn.Write([]byte("hello\n"))
    if err != nil {
        log.Println(n, err)
        return
    }
    buf := make([]byte, 100)
    n, err = conn.Read(buf)
    if err != nil {
        log.Println(n, err)
        return
    }
    println(string(buf[:n]))
}

```