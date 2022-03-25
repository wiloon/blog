---
title: META-INF, MANIFEST.MF
author: "-"
date: 2014-01-01T14:36:05+00:00
url: /?p=6102
categories:
  - java
tags:
  - java

---
## META-INF, MANIFEST.MF

做过 JAVA EE 开发的工程师应该都知道在 JAVA build 出来的 JAR 或者 WAR 的顶层目录下有个 META-INF 文件夹吧，可是有多少人能够清楚说出这个文件夹到底是做神马的? What is the purpose of META-INF? 恐怕不是都能说的清楚准确吧。

把这个问题抛出来，是因为我在公司的项目中发现 META-INF 这个文件夹被误用了，看来不是每个人都清楚 :)

所谓 META-INF, 说白了就是存放一些 meta information 相关的文件的这么一个文件夹, 一般来说尽量不要自己手工放置文件到这个文件夹。怎么理解这句话呢？ 就是说这个文件夹应该被看作是 JAVA 工程的一个内部 META 目录，所以这个目录下的文件应该都是 build 工具来生成的。我们自己的文件应该直接放到根目录下或者其他的子目录中。

根据官方的 JAR file specification (http://docs.oracle.com/javase/7/docs/technotes/guides/jar/jar.html), 一个典型的 META-INF 目录下可能包含如下几种文件或者子目录: 

- MANIFEST.MF: The manifest file that is used to define extension and package related data.
- INDEX.LIST
- x.SF
- x.DSA
- services/

不过理想和现实总是有差距，现在即使一些著名的开源代码对 META-INF 的使用上都存在大的差异，类似 Apache CXF 中就有这样的Spring配置: 

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns:jaxws="http://cxf.apache.org/jaxws"
     xsi:schemaLocation="
http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-2.0.xsd
http://cxf.apache.org/jaxws http://cxf.apache.org/schema/jaxws.xsd">

     <import resource="classpath:META-INF/cxf/cxf.xml" />
     <import resource="classpath:META-INF/cxf/cxf-extension-soap.xml" />
     <import resource="classpath:META-INF/cxf/cxf-servlet.xml" />
  ...
</beans>
```
更多讨论见stackoverflow的一个Q&A:

>http://stackoverflow.com/questions/70216/whats-the-purpose-of-meta-inf
>http://umi.iteye.com/blog/1503898
