---
title: golang grpc
author: "-"
date: 2017-09-07T04:25:32+00:00
url: grpc/go
categories:
  - rpc

---
### grpc
GRPC 是在 http2 之上运行的
## golang grpc

### install protocol compiler plugins
```bash
$ go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.26
$ go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1

```

```bash
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    helloworld/helloworld.proto

  
protoc -I proto/ proto/helloworld.proto -go_out=plugins=grpc:proto

```

### grpc-dump
    go install github.com/bradleyjkemp/grpc-tools/grpc-dump@latest
    grpc-dump --port=12345
    http_proxy=http://localhost:12345 my-app

>https://github.com/bradleyjkemp/grpc-tools
https://grpc.io/docs/quickstart/go.html#prerequisites
  
http://www.blogjava.net/killme2008/archive/2010/01/20/310206.html