---
title: golang MP4文件服务器
author: "-"
date: 2019-09-27T14:23:16+00:00
url: /?p=14964
categories:
  - Inbox
tags:
  - reprint
---
## golang MP4 文件服务器

https://studygolang.com/articles/11204

```go
package main

import (
    "github.com/gorilla/handlers"
    "log"
    "net/http"
    "os"
    "time"
)

func ServeHTTP(w http.ResponseWriter, r *http.Request) {
    video, err := os.Open("/tmp/foo.mp4")
    if err != nil {
        log.Fatal(err)
    }
    defer video.Close()

    http.ServeContent(w, r, "foo.mp4", time.Now(), video)
}

func main() {
    http.HandleFunc("/", ServeHTTP)
    _ = http.ListenAndServe(":8089", handlers.LoggingHandler(os.Stdout, http.DefaultServeMux))
}

```