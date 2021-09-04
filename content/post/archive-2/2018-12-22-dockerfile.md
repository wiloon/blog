---
title: dockerfile
author: "-"
type: post
date: 2018-12-22T13:02:46+00:00
url: /?p=13180
categories:
  - Uncategorized

---
```
FROM golang:1.12.4 AS build

ENV GO111MODULE on
WORKDIR /go/src/xxx.com/xxx

ADD . .
ADD cmd cmd
ADD internal internal
ADD pkg pkg

RUN CGO_ENABLED=0 GOOS=linux go build -a cmd/xxx.go

FROM alpine AS prod

COPY --from=build /go/src/xxx.com/xxx/xxx .

# dev
ADD configs/xxx.json .
CMD ["./xxx"]
```

### ENV

ENV 设置环境变量
  
格式有两种: 

ENV <key> <value>
  
ENV <key1>=<value1> <key2>=<value2>...
  
这个指令很简单,就是设置环境变量而已,无论是后面的其它指令,如 RUN,还是运行时的应用,都可以直接使用这里定义的环境变量。

ENV VERSION=1.0 DEBUG=on \
      
NAME="Happy Feet"

FROM 指定基础镜像
  
RUN 执行命令
  
ENV 设置环境变量
  
格式有两种: 
  
ENV <key> <value>
  
ENV <key1>=<value1> <key2>=<value2>...
  
这个指令很简单,就是设置环境变量而已,无论是后面的其它指令,如 RUN,还是运行时的应用,都可以直接使用这里定义的环境变量

COPY 目标路径不存时会自动创建

### COPY
Same as 'ADD' but without the tar and remote url handling.
  
COPY的语法与功能与ADD相同,只是不支持上面讲到的<src>是远程URL、自动解压这两个特性,但是Best Practices for Writing Dockerfiles建议尽量使用COPY,并使用RUN与COPY的组合来代替ADD,这是因为虽然COPY只支持本地文件拷贝到container,但它的处理比ADD更加透明,建议只在复制tar文件时使用ADD,如ADD trusty-core-amd64.tar.gz /。

### WORKDIR

WORKDIR指令用于设置Dockerfile中的RUN、CMD和ENTRYPOINT指令执行命令的工作目录(默认为/目录),该指令在Dockerfile文件中可以出现多次,如果使用相对路径则为相对于WORKDIR上一次的值,例如WORKDIR /a,WORKDIR b,RUN pwd最终输出的当前目录是/a/b。（RUN cd /a/b,RUN pwd是得不到/a/b的）

### create file 
    RUN echo 'All of your\n\
    multiline that you ever wanted\n\
    into a dockerfile\n'\
    >> /etc/example.conf

<http://blog.wiloon.com/?p=11796>
http://dockone.io/article/8196