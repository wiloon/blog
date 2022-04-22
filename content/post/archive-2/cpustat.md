---
title: gomock
author: "-"
date: 2017-05-04T07:47:46+00:00
url: gomock
categories:
  - Go

tags:
  - reprint
---
## gomock

```bash
go install github.com/golang/mock/mockgen@v1.6.0

mockgen -source feeds/feeds.go -destination feeds/mocks/feeds_mock.go -package mocks

```

- -source：设置需要模拟 (mock）的接口文件
- -destination：设置 mock 文件输出的地方，若不设置则打印到标准输出中
- -package：设置 mock 文件的包名，若不设置则为 mock_ 前缀加上文件名 (如本文的包名会为 mock_person）