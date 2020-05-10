---
title: 如何优雅地等待所有的goroutine退出
author: wiloon
type: post
date: 2016-10-12T07:10:06+00:00
url: /?p=9291
categories:
  - Uncategorized

---
http://www.cnblogs.com/cobbliu/p/4461866.html

Table of Contents
  
1. 通过Channel传递退出信号
  
2. 使用waitgroup
  
goroutine和channel是Go语言非常棒的特色，它们提供了一种非常轻便易用的并发能力。但是当您的应用进程中有很多goroutine的时候，如何在主流程中等待所有的goroutine 退出呢？

通过Channel传递退出信号
  
Go的一大设计哲学就是：通过Channel共享数据，而不是通过共享内存共享数据。主流程可以通过channel向任何goroutine发送停止信号，就像下面这样：

func run(done chan int) {
  
for {
  
select {
  
case <-done:
  
fmt.Println(“exiting…”)
  
done <- 1
  
break
  
default:
  
}

time.Sleep(time.Second * 1)
  
fmt.Println(“do something”)
  
}
  
}

func main() {
  
c := make(chan int)

go run(c)

fmt.Println(“wait”)
  
time.Sleep(time.Second * 5)

c <- 1
  
<-c

fmt.Println(“main exited”)
  
}

这种方式可以实现优雅地停止goroutine，但是当goroutine特别多的时候，这种方式不管在代码美观上还是管理上都显得笨拙不堪。
  
2 使用waitgroup
  
sync包中的Waitgroup结构，是Go语言为我们提供的多个goroutine之间同步的好刀。下面是官方文档对它的描述：

A WaitGroup waits for a collection of goroutines to finish. The main goroutine calls Add to set the number of goroutines to wait for.
  
Then each of the goroutines runs and calls Done when finished. At the same time, Wait can be used to block until all goroutines have finished.

通常情况下，我们像下面这样使用waitgroup:

创建一个Waitgroup的实例，假设此处我们叫它wg
  
在每个goroutine启动的时候，调用wg.Add(1)，这个操作可以在goroutine启动之前调用，也可以在goroutine里面调用。当然，也可以在创建n个goroutine前调用wg.Add(n)
  
当每个goroutine完成任务后，调用wg.Done()
  
在等待所有goroutine的地方调用wg.Wait()，它在所有执行了wg.Add(1)的goroutine都调用完wg.Done()前阻塞，当所有goroutine都调用完wg.Done()之后它会返回。
  
那么，如果我们的goroutine是一匹不知疲倦的牛，一直孜孜不倦地工作的话，如何在主流程中告知并等待它退出呢？像下面这样做：

type Service struct {
  
// Other things

ch chan bool
  
waitGroup *sync.WaitGroup
  
}

func NewService() *Service {
  
s := &Service{
  
// Init Other things
  
ch: make(chan bool),
  
waitGroup: &sync.WaitGroup{},
  
}

return s
  
}

func (s *Service) Stop() {
  
close(s.ch)
  
s.waitGroup.Wait()
  
}

func (s *Service) Serve() {
  
s.waitGroup.Add(1)
  
defer s.waitGroup.Done()

for {
  
select {
  
case <-s.ch:
  
fmt.Println(“stopping…”)
  
return
  
default:
  
}
  
s.waitGroup.Add(1)
  
go s.anotherServer()
  
}
  
}
  
func (s *Service) anotherServer() {
  
defer s.waitGroup.Done()
  
for {
  
select {
  
case <-s.ch:
  
fmt.Println(“stopping…”)
  
return
  
default:
  
}

// Do something
  
}
  
}

func main() {

service := NewService()
  
go service.Serve()

// Handle SIGINT and SIGTERM.
  
ch := make(chan os.Signal)
  
signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
  
fmt.Println(<-ch)

// Stop the service gracefully.
  
service.Stop()
  
}
  
是不是方便优雅多了？
  
Author: Cobbliu

Created: 2015-04-28 Tue 00:24