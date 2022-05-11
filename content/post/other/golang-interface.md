---
title: golang  方法, 接口, 继承
author: "-"
date: 2012-11-18T15:12:11+00:00
url: /?p=4716
categories:
  - inbox
tags:
  - reprint
---
## golang  方法, 接口, 继承

<http://www.cnblogs.com/chenny7/p/4497969.html>

Go语言没有沿袭传统面向对象编程中的诸多概念，比如继承、虚函数、构造函数和析构函数、隐藏的 this 指针等。

## go 方法
  
Go 语言中同时有函数和方法。方法就是一个包含了接收器 (receiver) 的函数，receiver 可以是内置类型或者结构体类型的一个值或者是一个指针。所有给定类型的方法属于该类型的方法集。

如下面的这个例子，定义了一个新类型Integer，它和int一样，只是为它内置的int类型增加了个新方法 Less()

### 接收器——方法作用的目标

接收器的格式如下：

```go
func (接收器变量 接收器类型) 方法名(参数列表) (返回参数) {
    函数体
}
```

```go
type Integer int

func (a Integer) Less(b Integer) bool {
    return a < b
}

func main() {

var a Integer = 1
    if a.Less(2) {
        fmt.Println("less then 2")
    }
}
```

可以看出，Go语言在自定义类型的对象中没有C++/Java那种隐藏的this指针，而是在定义成员方法时显式声明了其所属的对象。

method的语法如下:

func (r ReceiverType) funcName(parameters) (results)
  
当调用method时，会将receiver作为函数的第一个参数:

funcName(r, parameters);
  
所以，receiver是值类型还是指针类型要看method的作用。如果要修改对象的值，就需要传递对象的指针。

指针作为Receiver会对实例对象的内容发生操作,而普通类型作为Receiver仅仅是以副本作为操作对象,并不对原实例对象发生操作。

复制代码
  
func (a *Ingeger) Add(b Integer) {

*a += b
  
}

func main() {

var a Integer = 1

a.Add(3)

fmt.Println("a =", a) // a = 4
  
}

如果Add方法不使用指针，则a返回的结果不变，这是因为Go语言函数的参数也是基于值传递。

注意: 当方法的接受者是指针时，即使用值类型调用那么方法内部也是对指针的操作。

之前说过，Go语言没有构造函数的概念，通常使用一个全局函数来完成。例如:

复制代码
  
func NewRect(x, y, width, height float64) *Rect {

return &Rect{x, y, width, height}
  
}

func main() {

rect1 := NewRect(1,2,10,20)

fmt.Println(rect1.width)

}

### 匿名组合, 继承

Go语言提供了继承，但是采用了组合的语法，我们将其称为匿名组合，例如:

```go
type Base struct {
    name string
}

func (base *Base) Set(myname string) {
    base.name = myname
}

func (base *Base) Get() string {
    return base.name
}

type Derived struct {
    Base
    age int
}

func (derived *Derived) Get() (nm string, ag int) {
    return derived.name, derived.age
}

func main() {
    b := &Derived{}

    b.Set("sina")
    fmt.Println(b.Get())
}
```

例子中，在Base类型定义了get()和set()两个方法，而Derived类型继承了Base类，并改写了Get()方法，在Derived对象调用Set()方法，会加载基类对应的方法；而调用Get()方法时，加载派生类改写的方法。

组合的类型和被组合的类型包含同名成员时， 会不会有问题呢？可以参考下面的例子:

```go
type Base struct {
    name string 
    age int
}

func (base *Base) Set(myname string, myage int) {
    base.name = myname
    base.age = myage
}

type Derived struct {
    Base 
    name string
}

func main() { 
    b := &Derived{}
    b.Set("sina", 30)
    fmt.Println("b.name =",b.name, "\tb.Base.name =", b.Base.name)
    fmt.Println("b.age =",b.age, "\tb.Base.age =", b.Base.age)
}
```

值语义和引用语义
  
值语义和引用语义的差别在于赋值，比如

b = a
  
b.Modify()
  
如果b的修改不会影响a的值，那么此类型属于值类型；如果会影响a的值，那么此类型是引用类型。

Go语言中的大多数类型都基于值语义，包括:

基本类型，如byte、int、bool、float32、string等；
  
复合类型，如arry、struct、pointer等；

