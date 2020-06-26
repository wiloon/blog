+++
author = "w1100n"
date = 2020-06-26T13:04:56Z
title = "nginx config, tls"

+++
server {
        #ssl参数
        listen              443 ssl;
        # 多域名配置
        server_name         foo.wiloon.com bar.wiloon.com;
        #证书文件
        ssl_certificate     example.com.crt;
        #私钥文件
        ssl_certificate_key example.com.key;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;
        #...
    }
    
 https://aotu.io/notes/2016/08/16/nginx-https/index.html
 