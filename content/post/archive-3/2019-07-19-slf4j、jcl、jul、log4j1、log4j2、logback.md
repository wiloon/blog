---
title: slf4j、jcl、jul、log4j1、log4j2、logback
author: wiloon
type: post
date: 2019-07-19T07:50:48+00:00
url: /?p=14690
categories:
  - Uncategorized

---
### log4j2

log4j-api:log4j2 定义的API
log4j-core:log4j2 上述API的实现

### log4j1.x > slf4j
log4j-over-slf4j

#### 直接依赖log4j1.x的换成log4j2输出

  * 排除掉log4j jar包
  * 引入依赖包 log4j-over-slf4j（实现log4j1桥接到slf4j）

```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>log4j-over-slf4j</artifactId>
    <version>1.7.28</version>
</dependency>
``` 

### common logging/jcl > slf4j

<https://blog.wiloon.com/?p=8549>
  
jcl-over-slf4j 原本是通过 JCL 输出日志的，会被 jcl-over-slf4j 桥接到slf4j输出

### slf4j > log4j1.x

slf4j-log4j12 使用slf4j + log4j1.x 输出日志

### common logging/jcl > log4j2.x

log4j-jcl commons-logging到log4j2的桥梁

### slf4j > log4j2.x

log4j-slf4j-impl slf4j到log4j2的桥梁

https://my.oschina.net/pingpangkuangmo/blog/410224?p=2