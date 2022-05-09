---
title: netty tcp tls
author: "-"
date: 2018-02-22T09:35:01+00:00
url: /?p=11907
categories:
  - Inbox
tags:
  - reprint
---
## netty tcp tls

输出tls握手日志
  
-Djavax.net.debug=SSL

```bash
#生成服务端密钥对和证书仓库
keytool -genkey -alias tlsServer -keysize 2048 -validity 365 -keyalg RSA \
-dname "CN=wiloon" -keypass password0 -storepass password0 -keystore server.jks

#生成客户端的密钥对和证书仓库, 用于将服务端的证书保存到客户端的授信证书仓库中,命令如下: 
keytool -genkey -alias tlsClient -keysize 2048 -validity 365 -keyalg RSA \
-dname "CN=localhost" -keypass password0 -storepass password0 -keystore client.jks

#导出服务端自签名证书
keytool -export -alias tlsServer -keystore server.jks -storepass password0 -file server.cer

# 导出客户端自签名证书
keytool -export -alias tlsClient -keystore client.jks -storepass password0 -file client.cer

#将服务端的证书导入到客户端的证书仓库中: 
keytool -import -trustcacerts -alias tlsServer -file server.cer -storepass password0 -keystore serverTrust.jks
keytool -import -trustcacerts -alias tlsClient -file client.cer -storepass password0 -keystore clientTrust.jks
```

<http://www.infoq.com/cn/articles/netty-security>
  
<https://segmentfault.com/a/1190000010054860>
