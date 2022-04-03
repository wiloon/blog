---
title: goroutine 退出, waitgroup, channel
author: "-"
date: 2016-10-12T07:10:06+00:00
url: goroutine/exit
categories:
  - Go
tags:
  - reprint
---
## 如何优雅地等待所有的 goroutine 退出

## WaitGroup

sync包中的 Waitgroup 结构,是Go语言为我们提供的多个goroutine之间同步的好刀。下面是官方文档对它的描述: 

A WaitGroup waits for a collection of goroutines to finish. The main goroutine calls Add to set the number of goroutines to wait for.
  
Then each of the goroutines runs and calls Done when finished. At the same time, Wait can be used to block until all goroutines have finished.

通常情况下,我们像下面这样使用waitgroup:

创建一个Waitgroup的实例,假设此处我们叫它wg
  
在每个goroutine启动的时候,调用wg.Add(1),这个操作可以在goroutine启动之前调用,也可以在goroutine里面调用。当然,也可以在创建n个goroutine前调用wg.Add(n)
  
当每个goroutine完成任务后,调用wg.Done()
  
在等待所有goroutine的地方调用wg.Wait(),它在所有执行了wg.Add(1)的goroutine都调用完wg.Done()前阻塞,当所有goroutine都调用完wg.Done()之后它会返回。

```go
import (
	"fmt"
	"sync"
	"time"
)

func main() {
	wg := &sync.WaitGroup{}

	wg.Add(1)
	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println("goroutine-0: ", i)
			time.Sleep(1 * time.Second)
		}
		wg.Done()
	}()

	go goroutine1(wg)
	wg.Wait()
}

func goroutine1(wg *sync.WaitGroup) {
	defer func() {
		wg.Done()
	}()
	for i := 0; i < 10; i++ {
		fmt.Println("goroutine-1: ", i)
		time.Sleep(1 * time.Second)
	}
}
```

### 通过 Channel 传递退出信号

goroutine 和 channel 是 Go 语言非常棒的特色,它们提供了一种非常轻便易用的并发能力。但是当您的应用进程中有很多goroutine的时候,如何在主流程中等待所有的 goroutine 退出呢？

通过 Channel 传递退出信号
  
Go 的一大设计哲学就是: 通过 Channel 共享数据, 而不是通过共享内存共享数据。主流程可以通过 channel 向任何 goroutine 发送停止信号, 就像下面这样
```go

func run(done chan int) {
  
for {
  
select {
  
case <-done:
  
fmt.Println("exiting…")
  
done <- 1
  
break
  
default:
  
}

time.Sleep(time.Second * 1)
  
fmt.Println("do something")
  
}
  
}

func main() {
  
c := make(chan int)

go run(c)

fmt.Println("wait")
  
time.Sleep(time.Second * 5)

c <- 1
  
<-c

fmt.Println("main exited")
  
}

```
这种方式可以实现优雅地停止goroutine,但是当goroutine特别多的时候,这种方式不管在代码美观上还是管理上都显得笨拙不堪。

>https://segmentfault.com/a/1190000037780837
>http://www.cnblogs.com/cobbliu/p/4461866.html

