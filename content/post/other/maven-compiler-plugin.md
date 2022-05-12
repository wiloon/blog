---
title: maven-compiler-plugin
author: "-"
date: 2014-12-30T05:56:31+00:00
url: maven/plugin
categories:
  - Java
tags:
  - Maven
---
## maven-compiler-plugin

maven-compiler-plugin 用于编译 java 源码, 3.0 以后的版本 默认用 javax.tools.JavaCompiler 编译

maven-compiler-plugin 3.6 和更高版本提供了一种新的配置方法

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.8.1</version>
    <configuration>
        <release>9</release>
    </configuration>
</plugin>
```

jdk 9 以上可以只声明 maven.compiler.release

```xml
<properties>
    <maven.compiler.release>17</maven.compiler.release>
</properties>
<!-- ... -->
<plugins>
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
    </plugin>
</plugins>
```

maven-compiler-plugin 从 3.6 开始可以只配置  `<maven.compiler.release>`, 来替代 `maven.compiler.source` and `maven.compiler.target`
maven-compiler-plugin 会从 `<properties>` 里读取 `maven.compiler.release`, 可以不配置到 plugin>configuration 下

"maven.compiler.release" as an replacement for source and target

<http://blog.csdn.net/zhaoyongnj2012/article/details/23970451>

在maven的默认配置中, 对于 jdk 的配置是 1.4 版本,那么创建/导入 maven 工程过程中, 工程中未指定 jdk版本。

对工程进行maven 的update, 就会出现工程依赖的 JRE System Library 会自动变成JavaSE-1.4。
  
解决方案1: 修改maven的默认jdk配置

maven 的 conf\setting.xml 文件中找到jdk配置的地方,修改如下:

```xml
<profile>
  
<id>jdk1.6</id>
  
true</activeByDefault>
  
<jdk>1.6</jdk>
  
</activation>
  
<properties>
  
<maven.compiler.source>1.6</maven.compiler.source>
  
<maven.compiler.target>1.6</maven.compiler.target>
  
<maven.compiler.compilerVersion>1.6</maven.compiler.compilerVersion>
  
</properties>
  
</profile>
```

解决方案2: 修改项目中pom.xml文件,这样避免在导入项目时的jdk版本指定

打开项目中pom.xml文件,修改如下:

```xml
  
<build>
  
<plugins>
  
<plugin>
  
<groupId>org.apache.maven.plugins</groupId>
  
maven-compiler-plugin</artifactId>
  
<configuration>
  
<source>1.6</source>
  
<target>1.6</target>
  
</configuration>
  
</plugin>
  
</plugins>
  
</build>

```
