---
title: go basic, golang basic
author: "-"
date: 2022-12-11 12:07:50
url: go
categories:
  - Go
tags:
  - reprint
  - remix
---
## go basic, golang basic

The Go Programming Language, Go 语言虽然是静态编译型语言, 但是它却拥有脚本化的语法, 支持多种编程范式(函数式和面向对象)。

Go 是 Google 开发的一种静态强类型、编译型、并发型, 并具有垃圾回收功能的编程语言。 罗伯特·格瑞史莫, 罗勃·派克及肯·汤普逊于 2007年9月开始设计 Go, 稍后 Ian Lance Taylor, Russ Cox 加入项目。 Go 是基于 Inferno 操作系统所开发的。
Go 语言是静态类型的编程语言

## go source code

[https://github.com/golang/go](https://github.com/golang/go)

## version

- latest: 1.23.0
- current: 1.17.7

## install

```Bash
# macos
brew search golang
brew upgrade golang
```

### hello world

```go
package main
import "fmt"
func main() {
    fmt.Println("hello world")
}
```

```bash
go run hello-world.go
go build hello-world.go
./hello-world
```

## 升级依赖包版本, upgrade package version

```bash
go list -m all|grep redis
# go list 返回: github.com/redis/go-redis/v9 v9.0.2

# 升级 go-redis 版本
go get -u github.com/redis/go-redis/v9
# -u The -u flag instructs get to update modules providing dependencies of packages named on the command line 
# to use newer minor or patch releases when available.

# 不带 -u 的 go get 在发现依赖包已经存在的时候不会更新, 加 -u 参数会检查依赖包是否有更新然后下载新版本.
# 升级 go-redis 到 9.0.4
go get -u github.com/redis/go-redis/v9@v9.0.4
```

- -u 更新包，包括他们的依赖项
- -v 输出详细信息

[http://studygolang.com/articles/1941](http://studygolang.com/articles/1941)
  
[https://gobyexample.com/hello-world](https://gobyexample.com/hello-world)

### math

```go
float64 保留2位小数
value, _ = strconv.ParseFloat(fmt.Sprintf("%.2f", value), 64)
func Dim(x, y float64) float64
函数返回x-y和0中的最大值
```

### go process, exec

```bash
https://colobu.com/2020/12/27/go-with-os-exec/
```

### commands

```bash
go get -u xorm.io/xorm
go run -race cmd.go // 竞态检测
```

### install

china mainland download
[https://golang.google.cn/](https://golang.google.cn/)

#### ubuntu

```bash
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt update
sudo apt install golang-go
```

#### windows

```bash
winget install GoLang.Go
```

### 环境变量

```bash
# gopath bin
export PATH="$PATH:$(go env GOPATH)/bin"

# 设置不走 proxy 的私有仓库,多个用逗号相隔 (可选) 
export GOPRIVATE=*.corp.example.com
export GOPRIVATE=git.wiloon.com

# todo, deprecated
export GOROOT=/root/go
export GOPATH=/root/gopath
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
export GOBIN=/path/to/go/bin

```

### internal package

Go 语言 1.4 版本增加了 Internal packages 特征用于控制包的导入, 即internal package只能被特定的包导入。
内部包的规范约定: 导出路径包含internal关键字的包, 只允许internal的父级目录及父级目录的子包导入, 其它包无法导入。

### 变量

变量是几乎所有编程语言中最基本的组成元素。从根本上说,变量相当于是对一块数据存储空间的命名,程序可以通过定义一个变量来申请一块数据存储空间,之后可以通过引用变量名来使用这块存储空间。
  
Go语言中的变量使用方式与C语言接近,但具备更大的灵活性。

#### 变量声明

Go语言的变量声明方式与C和C++语言有明显的不同。对于纯粹的变量声明,Go语言引入了关键字var,而类型信息放在变量名之后,示例如下:

```go
var v1 int
var foo, bar int
var width, height = 100, 50
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

对于声明变量时需要进行初始化的场景,var关键字可以保留,但不再是必要的元素,如下:

```go
var v1 int = 10 // 正确的使用方式1
var v2 = 10 // 正确的使用方式2,编译器可以自动推导出v2的类型
v3 := 10 // 正确的使用方式3,编译器可以自动推导出v3的类型
```

以上三种用法的效果是完全一样的。与第一种用法相比,第三种用法需要输入的字符数大大减少,是懒程序员和聪明程序员的最佳选择。这里Go语言也引入了另一个C和C++中没有的符号 (冒号和等号的组合:=),用于明确表达同时进行变量声明和初始化的工作 。
指定类型已不再是必需的,Go编译器可以从初始化表达式的右值推导出该变量应该声明为 4
哪种类型,这让Go语言看起来有点像动态类型语言,尽管Go语言实际上是 不折不扣 的强类型语言(静态类型语言)。
当然,出现在:=左侧的变量不应该是已经被声明过的,否则会导致编译错误,比如下面这个 :
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
  
_,_, nickName := "May", "Chan", "Chibi Maruko"

## 常量

```go
const (
c0 = iota // iota被重设为0 // c0 == 0
c1 = iota // c1 == 1
c2 = iota // c2 == 2
) 
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

Go的常量定义可以限定常量类型,但不是必需的。如果定义常量时没有指定类型,那么它与字面常量一样,是无类型常量。常量定义的右值也可以是一个在编译期运算的常量表达式,比如:
  
const mask = 1 << 3

由于常量的赋值是一个编译期行为,所以右值不能出现任何需要运行期才能得出结果的表达式,比如试图以如下方式定义常量就会导致编译错误:
  
const Home = os.GetEnv("HOME")
  
原因很简单,os.GetEnv()只有在运行期才能知道返回结果,在编译期并不能确定,所以无法作为常量定义的右值。
  
预定义常量

Go语言预定义了这些常量:true、false和iota。iota比较特殊,可以被认为是一个可被编译器修改的常量,在每一个const关键字出现时被常量定义,

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
  
)
  
const (
  
a = 1 << iota // a == 1 (iota在每个const开头被重设为0)
  
b = 1 << iota // b == 2
  
c = 1 << iota // c == 4
  
)

### 读环境变量

```go
func main(){
    var JAVAHOME string
    JAVAHOME = os.Getenv("JAVA_HOME")
    fmt.Println(JAVAHOME)
}
```

### 废弃的函数

```bash
// Deprecated
func foo(){}
```

## go env

### 查看go语言的环境变量

```bash
go env
```

### 设置 go env

```bash
go env -w GO111MODULE=on
```

## date time

```bash
time.Now()
```

### 时间差

```bash
t2.Sub(t1)
```

### sha256

```bash
sum := sha256.Sum256([]byte("hello world\n"))
```

### csv

[https://cloud.tencent.com/developer/article/1059643](https://cloud.tencent.com/developer/article/1059643)

### go build

- -o, 指定输出文件 路径/文件名 `go build -o /tmp/foo foo.go`

```bash
# -a
强行对所有涉及到的代码包 (包含标准库中的代码包) 进行重新构建, 即使它们已经是最新的了。
# -installsuffix
为了使当前的输出目录与默认的编译输出目录分离,可以使用这个标记。此标记的值会作为结果文件的父目录名称的后缀。其实,如果使用了-race标记,这个标记会被自动追加且其值会为race。如果我们同时使用了-race标记和-installsuffix,那么在-installsuffix标记的值的后面会再被追加_race,并以此来作为实际使用的后缀。
# -x
打印详细信息
# -n
查看具体操作,不执行
# -i
安装归档文件
# -v
查看编译的代码包名称
# -o
指定输出文件 路径/文件名 `go build -o /tmp/foo foo.go`
# glibc 静态编译
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags '-s -w --extldflags "-static -fpic"' -o "$binPath" "$name.go"
# -ldflags="-s -w" -s: 忽略符号表和调试信息。-w: 忽略 DWARF 调试信息，使用该选项后将无法使用gdb进行调试。
# remove the symbol and debug info with go build -ldflags "-s -w".
go build -ldflags="-s -w" main.go 

```

```bash
#查看 golang 环境变量
go env
# 查看 Go 支持 OS 和平台列表
go tool dist list

# go mod initialize a new module
go mod init github.com/you/hello
```

## Go 交叉编译, go cross compile

设置 GOOS 和 GOARCH 两个环境变量生成所需平台的 Go 程序

常用的一些值

### GOOS

- darwin
- windows
- linux

### GOARCH

- amd64
- arm64

```bash
# windows, amd64
GOOS=windows GOARCH=amd64 go build foo.go
# 目标系统 linux
GOOS=linux GOARCH=amd64 go build foo.go
```

## conditional compilation, 条件编译

windows 环境编译时忽略标注 `//go:build linux` 的文件

```go
//go:build darwin || linux

```

### macos M2 编译 linux amd64

```bash
brew tap messense/macos-cross-toolchains
brew install x86_64-unknown-linux-gnu

export CC=x86_64-unknown-linux-gnu-gcc
export CXX=x86_64-unknown-linux-gnu-g++
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build -o ${package_name} enx-api.go

```

### go install

go install 可忽略当前目录或上层目录的 go.mod 文件,这对于在不影响主模块依赖的情况下，安装二进制很方便；
go install 被设计为“用于构建和安装二进制文件”， go get 则被设计为 “用于编辑 go.mod 变更依赖”，并且使用时，应该与 -d 参数共用，在将来版本中 -d 可能会默认启用；
如果你在模块目录中，并且你不带 @version 执行安装的话，只能安装 go.mod 中已经包含的版本。并且不能安装未出现在 go.mod 中的包。
与build命令相比, install命令在编译源码后还会将可执行文件或库文件安装到约定的目录下。

go install 编译出的可执行文件以其所在目录名(DIR)命名
  
go install 将可执行文件安装到与src同级别的bin目录下,bin目录由go install自动创建
  
go install 将可执行文件依赖的各种package编译后,放在与src同级别的pkg目录下.

[http://tonybai.com/2012/08/17/hello-go/](http://tonybai.com/2012/08/17/hello-go/)

```bash
go install github.com/wiloon/pingd-proxy@v0.0.1
```

### 一个函数可以作为参数传递给另一个函数

```go
package main

import "fmt"

func dd(i func(int, int) int) int {
    fmt.Printf("i type: %T\n", i)
    return i(1, 2)
}

func main() {
    ee := func(x, y int) int {
        return x + y
    }
    fmt.Printf("ee type: %T\n", ee)
    fmt.Println(dd(ee))
}
```

### humanize

github.com/dustin/go-humanize

---

[https://cyent.github.io/golang/datatype/funcvalue_parameter/](https://cyent.github.io/golang/datatype/funcvalue_parameter/)

## release notes

### 1.17

[https://tip.golang.org/doc/go1.17](https://tip.golang.org/doc/go1.17)

### Go 程序是怎样跑起来的

[https://zhuanlan.zhihu.com/p/71993748](https://zhuanlan.zhihu.com/p/71993748)

### go 程序启动过程

[https://juejin.cn/post/6942509882281033764](https://juejin.cn/post/6942509882281033764)

## golang install

GOPATH:

linux:
  
```bash

mkdir -p /home/wiloon/my-projects/golang/lib/

mkdir -p /home/wiloon/my-projects/golang/projects/

export GOPATH="/home/wiloon/my-projects/golang/lib/:/home/wiloon/my-projects/golang/projects/"

#check golang version
  
go version
  
```

windows:
  
GOPATH=C:\workspace\myproject\golang\lib;C:\workspace\myproject\golang\gox

[https://moelove.info/2020/12/19/Go-1.16-%E4%B8%AD%E5%85%B3%E4%BA%8E-go-get-%E5%92%8C-go-install-%E4%BD%A0%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E7%9A%84%E5%9C%B0%E6%96%B9/](https://moelove.info/2020/12/19/Go-1.16-%E4%B8%AD%E5%85%B3%E4%BA%8E-go-get-%E5%92%8C-go-install-%E4%BD%A0%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E7%9A%84%E5%9C%B0%E6%96%B9/)

### 查看 golang 文档

```bash
    go doc io.EOF
```

### os.Exit()

Conventionally, code zero indicates success, non-zero an error

### 选择器

在 Go 语言中，表达式 foo.bar 可能表示两件事。如果 foo 是一个包名，那么表达式就是一个所谓的限定标识符，用来引用包 foo 中的导出的标识符。由于它只用来处理导出的标识符，bar 必须以大写字母开头(译注：如果首字母大写，则可以被其他的包访问；如果首字母小写，则只能在本包中使用）：

package foo
import "fmt"
func Foo() {
    fmt.Println("foo")
}
func bar() {
    fmt.Println("bar")
}

package main
import "github.com/mlowicki/foo"
func main() {
    foo.Foo()
}
这样的程序会工作正常。但是 (主函数）调用 foo.bar() 会在编译时报错 —— cannot refer to unexported name foo.bar(无法引用未导出的名称 foo.bar)。

如果 foo 不是 一个包名，那么 foo.bar 就是一个选择器表达式。它访问 foo 表达式的字段或方法。点之后的标识符被称为 selector (选择器）。关于首字母大写的规则并不适用于这里。它允许从定义了 foo 类型的包中选择未导出的字段或方法：

package main
import "fmt"
type T struct {
    age byte
}
func main() {
    fmt.Println(T{age: 30}.age)
}
该程序打印：30

[https://studygolang.com/articles/14628](https://studygolang.com/articles/14628)

## 复合字面量

```go
var numbers = [1, 2, 3, 4]
var thing = {name: "Raspberry Pi", generation: 2, model: "B"}
// 复合字面量: name: "Raspberry Pi", generation: 2, model: "B"
```

```go
type location struct {
    lat, long float64
}

opportunity := location{lat: -1.9462, long: 354.4734}
// 复合字面量: lat: -1.9462, long: 354.4734
fmt.Println(opportunity)

insight := location{lat: 4.5, long: 135.9}
fmt.Println(insight)

```

```go
spirit := location{-14.5684, 175.472636}
// 复合字面量: -14.5684, 175.472636
fmt.Println(spirit)

```

[https://studygolang.com/articles/12913](https://studygolang.com/articles/12913)

[https://livebook.manning.com/concept/go/composite-literal](https://livebook.manning.com/concept/go/composite-literal)

### is pointer to interface, not interface

 执行下面代码会出现”type *net.Conn is pointer to interface, not interface)“错误，原因是因为”net.Conn”是interface而不是struct，不能用指针方式传递。

1    func connHandler(client *net.Conn) {
2        // do something
3    }
4
5    func somefunc() {
6        // ...
7        client, _ := listener.Accept()
8        connHandler(&client)
9    }
GO语言中interface是一种特殊的数据结构，包含两部分内容：

一个指向方法表的指针
一个指向实际数据的指针
interface

因为这种特殊的数据结构所以interface的指针指向的结构既没有实际数据也没有对应方法，那么就无法直接访问所需的内容，鉴于此原因我推测GO语言的开发者直接屏蔽掉了指向interface指针的用法。这种情况的正确如下：

1    func connHandler(client net.Conn) {
2        // do something
3    }
4
5    func somefunc() {
6        // ...
7        client, _ := listener.Accept()
8        connHandler(client)
9    }

[http://www.singleye.net/2017/11/go%E8%AF%AD%E8%A8%80%E7%BC%96%E7%A8%8B%E9%99%B7%E9%98%B1/](http://www.singleye.net/2017/11/go%E8%AF%AD%E8%A8%80%E7%BC%96%E7%A8%8B%E9%99%B7%E9%98%B1/)

## range

```go
for pos, char := range str {
    ...
}

```

## 创建长度为0的slice时发生了什么

## gofmt

```bash
gofmt -w foo.go
# -w    write result to (source) file instead of stdout
```

## Go 匿名函数

### 函数定义

```go
func(参数列表)(返回参数列表){
    函数体
}
```

### 在定义时调用匿名函数

```go
func(data int) {
    fmt.Println("hello", data)
}(100)
```

### 匿名函数赋值给变量

```go

// 将匿名函数体保存到f()中
f := func(data int) {
    fmt.Println("hello", data)
}
// 使用f()调用
f(100)

```

[http://c.biancheng.net/view/57.html](http://c.biancheng.net/view/57.html)

## go, url encode, query escape

func QueryEscape(s string) string

```go
package main

import (
    "fmt"
    "net/url"
)

func main() {
    s := "this will be esc@ped!"
    fmt.Println("http://example.com/say?message="+url.QueryEscape(s))
}

```

## if

if 可以包含一个初始化语句（如：给一个变量赋值）。这种写法具有固定的格式（在初始化语句后方必须加上分号）

```go
if initialization; condition {
    // do something
}
```

例如:

```go
val := 10
if val > max {
    // do something
}
```

你也可以这样写:

```go
if val := 10; val > max {
    // do something
}
```

————————————————
原文作者：Go 技术论坛文档：《Go 入门指南（）》
转自链接：[https://learnku.com/docs/the-way-to-go/if-else-structure/3592](https://learnku.com/docs/the-way-to-go/if-else-structure/3592)
版权声明：翻译文档著作权归译者和 LearnKu 社区所有。转载请保留原文链接

## golang, redis

[https://github.com/redis/go-redis](https://github.com/redis/go-redis)

## upx 压缩

upx 是一种加壳的操作, 可能会被杀毒软件识别成病毒

```bash
# archlinux
pacman -Sy upx
```

upx 是一个常用的压缩动态库和可执行文件的工具，通常可减少 50-70% 的体积。

upx 压缩后的程序和压缩前的程序一样，无需解压仍然能够正常地运行，这种压缩方法称之为带壳压缩，压缩包含两个部分：

在程序开头或其他合适的地方插入解压代码；
将程序的其他部分压缩。
执行时，也包含两个部分：

首先执行的是程序开头的插入的解压代码，将原来的程序在内存中解压出来；
再执行解压后的程序。
也就是说，upx 在程序执行时，会有额外的解压动作，不过这个耗时几乎可以忽略。

如果对编译后的体积没什么要求的情况下，可以不使用 upx 来压缩。一般在服务器端独立运行的后台服务，无需压缩体积。

[https://github.com/upx/upx](https://github.com/upx/upx)

```bash
# 压缩率，1-9，1 代表最低压缩率，9 代表最高压缩率。
upx -9 foo.exe
```

go build 不加参数编译出的 .exe 大小: 10,688,000B, 加编译参数 -ldflags="-s -w" 之后 7,797,760B, upx -9 之后 2,755,072B.

## log

```go
import (
 "log"
 "testing"
)

func Test0(t *testing.T) {
 foo := "params0"
 log.Println("test:", foo)
}
// 2023/11/15 14:14:23 test: params0
// Spaces are always added between operands and a newline is appended.
```

## go tool

一些 golang 提供的工具, 比如 objdump, pprof; 不带参数执行 `go tool` 会打印工具列表

```Bash
# golang 编译为汇编代码
#-N    disable optimizations
#-l    disable inlining
#-S    print assembly listing
go tool compile -N -l -S main.go
go tool objdump -S -s "main.main" main64.exe
```

## check weather linux or windows

```Go
package main
 
import (
	"runtime"
	"fmt"
)
 
func main() {
    sysType := runtime.GOOS
 
    if sysType == 'linux' {
       // LINUX系统
    } 
 
    if sysType == 'windows' {
        // windows系统
    }
}
```

## go 1.22

https://www.51cto.com/article/777578.html

https://zhuanlan.zhihu.com/p/673906980

## exec Shell command

```Bash
cmd := exec.Command("/bin/sh", "-c", "sudo find ...")
```