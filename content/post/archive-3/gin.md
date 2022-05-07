---
title: gin
author: "-"
date: 2019-05-23T13:31:30+00:00
url: /?p=14394
categories:
  - Inbox
tags:
  - reprint
---
## gin
https://github.com/gin-gonic/gin#quick-start

```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

func main() {
    router := gin.Default()
    router.GET("/path0", func(c *gin.Context) {
        firstname := c.DefaultQuery("params0", "Guest")
        lastname := c.Query("params1") // shortcut for c.Request.URL.Query().Get("lastname")

        c.String(http.StatusOK, "Hello %s %s", firstname, lastname)
    })
    router.Run(":8080")
}
```