---
title: golang base64
author: "-"
date: 2019-03-21T03:15:11+00:00
url: /?p=13893
categories:
  - Inbox
tags:
  - reprint
---
## golang base64
http://www.01happy.com/golang-base64-encode-decode/

golang中base64编码和解码
   
Golang 3年前 (2016-08-05) 1011浏览 0评论
  
golang中base64的编码和解码可以用内置库encoding/base64

package main

import (
      
"encoding/base64"
      
"fmt"
      
"log"
  
)

func main() {
      
input := []byte("hello golang base64 快乐编程http://www.01happy.com +~")

    // 演示base64编码
    encodeString := base64.StdEncoding.EncodeToString(input)
    fmt.Println(encodeString)
    
    // 对上面的编码结果进行base64解码
    decodeBytes, err := base64.StdEncoding.DecodeString(encodeString)
    if err != nil {
        log.Fatalln(err)
    }
    fmt.Println(string(decodeBytes))
    
    fmt.Println()
    
    // 如果要用在url中，需要使用URLEncoding
    uEnc := base64.URLEncoding.EncodeToString([]byte(input))
    fmt.Println(uEnc)
    
    uDec, err := base64.URLEncoding.DecodeString(uEnc)
    if err != nil {
        log.Fatalln(err)
    }
    fmt.Println(string(uDec))
    

}
  
运行输出: 

go run encode.go
  
aGVsbG8gZ29sYW5nIGJhc2U2NCDlv6vkuZDnvJbnqItodHRwOi8vd3d3LjAxaGFwcHkuY29tICt+
  
hello golang base64 快乐编程http://www.01happy.com +~

aGVsbG8gZ29sYW5nIGJhc2U2NCDlv6vkuZDnvJbnqItodHRwOi8vd3d3LjAxaGFwcHkuY29tICt-
  
hello golang base64 快乐编程http://www.01happy.com +~