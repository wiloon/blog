---
title: go command
author: wiloon
type: post
date: 2017-11-16T02:54:01+00:00
url: /?p=11440
categories:
  - Uncategorized

---
### go build

```bash
# -a
强行对所有涉及到的代码包（包含标准库中的代码包）进行重新构建，即使它们已经是最新的了。
# -installsuffix
为了使当前的输出目录与默认的编译输出目录分离，可以使用这个标记。此标记的值会作为结果文件的父目录名称的后缀。其实，如果使用了-race标记，这个标记会被自动追加且其值会为race。如果我们同时使用了-race标记和-installsuffix，那么在-installsuffix标记的值的后面会再被追加_race，并以此来作为实际使用的后缀。
#### -x
打印详细信息
#### -n
查看具体操作，不执行
#### -i
安装归档文件
#### -v
查看编译的代码包名称
# -o
指定输出文件
```

```bash
#查看golang 环境变量
go env
# 查看Go支持OS和平台列表
go tool dist list

# go mod initialize a new module
go mod init github.com/you/hello

```

go build
  
通过go build加上要编译的Go源文件名，我们即可得到一个可执行文件，默认情况下这个文件的名字为源文件名字去掉.go后缀。

go build hellogo.go

当然我们也 可以通过-o选项来指定其他名字：
  
go build -o myfirstgo hellogo.go

go build -x -v hellogo.go

如果我们在go-examples目录下直接执行go build命令，后面不带文件名，我们将得到一个与目录名同名的可执行文件：

$ go build
  
$ ls
  
go-examples hellogo.go

go install
  
与build命令相比，install命令在编译源码后还会将可执行文件或库文件安装到约定的目录下。

go install编译出的可执行文件以其所在目录名(DIR)命名
  
go install将可执行文件安装到与src同级别的bin目录下，bin目录由go install自动创建
  
go install将可执行文件依赖的各种package编译后，放在与src同级别的pkg目录下.
  
参考资料：

http://tonybai.com/2012/08/17/hello-go/