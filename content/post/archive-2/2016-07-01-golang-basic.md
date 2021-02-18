---
title: golang basic
author: w1100n
type: post
date: 2016-07-01T08:06:08+00:00
url: /?p=9096

---
### commands
    go get -u xorm.io/xorm

### install
#### ubuntu
    sudo add-apt-repository ppa:longsleep/golang-backports
    sudo apt update
    sudo apt install golang-go

### 环境变量
    # 设置不走 proxy 的私有仓库，多个用逗号相隔（可选）
    export GOPRIVATE=*.corp.example.com
    export GOPRIVATE=git.wiloon.com

### internal package
Go语言1.4版本增加了 Internal packages 特征用于控制包的导入，即internal package只能被特定的包导入。
内部包的规范约定：导出路径包含internal关键字的包，只允许internal的父级目录及父级目录的子包导入，其它包无法导入。

### 变量
变量是几乎所有编程语言中最基本的组成元素。从根本上说,变量相当于是对一块数据存储空间的命名,程序可以通过定义一个变量来申请一块数据存储空间,之后可以通过引用变量名来使用这块存储空间。
  
Go语言中的变量使用方式与C语言接近,但具备更大的灵活性。

#### 变量声明
Go语言的变量声明方式与C和C++语言有明显的不同。对于纯粹的变量声明,Go语言引入了关键字var,而类型信息放在变量名之后,示例如下:

```golang
var v1 int
var v2 string

var v3 [10] int  // 数组
var v4 [] int  // 数组切片
var v5 struct {
    f int
}
var v6 *int   // 指针
var v7 map[string]intvar v8 func(a int) int   // map,key为string类型,value为int类型
```

变量声明语句不需要使用分号作为结束符。与C语言相比,Go语言摒弃了语句必须以分号作为语句结束标记的习惯。
  
### 变量初始化
对于声明变量时需要进行初始化的场景,var关键字可以保留,但不再是必要的元素,如下 ：

```golang
var v1 int = 10 // 正确的使用方式1
var v2 = 10 // 正确的使用方式2,编译器可以自动推导出v2的类型
v3 := 10 // 正确的使用方式3,编译器可以自动推导出v3的类型
```

以上三种用法的效果是完全一样的。与第一种用法相比,第三种用法需要输入的字符数大大减少,是懒程序员和聪明程序员的最佳选择。这里Go语言也引入了另一个C和C++中没有的符号 (冒号和等号的组合:=),用于明确表达同时进行变量声明和初始化的工作 。
指定类型已不再是必需的,Go编译器可以从初始化表达式的右值推导出该变量应该声明为 4
哪种类型,这让Go语言看起来有点像动态类型语言,尽管Go语言实际上是 不折不扣 的强类型语言(静态类型语言)。
当然,出现在:=左侧的变量不应该是已经被声明过的,否则会导致编译错误,比如下面这个 ：
var i inti := 2
  
会导致类似如下的编译错误:
  
no new variables on left side of :=

变量赋值在Go语法中,变量初始化和变量赋值是两个不同的概念。下面为声明一个变量之后的赋值
  
过程:
  
var v10 intv10 = 123
  
Go语言的变量赋值与多数语言一致,但Go语言中提供了C/C++程序员期盼多年的多重赋值功能,比如下面这个交换i和j变量的语句:
  
i, j = j, i
  
在不支持多重赋值的语言中,交互两个变量的内容需要引入一个中间变量:
  
t = i; i = j; j = t;

匿名变量
  
我们在使用传统的强类型语言编程时,经常会出现这种情况,即在调用函数时为了获取一个值,却因为该函数返回多个值而不得不定义一堆没用的变量。在Go中这种情况可以通过结合使用多重返回和匿名变量来避免这种丑陋的写法,让代码看起来更加优雅。
  
_, _, nickName := "May", "Chan", "Chibi Maruko"

## 常量

