---
title: alpine basic
author: "-"
date: 2019-04-23T06:24:28+00:00
url: /?p=14227
categories:
  - inbox
tags:
  - reprint
---
## alpine basic

### alpine mirror

    vi /etc/apk/repositories
  
b. 将里面 dl-cdn.alpinelinux.org 的 改成 mirrors.aliyun.com ; 保存退出即可

    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

### alpine install telnet

```bash
apk update
apk add busybox-extras
busybox-extras telnet localhost 6900

apk add drill
apk add tcpdump
    apk add curl
```

明明镜像中有对应的二进制文件，但是执行时却提示 not found 或 no such file¶
有时可能会遇到明明镜像中存在相应的二进制文件，但是执行对应的二进制文件时却提示 not found 或 no such file 错误，类似下面这样:

## ls /usr/bin/grep

/usr/bin/grep

## /usr/bin/grep

/bin/sh: /usr/bin/grep: not found

常见原因：该二进制文件是使用动态链接方式编译了一个使用了 GLIBC 库的程序生成的，但是 alpne 镜像中没有 GLIBC 库而是用的 MUSL LIBC 库，这样就会导致该二进制文件无法被执行。

解决办法：下面两个解决方法

改为静态编译
如果要使用动态链接函数编译的话，不要依赖 GLIBC  (比如编译 Go 程序的时候指定 CGO_ENABLED=0 ） 或者在 alpine 中编译一个依赖 MUSL LIBC 的版本

## golang cgo

```bash
FROM alpine:edge AS build
RUN apk update
RUN apk upgrade
RUN apk add --update go=1.8.3-r0 gcc=6.3.0-r4 g++=6.3.0-r4
WORKDIR /app
ENV GOPATH /app
ADD src /app/src
RUN go get server # server is name of our application
RUN CGO_ENABLED=1 GOOS=linux go install -a server

FROM alpine:edge
WORKDIR /app
RUN cd /app
COPY --from=build /app/bin/server /app/bin/server
CMD ["bin/server"]

```

><https://megamorf.gitlab.io/2019/09/08/alpine-go-builds-with-cgo-enabled/>
><https://pkgs.alpinelinux.org/packages>
