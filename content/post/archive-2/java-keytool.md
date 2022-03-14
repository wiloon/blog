---
title: java Keytool
author: "-"
date: 2019-01-06T10:56:09+00:00
url: /?p=13338

categories:
  - inbox
tags:
  - reprint
---
## java Keytool
```bash
keytool -list -v -keystore  /usr/java/default/jre/lib/security/cacerts

sudo /usr/lib/jvm/java-8-openjdk/bin/keytool -importcert -keystore /usr/lib/jvm/java-8-openjdk/jre/lib/security/cacerts -storepass changeit -noprompt  -file xxx.crt -alias "xxx.crt"

# jdk 导入 证书
keytool.exe -importcert -keystore "C:\Program Files\Java\jdk1.8.0_201\jre\lib\security\cacerts" -storepass changeit -noprompt  -file E:\xxx.cer -alias "xxx"
```

Keytool 是一个Java 数据证书的管理工具 ,Keytool 将密钥 (key) 和证书 (certificates) 存在一个称为keystore的文件中 在keystore里,包含两种数据: 
  
密钥实体 (Key entity) ——密钥 (secret key) 又或者是私钥和配对公钥 (采用非对称加密) 
  
可信任的证书实体 (trusted certificate entries) ——只包含公钥

ailas(别名)每个keystore都关联这一个独一无二的alias,这个alias通常不区分大小写
  
JDK中keytool 常用命令:

| param      | comments                                                                               |
| ---------- | -------------------------------------------------------------------------------------- |
| -genkey    | 在用户主目录中创建一个默认文件".keystore",还会产生一个mykey的别名,mykey中包含用户的公钥、私钥和证书              |
| -alias     | 产生别名                                                                                   |
| -keystore  | 指定密钥库的名称(产生的各类信息将不在.keystore文件中)                                                       |
| -keysize   | 指定密钥长度                                                                                 |
| -validity  | 指定创建的证书有效期多少天                                                                          |
| -keyalg    | 指定密钥的算法 (如 RSA DSA (如果不指定默认采用DSA) )                                                      |
| -dname     | 指定证书拥有者信息 例如:  "CN=名字与姓氏,OU=组织单位名称,O=组织名称,L=城市或区域名称,ST=州或省份名称,C=单位的两字母国家代码" |
| -keypass   | 指定别名条目的密码(私钥的密码)                                                                       |
| -storepass | 指定密钥库的密码(获取keystore信息所需的密码)                                                            |
| -list      | 显示密钥库中的证书信息                                                                            |
| -v         | 显示密钥库中的证书详细信息                                                                          |
| -export    | 将别名指定的证书导出到文件                                                                          |
| -printcert | 查看导出的证书信息                                                                              |
| -file      | 参数指定导出到文件的文件名                                                                          |
| -import    | 将已签名数字证书导入密钥库, keytool -import -alias 指定导入条目的别名 -keystore 指定keystore -file 需导入的证书      |