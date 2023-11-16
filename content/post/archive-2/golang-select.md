---
title: golang select
author: "-"
date: 2017-11-17T08:37:36+00:00
url: go/select
categories:
  - Go
tags:
  - reprint
---
## golang select

```go
package main

import (
 "fmt"
 "time"
)

func main() {
 fmt.Println("selectx")

 ch0 := make(chan struct{})
 ch1 := make(chan struct{})

 go func() {
  for {
   select {
   case v0 := <-ch0:
    fmt.Println("ch0: ", v0)
   case v1 := <-ch1:
    fmt.Println("ch1: ", v1)
   }
  }
 }()

 time.Sleep(1 * time.Second)

 ch0 <- struct{}{}
 ch1 <- struct{}{}
 ch0 <- struct{}{}
 ch1 <- struct{}{}
 ch1 <- struct{}{}
 ch1 <- struct{}{}
 time.Sleep(3 * time.Second)
 fmt.Println("selectx end")
}

// output:
// ch0:  {}
// ch1:  {}
// ch0:  {}
// ch1:  {}
// ch1:  {}
// ch1:  {}
```

代码执行到 select 时默认会阻塞, 直到任意一个 case 评估通过, 如果有多个 case 符合执行条件就从里面随机选一个执行.

- 除 default 外, 如果只有一个 case 语句评估通过, 那么就执行这个 case 里的语句；
- 除 default 外, 如果有多个 case 语句评估通过, 那么通过伪随机的方式随机选一个；
- 如果 default 外的 case 语句都没有通过评估, 那么执行 default 里的语句；
- 如果没有 default, 那么代码块会被阻塞, 直到有一个 case 通过评估；否则一直阻塞
- 如果 case 语句中 的 receive 操作的对象是 nil channel, 那么也会阻塞

[https://yanyiwu.com/work/2014/11/08/golang-select-typical-usage.html](https://yanyiwu.com/work/2014/11/08/golang-select-typical-usage.html)

golang 的 select 的功能和 select, poll, epoll 相似, 就是监听 IO 操作, 当 IO 操作发生时, 触发相应的动作。

示例:

```go
ch1 := make (chan int, 1)
  
ch2 := make (chan int, 1)

// ...

select {
case <-ch1:
  fmt.Println("ch1 pop one element")
  
case <-ch2:
  fmt.Println("ch2 pop one element")
}
```
  
注意到 select 的代码形式和 switch 非常相似, 不过 select 的 case 里的操作语句只能是 **IO 操作**

此示例里面 select 会一直等待等到某个 case 语句完成, 也就是等到成功从 ch1 或者 ch2 中读到数据。 则 select 语句结束

【使用 select 实现 timeout 机制】

如下:

```go
timeout := make (chan bool, 1)
  
go func() {
      
time.Sleep(1e9) // sleep one second
      
timeout <- true
  
}()
  
ch := make (chan int)
  
select {
  
case <- ch:
  
case <- timeout:
      
fmt.Println("timeout!")
  
}
```
  
当超时时间到的时候,case2 会操作成功。 所以 select 语句则会退出。 而不是一直阻塞在 ch 的读取操作上。 从而实现了对 ch 读取操作的超时设置。

下面这个更有意思一点。

当 select 语句带有 default 的时候:

```go
ch1 := make (chan int, 1)
  
ch2 := make (chan int, 1)

select {
  
case <-ch1:
      
fmt.Println("ch1 pop one element")
  
case <-ch2:
      
fmt.Println("ch2 pop one element")
  
default:
      
fmt.Println("default")
  
}
```
  
此时因为 ch1 和 ch2 都为空,所以 case1 和 case2 都不会读取成功。 则 select 执行 default 语句。

就是因为这个 default 特性, 我们可以使用 select 语句来检测 chan 是否已经满了。

如下:

```go
ch := make (chan int, 1)
ch <- 1
  
select {
  case ch <- 2:
  default:
    fmt.Println("channel is full !")
}
```
  
因为 ch 插入 1 的时候已经满了, 当 ch 要插入 2 的时候,发现 ch 已经满了 (case1 阻塞住) , 则 select 执行 default 语句。 这样就可以实现对 channel 是否已满的检测, 而不是一直等待。

比如我们有一个服务, 当请求进来的时候我们会生成一个 job 扔进 channel, 由其他协程从 channel 中获取 job 去执行。 但是我们希望当 channel 满了的时候, 将该 job 抛弃并回复 【服务繁忙,请稍微再试。】 就可以用 select 实现该需求。

[https://segmentfault.com/a/1190000006815341](https://segmentfault.com/a/1190000006815341)

[https://talks.golang.org/2012/concurrency.slide#32](https://talks.golang.org/2012/concurrency.slide#32)
