---
title: openssl
author: wiloon
type: post
date: 2017-10-30T09:16:49+00:00
url: /?p=11332
categories:
  - Uncategorized

---
```bash
  
\# openssl 解密
  
openssl pkeyutl -inkey xxx-pri.pem -decrypt -pkeyopt rsa\_padding\_mode:oaep -pkeyopt rsa\_oaep\_md:sha256 -in foo.bin -out result.dec

\# 查看公钥内容
  
openssl rsa -inform PEM -in xxx-pub.pem -pubin -text

\# generate private key
  
openssl genrsa -out pri2048.key 2048

\# generate public key
  
openssl rsa -inform PEM -outform PEM -in pri2048.key -out pub2048.key -pubout
  
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