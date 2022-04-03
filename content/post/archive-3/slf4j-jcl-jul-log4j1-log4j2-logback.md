---
title: slf4j、jcl、jul、log4j1、log4j2、logback
author: "-"
date: 2019-07-19T07:50:48+00:00
url: /?p=14690

categories:
  - inbox
tags:
  - reprint
---
## slf4j、jcl、jul、log4j1、log4j2、logback

### slf4j > log4j2.x

log4j-slf4j-impl slf4j 到 log4j2 的桥梁

### 直接依赖log4j1.x的换成log4j2输出, log4j1.x > slf4j
  * 排除掉log4j jar包
  * 引入依赖包 log4j-over-slf4j (实现log4j1桥接到slf4j) 

```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>log4j-over-slf4j</artifactId>
    <version>1.7.32</version>
</dependency>
``` 

### commons-logging
commons-logging:commons-logging的原生全部内容

#### org.apache.logging.log4j:log4j-jcl
commons-logging/jcl > log4j2.x
org.apache.logging.log4j:log4j-jcl: commons-logging 桥接到 log4j2

```xml
<!-- https://mvnrepository.com/artifact/org.apache.logging.log4j/log4j-jcl -->
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-jcl</artifactId>
    <version>2.13.3</version>
</dependency>
```

#### jcl-over-slf4j
commons-logging/jcl > slf4j
<https://blog.wiloon.com/?p=8549>

jcl-over-slf4j 原本是通过 JCL 输出日志的，会被 jcl-over-slf4j 桥接到slf4j输出

### slf4j > log4j1.x
slf4j-log4j12 使用 slf4j + log4j1.x 输出日志

https://my.oschina.net/pingpangkuangmo/blog/410224?p=2

### jul>slf4j>log4j2
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>jul-to-slf4j</artifactId>
        <version>1.7.25</version>
    </dependency>
    
    // Optionally remove existing handlers attached to j.u.l root logger
     SLF4JBridgeHandler.removeHandlersForRootLogger();  // (since SLF4J 1.6.5)
    
     // add SLF4JBridgeHandler to j.u.l's root logger, should be done once during
     // the initialization phase of your application
     SLF4JBridgeHandler.install();
     
     https://github.com/influxdata/influxdb-java/issues/443