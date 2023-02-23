---
title: golang grpc
author: "-"
date: 2017-09-07T04:25:32+00:00
url: grpc/go
categories:
  - Go
tags:
  - reprint
  - RPC
---
### grpc

gRPC通过 HTTP2 协议传输

### protobuf

```bash
syntax = "proto3";
option go_package="./;api";

```

## golang grpc

### install protocol compiler plugins

在 <https://pkg.go.dev/google.golang.org/protobuf/cmd/protoc-gen-go> 可以看到最新的版本号

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.27.1
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1.0
# 安装后查看 版本
./protoc-gen-go --version
./protoc-gen-go-grpc --version
```

```bash
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    helloworld/helloworld.proto

  
protoc -I proto/ proto/helloworld.proto -go_out=plugins=grpc:proto

```

### grpc-dump

```bash
go install github.com/bradleyjkemp/grpc-tools/grpc-dump@latest
grpc-dump --port=12345
http_proxy=http://localhost:12345 my-app
```

### wireshark grpc

<https://mp.weixin.qq.com/s/BdcFRO58ytrtcpYZVT1ymQ>

Wireshark>Edit->Preference->Protocols->Protobuf

#### analyze

Analyze>Decode As
在current列选择http2

### streaming

gRPC 的流式，分为三种类型：

Server-side streaming RPC：服务器端流式 RPC
Client-side streaming RPC：客户端流式 RPC
Bidirectional streaming RPC：双向流式 RPC
<https://colobu.com/2017/04/06/dive-into-gRPC-streaming/>  
<https://segmentfault.com/a/1190000016503114>  
<https://github.com/bradleyjkemp/grpc-tools>  
<https://grpc.io/docs/quickstart/go.html#prerequisites>
  
<http://www.blogjava.net/killme2008/archive/2010/01/20/310206.html>

#### gRPC over HTTP2

<https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md>
