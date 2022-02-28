---
title: go channel
author: "-"
date: 2017-11-09T06:11:50+00:00
url: channel
categories:
  - golang
tags:
  - reprint
---
## go channel

channel 是 Go 中的一个核心类型, 你可以把它看成一个管道, 通过它并发核心单元就可以发送或者接收数据进行通讯。

```golang
<-      // channel 的操作符是箭头
ch <- v     // 发送值 v 到 Channel ch 中
v := <-ch   // 从 Channel c h中接收数据, 并将数据赋值给 v
            // (箭头的指向就是数据的流向)

// channel 定义
var dataChan <-chan []byte

// channel 初始化, 初始化之后才能使用
dataChan = make(<-chan []byte)
```

就像 map 和 slice 数据类型一样, channel必须先创建再使用

```golang
// 创建 channel
make (chan type)
make (chan type,N) //表示该channel自带N个type类型大小的buffer,只有该chan满/空时，调用方才会被阻塞
ch := make(chan int)

// 使用make初始化Channel,并且可以设置容量:
make(chan int, 100)
```

### for 可以处理channel

```golang
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


### 使用chan struct{}作为信号channel
场景：使用channel传递信号，而不是传递数据时
原理：没数据需要传递时，传递空struct
用法：
```go
// 上例中的Handler.stopCh就是一个例子，stopCh并不需要传递任何数据
// 只是要给所有协程发送退出的信号
type Handler struct {
    stopCh chan struct{}
    reqCh chan *Request
}

```

通常struct{}类型channel的用法是使用同步，一般不需要往channel里面写数据，只有读等待，而读等待会在channel被关闭的时候返回。


往chann struct{}写入数据
另一个问题，我们能不能往struct{}类型的channel里面写数据呢，答案当然也是可以的。

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
在foo()入口处给ch赋了一个值
注意写法是"struct{}{}"，第一个"{}"对表示类型，第二个"{}"对表示一个类型对象实例。

作者：CodingCode
链接：https://www.jianshu.com/p/7f45d7989f3a
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

