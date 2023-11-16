---
title: protocol buffers, protobuf
author: "-"
date: 2018-11-19T02:11:42.000+00:00
url: protobuf
categories:
  - inbox
tags:
  - reprint
---
## protocol buffers, protobuf

### install protoc

```bash
# archlinux 可以从仓库直接安装
pacman -S protobuf
# 其它发行版, 比如ubuntu 可以下载二进制包 解压即可.
https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protoc-3.6.1-linux-x86_64.zip
# set protoc to PATH
protoc -help
```

- windows

download protoc  
[https://developers.google.com/protocol-buffers/docs/downloads](https://developers.google.com/protocol-buffers/docs/downloads)

### define message formates in a .proto file

```bash
    syntax = "proto3";
    package package0;
    option java_package = "com.wiloon.test.protobuf.package0";
    
    message Msg0 {

    // comments0
    string foo = 1;
    ObjType enum0 = 2;
    uint64 timestamp = 5;
    int32 type = 6;

        //类型
        enum ObjType {
            type0 = 0;
            type1 = 1;
        }
    }
```

### generate java/golang code

```bash
export SRC_DIR=/pathToSrcDir
export DST_DIR=$SRC_DIR
```

#### golang

```bash
# 安装 protoc-gen-go
# install protocol buffers plugin
# go: module github.com/golang/protobuf is deprecated: Use the "google.golang.org/protobuf" module instead.

# 废弃，deprecated
go get -u github.com/golang/protobuf/protoc-gen-go

# 建议用这个
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.26
# 或
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

# generate golang code
protoc -I=$SRC_DIR --go_out=$DST_DIR $SRC_DIR/proto0.proto
protoc --proto_path=$SRC_DIR --go_out=$DST_DIR  --go_opt=paths=source_relative $SRC_DIR/foo.proto
# -I, --proto_path: .proto 文件目录
# --go_out： 输出目录
```

#### java

Java 工程建议使用下面的 protobuf-maven-plugin 方式

##### protoc java

```bash
# Java, generate java code
protoc -I=$SRC_DIR --java_out=$DST_DIR $SRC_DIR/proto0.proto
```

### protobuf > json

```go
import  "github.com/golang/protobuf/jsonpb"
```

rotobuf 是 google 提供的一个开源序列化框架, 类似于 XML, JSON 这样的数据表示语言, 其最大的特点是基于二进制, 因此比传统的 XML 表示高效短小得多。虽然是二进制数据格式, 但并没有因此变得复杂, 开发人员通过按照一定的语法定义结构化的消息格式,然后送给命令行工具,工具将自动生成相关的类,可以支持java、c++、python等语言环境。通过将这些类包含在项目中,可以很轻松的调用相关方法来完成业务消息的序列化与反序列化工作。

protobuf在google中是一个比较核心的基础库,作为分布式运算涉及到大量的不同业务消息的传递,如何高效简洁的表示、操作这些业务消息在google这样的大规模应用中是至关重要的。而protobuf这样的库正好是在效率、数据大小、易用性之间取得了很好的平衡。

更多信息可参考官方文档

[http://blog.csdn.net/ciml/article/details/5753367](http://blog.csdn.net/ciml/article/details/5753367)

java protobuf

[https://blog.csdn.net/u014801432/article/details/82558380](https://blog.csdn.net/u014801432/article/details/82558380)

### maven + protobuf， protobuf-maven-plugin

[https://gist.github.com/cqc3073/7766447823ac29a70ddeaf403df1f5f6](https://gist.github.com/cqc3073/7766447823ac29a70ddeaf403df1f5f6)

- 在 src/main/proto 下定义 proto 文件
- 在 pom.xml 中配置

```xml
<properties>
    <protobuf.version>3.17.0</protobuf.version>
    <os-maven-plugin.version>1.7.0</os-maven-plugin.version>
    <protobuf-maven-plugin.version>0.6.1</protobuf-maven-plugin.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.google.protobuf</groupId>
        <artifactId>protobuf-java</artifactId>
        <version>${protobuf.version}</version>
    </dependency>
</dependencies>

<build>
    <extensions>
        <extension>
            <groupId>kr.motd.maven</groupId>
            <artifactId>os-maven-plugin</artifactId>
            <version>${os-maven-plugin.version}</version>
        </extension>
    </extensions>
    <plugins>
        <plugin>
            <groupId>org.xolstice.maven.plugins</groupId>
            <artifactId>protobuf-maven-plugin</artifactId>
            <version>${protobuf-maven-plugin.version}</version>
            <extensions>true</extensions>
            <configuration>
                <protocArtifact>com.google.protobuf:protoc:${protobuf.version}:exe:${os.detected.classifier}</protocArtifact>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>compile</goal>
                        <goal>test-compile</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

运行 `mvn compile`, 就可以在 target/generated-sources 下看到生成的源码了  
reload maven 工程, idea会自动 识别生成的java代码, maven>reload project  
