---
title: Go 指针, pointer
author: "-"
date: 2016-10-12T00:12:13+00:00
url: go/pointer
categories:
  - Go
tags:
  - reprint
  - Pointer
---
## Go 指针, pointer

- 普通指针
- uintptr
- unsafe.Pointer

对于Go语言, 严格意义上来讲, 只有一种传递, 也就是按值传递 (by value)。当一个变量当作参数传递的时候, 会创建一个变量的副本, 然后传递给函数或者方法, 你可以看到这个副本的地址和变量的地址是不一样的。

当变量当做指针被传递的时候, 一个新的指针被创建, 它指向变量指向的同样的内存地址, 所以你可以将这个指针看成原始变量指针的副本。当这样理解的时候, 我们就可以理解成Go总是创建一个副本按值转递, 只不过这个副本有时候是变量的副本, 有时候是变量指针的副本。

Go 语言保留着C中值和指针的区别, 但是对于指针繁琐用法进行了大量的简化,引入引用的概念。所以在Go语言中,你几乎不用担心会因为直接操作内寸而引起各式各样的错误。Go语言的指针, 基本上只剩下用于区分 by ref 和 by val 语义。

## 指针地址和指针类型

一个指针变量可以指向任何一个值的内存地址，它所指向的值的内存地址在 32 和 64 位机器上分别占用 4 或 8 个字节，占用字节的大小与所指向的值的大小无关。当一个指针被定义后没有分配到任何变量时，它的默认值为 nil。指针变量通常缩写为 ptr。

