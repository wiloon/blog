---
title: golang, cgo, CGO_ENABLED
author: "-"
date: 2019-04-05T14:23:16+00:00
url: /?p=14106

categories:
  - inbox
tags:
  - reprint
---
## golang, cgo, CGO_ENABLED
### go build
    CGO_ENABLED=0 GOOS=linux go build -v -a -o name0 main.go

# cgo
CGO 提供了 golang 和 C 语言相互调用的机制。某些第三方库可能只有 C/C++ 的实现，完全用纯 golang 的实现可能工程浩大，这时候 CGO 就派上用场了。可以通 CGO 在 golang 在调用 C 的接口，C++ 的接口可以用 C 包装一下提供给 golang 调用。被调用的 C 代码可以直接以源代码形式提供或者打包静态库或动态库在编译时链接。推荐使用静态库的方式，这样方便代码隔离，编译的二进制也没有动态库依赖方便发布也符合 golang 的哲学。

CGO_ENABLED=0 的情况下，Go采用纯静态编译；


### CGO_ENABLED=1
go build 编译时会添加一些动态库链接 如 glibc
cgo，允许你在Go代码中调用C代码
我们以os/user为例，在 CGO_ENABLED=1，即 cgo 开启的情况下，os/user 包中的 lookupUserxxx 系列函数采用了 c 版本的实现，我们看到在 $GOROOT/src/os/user/lookup_unix.go 中的 build tag 中包含了 build cgo。这样一来，在 CGO_ENABLED=1，该文件将被编译，该文件中的c版本实现的lookupUser将被使用

如果CGO_ENABLED=1，但依然要强制静态编译，需传递-linkmode=external给cmd/link。

https://johng.cn/cgo-enabled-affect-go-static-compile/

https://johng.cn/cgo-enabled-affect-go-static-compile/embed/#?secret=w5uCEbc4UP

---

https://studygolang.com/articles/16315  
https://zhuanlan.zhihu.com/p/349197066  
https://tonybai.com/2017/06/27/an-intro-about-go-portability/   


### go cpp
>https://github.com/arrieta/golang-cpp-basic-example/tree/master
