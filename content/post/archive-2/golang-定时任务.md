---
title: golang 定时器, timer, ticker
author: "-"
date: 2017-09-10T07:20:58.000+00:00
url: "go/ticker"
categories:
  - Go
tags:
  - timer
---
## golang 定时器, timer, ticker

Go 可以借助 time.After/time.Ticker 来实现延迟/定时触发器, 主要原理是借助无缓冲 channel 无数据时读取操作会阻塞当前协程, Go 会在给定的时间后向 channel 中写入一些数据 (当前时间), 故阻塞的协程可以恢复运行, 达到延迟或定时执行的功能。

## time.Ticker

ticker 只要定义完成,从此刻开始计时, 不需要任何其他的操作, 每隔固定时间都会触发。

```go
ticker := time.NewTicker(500 * time.Millisecond)
go func() {
    for t := range ticker.C {
    fmt.Println("Tick at", t)
    }
}()
```

### 立即执行一次

```go
ticker := time.NewTicker(period)
for ; true; <-ticker.C {
    // ...
}
```

### timer

使用timer定时器,超时后需要重置,才能继续触发。

```go
d := time.Duration(time.Second*2)

    t := time.NewTimer(d)
    defer t.Stop()

    for {
            <- t.C

            fmt.Println("timeout...")
    // need reset
    t.Reset(time.Second*2)
    }
```

### 执行若干次后退出

```go
func main() {
    // 创建一个计时器
    timeTicker := time.NewTicker(time.Second * 2)
    i := 0
    for {
        if i > 5 {
            break
        }

        fmt.Println(time.Now().Format("2006-01-02 15:04:05"))
        i++
        <-timeTicker.C
    }
    // 清理计时器
    timeTicker.Stop()
}
```

<https://my.oschina.net/u/943306/blog/149395>

### After函数 time.After(time.Duration)

和Sleep差不多,意思是多少时间之后,但在取出管道内容前不阻塞

fmt.Println("the 1")

tc:=time.After(time.Second) //返回一个time.C这个管道,1秒(time.Second)后会在此管道中放入一个时间点(time.Now())

//时间点记录的是放入管道那一刻的时间值

fmt.Println("the 2")

fmt.Println("the 3")

<-tc //阻塞中,直到取出tc管道里的数据

fmt.Println("the 4")

//【结果】立即打印123,等了1秒不到一点点的时间,打印了4,结束

//打印the 1后,获得了一个空管道,这个管道1秒后会有数据进来

//打印the 2, (这里可以做更多事情)

//打印the 3

//等待,直到可以取出管道的数据 (取出数据的时间与获得tc管道的时间正好差1秒钟)

//打印the 4

<http://www.jianshu.com/p/8fd62c805ee5>

Go有一个package名字叫time,通过这个package可以很容易的实现与时间有关的操作。time package中有一个ticker结构,可以实现定时任务。

import "time"

ticker := time.NewTicker(time.Minute * 1)

go func() {

for _ = range ticker.C {

fmt.Printf("ticked at %v", time.Now())

}

}()

上面的打印方法会每隔一分钟把当前时间打印出来。修改间隔时间和要执行的函数,就能实现你需要的定时任务。

作者: 蓝色信仰

链接: <http://www.jianshu.com/p/8fd62c805ee5>

來源: 简书

著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

<https://github.com/golang/go/issues/17601>

<https://blog.csdn.net/lanyang123456/article/details/79794183>
