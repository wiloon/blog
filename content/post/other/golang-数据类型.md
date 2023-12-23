---
title: golang  数据类型
author: "-"
date: 2015-04-27T14:00:54+00:00
url: go/data-type
categories:
  - Go
tags:
  - reprint
---
## golang  数据类型

### 常量

```go

const ROOT_PATH = "/"
```

### Boolean

布尔值的类型为 bool，true或false，默认false

```go
var isActive bool  // 全局变量声明
var enabled, disabled = true, false  // 忽略类型的声明
func test() {
    var available bool  // 一般声明
    valid := false      // 简短声明
    available = true    // 赋值操作
}
```

## 数值类型

### 整数类型

整数类型有无符号和带符号两种。 Go同时支持int和uint，这两种类型的长度相同，但具体长度取决于不同编译器的实现。
Go里面也有直接定义好位数的类型:
rune, int8, int16, int32, int64和byte, uint8, uint16, uint32, uint64。

### 整数

```bash
    int8 (-128 -> 127)   
    int16 (-32768 -> 32767) 
    int32 (-2,147,483,648 -> 2,147,483,647)   
    int64 (-9,223,372,036,854,775,808 -> 9,223,372,036,854,775,807)   
```

### 无符号整数

```bash
    uint8 (0 -> 255)   
    uint16 (0 -> 65,535)   
    uint32 (0 -> 4,294,967,295)   
    uint64 (0 -> 18,446,744,073,709,551,615)   
    其中rune是int32的别称 byte是uint8的别称  
```

### 浮点数

浮点数的类型有float32和float64两种 (没有float类型) ，默认是float64。 (IEEE-754 标准)
  
应尽可能地使用 float64，因为 math 包中所有有关数学运算的函数都会要求接收这个类型。

float32 (+- 1e-45 -> +- 3.4 * 1e38)
  
float64 (+- 5 1e-324 -> 107 1e308)

### 复数

默认类型是 complex128 (64位实数+64位虚数) 。如果需要小一些的，也有complex64(32位实数+32位虚数)。
  
复数的形式为RE + IMi，其中RE是实数部分，IM是虚数部分，而最后的i是虚数单位。

var c1 complex64 = 5 + 10i
  
fmt.Printf("The value is: %v", c1)
  
// 输出:  5 + 10i
  
格式化说明符

在格式化字符串里，
  
%d 用于格式化整数 (%x 和 %X 用于格式化 16 进制表示的数字) ，
  
%g 用于格式化浮点型 (%f 输出浮点数，%e 输出科学计数表示法) ，
  
%0d 用于规定输出定长的整数，其中开头的数字 0 是必须的。

%n.mg 用于表示数字 n 并精确到小数点后 m 位，除了使用 g 之外，还可以使用 e 或者 f，例如: 使用格式化字符串 %5.2e 来输出 3.4 的结果为 3.40e+00。

### 字符串 string

字符串就是一串固定长度的字符连接起来的字符序列。Go的字符串是由单个字节连接起来的。也就是说对于传统的字符串是由字符组成的，而Go的字符串不同，它是由字节组成的。

Go语言的字符串的字节使用UTF-8编码标识Unicode文本。
  
