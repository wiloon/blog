---
title: Java tls, JSSE
author: "-"
date: 2018-02-11T05:31:05+00:00
url: /?p=11866
categories:
  - Inbox
tags:
  - reprint
---
## Java tls, JSSE
Java JSSE Java Secure Socket Extension
  
JDK 中的 JSSE (javax.net.ssl) ,提供了对 SSL 和 TLS 的支持
  
SSL/TLS 协议 (RFC2246 RFC4346) 处于 TCP/IP 协议与各种应用层协议之间,为数据通讯提供安全支持。

  1. SSL/TLS 记录协议 (SSL/TLS Record Protocol) ,它建立在可靠的传输层协议 (如 TCP) 之上,为上层协议提供数据封装、压缩、加密等基本功能。
  2. SSL/TLS 握手协议 (SSL/TLS Handshake Protocol) ,它建立在 SSL/TLS 记录协议之上,用于在实际的数据传输开始前,通讯双方进行身份认证、协商加密算法、交换加密密钥等初始化协商功能。

从协议使用方式来看,又可以分成两种类型: 
  
1. SSL/TLS 单向认证,就是用户到服务器之间只存在单方面的认证,即客户端会认证服务器端身份,而服务器端不会去对客户端身份进行验证。
  
2.SSL/TLS 双向认证,就是双方都会互相认证,也就是两者之间将会交换证书。基本的过程和单向认证完全一样,只是在协商阶段多了几个步骤.

对称算法 (symmetric cryptography) : 就是需要双方使用一样的 key 来加密解密消息算法,常用密钥算法有 Data Encryption Standard (DES) 、triple-strength DES (3DES) 、Rivest Cipher 2  (RC2) 和 Rivest Cipher 4 (RC4) 。因为对称算法效率相对较高,因此 SSL 会话中的敏感数据都用通过密钥算法加密。

非对称算法 (asymmetric cryptography) : 就是 key 的组成是公钥私钥对  (key-pair) ,公钥传递给对方私钥自己保留。公钥私钥算法是互逆的,一个用来加密,另一个可以解密。常用的算法有 Rivest Shamir Adleman (RSA) 、Diffie-Hellman (DH) 。非对称算法计算量大比较慢,因此仅适用于少量数据加密,如对密钥加密,而不适合大量数据的通讯加密。

jks 是 java 的 key store 文件格式. java 提供 keytool 工具操作jks.
  
keytool 是随 jre 发布的工具. 所以只要你安装了 jre 就有这个工具.
  
在windows上,是keytool.exe. 在Lunix上,是 keytool

jks 类似于 pfx(p12) 文件, 有密码加密, 可以保存多个key 或者证书等等. key 或者 证书被称为一个 entry, 每个entry有个别名(alias). 操作时需要制定别名.

KeyStore是服务器的密钥存储库,存服务器的公钥私钥证书

TrustStore是服务器的信任密钥存储库,存CA公钥,但有一部分人存的是客户端证书集合
  
keystore和truststore其本质都是keystore。只不过二者盛放的密钥所有者不同而已,对于keystore一般存储自己的私钥和公钥,而truststore则用来存储自己信任的对象的公钥。

下面是几个常见的错误

1.KeyStore和TrustStore做成同一个JKS文件或PKCS12文件。通过导入客户端证书来实现验证客户端证书。实际生产中并不能这么做,客户端有成千上万个,你不可能都去导吧。

2.openssl生成CA、server、client证书,用同样的方法转成PKCS12文件,KeyStore指定server.p12,TrustStore指定CA.p12、浏览器证书个人存储区存client.p12,受信任的根证书颁发机构存CA.p12,总体思路是对的,但是CA这里这里绝对不能将私钥也导入到PKCS12中,一个正常的CA要是把CA私钥泄露了那不就惨了。

KeyTool 生成自签发证书

eytool常用命令
  
-alias 产生别名
  
-keystore 指定密钥库的名称(就像数据库一样的证书库,可以有很多个证书,cacerts这个文件是jre自带的,
               
你也可以使用其它文件名字,如果没有这个文件名字,它会创建这样一个)
  
-storepass 指定密钥库的密码
  
-keypass 指定别名条目的密码
  
-list 显示密钥库中的证书信息
  
-v 显示密钥库中的证书详细信息
  
-export 将别名指定的证书导出到文件
  
-file 参数指定导出到文件的文件名
  
-delete 删除密钥库中某条目
  
-import 将已签名数字证书导入密钥库
  
-keypasswd 修改密钥库中指定条目口令
  
-dname 指定证书拥有者信息
  
-keyalg 指定密钥的算法
  
-validity 指定创建的证书有效期多少天
  
-keysize 指定密钥长度
  
If -rfc is specified, output format is BASE64-encoded PEM; otherwise, a binary DER is created.

第一步: 为服务器生成证书

