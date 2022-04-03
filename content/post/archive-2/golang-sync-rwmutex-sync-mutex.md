---
title: golang sync.RWMutex, sync.Mutex, 锁
author: "-"
date: 2018-04-13T02:31:40+00:00
url: go/mutex
categories:
  - golang

tags:
  - reprint
---
## golang sync.RWMutex, sync.Mutex, 锁
golang 中 sync 包实现了两种锁 Mutex  (互斥锁) 和 RWMutex  (读写锁) , 其中 RWMutex 是基于 Mutex 实现的, 只读锁的实现使用类似引用计数器的功能．

  * Mutex: 互斥锁
  * RWMutex: 读写锁

type Mutex
      
func (m *Mutex) Lock()
      
func (m *Mutex) Unlock()
  
type RWMutex
      
func (rw *RWMutex) Lock()
      
func (rw *RWMutex) RLock()
      
func (rw *RWMutex) RLocker() Locker
      
func (rw *RWMutex) RUnlock()
      
func (rw *RWMutex) Unlock()

其中 Mutex 为互斥锁, Lock() 加锁, Unlock() 解锁,使用 Lock() 加锁后, 便不能再次对其进行加锁, 直到利用 Unlock() 解锁对其解锁后, 才能再次加锁．适用于读写不确定场景, 即读写次数没有明显的区别, 并且只允许只有一个读或者写的场景, 所以该锁叶叫做全局锁．

func (m *Mutex) Unlock() 用于解锁 m, 如果在使用 Unlock() 前未加锁,就会引起一个运行错误．

已经锁定的Mutex并不与特定的goroutine相关联,这样可以利用一个goroutine对其加锁,再利用其他goroutine对其解锁．

正常运行例子: 

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

当Unlock()在Lock()之前使用时,便会报错

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

当在解锁之前再次进行加锁,便会死锁状态

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
  
RWMutex是一个读写锁,该锁可以加多个读锁或者一个写锁,其经常用于读次数远远多于写次数的场景．

func (rw *RWMutex) Lock()写锁,如果在添加写锁之前已经有其他的读锁和写锁,则lock就会阻塞直到该锁可用,为确保该锁最终可用,已阻塞的 Lock 调用会从获得的锁中排除新的读取器,即写锁权限高于读锁,有写锁时优先进行写锁定
    
func (rw *RWMutex) Unlock()写锁解锁,如果没有进行写锁定,则就会引起一个运行时错误．

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
      
func (rw *RWMutex) RLock() 读锁,当有写锁时,无法加载读锁,当只有读锁或者没有锁时,可以加载读锁,读锁可以加载多个,所以适用于＂读多写少＂的场景

func (rw *RWMutex)RUnlock()读锁解锁,RUnlock 撤销单次 RLock 调用,它对于其它同时存在的读取器则没有效果。若 rw 并没有为读取而锁定,调用 RUnlock 就会引发一个运行时错误(注: 这种说法在go1.3版本中是不对的,例如下面这个例子)。

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

运行结果: １
  
但是程序中先尝试 解锁读锁,然后才加读锁,但是没有报错,并且能够正常输出．

分析: go1.3版本中出现这种情况的原因分析,通过阅读源码可以很清晰的得到结果

```go
func (rw *RWMutex) RUnlock() {  
    if raceenabled {  
        _ = rw.w.state  
        raceReleaseMerge(unsafe.Pointer(&rw.writerSem))  
        raceDisable()  
    }  
    if atomic.AddInt32(&rw.readerCount, -1) < 0 {//readercounter初始值为０,调用RUnLock之后变为-1,继续往下执行  
        // A writer is pending.  
        if atomic.AddInt32(&rw.readerWait, -1) == 0 {//此时readerwaiter变为１,1-1之后变为０,可以继续以后的操作．  
            // The last reader unblocks the writer.  
            runtime_Semrelease(&rw.writerSem)  
        }  
    }  
    if raceenabled {  
        raceEnable()  
    }  
}  
```

当RUnlock多于RLock多个时,便会报错,进入死锁．实例如下: 

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
    l.RUnlock()//此处出现死锁  
    fmt.Println("1")  
    l.RLock()  
}
```

运行结果: 
  

fatal error: all goroutines are asleep - deadlock!
  
总结: 

所以在go1.3版本中,运行过程中允许RUnLock早于RLock一个,也只能早于１个 (注: 虽然代码允许,但是强烈不推荐使用) ,并且在早于之后必须利用RLock进行加锁才可以继续使用

https://blog.csdn.net/chenbaoke/article/details/41957725