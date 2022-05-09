---
title: go handle handleFunction
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=11589
categories:
  - Inbox
tags:
  - reprint
---
## go handle handleFunction

  
    Go语言的"http.Handle"和"http.HandleFunc"
  


https://nanxiao.me/golang-http-handle-handlefunc/embed/#?secret=WkvqrIWZ2A

```java
  
// Handle
  
package main
  
import (
      
"net/http"
      
"log"
  
)

type httpServer struct {
  
}

func (server httpServer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
      
w.Write([]byte(r.URL.Path))
  
}

func main() {
      
var server httpServer
      
http.Handle("/", server)
      
log.Fatal(http.ListenAndServe("localhost:9000", nil))
  
}
  
```

[code lang=text]
  
// HandleFunc: 
  
package main
  
import (
      
"net/http"
      
"log"
  
)

func main() {
      
http.HandleFunc("/", func (w http.ResponseWriter, r *http.Request){
          
w.Write([]byte(r.URL.Path))
      
})
      
log.Fatal(http.ListenAndServe("localhost:9000", nil))
  
}
  
```