C语言中的数组比较特别，通过函数传递一个数组的时候基于引用语义，但是在结构体定义数组变量的时候基于值语义。而在Go语言中，数组和基本类型没有区别，是很纯粹的值类型，例如:

var a = [3] int{1,2,3}
  
var b = a
  
b[1]++
  
fmt.Println(a, b) // [1 2 3] [1 3 3]
  
从结果看，b=a赋值语句是数组内容的完整复制，要想表达引用，需要用指针:

var a = [3] int{1,2,3}
  
var b = &a// 引用语义
  
b[1]++
  
fmt.Println(a, b) // [1 3 3] [1 3 3]

接口
  
Interface 是一组抽象方法 (未具体实现的方法/仅包含方法名参数返回值的方法) 的集合，如果实现了 interface 中的所有方法，即该类/对象就实现了该接口。

Interface 的声明格式:

type interfaceName interface {

//方法列表
  
}
  
Interface 可以被任意对象实现，一个类型/对象也可以实现多个 interface；
  
interface的变量可以持有任意实现该interface类型的对象。

如下面的例子:

复制代码
  
package main

    import "fmt"
    
    type Human struct {
        name string
        age int
        phone string
    }
    
    type Student struct {
        Human //匿名字段
        school string
        loan float32
    }
    
    type Employee struct {
        Human //匿名字段
        company string
        money float32
    }
    
    //Human实现SayHi方法
    func (h Human) SayHi() {
        fmt.Printf("Hi, I am %s you can call me on %s\n", h.name, h.phone)
    }
    
    //Human实现Sing方法
    func (h Human) Sing(lyrics string) {
        fmt.Println("La la la la...", lyrics)
    }
    
    //Employee重载Human的SayHi方法
    func (e Employee) SayHi() {
        fmt.Printf("Hi, I am %s, I work at %s. Call me on %s\n", e.name,
            e.company, e.phone)
        }
    
    // Interface Men被Human,Student和Employee实现
    // 因为这三个类型都实现了这两个方法
    type Men interface {
        SayHi()
        Sing(lyrics string)
    }
    
    func main() {
        mike := Student{Human{"Mike", 25, "222-222-XXX"}, "MIT", 0.00}
        paul := Student{Human{"Paul", 26, "111-222-XXX"}, "Harvard", 100}
        sam := Employee{Human{"Sam", 36, "444-222-XXX"}, "Golang Inc.", 1000}
        tom := Employee{Human{"Tom", 37, "222-444-XXX"}, "Things Ltd.", 5000}
    
        //定义Men类型的变量i
        var i Men
    
        //i能存储Student
        i = mike
        fmt.Println("This is Mike, a Student:")
        i.SayHi()
        i.Sing("November rain")
    
        //i也能存储Employee
        i = tom
        fmt.Println("This is tom, an Employee:")
        i.SayHi()
        i.Sing("Born to be wild")
    
        //定义了slice Men
        fmt.Println("Let's use a slice of Men and see what happens")
        x := make([]Men, 3)
        //这三个都是不同类型的元素，但是他们实现了interface同一个接口
        x[0], x[1], x[2] = paul, sam, mike
    
        for _, value := range x{
            value.SayHi()
        }
    }

复制代码

空接口

空interface(interface{})不包含任何的method，正因为如此，所有的类型都实现了空interface。空interface对于描述起不到任何的作用(因为它不包含任何的method) ，但是空interface在我们需要存储任意类型的数值的时候相当有用，因为它可以存储任意类型的数值。它有点类似于C语言的void*类型。

复制代码
  
// 定义a为空接口

var a interface{}

var i int = 5

s := "Hello world"

// a可以存储任意类型的数值

a = i

a = s
  
复制代码

interface的变量里面可以存储任意类型的数值 (该类型实现了interface) ，那么我们怎么反向知道这个interface变量里面实际保存了的是哪个类型的对象呢？目前常用的有两种方法: switch测试、Comma-ok断言。

switch测试如下:

复制代码
  
type Element interface{}
  
type List [] Element

type Person struct {

name string

age int
  
}

//打印
  
func (p Person) String() string {

return "(name: " + p.name + " - age: "+strconv.Itoa(p.age)+ " years)"
  
}

