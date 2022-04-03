---
title: go mod
author: "-"
date: 2018-10-20T09:32:26.000+00:00
url: go/mod
categories:
- Golang

tags:
  - reprint
---
## go mod
```bash
export GO111MODULE=on

go mod init project0 # 初始化
go mod tidy             #拉取缺少的模块, 移除不用的模块。
go mod download         #下载依赖包
go mod graph            #打印模块依赖图
go mod vendor           #将依赖复制到vendor下
go mod verify           #校验依赖
go mod why              #解释为什么需要依赖
go list -m -json all    #依赖详情
go mod edit -go=1.15
```

go.mod 如何编辑
在 Go 1.16 中，另一个行为变更是 go build 和 go test 不会自动编辑 go.mod 了，基于以上信息，Go 1.16 中将进行如下处理：

通过在代码中修改 import 语句，来修改 go.mod：

go get 可用于添加新模块；
go mod tidy 删除掉无用的模块；
将未导入的模块写入 go.mod:

go get <package>[@<version>];
go mod tidy 也可以；
手动编辑；


>https://moelove.info/2020/12/19/Go-1.16-%E4%B8%AD%E5%85%B3%E4%BA%8E-go-get-%E5%92%8C-go-install-%E4%BD%A0%E9%9C%80%E8%A6%81%E6%B3%A8%E6%84%8F%E7%9A%84%E5%9C%B0%E6%96%B9/
