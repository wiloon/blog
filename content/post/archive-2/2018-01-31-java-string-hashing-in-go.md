---
title: Java string hashing in Go
author: wiloon
type: post
date: 2018-01-31T08:44:45+00:00
url: /?p=11810
categories:
  - Uncategorized

---
https://www.manniwood.com/2016\_03\_20/fun\_with\_java\_string\_hashing.html

```java
  
func ActualHash(s string) int32 {
      
var h int32
      
for i := 0; i < len(s); i++ {
          
h = 31*h + int32(s[i])
      
}
      
return h
  
}
  
```