每个变量在运行时都拥有一个地址，这个地址代表变量在内存中的位置。Go语言中使用在变量名前面添加&操作符 (前缀）来获取变量的内存地址 (取地址操作），格式如下：

```go
ptr := &v    // v 的类型为 T
```

其中 v 代表被取地址的变量，变量 v 的地址使用变量 ptr 进行接收，ptr 的类型为 `*T`，称做 T 的指针类型，* 代表指针。

```go
// &: 取地址
// *: 解析地址

var p *int // p 的类型是: int 型的指针

// Foo, Bar 的类型是指针
type TestItem struct {
    Foo *string //指针类型
    Bar *string
}
```

```go
package main

import "fmt"

func main() {
    var cat int = 1
    var str string = "banana"
    // 0xc00001a0b0 0xc000010230
    fmt.Printf("%p %p", &cat, &str)
}
```

```go
package basic

import (
    "fmt"
)

func PointerTest() {

    var i int  // i 的类型是 int 型
    i = 1      // i 的值为 1;
    var p *int // p 的类型是 int型的指针
    p = &i     // p 的值为 i 的地址

    fmt.Printf("i=%d;p=%d;*p=%d\n", i, p, *p)

    *p = 2 // *p 的值为 [[i的地址]的指针] (其实就是i), 这行代码也就等价于 i = 2
    fmt.Printf("i=%d;p=%d;*p=%d\n", i, p, *p)

    i = 3 // 验证想法
    fmt.Printf("i=%d;p=%d;*p=%d\n", i, p, *p)
}

```

这段代码执行结果:
  
```
i=1;p=0x4212f100;_p=1
i=2;p=0x4212f100;_p=2
i=3;p=0x4212f100;*p=3
```

### 函数的参数传递

```bash
package main

import "fmt"

type abc struct {
    v int
}

func (a abc) foo() { //传入的是值,而不是引用
    a.v = 1
    fmt.Printf("1:%d\n", a.v)
}
func (a *abc) bar() { //传入的是引用,而不是值
    fmt.Printf("2:%d\n", a.v)
    a.v = 2
    fmt.Printf("3:%d\n", a.v)
}
func (a *abc) fooBar() { //传入的是引用,而不是值
    fmt.Printf("4:%d\n", a.v)
}
func main() {
    oneObj := abc{} //new(abc);
    oneObj.foo()
    oneObj.bar()
    oneObj.fooBar()
}
```
  
### 输出结果

```
1:1
2:0
3:2
4:2
```

### 传值与传指针

当我们传一个参数值到被调用函数里面时, 实际上是传了这个值的一份copy,当在被调用函数中修改参数值的时候, 调用函数中相应实参不会发生任何变化, 因为数值变化只作用在copy上。

传指针比较轻量级 (8 bytes), 只是传内存地址, 我们可以用指针传递体积大的结构体。如果用参数值传递的话, 在每次copy上面就会花费相对较多的系统开销 (内存和时间) 。所以当你要传递大的结构体的时候,用指针是一个明智的选择。

Go语言中string,slice,map这三种类型的实现机制类似指针,所以可以直接传递,而不用取地址后传递指针。 (注: 若函数需改变slice的长度,则仍需要取地址传递指针)

要访问指针 p 指向的结构体中某个元素 x,不需要显式地使用 * 运算,可以直接 p.x ；

一个稍微复杂的例子

package main

import "fmt"

type S map[string][]string

func Summary(paramstring)(s*S){
  
s=&S{
  
"name":[]string{param},
  
"profession":[]string{"Javaprogrammer","ProjectManager"},
  
"interest(lang)":[]string{"Clojure","Python","Go"},
  
"focus(project)":[]string{"UE","AgileMethodology","SoftwareEngineering"},
  
"hobby(life)":[]string{"Basketball","Movies","Travel"},
  
}
  
return s
  
}

func main(){
  
s:=Summary("Harry")
  
fmt.Printf("Summary(address):%v\r\n",s)
  
fmt.Printf("Summary(content):%v\r\n",*s)
  
}

输出:
  
Summary(address): 0x42131100
  
Summary(content): map[profession:[Java programmer Project Manager] interest(lang):[Clojure Python Go] hobby(life):[Basketball Movies Travel] name:[Harry] focus(project):[UE Agile Methodology Software Engineering]]
  
exit code 0, process exited normally.
  
参考资料:

使用Go语言一段时间的感受

    使用Go语言一段时间的感受
  
### T的副本创建

    package main
    import "fmt"
    type Bird struct {
        Age  int
        Name string
    }
    func passV(b Bird) {
        b.Age++
        b.Name = "Great" + b.Name
        fmt.Printf("传入修改后的Bird:\t %+v, \t内存地址: %p\n", b, &b)
    }
    func main() {
        parrot := Bird{Age: 1, Name: "Blue"}
        fmt.Printf("原始的Bird:\t\t %+v, \t\t内存地址: %p\n", parrot, &parrot)
        passV(parrot)
        fmt.Printf("调用后原始的Bird:\t %+v, \t\t内存地址: %p\n", parrot, &parrot)
    }

### *T的副本创建

    package main
    import "fmt"
    type Bird struct {
        Age  int
        Name string
    }
    func passP(b *Bird) {
        b.Age++
        b.Name = "Great" + b.Name
        fmt.Printf("传入修改后的Bird:\t %+v, \t内存地址: %p, 指针的内存地址: %p\n", *b, b, &b)
    }
    func main() {
        parrot := &Bird{Age: 1, Name: "Blue"}
        fmt.Printf("原始的Bird:\t\t %+v, \t\t内存地址: %p, 指针的内存地址: %p\n", *parrot, parrot, &parrot)
        passP(parrot)
        fmt.Printf("调用后原始的Bird:\t %+v, \t内存地址: %p, 指针的内存地址: %p\n", *parrot, parrot, &parrot)
    }

### 打印对象地址

```go
package main

import "fmt"

func byval(q *int) {
    fmt.Printf("3. byval -- q %T: &q=%p q=&i=%p  *q=i=%v\n", q, &q, q, *q)
    *q = 4143
    fmt.Printf("4. byval -- q %T: &q=%p q=&i=%p  *q=i=%v\n", q, &q, q, *q)
    q = nil
}

func main() {
    i := int(42)
    fmt.Printf("1. main  -- i  %T: &i=%p i=%v\n", i, &i, i)
    p := &i
    fmt.Printf("2. main  -- p %T: &p=%p p=&i=%p p=%v *p=i=%v\n", p, &p, p, p, *p)
    byval(p)
    fmt.Printf("5. main  -- p %T: &p=%p p=&i=%p  *p=i=%v\n", p, &p, p, *p)
    fmt.Printf("6. main  -- i  %T: &i=%p i=%v\n", i, &i, i)
}
```

---

[http://blog.jobbole.com/14386/embed/#?secret=rAI8Jn2kEL](http://blog.jobbole.com/14386/embed/#?secret=rAI8Jn2kEL)
[http://my.oschina.net/nalan/blog/77373](http://my.oschina.net/nalan/blog/77373)
[http://ilovers.sinaapp.com/drupal/node/33](http://ilovers.sinaapp.com/drupal/node/33)
[http://www.cnblogs.com/ghj1976/archive/2013/02/28/2936595.html](http://www.cnblogs.com/ghj1976/archive/2013/02/28/2936595.html)
[https://colobu.com/2017/01/05/-T-or-T-it-s-a-question/](https://colobu.com/2017/01/05/-T-or-T-it-s-a-question/)
>[http://c.biancheng.net/view/21.html](http://c.biancheng.net/view/21.html)

---

>[https://shockerli.net/post/golang-faq-cannot-take-the-address/](https://shockerli.net/post/golang-faq-cannot-take-the-address/)

先看代码
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
package main

type B struct {
    Id int
}

func New() B {
    return B{}
}

func New2() *B {
    return &B{}
}

func (b *B) Hello() {
    return
}

func (b B) World() {
    return
}

func main() {
    // 方法的接收器为 *T 类型
    New().Hello() // 编译不通过

    b1 := New()
    b1.Hello() // 编译通过

    b2 := B{}
    b2.Hello() // 编译通过

    (B{}).Hello() // 编译不通过
    B{}.Hello()   // 编译不通过

    New2().Hello() // 编译通过

    b3 := New2()
    b3.Hello() // 编译通过

    b4 := &B{} // 编译通过
    b4.Hello() // 编译通过

    (&B{}).Hello() // 编译通过

    // 方法的接收器为 T 类型
    New().World() // 编译通过

    b5 := New()
    b5.World() // 编译通过

    b6 := B{}
    b6.World() // 编译通过

    (B{}).World() // 编译通过
    B{}.World()   // 编译通过

    New2().World() // 编译通过

    b7 := New2()
    b7.World() // 编译通过

    b8 := &B{} // 编译通过
    b8.World() // 编译通过

    (&B{}).World() // 编译通过
}
输出结果
1
2
3
4
5
6
./main.go:25:10: cannot call pointer method on New()
./main.go:25:10: cannot take the address of New()
./main.go:33:10: cannot call pointer method on B literal
./main.go:33:10: cannot take the address of B literal
./main.go:34:8: cannot call pointer method on B literal
./main.go:34:8: cannot take the address of B literal
问题总结
假设 T 类型的方法上接收器既有 T 类型的，又有 *T 指针类型的，那么就不可以在不能寻址的 T 值上调用*T 接收器的方法

&B{} 是指针，可寻址
B{} 是值，不可寻址
b := B{} b是变量，可寻址
延伸思考
Go 语言规范中规定了可寻址(addressable)对象的定义：

For an operand x of type T, the address operation &x generates a pointer of type *T to x. The operand must be addressable, that is, either a variable, pointer indirection, or slice indexing operation; or a field selector of an addressable struct operand; or an array indexing operation of an addressable array. As an exception to the addressability requirement, x may also be a (possibly parenthesized) composite literal. If the evaluation of x would cause a run-time panic, then the evaluation of &x does too.

对于类型为 T 的操作数 x，地址操作符 &x 将生成一个类型为 *T 的指针指向 x。操作数必须可寻址，即，变量、间接指针、切片索引操作，或可寻址结构体的字段选择器，或可寻址数组的数组索引操作。作为可寻址性要求的例外，x 也可为 (圆括号括起来的）复合字面量。如果对 x 的求值会引起运行时恐慌，那么对 &x 的求值也会引起恐慌。

For an operand x of pointer type *T, the pointer indirection*x denotes the variable of type T pointed to by x. If x is nil, an attempt to evaluate *x will cause a run-time panic.

对于指针类型为 *T 的操作数 x，间接指针*x 表示类型为 T 的值指向 x。若 x 为 nil，尝试求值 *x 将会引发运行时恐慌。

以下几种是可寻址的：

一个变量: &x
指针引用(pointer indirection): &*x
slice 索引操作(不管 slice 是否可寻址): &s[1]
可寻址 struct 的字段: &point.X
可寻址数组的索引操作: &a[0]
composite literal 类型: &struct{ X int }{1}
下列情况 x 是不可以寻址的，不能使用 &x 取得指针：

字符串中的字节
map 对象中的元素
接口对象的动态值(通过 type assertions 获得)
常数
literal 值(非 composite literal)
package 级别的函数
方法 method(用作函数值)
中间值(intermediate value):
函数调用
显式类型转换
各种类型的操作 (除了指针引用 pointer dereference 操作 *x):
channel receive operations
sub-string operations
sub-slice operations
加减乘除等运算符
有几个点需要解释下：

常数为什么不可以寻址?
如果可以寻址的话，我们可以通过指针修改常数的值，破坏了常数的定义。

map 的元素为什么不可以寻址？
两个原因，如果对象不存在，则返回零值，零值是不可变对象，所以不能寻址，如果对象存在，因为 Go 中 map 实现中元素的地址是变化的，这意味着寻址的结果是无意义的。

为什么 slice 不管是否可寻址，它的元素读是可以寻址的？
因为 slice 底层实现了一个数组，它是可以寻址的。

为什么字符串中的字符/字节又不能寻址呢？
因为字符串是不可变的。

规范中还有几处提到了 addressable:

调用一个接收者为指针类型的方法时，使用一个可寻址的值将自动获取这个值的指针
++、-- 语句的操作对象必须可寻址或者是 map 的索引操作
赋值语句 = 的左边对象必须可寻址，或者是 map 的索引操作，或者是 _
上条同样使用 for ... range 语句
参考资料
Spec: Address operators
“cannot take the address of” and “cannot call pointer method on” - stackoverflow
go addressable 详解
文章作者 Jioby

发布日期 2019-11-28

上次更新 2019-11-28

许可协议 CC BY-NC-ND 4.0
 (如需转载，请在评论区留言您的博客地址或公众号名称等，留言后可无需等待确认）

原文链接 [https://shockerli.net/post/golang-faq-cannot-take-the-address/](https://shockerli.net/post/golang-faq-cannot-take-the-address/)

>[https://shockerli.net/post/golang-faq-cannot-take-the-address/](https://shockerli.net/post/golang-faq-cannot-take-the-address/)

## uintptr

如果你看go 的源码，尤其是 runtime 的部分的源码，你一定经常会发现 unsafe.Pointer 和 uintptr 这两个函数，例如下面就是 runtime 里面的 map 源码实现里面的一个函数

```go
func (b *bmap) overflow(t *maptype) *bmap {
    return *(**bmap)(add(unsafe.Pointer(b), uintptr(t.bucketsize)-sys.PtrSize))
}
```

Go 中的指针及与指针对指针的操作主要有以下三种：

- 普通的指针类型，例如 var intptr *T，定义一个T类型指针变量。
- 内置类型 uintptr，本质是一个无符号的整型，它的长度是跟平台相关的，它的长度可以用来保存一个指针地址。
- 是 unsafe 包提供的 Pointer，表示可以指向任意类型的指针。

## 普通的指针类型

```go
count := 1
Counter(&count)
fmt.Println(count)

func Counter(count *int) {
    *count++
}
```

普通指针可以通过引用来修改变量的值，这个跟C语言指针有点像。

## uintptr 类型

uintptr 用来进行指针计算，因为它是整型，所以很容易计算出下一个指针所指向的位置。uintptr 在builtin 包中定义，定义如下：

```go
// uintptr is an integer type that is large enough to hold the bit pattern of any pointer.
// uintptr是一个能足够容纳指针位数大小的整数类型
type uintptr uintptr
```

虽然uintpr 保存了一个指针地址，但它只是一个值，不引用任何对象。因此使用的时候要注意以下情况：

1. 如果uintptr 地址相关联对象移动，则其值也不会更新。例如goroutine 的堆栈信息发生变化
2. uintptr 地址关联的对象可以被垃圾回收。GC不认为uintptr 是活引用，因此unitptr 地址指向的对象可以被垃圾收集。

一个uintptr 可以被转换成 unsafe.Pointer, 同时 unsafe.Pointer 也可以被转换为 uintptr。可以使用使用 uintptr + offset 计算出地址，然后使用unsafe.Pointer 进行转换，格式如下：p = unsafe.Pointer(uintptr(p) + offset)

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
    
	// lastUintP := firstUintPtr + 9*itemSize // 错误用法，firstUintPtr 可能随时被 GC 回收， GC会把 firstUintPtr 当成 普通 uint， GC 并不知道它是一个指针
    lastUintP := uintptr(firstUnsafe) + 9*itemSize
    fmt.Printf("itemSize: %v\n", uintptr(firstUnsafe) + 9*itemSize)
    end := unsafe.Pointer(lastUintP)
    fmt.Printf("end: %v\n", end)
    // 等价于unsafe.Pointer(&b[9])
    fmt.Println(*(*int)(end))
    // 9
}
```

[https://segmentfault.com/a/1190000039165125](https://segmentfault.com/a/1190000039165125)

## unsafe.Pointer

Go 的普通指针是不支持指针运算和转换

首先，Go 是一门静态语言，所有的变量都必须为标量类型。不同的类型不能够进行赋值、计算等跨类型的操作。那么指针也对应着相对的类型，也在 Compile 的静态类型检查的范围内。同时静态语言，也称为强类型。也就是一旦定义了，就不能再改变它

```go
// 错误示例
func main(){
    num := 5
    numPointer := &num

    flnum := (*float32)(numPointer)
    fmt.Println(flnum)
}

// ...: cannot convert numPointer (type *int) to type*float32
```

在示例中，我们创建了一个 num 变量，值为 5，类型为 int。取了其对于的指针地址后，试图强制转换为 *float32，结果失败...

unsafe.Pointer 表示任意类型且可寻址的指针值， 可以在不同的指针类型之间转换

- 任何类型的指针值都可以转换为 unsafe.Pointer
- unsafe.Pointer 可以转换为任何类型的指针值
- uintptr 可以转换为 unsafe.Pointer
- unsafe.Pointer 可以转换为 uintptr

## Offsetof

```go
type Num struct {
    i string
    j int64
}

func main() {
    n := Num{i: "foo", j: 1}
    nPointer := unsafe.Pointer(&n)

    niPointer := (*string)(nPointer)
    *niPointer = "bar"

    njPointer := (*int64)(unsafe.Pointer(uintptr(nPointer) + unsafe.Offsetof(n.j)))
    *njPointer = 2

    fmt.Printf("n.i: %s, n.j: %d", n.i, n.j)
}

// n.i: bar, n.j: 2
```

## 结构体的一些基本概念

结构体的成员变量在内存存储上是一段连续的内存
结构体的初始地址就是第一个成员变量的内存地址
基于结构体的成员地址去计算偏移量。就能够得出其他成员变量的内存地址

nsafe.Offsetof：返回成员变量 x 在结构体当中的偏移量。更具体的讲，就是返回结构体初始位置到 x 之间的字节数。需要注意的是入参 ArbitraryType 表示任意类型，并非定义的 int。它实际作用是一个占位符

func Offsetof(x ArbitraryType) uintptr

[https://segmentfault.com/a/1190000017389782](https://segmentfault.com/a/1190000017389782)
