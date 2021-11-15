---
title: maven config, maven-compiler-plugin
author: "-"
date: 2014-12-30T05:56:31+00:00
url: maven/config
tags:
  - Maven

---
## maven config, maven-compiler-plugin

maven-compiler-plugin 3.6和更高版本提供了一种新方法

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    maven-compiler-plugin</artifactId>
    <version>3.8.0</version>
    <configuration>
        <release>9</release>
    </configuration>
</plugin>

也可以只声明: 

<properties>
    <maven.compiler.release>16</maven.compiler.release>
</properties>

maven-compiler-plugin 从3.6开始可以只配置 maven.compiler.release, 来替代maven.compiler.source and maven.compiler.target
maven-compiler-plugin 会从 <properties> 里读取maven.compiler.release, 可以不配置到plugin>configuration下

"maven.compiler.release" as an replacement for source and target

http://blog.csdn.net/zhaoyongnj2012/article/details/23970451

在maven的默认配置中,对于jdk的配置是1.4版本,那么创建/导入maven工程过程中,工程中未指定jdk版本。

对工程进行maven的update,就会出现工程依赖的JRE System Library会自动变成JavaSE-1.4。
  
解决方案1: 修改maven的默认jdk配置

maven的conf\setting.xml文件中找到jdk配置的地方,修改如下: 


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


[html] view plaincopy
  
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

