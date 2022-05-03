---
title: dockerfile
author: "-"
date: 2018-12-22T13:02:46+00:00
url: dockerfile
categories:
  - container
tags:
  - reprint
---

## dockerfile

```bash
FROM golang:1.17.8 AS build
ENV GO111MODULE on
ARG APP_NAME=rssx-api
WORKDIR /workdir
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOPROXY=https://goproxy.io go build -a -o ${APP_NAME} main.go

FROM alpine:3.15.0 AS prod
ARG APP_NAME=rssx-api
COPY --from=build /workdir/${APP_NAME} /data/${APP_NAME}
COPY config.toml config.toml
COPY config.toml /data/config.toml
ENV APPLICATION_NAME ${APP_NAME}
CMD "/data/${APPLICATION_NAME}"

```

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

### 环境变量

设置环境变量 USERNAME 默认值为 admin，后面可以通过docker run -e USERNAME="XXXXXX"修改，这个环境变量在容器里也可以$USERNAME获取

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

WORKDIR指令用于设置Dockerfile中的RUN、CMD和ENTRYPOINT指令执行命令的工作目录(默认为/目录),该指令在Dockerfile文件中可以出现多次,如果使用相对路径则为相对于WORKDIR上一次的值,例如WORKDIR /a,WORKDIR b,RUN pwd最终输出的当前目录是/a/b。 (RUN cd /a/b,RUN pwd是得不到/a/b的) 

### create file

```bash
RUN echo 'All of your\n\
multiline that you ever wanted\n\
into a dockerfile\n'\
>> /etc/example.conf
```

<http://blog.wiloon.com/?p=11796>
http://dockone.io/article/8196

## Dockerfile RUN，CMD，ENTRYPOINT命令区别

Dockerfile中RUN，CMD和ENTRYPOINT都能够用于执行命令，下面是三者的主要用途：

## RUN

RUN命令执行命令并创建新的镜像层，通常用于安装软件包

## CMD

CMD命令设置容器启动后默认执行的命令及其参数，但CMD设置的命令能够被 docker run 命令后面的命令行参数替换

## ENTRYPOINT

ENTRYPOINT配置容器启动时的执行命令 (不会被忽略，一定会被执行，即使运行 docker run 时指定了其他命令）

## Shell 格式和 Exec 格式运行命令

我们可用两种方式指定 RUN、CMD 和 ENTRYPOINT 要运行的命令：Shell 格式和 Exec 格式：

Shell格式：`<instruction> <command>`。例如：apt-get install python3
Exec格式：`<instruction>` ["executable", "param1", "param2", ...]。例如： ["apt-get", "install", "python3"]
CMD 和 ENTRYPOINT 推荐使用 Exec 格式，因为指令可读性更强，更容易理解。RUN 则两种格式都可以。

Run命令
RUN 指令通常用于安装应用和软件包。RUN 在当前镜像的顶部执行命令，并通过创建新的镜像层。Dockerfile 中常常包含多个 RUN 指令。下面是一个例子：

RUN apt-get update && apt-get install -y \  
 bzr \
 cvs \
 git \
 mercurial \
 subversion
apt-get update 和 apt-get install 被放在一个 RUN 指令中执行，这样能够保证每次安装的是最新的包。如果 apt-get install 在单独的 RUN 中执行，则会使用 apt-get update 创建的镜像层，而这一层可能是很久以前缓存的。

CMD命令
CMD 指令允许用户指定容器的默认执行的命令。此命令会在容器启动且 docker run 没有指定其他命令时运行。下面是一个例子：

CMD echo "Hello world"
运行容器 docker run -it [image] 将输出：

Hello world
但当后面加上一个命令，比如 docker run -it [image] /bin/bash，CMD 会被忽略掉，命令 bash 将被执行：

root@10a32dc7d3d3:/#
ENTRYPOINT命令
ENTRYPOINT 的 Exec 格式用于设置容器启动时要执行的命令及其参数，同时可通过CMD命令或者命令行参数提供额外的参数。ENTRYPOINT 中的参数始终会被使用，这是与CMD命令不同的一点。下面是一个例子：

ENTRYPOINT ["/bin/echo", "Hello"]  
当容器通过 docker run -it [image] 启动时，输出为：

Hello
而如果通过 docker run -it [image] CloudMan 启动，则输出为：

Hello CloudMan
将Dockerfile修改为：

ENTRYPOINT ["/bin/echo", "Hello"]  
CMD ["world"]
当容器通过 docker run -it [image] 启动时，输出为：

Hello world
而如果通过 docker run -it [image] CloudMan 启动，输出依旧为：

Hello CloudMan
ENTRYPOINT 中的参数始终会被使用，而 CMD 的额外参数可以在容器启动时动态替换掉。

总结
使用 RUN 指令安装应用和软件包，构建镜像。
如果 Docker 镜像的用途是运行应用程序或服务，比如运行一个 MySQL，应该优先使用 Exec 格式的 ENTRYPOINT 指令。CMD 可为 ENTRYPOINT 提供额外的默认参数，同时可利用 docker run 命令行替换默认参数。
如果想为容器设置默认的启动命令，可使用 CMD 指令。用户可在 docker run 命令行中替换此默认命令。

作者：伊凡的一天
链接：https://www.jianshu.com/p/f0a0f6a43907
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


### arg 和 env

在使用 docker-compoe 构建镜像的时候会感觉 ARG 和 ENV 的作用很相似, 但是这两个存在就肯定有它的原因

它们起作用的时机
arg 是在 build 的时候存在的, 可以在 Dockerfile 中当做变量来使用
env 是容器构建好之后的环境变量, 不能在 Dockerfile 中当参数使用
从这里可以看出来 ARG 就是专门为构建镜像而生的

拿一个具体的例子

# Dockerfile
FROM redis:3.2-alpine

LABEL maintainer="GPF <5173180@qq.com>"

ARG REDIS_SET_PASSWORD=developer
ENV REDIS_PASSWORD ${REDIS_SET_PASSWORD}

VOLUME /data

EXPOSE 6379

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]

