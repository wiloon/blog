---
title: openssl command
author: wiloon
type: post
date: 2018-12-04T05:48:38+00:00
url: /?p=12962
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">openssl s_client -connect 127.0.0.1:443

# add password
openssl rsa -in [foo.key] -aes256 -passout pass:xxxxxx -out out.key

#remove a private key password
openssl rsa -in [file1.key] -out [file2.key]
</code></pre>

### 生成TLS证书

<pre><code class="language-bash line-numbers">服务器端的证书生成
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
</code></pre>