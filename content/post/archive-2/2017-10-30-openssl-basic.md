---
title: openssl basic
author: wiloon
type: post
date: 2017-10-30T09:16:49+00:00
url: /?p=11332
categories:
  - Uncategorized

---
```bash
# openssl 解密  
openssl pkeyutl -inkey xxx-pri.pem -decrypt -pkeyopt rsa\_padding\_mode:oaep -pkeyopt rsa\_oaep\_md:sha256 -in foo.bin -out result.dec

# 查看公钥内容  
openssl rsa -inform PEM -in xxx-pub.pem -pubin -text

# generate private key  
openssl genrsa -out pri2048.key 2048

# generate public key  
openssl rsa -inform PEM -outform PEM -in pri2048.key -out pub2048.key -pubout

# 查看证书信息
openssl x509 -noout -text -in ca.crt

# 验证证书
openssl verify selfsign.crt
```

https://github.com/denji/golang-tls

Generate private key (.key)

# Key considerations for algorithm "RSA" ≥ 2048-bit

openssl genrsa -out server.key 2048

# Key considerations for algorithm "ECDSA" ≥ secp384r1

# List ECDSA the supported curves (openssl ecparam -list_curves)

openssl ecparam -genkey -name secp384r1 -out server.key
  
Generation of self-signed(x509) public key (PEM-encodings .pem|.crt) based on the private (.key)

openssl req -new -x509 -sha256 -key server.key -out server.crt -days 3650


```bash
openssl s_client -connect 127.0.0.1:443

# add password
openssl rsa -in [foo.key] -aes256 -passout pass:xxxxxx -out out.key

#remove a private key password
openssl rsa -in [file1.key] -out [file2.key]
```

### 生成TLS证书

```bash服务器端的证书生成
生成服务器端的私钥
openssl genrsa -out certs/server.key 2048
生成服务器端证书
openssl req -new -x509 -key certs/server.key -out certs/server.pem -days 3650
openssl req -new -nodes -x509 -out certs/server.pem -keyout certs/server.key -days 3650 -subj "/C=CN/ST=LN/L=DL/O=pingd/OU=O0/CN=www.wiloon.com/emailAddress=wiloon.wy@gmail.com"

客户端的证书生成
生成客户端的私钥
openssl genrsa -out certs/client.key 2048
生成客户端的证书
openssl req -new -x509 -key client.key -out client.pem -days 3650
openssl req -new -nodes -x509 -out certs/client.pem -keyout certs/client.key -days 3650 -subj "/C=CN/ST=LN/L=DL/O=pingd/OU=O0/CN=www.wiloon.com/emailAddress=wiloon.wy@gmail.com"
```
