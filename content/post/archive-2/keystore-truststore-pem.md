---
title: 证书, x509, keystore, truststore, pem, 
author: "-"
date: 2018-02-22T07:21:37+00:00
url: /?p=11902
categories:
  - inbox
tags:
  - reprint
---
## 证书, x509, keystore, truststore, pem,
### 证书和编码
X.509证书,其核心是根据RFC 5280编码或数字签名的数字文档。

实际上，术语X.509证书通常指的是IETF的PKIX证书和X.509 v3证书标准的CRL 文件，即如RFC 5280 (通常称为PKIX for Public Key Infrastructure (X.509））中规定的。

### .CRT 扩展名
.CRT = CRT扩展用于证书。 证书可以被编码为二进制DER或ASCII PEM。 CER和CRT扩展几乎是同义词。 最常见的于Unix 或类Unix系统。

### .cer
.CER扩展名
 CER = .crt的替代形式 (Microsoft Convention）您可以在微软系统环境下将.crt转换为.cer (.both DER编码的.cer，或base64 [PEM]编码的.cer）。

可参考：https://support.comodo.com/index.php?/Knowledgebase/Article/View/361/17/how-do-i-convert-crt-file-into-the-microsoft-cer-format

.cer文件扩展名也被IE识别为 一个运行MS cryptoAPI命令的命令 (特别是rundll32.exe cryptext.dll，CryptExtOpenCER），该命令显示用于导入和/或查看证书内容的对话框。 

### .KEY 扩展名
     .KEY = KEY扩展名用于公钥和私钥PKCS＃8。 键可以被编码为二进制DER或ASCII PEM。

---

PEM是由RFC1421至1424定义的一种数据格式。其实前面的.cert和.key文件都是PEM格式的,只不过在有些系统中 (比如Windows) 会根据扩展名不同而做不同的事。所以当你看到.pem文件时,它里面的内容可能是certificate也可能是key,也可能两个都有,要看具体情况。可以通过openssl查看。  

X.509 - 是一种常见通用的证书标准,主要定义了证书中应该包含哪些内容.其详情可以参考RFC5280,SSL使用的就是这种证书标准.  
X.509是常见通用的证书格式。所有的证书都符合为Public Key Infrastructure (PKI) 制定的 ITU-T X509 国际标准。  
证书标准

X.509 DER 编码(ASCII)的后缀是:  .DER .CER .CRT  
X.509 PEM 编码(Base64)的后缀是:  .PEM .CER .CRT  
.cer/.crt是用于存放证书,它是2进制形式存放的,不含私钥。  
.pem跟crt/cer的区别是它以Ascii来表示。  

编码格式
同样的X.509证书,可能有不同的编码格式,目前有以下两种编码格式.

### PEM 

.PEM = PEM扩展用于不同类型的X.509v3文件，是以“ - BEGIN ...”前缀的ASCII (Base64）数据。

Privacy Enhanced Mail,打开看文本格式,以"-----BEGIN..."开头, "-----END..."结尾,内容是BASE64编码.
查看PEM格式证书的信息:

    openssl x509 -in certificate.pem -text -noout

Apache和*NIX服务器偏向于使用这种编码格式.

#### convert multi line pem to signle line pem
    awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' cert-name.pem

https://docs.vmware.com/cn/Unified-Access-Gateway/2.9/com.vmware.access-point-29-deploy-config/GUID-870AF51F-AB37-4D6C-B9F5-4BFEB18F11E9.html

### .DER 扩展名
.DER = DER扩展用于二进制DER编码证书。

这些文件也可能承载CER或CRT扩展。 正确的说法是“我有一个DER编码的证书”不是“我有一个DER证书”。
### DER 
Distinguished Encoding Rules, 打开看是二进制格式,不可读.
查看DER格式证书的信息:

    openssl x509 -in certificate.der -inform der -text -noout

Java和Windows服务器偏向于使用这种编码格式.

相关的文件扩展名
这是比较误导人的地方,虽然我们已经知道有PEM和DER这两种编码格式,但文件扩展名并不一定就叫"PEM"或者"DER",常见的扩展名除了PEM和DER还有以下这些,它们除了编码格式可能不同之外,内容也有差别,但大多数都能相互转换编码格式.

CRT - CRT应该是certificate的三个字母,其实还是证书的意思,常见于*NIX系统,有可能是PEM编码,也有可能是DER编码,大多数应该是PEM编码,相信你已经知道怎么辨别.

CER - 还是certificate,还是证书,常见于Windows系统,同样的,可能是PEM编码,也可能是DER编码,大多数应该是DER编码.

KEY - 通常用来存放一个公钥或者私钥,并非X.509证书,编码同样的,可能是PEM,也可能是DER.
查看KEY的办法:openssl rsa -in mykey.key -text -noout
如果是DER格式的话,同理应该这样了:openssl rsa -in mykey.key -text -noout -inform der

CSR - Certificate Signing Request,即证书签名请求,这个并不是证书,而是向权威证书颁发机构获得签名证书的申请,其核心内容是一个公钥(当然还附带了一些别的信息),在生成这个申请的时候,同时也会生成一个私钥,私钥要自己保管好.做过iOS APP的朋友都应该知道是怎么向苹果申请开发者证书的吧.
查看的办法:openssl req -noout -text -in my.csr (如果是DER格式的话照旧加上-inform der,这里不写了)

PFX/P12 - predecessor of PKCS#12,对*nix服务器来说,一般CRT和KEY是分开存放在不同文件中的,但Windows的IIS则将它们存在一个PFX文件中,(因此这个文件包含了证书及私钥)这样会不会不安全？应该不会,PFX通常会有一个"提取密码",你想把里面的东西读取出来的话,它就要求你提供提取密码,PFX使用的时DER编码,如何把PFX转换为PEM编码？
openssl pkcs12 -in for-iis.pfx -out for-iis.pem -nodes
这个时候会提示你输入提取代码. for-iis.pem就是可读的文本.
生成pfx的命令类似这样:openssl pkcs12 -export -in certificate.crt -inkey privateKey.key -out certificate.pfx -certfile CACert.crt

其中CACert.crt是CA(权威证书颁发机构)的根证书,有的话也通过-certfile参数一起带进去.这么看来,PFX其实是个证书密钥库.

JKS - 即Java Key Storage,这是Java的专利,跟OpenSSL关系不大,利用Java的一个叫"keytool"的工具,可以将PFX转为JKS,当然了,keytool也能直接生成JKS,不过在此就不多表了.

证书编码的转换
PEM转为DER openssl x509 -in cert.crt -outform der -out cert.der

DER转为PEM openssl x509 -in cert.crt -inform der -outform pem -out cert.pem

(提示:要转换KEY文件也类似,只不过把x509换成rsa,要转CSR的话,把x509换成req...)

获得证书
向权威证书颁发机构申请证书

用这命令生成一个csr: openssl req -newkey rsa:2048 -new -nodes -keyout my.key -out my.csr
把csr交给权威证书颁发机构,权威证书颁发机构对此进行签名,完成.保留好csr,当权威证书颁发机构颁发的证书过期的时候,你还可以用同样的csr来申请新的证书,key保持不变.

或者生成自签名的证书
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
在生成证书的过程中会要你填一堆的东西,其实真正要填的只有Common Name,通常填写你服务器的域名,如"yourcompany.com",或者你服务器的IP地址,其它都可以留空的.
生产环境中还是不要使用自签的证书,否则浏览器会不认,或者如果你是企业应用的话能够强制让用户的浏览器接受你的自签证
书也行.向权威机构要证书通常是要钱的,但现在也有免费的,仅仅需要一个简单的域名验证即可.有兴趣的话查查"沃通数字证书".

### convert pem to der
    openssl x509 -outform der -in certificate.pem -out certificate.der

### pem to jks
    https://docs.oracle.com/cd/E35976_01/server.740/es_admin/src/tadm_ssl_convert_pem_to_jks.html

---
https://www.cnblogs.com/guogangj/p/4118605.html

作者: 刘长元  
链接: https://www.zhihu.com/question/29620953/answer/45012411  
来源: 知乎  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。  
https://www.zhihu.com/question/29620953


查看证书
 即使PEM编码的证书是ASCII，它们是不可读的。这里有一些命令可以让你以可读的形式输出证书的内容;

 1.1）查看PEM编码证书
openssl x509 -in cert.pem -text -noout

openssl x509 -in cert.cer -text -noout

openssl x509 -in cert.crt -text -noout

 如果您遇到这个错误，这意味着您正在尝试查看DER编码的证书，并需要使用“查看DER编码证书”中的命令。
unable to load certificate

12626:error:0906D06C:PEMroutines:PEM_read_bio:no start line:pem_lib.c:647:Expecting: TRUSTEDCERTIFICATE
1.2）查看DER编码证书
openssl x509 -in certificate.der -inform der -text -noout

如果您遇到以下错误，则表示您尝试使用DER编码证书的命令查看PEM编码证书。在“查看PEM编码的证书”中使用命令
unable to load certificate

13978:error:0D0680A8:asn1 encodingroutines:ASN1_CHECK_TLEN:wrong tag:tasn_dec.c:1306:

13978:error:0D07803A:asn1 encodingroutines:ASN1_ITEM_EX_D2I:nested asn1 error:tasn_dec.c:380:Type=X509

2）转换证书格式
转换可以将一种类型的编码证书存入另一种。 (即PEM到DER转换）
PEM到DER
openssl x509 -in cert.crt -outform der-out cert.der
DER到PEM
openssl x509 -in cert.crt -inform der -outform pem -out cert.pem

3）组合证书
在某些情况下，将多个X.509基础设施组合到单个文件中是有利的。一个常见的例子是将私钥和公钥两者结合到相同的证书中。

组合密钥和链的最简单的方法是将每个文件转换为PEM编码的证书，然后将每个文件的内容简单地复制到一个新文件中。这适用于组合文件以在Apache中使用的应用程序。

4)证书提取
一些证书将以组合形式出现。 一个文件可以包含以下任何一个：证书，私钥，公钥，签名证书，证书颁发机构 (CA）和/或权限链。

 

五、原文链接
https://support.ssl.com/index.php?/Knowledgebase/Article/View/19/0/der-vs-crt-vs-cer-vs-pem-certificates-and-how-to-convert-them



>https://blog.csdn.net/xiangguiwang/article/details/76400805

