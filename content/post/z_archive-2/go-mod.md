---
title: go mod
author: "-"
date: 2018-10-20T09:32:26.000+00:00
url: go/mod
categories:
  - Go
tags:
  - reprint
---
## go mod

```bash
go mod edit [editing flags] [go.mod]
```

### commands

```bash
# upgrade go version to 1.21.4
go mod edit -go 1.21.4

export GO111MODULE=on

go mod init project0    # 初始化
go mod tidy             # 拉取缺少的模块, 移除不用的模块。
go mod download         # 下载依赖包
go mod graph            # 打印模块依赖图
go mod vendor           # 将依赖复制到 vendor 下
go mod verify           # 校验依赖
go mod why              # 打印为什么需要依赖
go list all             # 打印所有的 package
go list -m all          # 打印所有的 module, The -m flag causes list to list modules instead of packages
go list -m -json all    # 依赖详情, json 格式
go mod edit -go=1.15

# 添加新模块
go get <package>[@<version>]
```

go.mod 如何编辑
在 Go 1.16 中，另一个行为变更是 go build 和 go test 不会自动编辑 go.mod 了，基于以上信息，Go 1.16 中将进行如下处理：

通过在代码中修改 import 语句，来修改 go.mod：

go mod tidy 删除掉无用的模块；
将未导入的模块写入 go.mod:

go mod tidy 也可以；
手动编辑；

[https://moelove.info/2020/12/19/Go-1.16-%E4%B8%AD%E5%85%B3%E4%BA%8E-go-get-%E5%92%8C-go-install-%E4%BD%A0%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E7%9A%84%E5%9C%B0%E6%96%B9/](https://moelove.info/2020/12/19/Go-1.16-%E4%B8%AD%E5%85%B3%E4%BA%8E-go-get-%E5%92%8C-go-install-%E4%BD%A0%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E7%9A%84%E5%9C%B0%E6%96%B9/)

## go mod replace

不过因为某些未知原因,并不是所有的包都能直接用 go get 获取到, 这时我们就需要使用 go modules 的 replace 功能了。 (当然大部分问题挂个梯子就能解决,但是我们也可以有其它选项)
  
使用 replace 替换 package

replace 顾名思义,就是用新的 package 去替换另一个 package, 他们可以是不同的 package, 也可以是同一个 package 的不同版本。看一下基本的语法:
  
go mod replace 必须带版本号, 不带版本号的 replace 只能用于 replace 到本地目录

## replace 到本地的包

```bash
# replace 到本地的包
# git.xxx.com/path/to/package 参照 go.mod 已有的 require 项, /path/to/local/package 配置到有go.mod文件的那层目录
go mod edit -replace=git.xxx.com/path/to/package@v1.0.2=/path/to/local/package

# replace到本地目录可以不带版本号
go mod edit -replace=github.com/wiloon/pingd-config=/home/wiloon/projects/pingd-config/
go mod edit -replace=github.com/wiloon/w-tcp-proxy=/root/projects/w-tcp-proxy
```

```bash
# old 是要被替换的package,new就是用于替换的package。
go mod edit -replace=old[@v]=new[@v]

# replace golang sys
go mod edit -replace=golang.org/x/sys@v0.0.0-20190526052359-791d8a0f4d09=github.com/golang/sys@v0.0.0-20190526052359-791d8a0f4d09

#after that, in the go.mod
replace git.xxx.com/path/to/package v1.0.2 => /path/to/local/package
```

```bash
replace golang.org/x/sys v0.0.0-20180909124046-d0be0721c37e => github.com/golang/sys v0.0.0-20180909124046-d0be0721c37e

replace golang.org/x/net v0.0.0-20190404232315-eb5bcb51f2a3 => github.com/golang/net v0.0.0-20190404232315-eb5bcb51f2a3

replace golang.org/x/text v0.3.0 => github.com/golang/text v0.3.0

replace golang.org/x/crypto v0.0.0-20190404164418-38d8ce5564a5 => github.com/golang/crypto v0.0.0-20190404164418-38d8ce5564a5

replace google.golang.org/appengine v1.6.0 => github.com/golang/appengine v1.6.0

```

这里有几点要注意:
  
replace 应该在引入新的依赖后立即执行, 以免 go tools 自动更新 mod 文件时使用了 old package 导致可能的失败
  
package后面的version不可省略。 (edit所有操作都需要版本tag)
  
version不能是master或者latest,这两者 go get 可用, 但是 go mod edit 不可识别,会报错。 (不知道是不是bug,虽然文档里表示可以这么用,希望go1.12能做点完善措施)
  
基于以上原因,我们替换一个package的步骤应该是这样的:

首先 go get new-package (如果你知道package的版本tag,那么这一步其实可以省略,如果想使用最新的版本而不想确认版本号,则需要这一步)
  
然后查看go.mod,手动复制new-package的版本号 (如果你知道版本号,则跳过,这一步十分得不人性化,也许以后会改进)
  
接着 go mod tidy 或者 go build 或者使用其他的 go tools, 他们会去获取 new-package 然后替换掉 old-package
  
最后,在你的代码里直接使用old-package的名字,golang会自动识别出replace,然后实际你的程序将会使用new-package,替换成功
  
下面我们仍然用chromedp的example做一个示例。

示例

chromedp使用了golang.org/x/image,这个package一般直连是获取不了的,但是它有一个github.com/golang/image的镜像,所以我们要用replace来用镜像替换它。

我们先来看看如果不replace的情况下的依赖情况:

没错,我们使用了原来的包,当然如果你无法获取到它的话是不会被记录进来的。

下面我们go get它的镜像:

## master表示获取最新的commit

go get github.com/golang/image@master
  
然后我们查看版本号:

cat go.mod
  
有了版本号,我们就能replace了:
  
go mod edit -replace=golang.org/x/image@v0.0.0-20180708004352-c73c2afc3b81=github.com/golang/image@v0.0.0-20180708004352-c73c2afc3b81
  
现在我们查看一下go.mod:
  
replace信息已经更新了,现在我们只要go mod tidy或者go build,我们的代码就可以使用new-package了。
  
更新后的go.sum,依赖已经替换成了镜像:
  
目前来看,replace做的远不如go get那样方便人性化,不过毕竟还只是测试阶段的功能,期待一下它在go1.12的表现吧。
  
如果有错误和疑问,欢迎在评论指出,也感谢@goozp提出的问题。

[https://stackoverflow.com/questions/53588764/how-to-add-local-dependence-to-vendor-when-using-go-mod](https://stackoverflow.com/questions/53588764/how-to-add-local-dependence-to-vendor-when-using-go-mod)
  
[https://www.cnblogs.com/apocelipes/p/9609895.html](https://www.cnblogs.com/apocelipes/p/9609895.html)
