---
author: "w1100n"
date: "2020-07-08 10:58:34"
title: "golang 生成二维码"
categories:
  - inbox
tags:
  - reprint
---
## "golang 生成二维码"

        import "github.com/skip2/go-qrcode"

        func main() {
            qrcode.WriteFile("http://www.wiloon.com/",qrcode.Medium,256,"./blog_qrcode.png")
        }
