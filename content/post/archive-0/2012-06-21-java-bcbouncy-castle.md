---
title: java BC/Bouncy Castle
author: w1100n
type: post
date: 2012-06-21T04:49:08+00:00
url: /?p=3563
categories:
  - Java

---
download  bcprov-jdk16-146.jar

add jar to '$JAVA_HOME$jrelibext'

java.security file in %JAVA_HOME%/jre/lib/security directory

add the following line like :

#
  
# List of providers and their preference orders (see above):
  
#
  
security.provider.1=sun.security.provider.Sun
  
security.provider.2=sun.security.rsa.SunRsaSign
  
security.provider.3=com.sun.net.ssl.internal.ssl.Provider
  
security.provider.4=com.sun.crypto.provider.SunJCE
  
security.provider.5=sun.security.jgss.SunProvider
  
security.provider.6=com.sun.security.sasl.Provider
  
security.provider.7=org.jcp.xml.dsig.internal.dom.XMLDSigRI
  
security.provider.8=sun.security.smartcardio.SunPCSC
  
security.provider.9=org.bouncycastle.jce.provider.BouncyCastleProvider