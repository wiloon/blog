---
title: Openssl 生成自签名证书, self-signed cert
author: "-"
date: 2019-03-24T03:49:46+00:00
url: self-signed-cert
categories:
  - CS
tags:
  - reprint
  - remix
---
## 自签名证书, self-signed cert

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


----

https://ayushsuman.medium.com/creating-elliptic-curve-based-certs-using-openssl-d4ebbb9d071f

```Bash
9621  mkdir certs private
9622  ll
9623  openssl ecparam -out private/ca-key.pem -name prime256v1 -genkey
9624  vim foo.cnf
9625  ll
9626  touch index.txt
9627  echo 01 > serial
9628  vim foo.cnf
9629  pwd
9630  vim foo.cnf
9631  openssl req -new -x509 -days 3650 -config foo.cnf -extensions v3_ca -key private/ca-key.pem -out certs/ca-cert.pem
9632  sudo cp certs/ca-cert.pem /usr/local/share/ca-certificates/ca-cert.pem
9633  ls -l certs
9634  sudo update-ca-certificates
9635  sudo cp certs/ca-cert.pem /usr/local/share/ca-certificates/ca-cert.crt
9636  cd /usr/local/share/ca-certificates/
9637  ll
9638  rm ca-cert.pem
9639  ll
9640  sudo rm ca-cert.pem
9641  rm rootCA.crt
9642  ll
9643  sudo rm rootCA.crt
9644  ll
9645  sudo update-ca-certificates
9649  cd tmp
9650  ll
9651  cd 111413
9652  ll
9653  vim foo.cnf
9654  rm certs/ca-cert.pem
9655  ll certs
9656  openssl req -new -x509 -days 3650 -config foo.cnf -extensions v3_ca -key private/ca-key.pem -out certs/ca-cert.pem
9657  sudo rm /usr/local/share/ca-certificates/ca-cert.crt
9658  sudo update-ca-certificates --refresh
9659  sudo update-ca-certificates --fresh
9660  sudo cp certs/ca-cert.pem /usr/local/share/ca-certificates/ca-cert.crt
9661  sudo update-ca-certificates
9662  openssl ecparam -out foo.key -name prime256v1 -genkey
9663  ll
9664  cat serial
9665  cat index.txt
9666  vim foo.cnf
9667  pwd
9668  vim foo.cnf
9669* cd
9671  ll
9672  openssl req -new -key foo.key -out foo.csr -sha256 -config foo.cnf -extensions v3_req
9673  ll
9674  openssl ca -keyfile private/ca-key.pem -cert certs/ca-cert.pem -in foo.csr -out foo.crt -config foo.cnf -extensions v3_req
9675  vim foo.cnf
9677  cat foo.cnf
9678  ll
9679  rm foo.csr
9680  openssl req -new -key foo.key -out foo.csr -sha256 -config foo.cnf -extensions v3_req
9681  ll
9682  openssl ca -keyfile private/ca-key.pem -cert certs/ca-cert.pem -in foo.csr -out foo.crt -config foo.cnf -extensions v3_req
9683  openssl req -new -key foo.key -out foo.csr -sha256 -config foo.cnf -extensions v3_req
9684  rm foo.csr
9685  openssl req -new -key foo.key -out foo.csr -sha256 -config foo.cnf -extensions v3_req
9686  openssl ca -keyfile private/ca-key.pem -cert certs/ca-cert.pem -in foo.csr -out foo.crt -config foo.cnf -extensions v3_req
9687  ll
9688  cat index.txt
9689  cat serial
9690  ll
9691  cat foo.crt
9692* cd
9693* ll
9694* cd
9696  cat foo.key
9697* cd
9698* curl -v https://hello.foo.com
9699  history
9700  history|grep mkdir
```

foo.cnf

```Bash
[ ca ]
default_ca = ca_default

[ ca_default ]
dir           = /home/foo/tmp/111413
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
0.organizationName              = wiloon
organizationalUnitName          = xpd
commonName                      = *.foo.com
emailAddress                    = foo@bar.com

[ v3_ca ]
subjectKeyIdentifier      = hash
authorityKeyIdentifier    = keyid:always,issuer
basicConstraints          = critical,CA:true
keyUsage                  = critical,digitalSignature,keyCertSign
nsComment                 = "OpenSSL Generated Certificate"

```

foo.cnf

```Bash
[ ca ]
default_ca = ca_default

[ ca_default ]
dir           = /home/foo/tmp/111413
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
commonName                      = *.foo.com
emailAddress                    = foo@bar.com

[ v3_req ]
basicConstraints     = critical,CA:false
keyUsage             = critical,digitalSignature
extendedKeyUsage     = serverAuth
subjectAltName       = @alternate_names
nsComment            = "OpenSSL Generated Certificate"

[ alternate_names ]
DNS.1       = foo.com
DNS.2       = hello.foo.com
DNS.3       = registry.foo.com
DNS.5       = localhost
DNS.6       = localhost.localdomain
IP.1        = 127.0.0.1
IP.2        = 10.124.44.91


```


### 客户端安装自签名证书

```Bash
# ubuntu
sudo rm /usr/local/share/ca-certificates/foo_cert.crt
sudo update-ca-certificates --fresh
# 将证书拷贝到目录“/usr/local/share/ca-certificates”
sudo cp foo_cert.crt /usr/local/share/ca-certificates
# 更新CA存储
sudo update-ca-certificates
```
