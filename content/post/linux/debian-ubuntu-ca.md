---
author: "-"
date: "2020-07-08 16:52:26"
title: "debian ubuntu ca"
categories:
  - inbox
tags:
  - reprint
---
## "debian ubuntu ca"

https://www.jianshu.com/p/abcee3270e9a
    
    mkdir /usr/share/ca-certificates/extra
    cp /tmp/$1.crt /usr/share/ca-certificates/extra/$1.crt
    update-ca-certificates

直白的说，运行这个工具，它最终会更新 /etc/ssl/certs/ca-certificates.crt 文件。这下你应该明白了，有了这个文件，不管是 Curl 还是 openssl 在发送 HTTPS 请求的时候，都可以校验 HTTPS 网站的真实身份了。

具体执行步骤如下: 

读取 /etc/ca-certificates.conf 文件，包含的内容就是所有 /usr/share/ca-certificates/mozilla/ 目录下的证书文件名。
将 /etc/ca-certificates.conf 文件对应的所有证书合并到 /etc/ssl/certs/ca-certificates.crt 文件中。

作者: 虞大胆的叽叽喳喳
链接: https://www.jianshu.com/p/abcee3270e9a
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。