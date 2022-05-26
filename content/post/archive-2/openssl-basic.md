---
title: openssl basic
author: "-"
date: 2017-10-30T09:16:49+00:00
url: openssl
categories:
  - Security
tags:
  - reprint
---
## openssl basic

## 查看私钥长度

```bash
    openssl rsa -in id_rsa.pem -text -noout

```

### get cert

```bash
    openssl s_client -connect  site.com:636 </dev/null 2>/dev/null  | openssl x509 -outform PEM > site.pem

```

### import cert into ca certs

```bash
    sudo keytool -importcert -noprompt -alias site-`date "+%Y%m%d%H%M%S"` -file ./site.pem -keystore /usr/java/latest/lib/security/cacerts -storepass changeit

```

### 查看证书信息 pem

```bash
openssl x509 -noout -text -in ca.crt
openssl x509 -noout -text -in foo.pem
```

### 查看 .der .crt 证书

```bash
    openssl x509 -inform der -text -noout -in foo.crt 
```

### pem格式转DER格式

```bash
openssl x509 -outform der -in charles.pem -out charles.crt

```

### 查看https证书

```bash
    openssl s_client -showcerts -connect www.baidu.com:443
    # 证书链是倒序的, 从上面数第一个是叶子节点, 跟浏览器里看到的证书顺序相反.
```

### 查看pem证书内容

```bash
    openssl x509 -in certificate.pem -text -noout

# openssl 解密
    openssl pkeyutl -inkey xxx-pri.pem -decrypt -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -in foo.bin -out result.dec

# 查看公钥内容
openssl rsa -inform PEM -in xxx-pub.pem -pubin -text

# generate private key
openssl genrsa -out pri2048.key 2048

# generate public key
openssl rsa -inform PEM -outform PEM -in pri2048.key -out pub2048.key -pubout

# 查看证书信息 pem
openssl x509 -noout -text -in ca.crt
openssl x509 -noout -text -in foo.pem

# 验证证书
openssl verify selfsign.crt
```

<https://github.com/denji/golang-tls>

Generate private key (.key)

Key considerations for algorithm "RSA" ≥ 2048-bit

openssl genrsa -out server.key 2048

Key considerations for algorithm "ECDSA" ≥ secp384r1

List ECDSA the supported curves (openssl ecparam -list_curves)

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

### rsa

生成2048位rsa私钥,保存为pem格式:

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -out unencrypted-private.pem

查看私钥内容:

openssl pkey -in unencrypted-private.pem -text -noout

生成对应的公钥:

openssl pkey -in unencrypted-private.pem -pubout -out pubkey.pem

查看对应的公钥:

openssl pkey -pubin -in pubkey.pem -text -noout

生成测试用文件:

echo some secret > tos.txt

用私钥给文件签名:

openssl pkeyutl -sign -in tos.txt -inkey unencrypted-private.pem -out tos.sig

用公钥验证签名:

openssl pkeyutl -verify -in tos.txt -sigfile tos.sig -pubin -inkey pubkey.pem

Signature Verified Successfully

用公钥恢复签名文件的内容:

openssl pkeyutl -verifyrecover -in tos.sig -pubin -inkey pubkey.pem

some secret

用公钥加密文件:

 openssl pkeyutl -encrypt -in tos.txt -pubin -inkey pubkey.pem -out tos.enc

用私钥解密文件:

openssl pkeyutl -decrypt -in tos.enc -inkey key.pem -out tos.dec

cat tos.dec

some secret

<https://my.oschina.net/u/1382972/blog/325442>

<https://www.openssl.org/>
