---
title: golang grpc
author: wiloon
type: post
date: 2017-09-07T04:25:32+00:00
url: /?p=11125
categories:
  - Uncategorized

---
```bash
  
go get google.golang.org/grpc
  
wget https://github.com/google/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip
  
set protoc to PATH
  
go get -u github.com/golang/protobuf/protoc-gen-go

protoc -help
  
protoc -I proto/ proto/helloworld.proto &#8211;go_out=plugins=grpc:proto

```

https://grpc.io/docs/quickstart/go.html#prerequisites
  
http://www.blogjava.net/killme2008/archive/2010/01/20/310206.html