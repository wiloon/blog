---
title: Golang， Signal
author: w1100n
type: post
date: 2020-02-24T03:41:55+00:00
url: /?p=15626
categories:
  - Uncategorized

---
https://colobu.com/2015/10/09/Linux-Signals/
信号(Signal)是Linux, 类Unix和其它POSIX兼容的操作系统中用来进程间通讯的一种方式。一个信号就是一个异步的通知，发送给某个进程，或者同进程的某个线程，告诉它们某个事件发生了。
当信号发送到某个进程中时，操作系统会中断该进程的正常流程，并进入相应的信号处理函数执行操作，完成后再回到中断的地方继续执行。
如果目标进程先前注册了某个信号的处理程序(signal handler),则此处理程序会被调用，否则缺省的处理程序被调用。

```golang
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