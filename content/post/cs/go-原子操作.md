---
title: go 原子操作
author: "-"
date: 2020-04-26T10:51:29+00:00
url: /?p=16090
categories:
  - Inbox
tags:
  - reprint
---
## go 原子操作
原子操作
  
像Java一样，Golang支持很多CAS操作。运行结果是unsaftCnt可能小于200，因为unsafeCnt++在机器指令层面上不是一条指令，而可能是从内存加载数据到寄存器、执行自增运算、保存寄存器中计算结果到内存这三部分，所以不进行保护的话有些更新是会丢失的。

package main

import (
      
"fmt"
      
"time"
      
"sync/atomic"
      
"runtime"
  
)

func main() {
      
// IMPORTANT!!!
      
runtime.GOMAXPROCS(4)

    // thread-unsafe
    var unsafeCnt int32 = 0
    for i := 0; i < 10; i++ {
        go func() {
            for i := 0; i < 20; i++ {
                time.Sleep(time.Millisecond)
                unsafeCnt++
            }
        }()
    }
    time.Sleep(time.Second)
    fmt.Println("cnt: ", unsafeCnt)
    
    // CAS toolkit
    var cnt int32 = 0
    for i := 0; i < 10; i++ {
        go func() {
            for i := 0; i < 20; i++ {
                time.Sleep(time.Millisecond)
                atomic.AddInt32(&cnt, 1)
            }
        }()
    }
    
    time.Sleep(time.Second)
    cntFinal := atomic.LoadInt32(&cnt)
    fmt.Println("cnt: ", cntFinal)
    

}
  
神奇CAS的原理
  
Golang的AddInt32()类似于Java中AtomicInteger.incrementAndGet()，其伪代码可以表示如下。二者的基本思想是一致的，本质上是 乐观锁: 首先，从内存位置M加载要修改的数据到寄存器A中；然后，修改数据并保存到另一寄存器B；最终，利用CPU提供的CAS指令 (Java通过JNI调用到) 用一条指令完成: 1) A值与M处的原值比较；2) 若相同则将B值覆盖到M处。
  
若不相同，则CAS指令会失败，说明从内存加载到执行CAS指令这一小段时间内，发生了上下文切换，执行了其他线程的代码修改了M处的变量值。那么重新执行前面几个步骤再次尝试。
  
ABA问题: 即另一线程修改了M位置的数据，但是从原值改为C，又从C改回原值。这样上下文切换回来，CAS指令发现M处的值"未改变" (实际是改了两次，最后改回来了) ，所以CAS指令正常执行，不会失败。这种问题在Java中可以用AtomicStampedReference/AtomicMarkableReference解决。
  
https://studygolang.com/articles/4414