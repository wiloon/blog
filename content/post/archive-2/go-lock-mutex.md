---
title: golang lock, sync.RWMutex, sync.Mutex, 锁
author: "-"
date: 2018-04-13T02:31:40+00:00
url: go/mutex
categories:
  - Go
tags:
  - reprint
  - lock
---
## golang lock, sync.RWMutex, sync.Mutex, 锁

在 Go 语言并发编程中，倡导**使用通信共享内存，不要使用共享内存通信**，而这个通信的媒介就是 Channel, Channel 是线程安全的，不需要考虑数据冲突问题，面对并发问题，我们始终应该优先考虑使用Channel，它是 first class 级别的，但是纵使有主角光环加持，Channel也不是万能的，它也需要配角，这也是共享内存存在的价值，其他语言中主流的并发编程都是通过共享内存实现的，共享内存必然涉及并发过程中的共享数据冲突问题，而为了解决数据冲突问题，Go 语言沿袭了传统的并发编程解决方案 - 锁机制，这些锁都位于 sync 包中。

golang 中 sync 包提供了两种锁 Mutex (互斥锁) 和 RWMutex (读写锁), 其中 RWMutex 是基于 Mutex 实现的, 只读锁的实现使用类似引用计数器(Reference Counting)的功能．

- Mutex: 互斥锁
- RWMutex: 读写锁

锁的作用都是为了解决并发情况下共享数据的原子操作和最终一致性问题

## Mutex, 互斥锁

```go
type Mutex struct {
    // contains filtered or unexported fields
}

func (m *Mutex) Lock()
func (m *Mutex) Unlock()
```

sync.Mutex 用于多个 goroutine 对共享资源的互斥访问。使用要点如下：

1. Lock() 加锁，Unlock() 解锁；
2. 对未解锁的 Mutex 使用 Lock() 会阻塞；
3. 对未上锁的 Mutex 使用 Unlock() 会导致 panic 异常。
4. 加锁之后未解锁, 再次加锁会导致死锁

使用 Lock() 加锁后, 便不能再次对其进行加锁, 直到用 Unlock() 解锁对其解锁后, 才能再次加锁. 适用于读写不确定场景, 即读写次数没有明显的区别, 并且只允许只有一个读或者写的场景, 所以该锁也叫做全局锁．

## 示例

```go
package main  

import (  
    "fmt"  
    "sync"  
)  

func main() {  
    var l *sync.Mutex  
    l = new(sync.Mutex)  
    l.Lock()  
    defer l.Unlock()  
    fmt.Println("1")  
}
```

结果输出: 1

当 Unlock() 在 Lock() 之前使用时, 会报错

```go
package main  

import (  
    "fmt"  
    "sync"  
)  

func main() {  
    var l *sync.Mutex  
    l = new(sync.Mutex)  
    l.Unlock()  
    fmt.Println("1")  
    l.Lock()  
}
```

运行结果:  panic: sync: unlock of unlocked mutex

在解锁之前两次加锁会导致死锁

```go
package main  

import (  
    "fmt"  
    "sync"  
)  

func main() {  
    var l *sync.Mutex  
    l = new(sync.Mutex)  
    l.Lock()  
    fmt.Println("1")  
    l.Lock()  
}
```

运行结果: 1

fatal error: all goroutines are asleep - deadlock!

## RWMutex, 读写锁

```go
type RWMutex
func (rw *RWMutex) Lock()
func (rw *RWMutex) RLock()
func (rw *RWMutex) RLocker() Locker
func (rw *RWMutex) RUnlock()
func (rw *RWMutex) Unlock()
```

- RWMutex 可以加一个写锁或多个读锁
- 读锁占用的情况下会阻止写，不会阻止读，多个 goroutine 可以同时获取读锁
- 适合于读多写少场景

### Lock(), Unlock()

