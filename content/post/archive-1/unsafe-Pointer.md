---
title: unsafe.Pointer
author: "-"
date: 2015-01-12T09:00:50+00:00
url: 7230
categories:
  - Go
tags:$
  - reprint
---
## unsafe.Pointer

Go 的普通指针是不支持指针运算和转换

首先，Go 是一门静态语言，所有的变量都必须为标量类型。不同的类型不能够进行赋值、计算等跨类型的操作。那么指针也对应着相对的类型，也在 Compile 的静态类型检查的范围内。同时静态语言，也称为强类型。也就是一旦定义了，就不能再改变它

错误示例
```go
func main(){
    num := 5
    numPointer := &num

    flnum := (*float32)(numPointer)
    fmt.Println(flnum)
}
```


# command-line-arguments
...: cannot convert numPointer (type *int) to type *float32
在示例中，我们创建了一个 num 变量，值为 5，类型为 int。取了其对于的指针地址后，试图强制转换为 *float32，结果失败...


## unsafe.Pointer 

unsafe.Pointer 表示任意类型且可寻址的指针值， 可以在不同的指针类型之间转换

任何类型的指针值都可以转换为 Pointer
Pointer 可以转换为任何类型的指针值
uintptr 可以转换为 Pointer
Pointer 可以转换为 uintptr

## Offsetof

```go
type Num struct {
    i string
    j int64
}

func main() {
    n := Num{i: "EDDYCJY", j: 1}
    nPointer := unsafe.Pointer(&n)

    niPointer := (*string)(nPointer)
    *niPointer = "煎鱼"

    njPointer := (*int64)(unsafe.Pointer(uintptr(nPointer) + unsafe.Offsetof(n.j)))
    *njPointer = 2

    fmt.Printf("n.i: %s, n.j: %d", n.i, n.j)
}


```

## 结构体的一些基本概念

结构体的成员变量在内存存储上是一段连续的内存
结构体的初始地址就是第一个成员变量的内存地址
基于结构体的成员地址去计算偏移量。就能够得出其他成员变量的内存地址

nsafe.Offsetof：返回成员变量 x 在结构体当中的偏移量。更具体的讲，就是返回结构体初始位置到 x 之间的字节数。需要注意的是入参 ArbitraryType 表示任意类型，并非定义的 int。它实际作用是一个占位符

func Offsetof(x ArbitraryType) uintptr


>https://segmentfault.com/a/1190000017389782

