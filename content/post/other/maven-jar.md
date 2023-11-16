---
title: Maven jar plugin
author: "-"
date: 2015-08-24T01:46:57+00:00
url: /?p=8143
categories:
  - Inbox
tags:
  - reprint
---
## Maven jar plugin

1.修改pom.xml增加如下内容

```xml
  
 <plugin> <groupId>org.apache.maven.plugins</groupId>

   
<artifactId>maven-jar-plugin</artifactId>
   
<version>2.4</version>
   
<configuration>
   

   
<manifest>
   
true</addClasspath>
   
<classpathPrefix>lib/</classpathPrefix>
   
<mainClass>com.sysware.HelloWorld</mainClass>
   
</manifest>
   
</archive>
   
</configuration> </plugin> 

```

运行mvn clean package即可

3.

```html```

<build>
  
<finalName>...</finalName><sourceDirectory>src/main/java</sourceDirectory>
  
<resources>
  
<!-- 控制资源文件的拷贝 -->
  
<resource>
  
<directory>src/main/resources</directory>
  
<targetPath>${project.build.directory}</targetPath>
  
</resource>
  
</resources> <plugins> <!-- 设置源文件编码方式 --><plugin> <groupId>org.apache.maven.plugins</groupId>
  
<artifactId>maven-compiler-plugin</artifactId>
  
<configuration>
  
<defaultLibBundleDir>lib</defaultLibBundleDir><source>1.6</source>
  
<target>1.6</target>
  
<encoding>UTF-8</encoding>
  
</configuration> </plugin> <!-- 打包jar文件时，配置manifest文件，加入lib包的jar依赖 --><plugin> <groupId>org.apache.maven.plugins</groupId>
  
<artifactId>maven-jar-plugin</artifactId>
  
<configuration>
  
<manifest>
  
true</addClasspath>
  
<classpathPrefix>lib/</classpathPrefix>
  
<mainClass>.....MonitorMain</mainClass>
  
</manifest>
  
</archive>
  
</configuration> </plugin> <!-- 拷贝依赖的jar包到lib目录 --><plugin> <groupId>org.apache.maven.plugins</groupId>
  
<artifactId>maven-dependency-plugin</artifactId>
  
<executions>
  
<execution>
  
<id>copy</id> <phase>package</phase> <goals>
  
<goal>copy-dependencies</goal>
  
</goals>
  
<configuration>
  
<outputDirectory>
  
${project.build.directory}/lib
  
</outputDirectory>
  
</configuration>
  
</execution>
  
</executions> </plugin> <!-- 解决资源文件的编码问题 --><plugin> <groupId>org.apache.maven.plugins</groupId>
  
maven-resources-plugin</artifactId>
  
<version>2.3</version>
  
<configuration>
  
<encoding>UTF-8</encoding>
  
</configuration> </plugin> <!-- 打包source文件为jar文件 --><plugin> maven-source-plugin</artifactId>
  
<version>2.1</version>
  
<configuration>
  
true</attach>
  
<encoding>UTF-8</encoding>
  
</configuration>
  
<executions>
  
<execution> <phase>compile</phase> <goals>
  
<goal>jar</goal>
  
</goals>
  
</execution>
  
</executions> </plugin> </plugins> </build>

4.

```html```

<build>
  
<resources>
  
<resource>
  
<targetPath>${project.build.directory}/classes</targetPath>
  
<directory>src/main/resources</directory>
  
<filtering>true</filtering>
  
<includes>
  
<include>**/*.xml</include>
  
</includes>
  
</resource>
  
</resources> <plugins> <plugin> <groupId>org.apache.maven.plugins</groupId>
  
maven-compiler-plugin</artifactId>
  
<version>3.0</version>
  
<configuration><source>1.6</source>
  
<target>1.6</target>
  
<encoding>UTF-8</encoding>
  
</configuration> </plugin> <plugin> <groupId>org.apache.maven.plugins</groupId>
  
maven-shade-plugin</artifactId>
  
<version>2.0</version>
  
<executions>
  
<execution> <phase>package</phase> <goals>
  
<goal>shade</goal>
  
</goals>
  
<configuration>
  
<transformers> <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
  
<mainClass>com.test.testguava.app.App</mainClass>
  
</transformer> <transformer implementation="org.apache.maven.plugins.shade.resource.AppendingTransformer">
  
<resource>applicationContext.xml</resource>
  
</transformer> </transformers> <shadedArtifactAttached>true</shadedArtifactAttached>
  
<shadedClassifierName>executable</shadedClassifierName>
  
</configuration>
  
</execution>
  
</executions> </plugin> </plugins> </build>
  
地址: [http://blog.csdn.net/johnnywww/article/details/7964326](http://blog.csdn.net/johnnywww/article/details/7964326)

上一篇Eclipse Fat jar 插件地址
  
下一篇Java 高手之路笔记 (1)

[http://blog.csdn.net/zhangdaiscott/article/details/6911640](http://blog.csdn.net/zhangdaiscott/article/details/6911640)

[http://blog.csdn.net/johnnywww/article/details/7964326](http://blog.csdn.net/johnnywww/article/details/7964326)
