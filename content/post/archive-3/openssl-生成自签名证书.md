---
title: Openssl 生成自签名证书
author: "-"
date: 2019-03-24T03:49:46+00:00
url: /?p=13935
categories:
  - Inbox
tags:
  - reprint
---
## Openssl 生成自签名证书
```bash
# 生成私钥
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
# Common Name: 输入 *.wiloon.com 这种方式生成通配符域名证书
# A challenge password: 密码可以留空

# 查看证书请求文件的内容
openssl req -text -noout -in server.csr

openssl x509 -req -in server.csr -out server.crt -signkey server.key -days 3650

# 这样就生成了有效期为: 10年的自签名证书 server.crt.


openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt -extensions v3_req -extfile openssl.cnf

```

https://ningyu1.github.io/site/post/51-ssl-cert/
  
http://liaoph.com/openssl-san/
  
https://codeday.me/bug/20170831/60851.html