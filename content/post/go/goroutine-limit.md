---
title: 控制协程(goroutine)的并发数量
author: "-"
date: 2011-10-31T09:13:20+00:00
url: goroutine/limit
categories:
  - Go
tags:
  - reprint
---
## 控制协程(goroutine)的并发数量

### ants
>https://github.com/panjf2000/ants/blob/master/README_ZH.md


利用 channel 的缓存区
可以利用信道 channel 的缓冲区大小来实现：

 
```go
// main_chan.go
func main() {
    var wg sync.WaitGroup
    ch := make(chan struct{}, 3)
    for i := 0; i < 10; i++ {
        ch <- struct{}{}
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            log.Println(i)
            time.Sleep(time.Second)
            <-ch
        }(i)
    }
    wg.Wait()
}
```

>https://geektutu.com/post/hpg-concurrency-control.html
