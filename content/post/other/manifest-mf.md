---
title: MANIFEST.MF
author: "-"
date: 2012-04-08T11:42:35+00:00
lastmod: 2026-06-27T04:52:28+08:00
url: manifest-mf
categories:
  - Java
tags:
  - java
  - jar
  - remix
  - AI-assisted
aliases:
  - /p2876/
---

## 字段速查

`MANIFEST.MF` 是 jar 的清单文件，位于 `META-INF/` 下，声明 jar 的入口、classpath 等元数据。常用字段：

| 字段 | 说明 |
| ---- | ---- |
| `Manifest-Version` | manifest 格式版本，通常 `1.0` |
| `Main-Class` | `java -jar` 时 JVM 执行的入口类 |
| `Class-Path` | 运行时需要的外部 jar 路径 |
| `Start-Class` | **Spring Boot 专有**：真正的应用主类（此时 `Main-Class` 指向 loader 的 `JarLauncher`） |

格式规则（容易踩坑）：

- 每行 `Key: Value`，冒号后**一个空格**
- 每行最长 **72 字节**，超长的值需换行并以**一个前导空格**续行
- 文件必须以**空行**结尾，否则最后一个属性会被静默忽略

Spring Boot 可执行 JAR 中 `Main-Class` / `Start-Class` 的分工，以及 JVM 如何读取 manifest 启动应用，见 [Spring Boot Executable JAR](../language/java/spring/spring-boot-executable-jar.md)。

## 历史

- 规范：Java JAR File Specification，属 Java SE 标准，由 Oracle（原 Sun）维护
- jar 格式基于 ZIP；`META-INF/MANIFEST.MF` 在最初的 jar 规范里就被强制要求

| 年份 | 事件 |
| ---- | ---- |
| 1996 | JDK 1.0，尚无 jar 格式 |
| 1997 | JDK 1.1 引入 jar 与 `MANIFEST.MF` |
| 1999 | JDK 1.2 扩展签名、sealed package 等 |
| 至今 | 核心结构未变；Spring Boot 等框架在其上追加自定义属性 |

## 完整字段说明（历史整理）

打开Java的JAR文件我们经常可以看到文件中包含着一个META-INF目录，这个目录下会有一些文件，其中必有一个MANIFEST.MF，这个文件描述了该Jar文件的很多信息，下面将详细介绍MANIFEST.MF文件的内容，先来看struts.jar中包含的MANIFEST.MF文件内容: 

    Manifest-Version: 1.0
    Created-By: Apache Ant 1.5.1
    Extension-Name: Struts Framework
    Specification-Title: Struts Framework
    Specification-Vendor: Apache Software Foundation
    Specification-Version: 1.1
    Implementation-Title: Struts Framework
    Implementation-Vendor: Apache Software Foundation
    Implementation-Vendor-Id: org.apache
    Implementation-Version: 1.1
    Class-Path:  commons-beanutils.jar commons-collections.jar commons-digester.jar commons-logging.jar commons-validator.jar jakarta-oro.jar struts-legacy.jar

如果我们把MANIFEST中的配置信息进行分类，可以归纳出下面几个大类: 

### 一. 一般属性

1. Manifest-Version
用来定义manifest文件的版本，例如: Manifest-Version: 1.0

2. Created-By
声明该文件的生成者，一般该属性是由jar命令行工具生成的，例如: Created-By: Apache Ant 1.5.1

3. Signature-Version
定义jar文件的签名版本

4. Class-Path
应用程序或者类装载器使用该值来构建内部的类搜索路径

### 二. 应用程序相关属性

1. Main-Class
定义jar文件的入口类，该类必须是一个可执行的类，一旦定义了该属性即可通过 java -jar x.jar来运行该jar文件。

### 三. 小程序(Applet)相关属性

1. Extendsion-List
该属性指定了小程序需要的扩展信息列表，列表中的每个名字对应以下的属性
  
2. <extension>-Extension-Name
3. <extension>-Specification-Version
4. <extension>-Implementation-Version
5. <extension>-Implementation-Vendor-Id
5. <extension>-Implementation-URL

### 扩展标识属性
1. Extension-Name
该属性定义了jar文件的标识，例如Extension-Name: Struts Framework

五. 包扩展属性

1. Implementation-Title   定义了扩展实现的标题
  
2. Implementation-Version   定义扩展实现的版本
  
3. Implementation-Vendor   定义扩展实现的组织
  
4. Implementation-Vendor-Id   定义扩展实现的组织的标识
  
5. Implementation-URL :   定义该扩展包的下载地址(URL)
  
6. Specification-Title   定义扩展规范的标题
  
7. Specification-Version   定义扩展规范的版本
  
8. Specification-Vendor   声明了维护该规范的组织
  
9. Sealed   定义jar文件是否封存，值可以是true或者false (这点我还不是很理解)

六. 签名相关属性

签名方面的属性我们可以来参照JavaMail所提供的mail.jar中的一段

Name: javax/mail/Address.class
  
Digest-Algorithms: SHA MD5
  
SHA-Digest: AjR7RqnN//cdYGouxbd06mSVfI4=
  
MD5-Digest: ZnTIQ2aQAtSNIOWXI1pQpw==

这段内容定义类签名的类名、计算摘要的算法名以及对应的摘要内容(使用BASE64方法进行编码)

七.自定义属性

除了前面提到的一些属性外，你也可以在MANIFEST.MF中增加自己的属性以及响应的值，例如J2ME程序jar包中就可能包含着如下信息

MicroEdition-Configuration: CLDC-1.0
  
MIDlet-Name: J2ME_MOBBER Midlet Suite
  
MIDlet-Info-URL: [http://www.javayou.com/](http://www.javayou.com/)
  
MIDlet-Icon: /icon.png
  
MIDlet-Vendor: Midlet Suite Vendor
  
MIDlet-1: mobber,/icon.png,mobber
  
MIDlet-Version: 1.0.0
  
MicroEdition-Profile: MIDP-1.0
  
MIDlet-Description: Communicator

关键在于我们怎么来读取这些信息呢？其实很简单，JDK给我们提供了用于处理这些信息的API，详细的信息请见java.util.jar包中，我们可以通过给JarFile传递一个jar文件的路径，然后调用JarFile的getManifest方法来获取Manifest信息。

[http://docs.oracle.com/javase/1.3/docs/guide/jar/jar.html](http://docs.oracle.com/javase/1.3/docs/guide/jar/jar.html)

[http://java.sun.com/developer/Books/javaprogramming/JAR/basics/manifest.html](http://java.sun.com/developer/Books/javaprogramming/JAR/basics/manifest.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-27 | 顶部新增「字段速查」（含 Spring Boot `Start-Class`、72 字节/空行结尾等格式规则）与「历史」小节；删除 reprint 标签 | 合并 comments-tree 启动打包文档的 MANIFEST.MF 章节 |