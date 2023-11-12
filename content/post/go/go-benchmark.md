---
title: go benchmark
author: "-"
date: 2012-05-23T01:26:24+00:00
url: go/benchmark
categories:
  - Go
tags:
  - reprint

---
## go benchmark

稳定的测试环境
当我们尝试去优化代码的性能时，首先得知道当前的性能怎么样。Go 语言标准库内置的 testing 测试框架提供了基准测试(benchmark)的能力，能让我们很容易地对某一段代码进行性能测试。

性能测试受环境的影响很大，为了保证测试的可重复性，在进行性能测试时，尽可能地保持测试环境的稳定。

机器处于闲置状态，测试时不要执行其他任务，也不要和其他人共享硬件资源。
机器是否关闭了节能模式，一般笔记本会默认打开这个模式，测试时关闭。
避免使用虚拟机和云主机进行测试，一般情况下，为了尽可能地提高资源的利用率，虚拟机和云主机 CPU 和内存一般会超分配，超分机器的性能表现会非常地不稳定。
超分配是针对硬件资源来说的，商业上对应的就是云主机的超卖。虚拟化技术带来的最大直接收益是服务器整合，通过 CPU、内存、存储、网络的超分配（Overcommitment）技术，最大化服务器的使用率。例如，虚拟化的技能之一就是随心所欲的操控 CPU，例如一台 32U(物理核心)的服务器可能会创建出 128 个 1U(虚拟核心)的虚拟机，当物理服务器资源闲置时，CPU 超分配一般不会对虚拟机上的业务产生明显影响，但如果大部分虚拟机都处于繁忙状态时，那么各个虚拟机为了获得物理服务器的资源就要相互竞争，相互等待。Linux 上专门有一个指标，Steal Time(st)，用来衡量被虚拟机监视器(Hypervisor)偷去给其它虚拟机使用的 CPU 时间所占的比例。

```bash
# 运行当前 package 内的用例, 只运行 test, 不运行 benchmark
# go test 命令默认不运行 benchmark 用例
go test 

# 只运行 benchmark

go test -bench=. -run=none
go test -bench . -run none

# 运行 test 和 benchmark
go test -bench .

# -bench 参数支持传入一个正则表达式，匹配到的用例才会得到执行，例如，只运行以 Fib 结尾的 benchmark 用例
go test -bench=Fib$ .
go test -bench='Fib$' .

```

<https://geektutu.com/post/hpg-benchmark.html>

>BenchmarkReader-8         409231              2549 ns/op

用例执行了 409231 次，每次花费约 2549 ns。总耗时约 1s, benchmark 的默认时间是 1s

BenchmarkFib-8 中的 -8 即 GOMAXPROCS, 默认等于 CPU 核数. 可以通过 -cpu 参数改变 GOMAXPROCS，-cpu 支持传入一个列表作为参数

```bash
go test -run=none -bench=. -cpu=2,4
```

### 提升准确度

benchmark 的默认时间是 1s，那么我们可以使用 -benchtime 指定为 5s

```bash
go test -run=none -bench=. -cpu=1 -benchtime=5s
```

实际执行的时间是 8s，比 benchtime 的 5s 要长，测试用例编译、执行、销毁等是需要时间的。

### 次数

-benchtime 的值除了是时间外，还可以是具体的次数。例如，执行 30 次可以用 -benchtime=30x

```bash
go test -run=none -bench=. -cpu=1 -benchtime=30x
```

### 轮数

-count 参数可以用来设置 benchmark 的轮数。例如，进行 3 轮 benchmark。

```bash
go test -run=none -bench=. -cpu=1 -count=3
```

### 内存

使用 -benchmem 参数看到内存分配的情况

```bash
go test -run=none -bench=. -cpu=1 -benchmem
```

### ResetTimer, StopTimer & StartTimer

benchmark 和普通的单元测试用例一样，都位于 _test.go 文件中。
函数名以 Benchmark 开头，参数是 b *testing.B。和普通的单元测试用例很像，单元测试函数名以 Test 开头，参数是 `t *testing.T`。

benchmark 是如何工作的
benchmark 用例的参数 b *testing.B，有个属性 b.N 表示这个用例需要运行的次数。b.N 对于每个用例都是不一样的。

那这个值是如何决定的呢？b.N 从 1 开始，如果该用例能够在 1s 内完成，b.N 的值便会增加，再次执行。b.N 的值大概以 1, 2, 3, 5, 10, 20, 30, 50, 100 这样的序列递增，越到后面，增加得越快。我们仔细观察上述例子的输出：

1
BenchmarkFib-8               202           5980669 ns/op
BenchmarkFib-8 中的 -8 即 GOMAXPROCS，默认等于 CPU 核数。可以通过 -cpu 参数改变 GOMAXPROCS，-cpu 支持传入一个列表作为参数

在这个例子中，改变 CPU 的核数对结果几乎没有影响，因为这个 Fib 的调用是串行的。

202 和 5980669 ns/op 表示用例执行了 202 次，每次花费约 0.006s。总耗时比 1s 略多。

><https://geektutu.com/post/hpg-benchmark.html>
><https://www.cnblogs.com/jiujuan/p/14604609.html>