命令:
  
keytool
  
-genkey
  
-alias tomcat(别名)
  
-keypass 123456(别名密码)
  
-keyalg RSA(算法)
  
-keysize 1024(密钥长度)
  
-validity 3650(有效期,天单位)
  
-keystore tomcat.keystore(指定生成证书的位置和证书名称)
  
-storepass 123456(获取keystore信息的密码)

方便复制版: 
  
keytool -genkey -alias tomcat -keypass 123456 -keyalg RSA -keysize 1024 -validity 3650 -keystore D:/keys/tomcat.keystore -storepass 123456

用keytool创建Keystore和Trustsotre文件

JSSE使用Truststore和Keystore文件来提供客户端和服务器之间的安全数据传输。keytool是一个工具可以用来创建包含公钥和密钥的的keystore文件,并且利用keystore文件来创建只包含公钥的truststore文件。在本文中,我们学习如何通过下面的5步简单的创建truststore和keystore文件: 

    生成一个含有一个私钥的keystore文件 
    验证新生成的keystor而文件 
    导出凭证文件 
    把认凭证件导入到truststore文件 
    验证新创建的truststore文件 
    

  1. 创建一个客户端 keystore - 含有一个私钥的keystore文件

keystore和key
  
key,存放了数字证书 (包括公钥和发布者的数字签名) ,以及私钥

生成JKS格式的KeyStore

JKS与其他密钥存储可有一个区别就是,不仅密钥存储库可以设置密码,并且里面的条目也可以设置密码,条目如果不设置密码默认与密钥库密码一致,条目可以存证书、密钥对,但是私钥不能直接导出
  
1.生成密钥库

不能单纯的生成一个密钥库,生成密钥库的时候必须同时生成一个条目
  
下面这个命令在当前工作目录生成了一个密钥库文件clientkeystore,里面存储了一个别名为client的密钥对

Java的Keytool工具可以把密钥和认证保存到keystore文件。 如果在windows上,keytool命令被放到Java的bin目录下(例如C:\Program Files\Java\jdk1.6.0_12)。如果是mac上是放在/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands目录下。
  
执行下列命令来生成keystore
  
keytool -genkey -alias sslclient -keysize 2048 -validity 3650 -keyalg RSA -dname "CN=localhost" -keypass 123456 -storepass 123456 -keystore sslclientkeys

  1. 验证新生成的keystor而文件
  
    keytool -list -v -keystore keystore.jks 

执行上面的命令后,你会看到key的详细信息: 

  1. 导出公钥证书
  
    将key以数字证书的形式从keystore中导出,数字证书 (包括公钥和发布者的数字签名) 
  
    下面的命令可以导出自签公钥证书

在这一步,你可以导出自我签署凭证或是Verisign或其他的认证机构的商业凭证的。这里只说导出自我签署的凭证: 

通过执行下面的命令把自我签署的凭证保存到 "selfsignedcert.cer"文件
  
keytool -export -alias certificatekey -keystore keystore.jks -storepass 123456 -file selfsignedcert.cer
  
keytool -export -alias certificatekey -keystore keystore.jks -rfc -file selfsignedcert.cer

执行上面的命令,会要求你输入密码,就是上面生成keystore的输入的密码"123456",

keytool -import -alias sslclient -keystore sslservertrust -file sslclient.cer
  
truststore和keystore的性质是一样的,都是存放key的一个仓库,区别在于,truststore里存放的是只包含公钥的数字证书,代表了可以信任的证书,而keystore是包含私钥的。

https://www.jianshu.com/p/981431a2b6ea
   
https://www.ibm.com/developerworks/cn/java/j-lo-ssltls/
  
https://www.ibm.com/developerworks/cn/java/j-lo-socketkeytool/index.html
  
https://waylau.com/essential-netty-in-action/CORE%20FUNCTIONS/Securing%20Netty%20applications%20with%20SSLTLS.html
  
https://www.jianshu.com/p/981431a2b6ea


  
    使用java keytool 查看,添加,删除 jks 文件
  


https://blog.byneil.com/%e4%bd%bf%e7%94%a8java-keytool-%e6%9f%a5%e7%9c%8b%e6%b7%bb%e5%8a%a0%e5%88%a0%e9%99%a4-jks-%e6%96%87%e4%bb%b6/embed/#?secret=701X4GNJmy
  
http://www.cnblogs.com/benio/archive/2010/09/15/1826990.html
  
http://yushan.iteye.com/blog/434955
  
http://lukejin.iteye.com/blog/605634
  
http://www.cnblogs.com/gsls200808/p/4500246.html
  
http://www.cnblogs.com/gaoxing/p/4805311.html
  
http://www.cnblogs.com/orientsun/archive/2012/07/26/2609444.html
  
https://docs.oracle.com/javase/8/docs/api/javax/net/ssl/SSLContext.html