字符串的表示很简单，用双引号("")或者反引号 (\`) 来创建. 例如: "hello world" 或者 \`hello world\`。

两者的区别: 双引号之间的转义符会被转义，而反引号之间的字符保持不变。

```Go
// 示例代码

var frenchHello string // 声明变量为字符串的一般方法

var emptyString string = "" // 声明了一个字符串变量，初始化为空字符串

func test() {

no, yes, maybe := "no", "yes", "maybe" // 简短声明，同时声明多个变量

japaneseHello := "Konichiwa" // 同上

frenchHello = "Bonjour" // 常规赋值

}
  
s := "hello"
  
c := []byte(s) // 将字符串 s 转换为 []byte 类型
  
c[0] = 'c'
  
s2 := string(c) // 再转换回 string 类型
  
fmt.Printf("%s\n", s2)
```

### string > []byte

```go
[]byte("Here is a string....")
```

### byte -- uint8, rune -- int32

byte和rune特殊类型是别名

byte就是unit8的别名
  
rune就是int32的别名

int和uint取决于操作系统 (32位机器上就是32字节，64位机器上就是64字节)

uint是32字节或者64字节
  
int和uint是一样的大小

[http://studygolang.com/articles/9852](http://studygolang.com/articles/9852)

golang的字符称为rune，等价于C中的char，可直接与整数转换

```bash
    var c rune='a' 
    var i int =98
    i1:=int(c)
    fmt.Println("'a' convert to",i1)
    c1:=rune(i)
    fmt.Println("98 convert to",string(c1))

    //string to rune
    for _, char := range []rune("世界你好") {
        fmt.Println(string(char))
    }
```

rune实际是整型，必需先将其转换为string才能打印出来，否则打印出来的是一个整数

c:='a'
fmt.Println(c)
fmt.Println(string(c))
fmt.Println(string(97))
输出

97
a
a

>[https://segmentfault.com/q/1010000000404709](https://segmentfault.com/q/1010000000404709)

## byte

```go
var foo byte
foo:=byte('A')
foo:=byte('\x00')
```

### rune, uint8, byte

Go语言的字符有以下两种：
一种是 uint8 类型，或者叫 byte 型，代表了 ASCII 码的一个字符。
另一种是 rune 类型，代表一个 UTF-8 字符，当需要处理中文、日文或者其他复合字符时，则需要用到 rune 类型。rune 类型等价于 int32 类型。

byte 类型是 uint8 的别名，对于只占用 1 个字节的传统 ASCII 编码的字符来说，完全没有问题，例如 var ch byte = 'A'，字符使用单引号括起来。

在 ASCII 码表中，A 的值是 65，使用 16 进制表示则为 41，所以下面的写法是等效的：
var ch byte = 65 或 var ch byte = '\x41'      // (\x 总是紧跟着长度为 2 的 16 进制数）

另外一种可能的写法是\后面紧跟着长度为 3 的八进制数，例如 \377。

Go语言同样支持 Unicode (UTF-8），因此字符同样称为 Unicode 代码点或者 runes，并在内存中使用 int 来表示。在文档中，一般使用格式 U+hhhh 来表示，其中 h 表示一个 16 进制数。

在书写 Unicode 字符时，需要在 16 进制数之前加上前缀\u或者\U。因为 Unicode 至少占用 2 个字节，所以我们使用 int16 或者 int 类型来表示。如果需要使用到 4 字节，则使用\u前缀，如果需要使用到 8 个字节，则使用\U前缀。
var ch int = '\u0041'
var ch2 int = '\u03B2'
var ch3 int = '\U00101234'
fmt.Printf("%d - %d - %d\n", ch, ch2, ch3) // integer
fmt.Printf("%c - %c - %c\n", ch, ch2, ch3) // character
fmt.Printf("%X - %X - %X\n", ch, ch2, ch3) // UTF-8 bytes
fmt.Printf("%U - %U - %U", ch, ch2, ch3)   // UTF-8 code point
输出：
65 - 946 - 1053236
A - β - r
41 - 3B2 - 101234
U+0041 - U+03B2 - U+101234

格式化说明符%c用于表示字符，当和字符配合使用时，%v或%d会输出用于表示该字符的整数，%U输出格式为 U+hhhh 的字符串。

Unicode 包中内置了一些用于测试字符的函数，这些函数的返回值都是一个布尔值，如下所示 (其中 ch 代表字符）：
判断是否为字母：unicode.IsLetter(ch)
判断是否为数字：unicode.IsDigit(ch)
判断是否为空白符号：unicode.IsSpace(ch)
UTF-8 和 Unicode 有何区别？
Unicode 与 ASCII 类似，都是一种字符集。

字符集为每个字符分配一个唯一的 ID，我们使用到的所有字符在 Unicode 字符集中都有一个唯一的 ID，例如上面例子中的 a 在 Unicode 与 ASCII 中的编码都是 97。汉字“你”在 Unicode 中的编码为 20320，在不同国家的字符集中，字符所对应的 ID 也会不同。而无论任何情况下，Unicode 中的字符的 ID 都是不会变化的。

UTF-8 是编码规则，将 Unicode 中字符的 ID 以某种方式进行编码，UTF-8 的是一种变长编码规则，从 1 到 4 个字节不等。编码规则如下：
0xxxxxx 表示文字符号 0～127，兼容 ASCII 字符集。
从 128 到 0x10ffff 表示其他字符。

根据这个规则，拉丁文语系的字符编码一般情况下每个字符占用一个字节，而中文每个字符占用 3 个字节。

广义的 Unicode 指的是一个标准，它定义了字符集及编码规则，即 Unicode 字符集和 UTF-8、UTF-16 编码等。

>[http://c.biancheng.net/view/18.html](http://c.biancheng.net/view/18.html)

## 值类型， 引用类型

值类型分别有：int 系列、float 系列、bool、string、array/数组和结构体

引用类型有：指针、slice/切片、管道/channel、接口/interface、map、函数等

值类型的特点是：变量直接存储值，内存通常在栈中分配

引用类型的特点是：变量存储的是一个地址，这个地址对应的空间里才是真正存储的值，内存通常在堆中分配

>[https://www.jianshu.com/p/9be895c65684?utm_campaign=studygolang.com&utm_medium=studygolang.com&utm_source=studygolang.com](https://www.jianshu.com/p/9be895c65684?utm_campaign=studygolang.com&utm_medium=studygolang.com&utm_source=studygolang.com)
