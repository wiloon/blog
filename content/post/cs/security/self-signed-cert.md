---
title: Openssl 生成自签名证书, self-signed cert
author: "-"
date: 2025-06-24 08:12:25
url: self-signed-cert
categories:
  - Security
tags:
  - reprint
  - remix
---
## 自签名证书, self-signed cert

```bash
sudo pacman -S openssl

# 查看默认的 OpenSSL 配置目录
openssl version -d

# Create two directories for all certs and root private key that you will generate
su - wiloon
mkdir -p /home/wiloon/apps/self-signed-cert
mkdir certs private

# list all available curves
openssl ecparam -list_curves

# 生成 ECDSA（椭圆曲线数字签名算法）密钥对, CA 密钥, root private key
# 参数: -noout - 抑制输出椭圆曲线参数, 如果不加这个参数，命令会同时输出曲线参数和私钥,加上后只输出私钥部分
# -genkey：生成密钥对
# prime256v1 secp256r1 / NIST P-256 256 默认、安全性好、广泛兼容（TLS 默认）
openssl ecparam -name prime256v1 -genkey -out private/ca-key.pem

# read ca key
openssl ec -in private/ca-key.pem -text -noout
```

准备一个生成 CA 证书的 配置文件 ca-cert.cnf, the value in the basicConstrains is CA:true

注意要修改 dir 的值

```bash
[ ca ]
default_ca = ca_default

[ ca_default ]
dir           = /home/wiloon/apps/self-signed-cert
database      = $dir/index.txt
serial        = $dir/serial
new_certs_dir = $dir/certs

certificate   = $dir/certs/ca-cert.pem
private_key   = $dir/private/ca-key.pem

default_days  = 365
default_md    = sha256
policy        = policy

# Policy dictates what these values in any certificate signed by your root certificate should be.
[ policy ]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

############################################################################################

[ req ]
prompt              = no
distinguished_name  = req_distinguished_name
x509_extensions     = v3_ca
string_mask         = utf8only

[ req_distinguished_name ]
countryName                     = CN
stateOrProvinceName             = Liaoning
localityName                    = Dalian
0.organizationName              = wiloon
organizationalUnitName          = xpd
commonName                      = *.wiloon.com
emailAddress                    = wangyue@wiloon.com

[ v3_ca ]
subjectKeyIdentifier      = hash
authorityKeyIdentifier    = keyid:always,issuer
basicConstraints          = critical,CA:true
keyUsage                  = critical,digitalSignature,keyCertSign
nsComment                 = "OpenSSL Generated Certificate"
```

index.txt 文件, 每次生成新证书, 这两个文件会被自动更新, 比如后面生成 wiloon.crt 的时候

```bash
touch index.txt
echo 01 > serial
```

```bash
# Generate the root certificate from the private key and the configs
openssl req -new -x509 -days 3650 -config ca-cert.cnf -extensions v3_ca -key private/ca-key.pem -out certs/ca-cert.pem

# read ca pem, root pem
openssl x509 -in certs/ca-cert.pem -text -noout
```

### 客户端安装 root certificate, ca-cert.pem

把刚才生成的 ca 根证书安装到客户端主机上, 让浏览器等信任这个 CA

```Bash
# ubuntu
sudo update-ca-certificates --fresh
# 将证书拷贝到目录“/usr/local/share/ca-certificates”
sudo cp foo_cert.crt /usr/local/share/ca-certificates
# 更新CA存储
sudo update-ca-certificates

# remove from Ubuntu
sudo rm /usr/local/share/ca-certificates/ca-cert.crt
sudo update-ca-certificates --fresh
```

```bash
# Generate the private key for one domain (某一个域名的私钥)
openssl ecparam -name prime256v1 -genkey -out wiloon.key
```

wiloon.cnf

- the value in the basicConstrains is CA:false instead, 这个证书不是 CA 证书, 只是普通的某一个域名的证书
- 申请证书的域名要写在 alternate_names 里

