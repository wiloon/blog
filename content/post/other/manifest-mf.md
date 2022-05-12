---
title: MANIFEST.MF
author: "-"
date: 2012-04-08T11:42:35+00:00
url: /?p=2876
categories:
  - Java
tags:
  - reprint
---
## MANIFEST.MF
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

### 四. 扩展标识属性
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
  
MIDlet-Info-URL: <http://www.javayou.com/>
  
MIDlet-Icon: /icon.png
  
MIDlet-Vendor: Midlet Suite Vendor
  
MIDlet-1: mobber,/icon.png,mobber
  
MIDlet-Version: 1.0.0
  
MicroEdition-Profile: MIDP-1.0
  
MIDlet-Description: Communicator

关键在于我们怎么来读取这些信息呢？其实很简单，JDK给我们提供了用于处理这些信息的API，详细的信息请见java.util.jar包中，我们可以通过给JarFile传递一个jar文件的路径，然后调用JarFile的getManifest方法来获取Manifest信息。

<http://docs.oracle.com/javase/1.3/docs/guide/jar/jar.html>

<http://java.sun.com/developer/Books/javaprogramming/JAR/basics/manifest.html>