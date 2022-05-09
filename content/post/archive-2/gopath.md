---
title: gopath
author: "-"
date: 2017-07-28T01:57:28+00:00
url: /?p=10946
categories:
  - Inbox
tags:
  - reprint
---
## gopath

GOPATH

### GOBIN

bin 目录里面存放的都是通过 go install 命令安装后,由 Go 命令源码文件生成的可执行文件 ( 在 Mac 平台下是 Unix executable 文件,在 Windows 平台下是 exe 文件) 。

该环境变量的值为 Go 语言的工作区的集合 (意味着可以有很多个) 。工作区类似于工作目录。每个不同的目录之间用: 分隔。 (不同操作系统,GOPATH 列表分隔符不同,UNIX-like 使用 :冒号,Windows 使用;分号)
  
注意: 有两种情况下,bin 目录会变得没有意义。

当设置了有效的 GOBIN 环境变量以后,bin 目录就变得没有意义。
  
如果 GOPATH 里面包含多个工作区路径的时候,必须设置 GOBIN 环境变量,否则就无法安装 Go 程序的可执行文件。

### pkg

pkg 目录是用来存放通过 go install 命令安装后的代码包的归档文件(.a 文件)。归档文件的名字就是代码包的名字。所有归档文件都会被存放到该目录下的平台相关目录中,即在
  
$GOPATH/pkg/$GOOS_$GOARCH 中,同样以代码包为组织形式。
  
这里有两个隐藏的环境变量,GOOS 和 GOARCH。这两个环境变量是不用我们设置的,系统就默认的。GOOS 是 Go 所在的操作系统类型,GOARCH 是 Go 所在的计算架构。平台相关目录是以
  
$GOOS_$GOARCH 命名的,Mac 平台上这个目录名就是 darwin_amd64。
  
命令源码文件:
  
声明自己属于 main 代码包、包含无参数声明和结果声明的 main 函数。
  
库源码文件

库源码文件就是不具备命令源码文件上述两个特征的源码文件。存在于某个代码包中的普通的源码文件。

库源码文件被安装后,相应的归档文件 (.a 文件) 会被存放到当前工作区的 pkg 的平台相关目录下。

### src

#### 命令源码文件

声明自己属于 main 代码包、包含无参数声明和结果声明的 main 函数。
  
命令源码文件被安装以后,GOPATH 如果只有一个工作区,那么相应的可执行文件会被存放当前工作区的 bin 文件夹下；如果有多个工作区,就会安装到 GOBIN 指向的目录下。
  
命令源码文件是 Go 程序的入口。
  
同一个代码包中最好也不要放多个命令源码文件。多个命令源码文件虽然可以分开单独 go run 运行起来,但是无法通过 go build 和 go install。

#### 库源码文件

库源码文件就是不具备命令源码文件上述两个特征的源码文件。存在于某个代码包中的普通的源码文件。
  
库源码文件被安装后,相应的归档文件 (.a 文件) 会被存放到当前工作区的 pkg 的平台相关目录下。

### 测试源码文件

名称以 _test.go 为后缀的代码文件,并且必须包含 Test 或者 Benchmark 名称前缀的函数。

```go
func TestXXX( t *testing.T) {
}
```

名称以 Test 为名称前缀的函数,只能接受 *testing.T 的参数,这种测试函数是功能测试函数。

```go
func BenchmarkXXX( b *testing.B) {
}
```

名称以 Benchmark 为名称前缀的函数,只能接受 *testing.B 的参数,这种测试函数是性能测试函数。

<https://www.jianshu.com/p/35a4ec1b3067>
  
<https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/01.2.md>