```Bash
[ ca ]
default_ca = ca_default

[ ca_default ]
dir           = /home/wiloon/apps/self-signed-cert
certs         = $dir/certs
database      = $dir/index.txt
new_certs_dir = $dir/certs
serial        = $dir/serial

default_days  = 365
default_md    = sha256
policy        = ca_policy

[ ca_policy ]
countryName            = supplied
stateOrProvinceName    = optional
organizationName       = supplied
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

############################################################################################

[ req ]
prompt              = no
distinguished_name  = req_distinguished_name
req_extensions      = v3_req
string_mask         = utf8only

[ req_distinguished_name ]
countryName                     = CN
stateOrProvinceName             = Liaoning
localityName                    = Dalian
0.organizationName              = wiloon
organizationalUnitName          = xpd
commonName                      = *.wiloon.com
emailAddress                    = wangyue@wiloon.com

[ v3_req ]
basicConstraints     = critical,CA:false
keyUsage             = critical,digitalSignature
extendedKeyUsage     = serverAuth
subjectAltName       = @alternate_names
nsComment            = "OpenSSL Generated Certificate"

[ alternate_names ]
DNS.1       = wiloon.com
DNS.2       = www.wiloon.com
DNS.3       = enx-dev.wiloon.com
DNS.4       = localhost
DNS.5       = localhost.localdomain
DNS.6       = kong.wiloon.com
DNS.7       = hello.wiloon.com
IP.1        = 127.0.0.1
IP.2        = 192.168.50.123 # localhost IP from Android emulators. Only for Android Developers.
```

```bash
# Create Certificate Signing Request (CSR)
# -key wiloon.key 指定私钥文件（用于签名 CSR）
# -config wiloon.cnf 使用自定义的 OpenSSL 配置文件
# wiloon.csr 是包含公钥信息和签名(私钥对 CSR 内容进行数字签名) 的请求文件，可以发送给 CA 来生成 .crt 证书。
openssl req -new -key wiloon.key -out wiloon.csr -sha256 -config wiloon.cnf -extensions v3_req

# read csr
openssl req -in wiloon.csr -text -noout
# 显示 CSR 里嵌的公钥
# 同时自动验证签名（如果签名无效，会报错）

# Generate Signed Certificate using the private key, configs and the CSR. 
# You also need to specify the root private key and root certifcate for signing.
# CA 会使用 CSR 里包含的公钥，来验证这个 CSR 的签名。
openssl ca -keyfile private/ca-key.pem -cert certs/ca-cert.pem -in wiloon.csr -out wiloon.crt -config wiloon.cnf -extensions v3_req

# read crt
openssl x509 -noout -text -in wiloon.crt

# To verify that the certificate is built correctly
openssl verify -CAfile certs/ca-cert.pem -verify_hostname hello.wiloon.com wiloon.crt

# check crt of web site
openssl s_client -connect site.domain:443


# R 代表已经撤销的证书
cat index.txt

# deploy to nginx
scp wiloon.crt root@192.168.50.130:/var/lib/containers/storage/volumes/certbot-conf/_data/fullchain.pem
scp wiloon.key root@192.168.50.130:/var/lib/containers/storage/volumes/certbot-conf/_data/privkey.pem
podman restart nginx
```

### 增加一个域名之后重新生成证书

```bash
#撤消旧证书, 
# 查看 index.txt, 找到最新的版本号
cat /home/wiloon/workspace/apps/self-signed-cert/index.txt

# 更新 csr 信息之后, 重新签发证书
# 撤销旧证书
# 注意 01.pem 是要撤消的证书
openssl ca -config ca-cert.cnf -revoke certs/05.pem

# 修改 wiloon.cnf, 加入新域名
vim wiloon.cnf

# 重新生成  csr
openssl req -new -key wiloon.key -out wiloon.csr -sha256 -config wiloon.cnf -extensions v3_req

# 重新签发证书, 跟前面的命令是一样的
openssl ca -keyfile private/ca-key.pem -cert certs/ca-cert.pem -in wiloon.csr -out wiloon.crt -config wiloon.cnf -extensions v3_req
```

```bash
# kong upload crt
curl -i -X POST http://192.168.50.64:8001/certificates \
  -F "cert=@wiloon.crt;type=text/plain" \
  -F "key=@wiloon.key;type=text/plain" \
  -F "snis=kong.wiloon.com"
```

https://ayushsuman.medium.com/creating-elliptic-curve-based-certs-using-openssl-d4ebbb9d071f

https://docs.openssl.org/master/man5/x509v3_config/

https://msol.io/blog/tech/create-a-self-signed-ecc-certificate/

https://dgu2000.medium.com/working-with-self-signed-certificates-in-chrome-walkthrough-edition-a238486e6858

https://www.ssldragon.com/zh/how-to/openssl/create-self-signed-certificate-openssl/

https://docs.openssl.org/3.4/man1/openssl-genpkey/#examples

https://ningyu1.github.io/site/post/51-ssl-cert/

http://liaoph.com/openssl-san/

https://codeday.me/bug/20170831/60851.html