```golang
const (
c0 = iota // iota被重设为0 // c0 == 0
c1 = iota // c1 == 1
c2 = iota // c2 == 2
）
```

在Go语言中,常量是指编译期间就已知且不可改变的值。常量可以是数值类型(包括整型、浮点型和复数类型)、布尔类型、字符串类型等 。
  
字面常量
  
所谓字面常量(literal),是指程序中硬编码的常量,如:
  
-12
  
3.14159265358979323846 // 浮点类型的常量3.2+12i // 复数类型的常量true // 布尔类型的常量"foo" // 字符串常量

Go语言的字面常量更接近我们自然语言中的常量概念,它是无类型的。只要这个常量在相应类型的值域范围内,就可以作为该类型的常量,比如上面的常量12,它可以赋值给int、uint、int32、int64、float32、float64、complex64、complex128等类型的变量。

### 常量定义
  
通过const关键字,你可以给字面常量指定一个友好的名字:
  
const Pi float64 = 3.14159265358979323846
  
const zero = 0.0
  
const u, v float32 = 0, 3
  
const a, b, c = 3, 4, "foo"//a=3,b=4,c="foo", 无类型整型和字符串常量

Go的常量定义可以限定常量类型,但不是必需的。如果定义常量时没有指定类型,那么它与字面常量一样,是无类型常量。常量定义的右值也可以是一个在编译期运算的常量表达式,比如：
  
const mask = 1 << 3

由于常量的赋值是一个编译期行为,所以右值不能出现任何需要运行期才能得出结果的表达式,比如试图以如下方式定义常量就会导致编译错误:
  
const Home = os.GetEnv("HOME")
  
原因很简单,os.GetEnv()只有在运行期才能知道返回结果,在编译期并不能确定,所以无法作为常量定义的右值。
  
预定义常量

Go语言预定义了这些常量:true、false和iota。iota比较特殊,可以被认为是一个可被编译器修改的常量,在每一个const关键字出现时被常量定义，

通过const关键字,你可以给字面常量指定一个友好的名字:

const Pi float64 = 3.14159265358979323846 // 无类型浮点常量// 无类型整型常量
  
const u, v float32 = 0, 3
  
const a, b, c = 3, 4, "foo"//a=3,b=4,c="foo", 无类型整型和字符串常量
  
const zero = 0.0

Go的常量定义可以限定常量类型,但不是必需的。如果定义常量时没有指定类型,那么它与字面常量一样,是无类型常量。常量定义的右值也可以是一个在编译期运算的常量表达式,比如
  
const mask = 1 << 3

由于常量的赋值是一个编译期行为,所以右值不能出现任何需要运行期才能得出结果的表达式,比如试图以如下方式定义常量就会导致编译错误:
  
const Home = os.GetEnv("HOME")

原因很简单,os.GetEnv()只有在运行期才能知道返回结果,在编译期并不能确定,所以重置为0,然后在下一个const出现之前,每出现一次iota,其所代表的数字会自动增1。从以下的例子可以基本理解iota的用法:
  
从以下的例子可以基本理解iota的用法:
  
const (
  
c0 = iota // iota被重设为0 // c0 == 0
  
c1 = iota // c1 == 1
  
c2 = iota // c2 == 2
  
）
  
const (
  
a = 1 << iota // a == 1 (iota在每个const开头被重设为0)
  
b = 1 << iota // b == 2
  
c = 1 << iota // c == 4
  
)

### goroutine

<http://www.wiloon.com/wordpress/?p=9101>

### 读环境变量

```golang
func main(){
    var JAVAHOME string
    JAVAHOME = os.Getenv("JAVA_HOME")
    fmt.Println(JAVAHOME)
}
```

### 废弃的函数

    // Deprecated
    func foo(){}

### command
        go env

## date time
    time.Now()
### 时间差
    t2.Sub(t1)

### sha256
     sum := sha256.Sum256([]byte("hello world\n"))