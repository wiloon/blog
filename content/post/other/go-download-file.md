---
title: golang download file
author: "-"
date: 2014-03-07T06:28:42+00:00
url: /?p=6358
categories:
  - Uncategorized
tags:
  - Jboss

---
## golang download file
http://www.open-open.com/code/view/1440512102513

```java
  
package main 

import (
          
"fmt"
          
"io"
          
"net/http"
          
"os"
      
) 

var (
          
url = "http://127.0.0.1:1789/src/qq.exe"
      
) 

func main() {
          
res, err := http.Get(url)
          
if err != nil {
              
panic(err)
          
}
          
f, err := os.Create("qq.exe")
          
if err != nil {
              
panic(err)
          
}
          
io.Copy(f, res.Body)
      
}
  
```