Lock() 加写锁, Unlock() 解写锁
如果在加写锁之前已经有其他的读锁和写锁, 则 Lock() 会阻塞直到该锁可用(Lock()之后的其它Lock()或RLock()也会被阻塞), 直到之前的锁都释放掉之后再加写锁,本次写锁解锁之后,如果同时有写锁和读锁在排队, 首个读锁将解除阻塞,然后才轮到写锁. 所以无论是读锁还是写锁都 不会有无限等待的情况 .
在 Lock() 之前使用 Unlock() 会导致 panic 异常

```go
package main

import (  
    "fmt"  
    "sync"  
)

func main() {
    var l *sync.RWMutex
    l = new(sync.RWMutex)
    l.Unlock()
    fmt.Println("1")
    l.Lock()
}
```

运行结果: panic: sync: unlock of unlocked mutex

## RLock(), RUnlock()

RLock() 加读锁，RUnlock() 解读锁
RLock() 加读锁时，如果存在写锁，则无法加读锁；当只有读锁或者没有锁时，可以加读锁，读锁可以加载多个
RUnlock() 解读锁，RUnlock() 撤销单次 RLock() 调用，对于其他同时存在的读锁则没有效果
在没有读锁的情况下调用 RUnlock() 会导致 panic 错误
RUnlock() 的个数不得多余 RLock()，否则会导致 panic 错误

## RUnlock()

func (rw *RWMutex) RUnlock() 读锁解锁, RUnlock 撤销单次 RLock 调用, 它对于其它同时存在的读取器则没有效果。若 rw 并没有为读取而锁定, 调用 RUnlock 就会引发一个运行时错误 (注: 这种说法在 go1.3 版本中是不对的, 例如下面这个例子)。

```go
package main  

import (  
    "fmt"  
    "sync"  
)  

func main() {  
    var l *sync.RWMutex  
    l = new(sync.RWMutex)  
    l.RUnlock()//１个RUnLock  
    fmt.Println("1")  
    l.RLock()                
}  
```

运行结果: 1

但是程序中先尝试 解锁读锁, 然后才加读锁, 但是没有报错, 并且能够正常输出．

分析: go1.3 版本中出现这种情况的原因分析, 通过阅读源码可以很清晰的得到结果

```go
func (rw *RWMutex) RUnlock() {
    if raceenabled {
        _ = rw.w.state
        raceReleaseMerge(unsafe.Pointer(&rw.writerSem))
        raceDisable()
    }
    if atomic.AddInt32(&rw.readerCount, -1) < 0 {//readercounter初始值为0,调用RUnLock之后变为-1,继续往下执行  
        // A writer is pending.
        if atomic.AddInt32(&rw.readerWait, -1) == 0 {//此时readerwaiter变为１,1-1之后变为0,可以继续以后的操作．  
            // The last reader unblocks the writer.
            runtime_Semrelease(&rw.writerSem)
        }
    }
    if raceenabled {
        raceEnable()
    }
}
```

当 RUnlock 多于 RLock 多个时, 便会报错, 进入死锁．实例如下

```go
package main  

import (  
    "fmt"  
    "sync"  
)  

type s struct {  
    readerCount int32  
}  

func main() {
    l := new(sync.RWMutex)
    l.RUnlock()
    l.RUnlock() //此处出现死锁
    fmt.Println("1")
    l.RLock()
}
```

运行结果:

fatal error: all goroutines are asleep - deadlock!
  
总结

所以在 go1.3 版本中, 运行过程中允许 RUnLock 早于 RLock 一个, 也只能早于1个 (注: 虽然代码允许,但是强烈不推荐使用), 并且在早于之后必须利用 RLock 进行加锁才可以继续使用

<https://blog.csdn.net/chenbaoke/article/details/41957725>

作者：WangZZ
链接：<https://www.jianshu.com/p/679041bdaa39>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

————————————————
版权声明：本文为CSDN博主「恋喵大鲤鱼」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/K346K346/article/details/90476721>

<https://laravelacademy.org/post/19928>
<https://en.wikipedia.org/wiki/Readers%E2%80%93writers_problem>
<https://en.wikipedia.org/wiki/Fetch-and-add>