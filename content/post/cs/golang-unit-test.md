---
title: Go unit test, 单体测试
author: "-"
date: 2016-07-13T00:45:41+00:00
url: go/test
categories:
  - Go
tags:
  - reprint
  - remix
  - test
---
## Go unit test, 单体测试

执行某一个测试文档

```bash
go test foo_test.go
go test -v foo_test.go

# 执行某一个文件中的某一个或几个函数
go test path/to/foo_test.go -run "^TestFunc0$"
```

Go 语言推荐测试文件和源代码文件放在一块，测试文件以 _test.go 结尾。比如，当前 package 有 calc.go 一个文件，我们想测试 calc.go 中的 Add 和 Mul 函数，那么应该新建 calc_test.go 作为测试文件。

### calc_test.go

```go

package main

import "testing"

func TestAdd(t *testing.T) {
    t.Log("test foo")
    if ans := Add(1, 2); ans != 3 {
        t.Errorf("1 + 2 expected be 3, but %d got", ans)
    }

    if ans := Add(-10, -20); ans != -30 {
        t.Errorf("-10 + -20 expected be -30, but %d got", ans)
    }
}
```

测试用例名称一般命名为 Test 加上待测试的方法名。
测试用的参数有且只有一个, 在这里是 t *testing.T

基准测试 (benchmark) 的参数是 `*testing.B`, TestMain 的参数是 *testing.M 类型。

运行 `go test`, 该 package 下所有的测试用例都会被执行。

`go test -v`, -v 参数会显示每个用例的测试结果，另外 `-cover` 参数可以查看覆盖率。

如果只想运行其中的一个用例, 例如 TestAdd, 可以用 -run 参数指定, 该参数支持通配符 *, 和部分正则表达式，例如 ^, $

$ go test -run TestAdd -v
=== RUN   TestAdd
--- PASS: TestAdd (0.00s)
PASS
ok      example 0.007s

### 子测试(Subtests)

```go
// calc_test.go

func TestMul(t *testing.T) {
    t.Run("pos", func(t *testing.T) {
        if Mul(2, 3) != 6 {
            t.Fatal("fail")
        }

    })
    t.Run("neg", func(t *testing.T) {
        if Mul(2, -3) != -6 {
            t.Fatal("fail")
        }
    })
}

```

之前的例子测试失败时使用 t.Error/t.Errorf，这个例子中使用 t.Fatal/t.Fatalf，区别在于前者遇错不停，还会继续执行其他的测试用例，后者遇错即停。

### table-driven tests

```go
//  calc_test.go
func TestMul(t *testing.T) {
    cases := []struct {
        Name           string
        A, B, Expected int
    }{
        {"pos", 2, 3, 6},
        {"neg", 2, -3, -6},
        {"zero", 2, 0, 0},
    }

    for _, c := range cases {
        t.Run(c.Name, func(t *testing.T) {
            if ans := Mul(c.A, c.B); ans != c.Expected {
                t.Fatalf("%d * %d expected %d, but %d got",
                    c.A, c.B, c.Expected, ans)
            }
        })
    }
}

```

### 帮助函数(helpers)

### setup 和 teardown

### Benchmark 基准测试

---

测试文件用 "_test" 结尾,测试的函数用Test开头

fibonacci.go
  
fibonacci_test.go

单元测试文件必须遵守下面原则:
  
文件名必须是_test.go结尾,这样执行go test的时候才会执行到相应的代码
  
必须import testing这个包
  
所有测试函数必须是Test开头
  
测试用例会按照源代码中写的顺序依次执行
  
测试函数的参数是testing.T,我们可以使用该类型来记录错误或者是测试状态
  
测试函数格式: *func TestXxx(t testing.T),Xxx部分可以任意字母数字的组合,但是首字母不能是小写
  
函数中通过调用testing.T 的Error,Errorf,FailNow,Fatal,FatalIf方法,说明测试不通过,调用Log方法来记录测试信息

```go
package gotest

import (
    "testing"
)

func Test_Division_1(t *testing.T) {
    if i, e := Division(6, 2); i != 3 || e != nil { //try a unit test on function
        t.Error("除法函数测试没通过") // 如果不是如预期的那么就报错
    } else {
        t.Log("第一个测试通过了") //记录一些你期望记录的信息
    }
}

func Test_Division_2(t *testing.T) {
    t.Error("就是不通过")
}
```

如何编写压力测试
  
压力测试用来检测函数的性能的,和编写单元功能的测试的方法类似,压力测试必须注意以下几点:

压力测试用例必须遵循如下格式,其中XXX可以是任意字母数字组合,但是首字母不能是小写字母

func BenchmarkXXX(b _testing.B) { ... }
  
go test不会默认执行压力测试的函数,如果要执行压力测试需要带上参数-test.bench,语法: -test.bench="test_name_regex",例如go test.bench="."_ 表示测试全部的压力测试函数
  
