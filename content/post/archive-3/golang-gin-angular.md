---
title: golang gin
author: "-"
date: 2019-05-25T03:19:59+00:00
url: /?p=14413
categories:
  - Inbox
tags:
  - reprint
---
## golang gin
### 重定向
https://www.cnblogs.com/zisefeizhu/p/12739223.html

    package main

    import (
      "github.com/gin-gonic/gin"
      "net/http"
    )

    func main() {
      r := gin.Default()
      //http重定向
      r.GET("/index", func(c *gin.Context) {
        //c.JSON(http.StatusOK, gin.H{
        //    "status": "ok",
        //})
        //跳转到sogo
        c.Redirect(http.StatusMovedPermanently, "https://www.sogo.com")
      })

      //路由重定向
      r.GET("/luyou", func(c *gin.Context) {
        //跳转到/luyou2对应的路由处理函数
        c.Request.URL.Path = "/luyou2"  //把请求的URL修改
        r.HandleContext(c)  //继续后续处理
      })
      r.GET("/luyou2", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
          "message":"路由重定向",
        })
      })
      r.Run(":9090")
    }