---
title: protocol buffers, protobuf
author: wiloon
type: post
date: 2018-11-19T02:11:42+00:00
url: /?p=12891
categories:
  - Uncategorized

---
### define message formates in a .proto file

<pre><code class="language-proto line-numbers">syntax = "proto3";
package package0;
option java_package = "com.wiloon.test.protobuf.package0";

message Msg0 {
    // comments0
    string foo = 1;
    ObjType enum0 = 2;
    uint64 timestamp = 5;

    //类型
    enum ObjType {
        type0 = 0;
        type1 = 1;
    }
}
</code></pre>

download protoc
  
https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protoc-3.6.1-linux-x86_64.zip

### maven 引入protobuf依赖<pre data-language=XML>

        <code class="language-markup line-numbers">&lt;dependency&gt;
            &lt;groupId&gt;com.google.protobuf&lt;/groupId&gt;
            &lt;artifactId&gt;protobuf-java&lt;/artifactId&gt;
            &lt;version&gt;3.10.0&lt;/version&gt;
        &lt;/dependency&gt;
</code></pre> 

<pre><code class="language-bash line-numbers">export SRC_DIR=/pathToSrcDir
export DST_DIR=/pathToSrcDir

# Java, generate java code
protoc -I=$SRC_DIR --java_out=$DST_DIR $SRC_DIR/proto0.proto

# Golang
# install protocol buffers plugin
go get -u github.com/golang/protobuf/protoc-gen-go

# generate golang code
protoc -I=$SRC_DIR --go_out=$DST_DIR $SRC_DIR/proto0.proto
</code></pre>

### protobuf > json

<pre><code class="language-go line-numbers">import  "github.com/golang/protobuf/jsonpb"
    marshaler := jsonpb.Marshaler{}
    str, _ := marshaler.MarshalToString(protobufObj0)
</code></pre>

rotobuf是google提供的一个开源序列化框架，类似于XML，JSON这样的数据表示语言，其最大的特点是基于二进制，因此比传统的XML表示高效短小得多。虽然是二进制数据格式，但并没有因此变得复杂，开发人员通过按照一定的语法定义结构化的消息格式，然后送给命令行工具，工具将自动生成相关的类，可以支持java、c++、python等语言环境。通过将这些类包含在项目中，可以很轻松的调用相关方法来完成业务消息的序列化与反序列化工作。

protobuf在google中是一个比较核心的基础库，作为分布式运算涉及到大量的不同业务消息的传递，如何高效简洁的表示、操作这些业务消息在google这样的大规模应用中是至关重要的。而protobuf这样的库正好是在效率、数据大小、易用性之间取得了很好的平衡。

更多信息可参考官方文档
  
http://blog.csdn.net/ciml/article/details/5753367
  
java protobuf
  
https://blog.csdn.net/u014801432/article/details/82558380