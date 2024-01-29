---
title: "golang 正则"
author: "-"
date: ""
url: ""
categories:
  - Go
tags:
  - regex
---
## "golang 正则"

https://studygolang.com/articles/7256

    func main() {
        fmt.Println(regexp.Match("H.* ", []byte("Hello World!")))
        // true 
    }
