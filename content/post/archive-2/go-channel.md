---
title: go channel
author: "-"
date: 2017-11-09T06:11:50+00:00
url: go/channel
categories:
  - Go
tags:
  - reprint
---
## go channel

channel 是 Go 中的一个核心类型, 可以把它看成一个管道, 通过它并发核心单元就可以发送或者接收数据进行通讯。

goroutine 是 Go 语言的基本调度单位, 而 channels 则是它们之间的通信机制。操作符 `<-` 用来指定管道的方向，发送或接收。如果未指定方向，则为双向管道。

golang 的 channel 就是一个 **环形队列/ringbuffer** 的实现。 我们称 chan 为管理结构，channel 里面可以放任何类型的对象，我们称之为元素。

## Channel 定义

```bash
ChannelType = ( "chan" | "chan<-" | "<-chan" ) ElementType .
```

可选的`<-`代表 channel 的方向(是数据的流向)。如果没有指定方向，那么 Channel 就是双向的，既可以接收数据，也可以发送数据。

```go
<-          // channel 的操作符
ch <- v     // 发送值 v 到 Channel ch 中
v := <-ch   // 从 Channel ch 中接收数据, 并将数据赋值给 v



var foo chan T        // 可以接收和发送类型为 T 的数据
var foo chan<- float64  // 只可以用来发送 float64 类型的数据
var foo <-chan int      // 只可以用来接收 int 类型的数据
// <-总是优先和最左边的类型结合。(The <- operator associates with the leftmost chan possible)

chan<- chan int    // 等价 chan<- (chan int)
chan<- <-chan int  // 等价 chan<- (<-chan int)
<-chan <-chan int  // 等价 <-chan (<-chan int)
chan (<-chan int)

// channel 定义
var dataChan <-chan []byte

// 使用 make 初始化 Channel, 并且可以设置容量, channel 初始化, 初始化之后才能使用
// 未设置容量的channel, 如果没有设置容量，或者容量设置为0, 说明Channel没有缓存，只有sender和receiver都准备好了后它们的通讯
// 无缓冲的channel由于没有缓冲发送和接收需要同步.
// channel无缓冲时，发送阻塞直到数据被接收，接收阻塞直到读到数据。
dataChan := make(<-chan []byte)
// 容量为100的 channel
ch := make(chan int, 100)
// 容量(capacity)代表Channel容纳的最多的元素的数量，代表Channel的缓存的大小。

// 创建一个双向channel, interface{}表示chan可以为任何类型
foo := make(chan interface{})

// 可以通过内建的close方法可以关闭Channel。
close(foo)

// channel的 receive支持 multi-valued assignment，如
v, ok := <-ch
```

往一个已经被close的channel中继续发送数据会导致run-time panic。

往nil channel中发送数据会一致被阻塞着。

从一个nil channel中接收数据会一直被block。

从一个被close的channel中接收数据不会被阻塞，而是立即返回，返回值是channel里的元素类型的零值(zero value, int:0, string:"", float:0)。

channel 有发送和接受两个主要操作。发送和接收两个操作都使用`<-`运算符。在发送语句中，channel 放`<-`运算符左边。在接收语句中，channel放`<-`运算符右边。一个不使用接收结果的接收操作也是合法的。

```go
// 发送操作
ch <- x 
// 接收操作
x = <-ch 
// 忽略接收到的值，合法
<-ch     
```

就像 map 和 slice 数据类型一样, channel 必须先创建再使用

```go
// 创建 channel
make (chan type)
make (chan type,N) //表示该channel自带N个type类型大小的buffer,只有该chan满/空时，调用方才会被阻塞
ch := make(chan int)

// 使用make初始化Channel,并且可以设置容量:
make(chan int, 100)
```

### for 可以处理 channel

```go
for i := range c {
        fmt.Println(i)
    }
```

receive 操作符
  
<-ch 用来从 channel ch 中接收数据,这个表达式会一直被 block, 直到有数据可以接收。
  
从一个 nil channel 中接收数据会一直被block。

从一个被 close 的 channel 中接收数据不会被阻塞,而是立即返回,接收完已发送的数据后会返回元素类型的零值(zero value)。

如前所述,你可以使用一个额外的返回参数来检查channel是否关闭。

<http://colobu.com/2016/04/14/Golang-Channels/>

### 使用 chan struct{} 作为信号 channel

场景：使用channel 传递信号，而不是传递数据时
原理：没数据需要传递时，传递空struct
用法：

```go
// 上例中的 Handler.stopCh 就是一个例子，
// stopCh 并不需要传递任何数据, 只是要给所有协程发送退出的信号
type Handler struct {
    stopCh chan struct{}
    reqCh chan *Request
}
```

通常 struct{} 类型 channel的用法是使用同步，一般不需要往channel里面写数据，只有读等待，而读等待会在channel被关闭的时候返回。

往chann struct{}写入数据
另一个问题，我们能不能往struct{}类型的channel里面写数据呢，答案当然也是可以的。

```go
package main

import (
    "time"
    "log"
)

var ch chan struct{} = make(chan struct{})

func foo() {
    ch <- struct{}{}
    log.Println("foo() 111");
    time.Sleep(5 * time.Second)
    log.Println("foo() 222");
    close(ch)
    log.Println("foo() 333");
}

func main() {

    log.Println("main() 111");
    go foo()
    log.Println("main() 222");
    <-ch
    log.Println("main() 333");
}
```

在foo()入口处给ch赋了一个值
注意写法是"struct{}{}"，第一个"{}"对表示类型，第二个"{}"对表示一个类型对象实例。

作者：CodingCode
链接：<https://www.jianshu.com/p/7f45d7989f3a>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

><https://segmentfault.com/a/1190000017958702>
如前所述,你可以使用一个额外的返回参数来检查channel是否关闭。

><https://www.jianshu.com/p/d24dfbb33781>
><https://go101.org/article/channel-closing.html>

关闭channel
Channel支持close操作，用于关闭channel，后面对该channel的任何发送操作都将导致panic异常。对一个已经被close过的channel进行接收操作依然可以接受到之前已经成功发送的数据；如果channel中已经没有数据的话将产生一个零值的数据。
从已经关闭的channel中读：
intStream := make(chan int)
close(intStream)
integer, ok := <- intStream
fmt.Pritf("(%v): %v", ok, integer)
// (false): 0
复制代码上面例子中通过返回值ok来判断channel是否关闭，我们还可以通过range这种更优雅的方式来处理已经关闭的channel：
intStream := make(chan int)
go func() {
    defer close(intStream)
    for i:=1; i<=5; i++{
        intStream <- i
    }
}()

for integer := range intStream {
    fmt.Printf("%v ", integer)
}
// 1 2 3 4 5

作者：彬叔
链接：<https://juejin.cn/post/6844903623667744781>
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

><https://colobu.com/2016/04/14/Golang-Channels/>
><https://zhuanlan.zhihu.com/p/299592156>