func main() {

list := make(List, 3)

list[0] = 1 //an int

list[1] = "Hello" //a string

list[2] = Person{"Dennis", 70}

    for index, element := range list{
        switch value := element.(type) {
            case int:
                fmt.Printf("list[%d] is an int and its value is %d\n", index, value)
            case string:
                fmt.Printf("list[%d] is a string and its value is %s\n", index, value)
            case Person:
                fmt.Printf("list[%d] is a Person and its value is %s\n", index, value)
            default:
                fmt.Println("list[%d] is of a different type", index)
        }   
    }   

}
  
复制代码

如果使用Comma-ok断言的话:

复制代码
  
func main() {

list := make(List, 3)

list[0] = 1 // an int

list[1] = "Hello" // a string

list[2] = Person{"Dennis", 70}

    for index, element := range list {
        if value, ok := element.(int); ok {
            fmt.Printf("list[%d] is an int and its value is %d\n", index, value)
        } else if value, ok := element.(string); ok {
            fmt.Printf("list[%d] is a string and its value is %s\n", index, value)
        } else if value, ok := element.(Person); ok {
            fmt.Printf("list[%d] is a Person and its value is %s\n", index, value)
        } else {
            fmt.Printf("list[%d] is of a different type\n", index)
        }
    }

}
  
复制代码

嵌入接口

正如struct类型可以包含一个匿名字段，interface也可以嵌套另外一个接口。

如果一个interface1作为interface2的一个嵌入字段，那么interface2隐式的包含了interface1里面的method。

反射

所谓反射 (reflect) 就是能检查程序在运行时的状态。

使用reflect一般分成三步，下面简要的讲解一下: 要去反射是一个类型的值(这些值都实现了空interface)，首先需要把它转化成reflect对象(reflect.Type或者reflect.Value，根据不同的情况调用不同的函数)。这两种获取方式如下:

t := reflect.TypeOf(i) //得到类型的元数据,通过t我们能获取类型定义里面的所有元素

v := reflect.ValueOf(i) //得到实际的值，通过v我们获取存储在里面的值，还可以去改变值

转化为reflect对象之后我们就可以进行一些操作了，也就是将reflect对象转化成相应的值，例如

tag := t.Elem().Field(0).Tag //获取定义在struct里面的标签
  
name := v.Elem().Field(0).String() //获取存储在第一个字段里面的值

获取反射值能返回相应的类型和数值

var x float64 = 3.4
  
v := reflect.ValueOf(x)
  
fmt.Println("type:", v.Type())
  
fmt.Println("kind is float64:", v.Kind() == reflect.Float64)
  
fmt.Println("value:", v.Float())

最后，反射的话，那么反射的字段必须是可修改的，我们前面学习过传值和传引用，这个里面也是一样的道理。反射的字段必须是可读写的意思是，如果下面这样写，那么会发生错误

var x float64 = 3.4
  
v := reflect.ValueOf(x)
  
v.SetFloat(7.1)

如果要修改相应的值，必须这样写

var x float64 = 3.4
  
p := reflect.ValueOf(&x)
  
v := p.Elem()
  
v.SetFloat(7.1)
  
上面只是对反射的简单介绍，更深入的理解还需要自己在编程中不断的实践。

### 继承机制

继承机制的简化版 上面的实现方案的一个问题是*IntegerConstant的方法调用中，出现了重复造轮子的问题。但是我们可以使用Go内建的嵌入机制来避免此类情况的出现。嵌入机制(匿名嵌入)允许类型之前共享代码和数据。
type IntegerConstant struct {
  Token
  value uint64
}

func (i *IntegerConstant) Value() uint64 {
  return i.value
}
IntegerConstant中匿名嵌入了Token类型，使得IntegerConstant"继承"了Token的字段和方法。

相比于Java，Go在继承和聚合之间的界限是很模糊的。Go中没有extends关键词。在语法的层次上，继承看上去与聚合没有什么区别。Go中聚合跟继承唯一的不同在于，继承自其他结构体的struct类型可以直接访问父类结构体的字段和方法。

----

<https://hackthology.com/golangzhong-de-mian-xiang-dui-xiang-ji-cheng.html>

<http://se77en.cc/2014/05/05/methods-interfaces-and-embedded-types-in-golang/>
  
<http://se77en.cc/2014/05/04/choose-whether-to-use-a-value-or-pointer-receiver-on-methods/>
  
<https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/02.6.md>
