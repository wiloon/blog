---
title: Openssl 生成自签名证书, self-signed cert
author: "-"
date: 2019-03-24T03:49:46+00:00
url: self-signed-cert
categories:
  - CS
tags:
  - reprint
  - reprint
---
## Openssl 生成自签名证书, self-signed cert

## ecc crt

https://ayushsuman.medium.com/creating-elliptic-curve-based-certs-using-openssl-d4ebbb9d071f

```Bash
# Create two directories for all certs and root private key that you will generate
mkdir certs private
# Generate the elliptic curve private key
openssl ecparam -out private/ca-key.pem -name prime256v1 -genkey
```

foo.cnf

修改 dir

```Bash
[ ca ]
default_ca = ca_default

[ ca_default ]
dir           = /home/user_0/path/to/tls
database      = $dir/index.txt
serial        = $dir/serial
new_certs_dir = $dir/certs


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
0.organizationName              = org_0
organizationalUnitName          = unit_0
commonName                      = *.wiloon.com
emailAddress                    = wiloon@email.com

[ v3_ca ]
subjectKeyIdentifier      = hash
authorityKeyIdentifier    = keyid:always,issuer
basicConstraints          = critical,CA:true
keyUsage                  = critical,digitalSignature,keyCertSign
nsComment                 = "OpenSSL Generated Certificate"
```

```Bash
touch index.txt
echo 01 > serial

# Generate the CA certificate using the command below —
# Generate the root certificate from the private key and the configs
openssl req -new -x509 -days 3650 -config foo.cnf -extensions v3_ca -key private/ca-key.pem -out certs/ca-cert.pem

# Add this cert to your trust store (for Ubuntu 22.04)
sudo cp certs/ca-cert.pem /usr/local/share/ca-certificates/ca-cert.crt
sudo update-ca-certificates

# remove from Ubuntu
sudo rm /usr/local/share/ca-certificates/ca-cert.crt
sudo update-ca-certificates --fresh

# add the CA certificate to your browser’s trust store.

# Generate the private key for one domain
openssl ecparam -out wiloon.key -name prime256v1 -genkey
```

wiloon.cnf

```Bash
[ ca ]
default_ca = ca_default

[ ca_default ]
dir           = /home/wiloon/path/to/tls
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
0.organizationName              = org_0
organizationalUnitName          = unit_0
commonName                      = *.wiloon.com
emailAddress                    = wiloon@email.com

[ v3_req ]
basicConstraints     = critical,CA:false
keyUsage             = critical,digitalSignature
extendedKeyUsage     = serverAuth
subjectAltName       = @alternate_names
nsComment            = "OpenSSL Generated Certificate"

[ alternate_names ]
DNS.1       = wiloon.com
DNS.2       = www.wiloon.com
DNS.3       = mail.wiloon.com
DNS.4       = ftp.wiloon.com
DNS.5       = localhost
DNS.6       = localhost.localdomain
IP.1        = 127.0.0.1
IP.2        = 10.0.2.2 # localhost IP from Android emulators. Only for Android Developers.
```


```Bash
# Create Certificate Signing Request
openssl req -new -key wiloon.key -out wiloon.csr -sha256 -config wiloon.cnf -extensions v3_req

# Generate Signed Certificate using the private key, configs and the CSR. 
# You also need to specify the root private key and root certifcate for signing.
openssl ca -keyfile private/ca-key.pem -cert certs/ca-cert.pem -in wiloon.csr -out wiloon.crt -config wiloon.cnf -extensions v3_req

```
 
https://msol.io/blog/tech/create-a-self-signed-ecc-certificate/

```Bash
# ist all available curves
openssl ecparam -list_curves

# read ec key
openssl ec -in key.pem -text -noout
# generates a Certificate Signing Request 
# with subj: openssl req -new -sha256 -key key.pem -subj "/CN=devops/C=BM/ST=Bermudian/L=Bermudian/O=Org/OU=IT" -out csr.csr

# read csr
openssl req -in csr.csr -text -noout 

openssl req -in csr.csr -text -noout | grep -i "Signature.*SHA256" && echo "All is well" || echo "This certificate will stop working in 2017! You must update OpenSSL to generate a widely-compatible certificate"
openssl x509 -noout -text -in certificate.pem

# check crt of web site
openssl s_client -connect site.domain:443
```



https://dgu2000.medium.com/working-with-self-signed-certificates-in-chrome-walkthrough-edition-a238486e6858

```Bash
# To check just created root certificate:
openssl x509 -in rootCA.pem -text -noout
```

```Bash

# To verify that the certificate is built correctly:
openssl verify -CAfile rootCA.pem -verify_hostname console.kyma.local tls.crt
```
---


https://www.ssldragon.com/zh/how-to/openssl/create-self-signed-certificate-openssl/

https://docs.openssl.org/3.4/man1/openssl-genpkey/#examples

```Bash

```

---

```bash

# 查看证书请求文件的内容
openssl req -text -noout -in server.csr
```

[https://ningyu1.github.io/site/post/51-ssl-cert/](https://ningyu1.github.io/site/post/51-ssl-cert/)
  
[http://liaoph.com/openssl-san/](http://liaoph.com/openssl-san/)
  
[https://codeday.me/bug/20170831/60851.html](https://codeday.me/bug/20170831/60851.html)

```Bash
# 查看默认的 OpenSSL 配置目录
openssl version -d
```
