---
title: maven pom
author: "-"
date: 2014-04-30T07:27:00+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: maven-pom
categories:
  - Java
tags:
  - maven
  - remix
  - AI-assisted
aliases:
  - /p6575/
---
## maven pom
基本内容: 
  
POM包括了所有的项目信息。
  
maven 相关: 
  
pom定义了最小的maven2元素，允许groupId,artifactId,version。所有需要的元素
  
groupId:项目或者组织的唯一标志，并且配置时生成的路径也是由此生成，如org.codehaus.mojo生成的相对路径为: /org/codehaus/mojo
  
artifactId: 项目的通用名称
  
version:项目的版本
  
packaging: 打包的机制，如pom, jar, maven-plugin, ejb, war, ear, rar, par
  
classifier: 分类

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
<modelVersion>4.0.0</modelVersion>
<groupId>com.wiloon</groupId>
wechat</artifactId>
<packaging>jar</packaging>
<version>1.0-SNAPSHOT</version>
<name>wechat</name>
<url>http://maven.apache.org</url>
<dependencies>
<dependency>
<groupId>junit</groupId>
junit</artifactId>
<version>3.8.1</version>
<scope>test</scope>
</dependency>
</dependencies>
</project>
compile plugin, war plugin, specify jdk version
<build>
<plugins>
<plugin>
<groupId>org.apache.maven.plugins</groupId>
maven-compiler-plugin</artifactId>
<configuration>
<source>1.7</source>
<target>1.7</target>
</configuration>
</plugin>
<plugin>
<groupId>org.apache.maven.plugins</groupId>
<artifactId>maven-war-plugin</artifactId>
</plugin>
</plugins>
</build>
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
