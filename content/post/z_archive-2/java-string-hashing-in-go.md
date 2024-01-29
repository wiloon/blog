---
title: Java string hashing in Go
author: "-"
date: 2018-01-31T08:44:45+00:00
url: /?p=11810
categories:
  - Inbox
tags:
  - reprint
---
## Java string hashing in Go
https://www.manniwood.com/2016_03_20/fun_with_java_string_hashing.html

```go
  
func ActualHash(s string) int32 {
      
var h int32
      
for i := 0; i < len(s); i++ {
          
h = 31*h + int32(s[i])
      
}
      
return h
  
}
  
```