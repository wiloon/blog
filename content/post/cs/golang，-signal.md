---
title: Golang，Signal
author: "-"
date: 2020-02-24T03:41:55+00:00
url: /?p=15626
categories:
  - Go
tags:
  - reprint
---
## Golang，Signal

https://colobu.com/2015/10/09/Linux-Signals/
信号(Signal)是Linux, 类Unix和其它POSIX兼容的操作系统中用来进程间通讯的一种方式。一个信号就是一个异步的通知，发送给某个进程，或者同进程的某个线程，告诉它们某个事件发生了。
当信号发送到某个进程中时，操作系统会中断该进程的正常流程，并进入相应的信号处理函数执行操作，完成后再回到中断的地方继续执行。
如果目标进程先前注册了某个信号的处理程序(signal handler),则此处理程序会被调用，否则缺省的处理程序被调用。

```go
signals := make(chan os.Signal)
  signal.Notify(signals, os.Interrupt, os.Kill, syscall.SIGTERM)
  // ...
      for s := range signals {
        if s == os.Interrupt || s == os.Kill || s == syscall.SIGTERM {
            break
        }
    }
    signal.Stop(signals)
```


Go中的Signal发送和处理
有时候我们想在Go程序中处理Signal信号，比如收到SIGTERM信号后优雅的关闭程序(参看下一节的应用)。
Go信号通知机制可以通过往一个channel中发送os.Signal实现。
首先我们创建一个os.Signal channel，然后使用signal.Notify注册要接收的信号。

package main
import "fmt"
import "os"
import "os/signal"
import "syscall"
func main() {
    // Go signal notification works by sending `os.Signal`
    // values on a channel. We'll create a channel to
    // receive these notifications (we'll also make one to
    // notify us when the program can exit).
    sigs := make(chan os.Signal, 1)
    done := make(chan bool, 1)
    // `signal.Notify` registers the given channel to
    // receive notifications of the specified signals.
    signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
    // This goroutine executes a blocking receive for
    // signals. When it gets one it'll print it out
    // and then notify the program that it can finish.
    go func() {
        sig := <-sigs
        fmt.Println()
        fmt.Println(sig)
        done <- true
    }()
    // The program will wait here until it gets the
    // expected signal (as indicated by the goroutine
    // above sending a value on `done`) and then exit.
    fmt.Println("awaiting signal")
    <-done
    fmt.Println("exiting")
}
go run main.go执行这个程序，敲入ctrl-C会发送SIGINT信号。 此程序接收到这个信号后会打印退出。

Go网络服务器如果无缝重启
Go很适合编写服务器端的网络程序。DevOps经常会遇到的一个情况是升级系统或者重新加载配置文件，在这种情况下我们需要重启此网络程序，如果网络程序暂停的时间较长，则给客户的感觉很不好。
如何实现优雅地重启一个Go网络程序呢。主要要解决两个问题: 

进程重启不需要关闭监听的端口
既有请求应当完全处理或者超时
@humblehack 在他的文章Graceful Restart in Golang中提供了一种方式，而Florian von Bock根据此思路实现了一个框架endless。
此框架使用起来超级简单:

err := endless.ListenAndServe("localhost:4242", mux)
只需替换 http.ListenAndServe 和 http.ListenAndServeTLS。

它会监听这些信号:  syscall.SIGHUP, syscall.SIGUSR1, syscall.SIGUSR2, syscall.SIGINT, syscall.SIGTERM, 和 syscall.SIGTSTP。

此文章提到的思路是: 

通过exec.Command fork一个新的进程，同时继承当前进程的打开的文件(输入输出，socket等)

file := netListener.File() // this returns a Dup()
path := "/path/to/executable"
args := []string{
    "-graceful"}
cmd := exec.Command(path, args...)
cmd.Stdout = os.Stdout
cmd.Stderr = os.Stderr
cmd.ExtraFiles = []*os.File{file}
err := cmd.Start()
if err != nil {
    log.Fatalf("gracefulRestart: Failed to launch, error: %v", err)
}
子进程初始化
网络程序的启动代码

server := &http.Server{Addr: "0.0.0.0:8888"}
 var gracefulChild bool
 var l net.Listever
 var err error
 flag.BoolVar(&gracefulChild, "graceful", false, "listen on fd open 3 (internal use only)")
 if gracefulChild {
     log.Print("main: Listening to existing file descriptor 3.")
     f := os.NewFile(3, "")
     l, err = net.FileListener(f)
 } else {
     log.Print("main: Listening on a new file descriptor.")
     l, err = net.Listen("tcp", server.Addr)
 }
父进程停止

if gracefulChild {
    parent := syscall.Getppid()
    log.Printf("main: Killing parent pid: %v", parent)
    syscall.Kill(parent, syscall.SIGTERM)
}
server.Serve(l)
同时他还提供的如何处理已经正在处理的请求。可以查看它的文章了解详细情况。

因此，处理特定的信号可以实现程序无缝的重启。

其它
graceful shutdown实现非常的简单，通过简单的信号处理就可以实现。本文介绍的是graceful restart,要求无缝重启，所以所用的技术相当的hack。

Facebook的工程师也提供了http和net的实现:  facebookgo。

参考资料
https://en.wikipedia.org/wiki/Unix_signal
http://hutaow.com/blog/2013/10/19/linux-signal/
http://www.ucs.cam.ac.uk/docs/course-notes/unix-courses/Building/files/signals.pdf
https://golang.org/pkg/os/signal/
https://gobyexample.com/signals
http://grisha.org/blog/2014/06/03/graceful-restart-in-golang/
https://fitstar.github.io/falcore/hot_restart.html
https://github.com/rcrowley/goagain




---

https://colobu.com/2015/10/09/Linux-Signals/