这是一个构建 redis 的文件, 中间有这么一句

1
2
ARG REDIS_SET_PASSWORD=developer
ENV REDIS_PASSWORD ${REDIS_SET_PASSWORD}
它是为

1
CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]
这一句服务的, 这句就是在启动 redis 的时候设置密码, 因为当执行 CMD 的时候,说明容器已经构建成功运行了起来,此时 CMD是在容器中执行容器中的命令, 因此 CMD 中的变量是用的环境变量而不是在 Dockerfile 中的变量,因此需要把 ARG 中的值在构建的时候赋值给 ENV

另一个使用 ARG 的例子
 
FROM nginx:1.13.1-alpine

LABEL maintainer="GPF <5173180@qq.com>"

#https://yeasy.gitbooks.io/docker_practice/content/image/build.html
RUN mkdir -p /etc/nginx/cert \
    && mkdir -p /etc/nginx/conf.d \
    && mkdir -p /etc/nginx/sites

COPY ./nginx.conf /etc/ngixn/nginx.conf
COPY ./conf.d/ /etc/nginx/conf.d/
COPY ./cert/ /etc/nginx/cert/

COPY ./sites /etc/nginx/sites/


ARG PHP_UPSTREAM_CONTAINER=php-fpm
ARG PHP_UPSTREAM_PORT=9000
RUN echo "upstream php-upstream { server ${PHP_UPSTREAM_CONTAINER}:${PHP_UPSTREAM_PORT}; }" > /etc/nginx/conf.d/upstream.conf

VOLUME ["/var/log/nginx", "/var/www"]

WORKDIR /usr/share/nginx/html

这里就只是用了ARG

 
ARG PHP_UPSTREAM_CONTAINER=php-fpm
ARG PHP_UPSTREAM_PORT=9000
RUN echo "upstream php-upstream { server ${PHP_UPSTREAM_CONTAINER}:${PHP_UPSTREAM_PORT}; }" > /etc/nginx/conf.d/upstream.conf
这里的变量用的就是 ARG 而不是 ENV了,因为这条命令运行在 Dockerfile 当中的, 像这种临时使用一下的变量没必要存环境变量的值就很适合使用 ARG

## 调试用的 shell 脚本

脚本第一行用的是 /bin/sh, 并不是每一个镜像都有 bash

```bash
#!/bin/sh

for i in {1..10}
do
  echo "$i"
  date
  sleep 10
done
```
