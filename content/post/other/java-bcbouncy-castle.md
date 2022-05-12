---
title: java BC/Bouncy Castle
author: "-"
date: 2012-06-21T04:49:08+00:00
url: /?p=3563
categories:
  - Java
tags:
  - reprint
---
## java BC/Bouncy Castle

我们知道，Java标准库提供了一系列常用的哈希算法。

但如果我们要用的某种算法，Java标准库没有提供怎么办？

方法一: 自己写一个，难度很大；

方法二: 找一个现成的第三方库，直接使用。

BouncyCastle就是一个提供了很多哈希算法和加密算法的第三方库。它提供了Java标准库没有的一些算法，例如，RipeMD160哈希算法。

download  bcprov-jdk16-146.jar

add jar to '$JAVA_HOME$jrelibext'

java.security file in %JAVA_HOME%/jre/lib/security directory

add the following line like :

### List of providers and their preference orders (see above):
    security.provider.1=sun.security.provider.Sun
    security.provider.2=sun.security.rsa.SunRsaSign
      
    security.provider.3=com.sun.net.ssl.internal.ssl.Provider
      
    security.provider.4=com.sun.crypto.provider.SunJCE
      
    security.provider.5=sun.security.jgss.SunProvider
      
    security.provider.6=com.sun.security.sasl.Provider
      
    security.provider.7=org.jcp.xml.dsig.internal.dom.XMLDSigRI
      
    security.provider.8=sun.security.smartcardio.SunPCSC
      
    security.provider.9=org.bouncycastle.jce.provider.BouncyCastleProvider


---

https://www.bouncycastle.org/
