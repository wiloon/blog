---
title: uintptr
author: "-"
date: 2014-12-30T09:09:43+00:00
url: uintptr
categories:
  - Go
tags:
  - reprint
---
## uintptr

如果你看go的源码，尤其是runtime的部分的源码，你一定经常会发现unsafe.Pointer和uintptr这两个函数，例如下面就是runtime里面的map源码实现里面的一个函数：

func (b *bmap) overflow(t *maptype) *bmap {
    return *(**bmap)(add(unsafe.Pointer(b), uintptr(t.bucketsize)-sys.PtrSize))
}
那么这两个方法有什么用呢？下面我们来重点介绍一下。

Go中的指针及与指针对指针的操作主要有以下三种：

一普通的指针类型，例如 var intptr *T，定义一个T类型指针变量。

二内置类型uintptr，本质是一个无符号的整型，它的长度是跟平台相关的，它的长度可以用来保存一个指针地址。

三是unsafe包提供的Pointer，表示可以指向任意类型的指针。

1.普通的指针类型
count := 1
Counter(&count)
fmt.Println(count)

func Counter(count *int) {
    *count++
}
普通指针可以通过引用来修改变量的值，这个跟C语言指针有点像。

2.uintptr类型
uintptr用来进行指针计算，因为它是整型，所以很容易计算出下一个指针所指向的位置。uintptr在builtin包中定义，定义如下：

// uintptr is an integer type that is large enough to hold the bit pattern of any pointer.
// uintptr是一个能足够容纳指针位数大小的整数类型
type uintptr uintptr
虽然uintpr保存了一个指针地址，但它只是一个值，不引用任何对象。因此使用的时候要注意以下情况：

1.如果uintptr地址相关联对象移动，则其值也不会更新。例如goroutine的堆栈信息发生变化

2.uintptr地址关联的对象可以被垃圾回收。GC不认为uintptr是活引用，因此unitptr地址指向的对象可以被垃圾收集。

一个uintptr可以被转换成unsafe.Pointer,同时unsafe.Pointer也可以被转换为uintptr。可以使用使用uintptr + offset计算出地址，然后使用unsafe.Pointer进行转换，格式如下：p = unsafe.Pointer(uintptr(p) + offset)


```go
func main() {
    n := 10

    b := make([]int, n)
    for i := 0; i < n; i++ {
        b[i] = i
    }
    fmt.Println(b)
    // [0 1 2 3 4 5 6 7 8 9]

    // 取slice的最后的一个元素
    firstP := &b[0]
    fmt.Printf("firstP: %v\n", firstP)
    firstUnsafe := unsafe.Pointer(firstP)
    fmt.Printf("firstUnsafe: %v\n", firstUnsafe)
    firstUintPtr := uintptr(firstUnsafe)
    fmt.Printf("firstUintPtr: %v\n", firstUintPtr)
    itemSize := unsafe.Sizeof(b[0])
    fmt.Printf("itemSize: %v\n", itemSize)
  //     lastUintP := firstUintPtr + 9*itemSize // 错误用法，firstUintPtr 可能随时被 GC 回收， GC会把 firstUintPtr 当成 普通 uint， GC 并不知道它是一个指针
    lastUintP := uintptr(firstUnsafe) + 9*itemSize
    fmt.Printf("itemSize: %v\n", uintptr(firstUnsafe) + 9*itemSize)
    end := unsafe.Pointer(lastUintP)
    fmt.Printf("end: %v\n", end)
    // 等价于unsafe.Pointer(&b[9])
    fmt.Println(*(*int)(end))
    // 9
}
```

>https://segmentfault.com/a/1190000039165125

