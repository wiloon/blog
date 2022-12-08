---
title: maven依赖本地非repository中的jar包
author: "-"
date: 2016-03-12T06:23:38+00:00
url: maven/local/jar
categories:
  - Maven
tags:
  - reprint
---
## maven依赖本地非repository中的jar包

maven依赖本地非repository中的jar包
  
<http://www.cnblogs.com/piaolingxue/archive/2011/10/12/2208871.html>
  
博客分类:
  
MAVEN
  
今天在使用maven编译打包一个web应用的时候,碰到一个问题:
  
项目在开发是引入了依赖jar包,放在了WEB-INF/lib目录下,并通过buildpath中将web libariary导入。
  
在eclipse中开发没有问题,但是使用maven编译插件开始便宜总是报找不到WEB-INF/lib这个jar包中的类。
  
显然实在编译的时候WEB-INF/lib并没有配置到maven-complier-plugin插件src目录中去,
  
于是将这个目录添加进去,还是不好使。无赖,先把这个jar包安装到本地库中,然后添加dependency。

后来google了下,发现maven提供了scope为system的依赖,文档的原文如下:
  
system
  
This scope is similar to provided except that you have to provide the JAR which contains it explicitly.
  
The artifact is always available and is not looked up in a repository.

这样就可以添加dependency而不需要再将WEB-INF/lib目录下的jar包安装到本地库中了。
  
具体配置录下:

```xml
<dependency>
  <groupId>org.apache</groupId>
  <artifactId>test</artifactId>
  <version>1.0</version>
  <scope>system</scope>
  <systemPath>${basedir}/src/main/webapp/WEB-INF/lib/paypal_base.jar</systemPath>
</dependency>
```

上面的groupId和artifactId这些都可随便填写就好.
