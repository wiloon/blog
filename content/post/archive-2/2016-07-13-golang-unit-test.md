---
title: golang unit test
author: w1100n
type: post
date: 2016-07-13T00:45:41+00:00
url: /?p=9130
categories:
  - Uncategorized

---
测试文件用 "_test" 结尾，测试的函数用Test开头

fibonacci.go
  
fibonacci_test.go

单元测试文件必须遵守下面原则: 
  
文件名必须是_test.go结尾，这样执行go test的时候才会执行到相应的代码
  
必须import testing这个包
  
所有测试函数必须是Test开头
  
测试用例会按照源代码中写的顺序依次执行
  
测试函数的参数是testing.T,我们可以使用该类型来记录错误或者是测试状态
  
测试函数格式: *func TestXxx(t testing.T),Xxx部分可以任意字母数字的组合，但是首字母不能是小写
  
函数中通过调用testing.T 的Error，Errorf，FailNow,Fatal,FatalIf方法，说明测试不通过，调用Log方法来记录测试信息

```golang
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
  
压力测试用来检测函数的性能的，和编写单元功能的测试的方法类似，压力测试必须注意以下几点: 

压力测试用例必须遵循如下格式，其中XXX可以是任意字母数字组合，但是首字母不能是小写字母
   
func BenchmarkXXX(b _testing.B) { ... }
  
go test不会默认执行压力测试的函数，如果要执行压力测试需要带上参数-test.bench,语法: -test.bench="test_name_regex",例如go test.bench="."_ 表示测试全部的压力测试函数
  
在压力测试用例中，请记得在循环体内使用testing.B.N，以使测试可以正常运行
  
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
  
链接: https://www.jianshu.com/p/41cdfd4a5707
  
来源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

http://www.01happy.com/golang-unit-testing/

一般为了保证整个系统的稳定性，通常都需要编写大量的单元测试，诸如像java的junit，php的phpunit等都提供了类似的功能。golang中的testing包提供了这个测试的功能，结合go test工具搞起来就很方便了。

golang中的单元测试不单有功能测试，也还提供了性能测试，非常给力。

功能测试
  
在golang的src目录下新建目录math，测试目录结构如下: 

golang单元测试目录
  
fibonacci.go代码如下，主要有一个Fibonacci函数
  
package lib

//斐波那契数列
  
//求出第n个数的值
  
func Fibonacci(n int64) int64 {
  
if n < 2 {
  
return n
  
}
  
return Fibonacci(n-1) + Fibonacci(n-2)
  
fibonacci_test.go就是测试的文件了，golang需要测试文件一律用"_test"结尾，测试的函数都用Test开头，代码如下: 
  
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
  
如果提示找不到包，则将该代码路径加入环境变量GOPATH就可以了。

can't load package: package lib: cannot find package "lib" in any of:
  
性能测试
  
结合上面的方法，这里测试一下函数的性能，如果需要进行性能测试，则函数开头使用Benchmark就可以了。

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
  
其中第二行输出表示这个函数运行了5000000次，平均运行一次的时间是436ns。

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
  
如果性能测试的方法非常多，那需要的时间就会比较久。可以通过-bench=参数设置需要运行的性能测试行数: 

$ go test -bench=Fibonacci20 lib
  
PASS
  
BenchmarkFibonacci20 50000 44367 ns/op
  
ok lib 2.677s