在压力测试用例中,请记得在循环体内使用testing.B.N,以使测试可以正常运行
  
文件名也必须是以_test.go结尾
  
新建压力测试文件webbench_test.go,代码如下所示:

func Benchmark_Division(b *testing.B) {

for i := 0; i < b.N; i++ { //use b.N for looping

Division(4, 5)

}
  
}

func Benchmark_TimeConsumingFunction(b *testing.B) {

b.StopTimer() //调用该函数停止压力测试的时间计数

//做一些初始化的工作,例如读取文件数据,数据库连接之类的,

//这样这些时间不影响我们测试函数本身的性能

b.StartTimer() //重新开始时间

for i := 0; i < b.N; i++ {

Division(4, 5)

}
  
}

```bash
go test -test.bench=".*"
#使用-count可以指定执行多少次
go test -test.bench=".*" -count=5
```

作者: Carrism
  
链接: [https://www.jianshu.com/p/41cdfd4a5707](https://www.jianshu.com/p/41cdfd4a5707)
  
来源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

[http://www.01happy.com/golang-unit-testing/](http://www.01happy.com/golang-unit-testing/)

一般为了保证整个系统的稳定性,通常都需要编写大量的单元测试,诸如像java的junit,php的phpunit等都提供了类似的功能。golang中的testing包提供了这个测试的功能,结合go test工具搞起来就很方便了。

golang中的单元测试不单有功能测试,也还提供了性能测试,非常给力。

功能测试
  
在golang的src目录下新建目录math,测试目录结构如下:

golang单元测试目录
  
fibonacci.go代码如下,主要有一个Fibonacci函数
  
package lib

//斐波那契数列
  
//求出第n个数的值
  
func Fibonacci(n int64) int64 {
  
if n < 2 {
  
return n
  
}
  
return Fibonacci(n-1) + Fibonacci(n-2)
  
fibonacci_test.go就是测试的文件了,golang需要测试文件一律用"_test"结尾,测试的函数都用Test开头,代码如下:
  
package lib

import (
  
"testing"
  
)

func TestFibonacci(t *testing.T) {
  
r := Fibonacci(10)
  
if r != 55 {
  
t.Errorf("Fibonacci(10) failed. Got %d, expected 55.", r)
  
}
  
}
  
使用go test测试这个程序

$ go test lib
  
ok lib 0.008s
  
如果提示找不到包,则将该代码路径加入环境变量GOPATH就可以了。

can't load package: package lib: cannot find package "lib" in any of:
  
性能测试
  
结合上面的方法,这里测试一下函数的性能,如果需要进行性能测试,则函数开头使用Benchmark就可以了。

//性能测试
  
func BenchmarkFibonacci(b *testing.B) {
  
for i := 0; i < b.N; i++ {
  
Fibonacci(10)
  
}
  
}
  
接下来执行这个性能测试:

$ go test -bench=. lib
  
PASS
  
BenchmarkFibonacci 5000000 436 ns/op
  
ok lib 2.608s
  
其中第二行输出表示这个函数运行了5000000次,平均运行一次的时间是436ns。

这个性能测试只测试参数为10的情况。如果有需要可以测试多个参数:

//测试参数为5的性能
  
func BenchmarkFibonacci5(b *testing.B) {
  
for i := 0; i < b.N; i++ {
  
Fibonacci(5)
  
}
  
}

//测试参数为20的性能
  
func BenchmarkFibonacci20(b *testing.B) {
  
for i := 0; i < b.N; i++ {
  
Fibonacci(20)
  
}
  
}
  
运行一下:

$ go test -bench=. lib
  
PASS
  
BenchmarkFibonacci 5000000 357 ns/op
  
BenchmarkFibonacci5 100000000 29.5 ns/op
  
BenchmarkFibonacci20 50000 44688 ns/op
  
ok lib 7.824s
  
如果性能测试的方法非常多,那需要的时间就会比较久。可以通过-bench=参数设置需要运行的性能测试行数:

```go
go test -bench=Fibonacci20 lib
  
PASS
  
BenchmarkFibonacci20 50000 44367 ns/op
  
ok lib 2.677s
```

[https://geektutu.com/post/quick-go-test.html](https://geektutu.com/post/quick-go-test.html)

[https://hedzr.com/golang/testing/golang-testing-1/](https://hedzr.com/golang/testing/golang-testing-1/)


## 命令行参数

https://siongui.github.io/2017/04/28/command-line-argument-in-golang-test/

```Go
package goef

import (
      "flag"
      "testing"
)

var pkgdir = flag.String("pkgdir", "", "dir of package containing embedded files")

func TestGenerateGoPackage(t *testing.T) {
      t.Log(*pkgdir)
}
```

```Bash
$ export PKGDIR=${GOPATH}/src/github.com/siongui/myvfs
$ go test -v embed.go buildpkg.go buildpkg_test.go -args -pkgdir=${PKGDIR}
```