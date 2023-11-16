---
title: Golang runtime
author: "-"
date: 2017-09-11T05:01:44+00:00
url: /?p=11160
categories:
  - Inbox
tags:
  - reprint
---
## Golang runtime

[http://www.jianshu.com/p/e45cea3e1723](http://www.jianshu.com/p/e45cea3e1723)

runtime 调度器是个非常有用的东西,关于 runtime 包几个方法:

Gosched: 让当前线程让出 cpu 以让其它线程运行,它不会挂起当前线程,因此当前线程未来会继续执行

NumCPU: 返回当前系统的 CPU 核数量

GOMAXPROCS: 设置最大的可同时使用的 CPU 核数

Goexit: 退出当前 goroutine(但是defer语句会照常执行)

NumGoroutine: 返回正在执行和排队的任务总数

GOOS: 目标操作系统

NumCPU

package main

import (

"fmt"

"runtime"
  
)

func main() {

fmt.Println("cpus:", runtime.NumCPU())

fmt.Println("goroot:", runtime.GOROOT())

fmt.Println("archive:", runtime.GOOS)
  
}
  
运行结果:

GOMAXPROCS

Golang 默认所有任务都运行在一个 cpu 核里,如果要在 goroutine 中使用多核,可以使用 runtime.GOMAXPROCS 函数修改,当参数小于 1 时使用默认值。

package main

import (

"fmt"

"runtime"
  
)

func init() {

runtime.GOMAXPROCS(1)
  
}

func main() {

// 任务逻辑...

}
  
Gosched

这个函数的作用是让当前 goroutine 让出 CPU,当一个 goroutine 发生阻塞,Go 会自动地把与该 goroutine 处于同一系统线程的其他 goroutine 转移到另一个系统线程上去,以使这些 goroutine 不阻塞

package main

import (

"fmt"

"runtime"
  
)

func init() {

runtime.GOMAXPROCS(1) //使用单核
  
}

func main() {

exit := make(chan int)

go func() {

defer close(exit)

go func() {

fmt.Println("b")

}()

}()

    for i := 0; i < 4; i++ {
        fmt.Println("a:", i)
    
        if i == 1 {
            runtime.Gosched()  //切换任务
        }
    }
    <-exit

}
  
结果:

使用多核测试:

package main

import (

"fmt"

"runtime"
  
)

func init() {

runtime.GOMAXPROCS(4) //使用多核
  
}

func main() {

exit := make(chan int)

go func() {

defer close(exit)

go func() {

fmt.Println("b")

}()

}()

    for i := 0; i < 4; i++ {
        fmt.Println("a:", i)
    
        if i == 1 {
            runtime.Gosched()  //切换任务
        }
    }
    <-exit

}
  
结果:

根据你机器来设定运行时的核数,但是运行结果不一定与上面相同,或者在 main 函数的最后加上 select{} 让程序阻塞,则结果如下:

多核比较适合那种 CPU 密集型程序,如果是 IO 密集型使用多核会增加 CPU 切换的成本。
