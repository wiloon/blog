---
title: java grpc
author: "-"
date: 2017-09-08T08:28:12+00:00
url: grpc/java
categories:
  - Java
tags:
  - reprint
  - rpc
---
## java grpc

### maven依赖

```xml
    <dependency>
      <groupId>io.grpc</groupId>
      <artifactId>grpc-netty-shaded</artifactId>
      <version>1.31.0</version>
    </dependency>
    <dependency>
      <groupId>io.grpc</groupId>
      <artifactId>grpc-protobuf</artifactId>
      <version>1.31.0</version>
    </dependency>
    <dependency>
      <groupId>io.grpc</groupId>
      <artifactId>grpc-stub</artifactId>
      <version>1.31.0</version>
    </dependency>
    <dependency> <!-- necessary for Java 9+ -->
      <groupId>org.apache.tomcat</groupId>
      <artifactId>annotations-api</artifactId>
      <version>6.0.53</version>
      <scope>provided</scope>
    </dependency>
```

create proto file in src/main/proto/foo.proto
option java_package = "com.wiloon.foo";

### maven

    执行 mvn compile, 就可以在target/generated-sources 下看到生成的源码了

gradle build
find generated source in
build/generated/source/proto/main/grpc/com/wiloon/foo/foo.java

<https://grpc.io/docs/quickstart/java.html>

<https://github.com/google/protobuf-gradle-plugin>
<https://www.jianshu.com/p/59ac036b0d7b>
