---
title: keystore, truststore, pem
author: wiloon
type: post
date: 2018-02-22T07:21:37+00:00
url: /?p=11902
categories:
  - Uncategorized

---
然后是PEM，它是由RFC1421至1424定义的一种数据格式。其实前面的.cert和.key文件都是PEM格式的，只不过在有些系统中（比如Windows）会根据扩展名不同而做不同的事。所以当你看到.pem文件时，它里面的内容可能是certificate也可能是key，也可能两个都有，要看具体情况。可以通过openssl查看。

X.509是常见通用的证书格式。所有的证书都符合为Public Key Infrastructure (PKI) 制定的 ITU-T X509 国际标准。
  
X.509 DER 编码(ASCII)的后缀是： .DER .CER .CRT

X.509 PAM 编码(Base64)的后缀是： .PEM .CER .CRT
  
.cer/.crt是用于存放证书，它是2进制形式存放的，不含私钥。
  
.pem跟crt/cer的区别是它以Ascii来表示。

作者：刘长元
  
链接：https://www.zhihu.com/question/29620953/answer/45012411
  
来源：知乎
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

https://www.zhihu.com/question/29620953