---
author: "-"
date: "2020-06-26T13:04:56Z"
title: "nginx config, tls"
categories:
  - Nginx
tags:
  - reprint
---
## "nginx config, tls"

## TLS, nginx config include

```bash
cat > /etc/nginx/tls.conf << EOF
ssl_certificate     /etc/letsencrypt/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/privkey.pem;
ssl_protocols       TLSv1.2;
ssl_ciphers         HIGH:!aNULL:!MD5;
EOF

vim /etc/nginx/conf.d/default.conf

# server config
server {
        listen 443 ssl;
        server_name foo.wiloon.com;
        include    /etc/nginx/tls.conf;

        location / {
          # ...
        }
}
```

### stream

代理远程桌面 3389 的 tcp 连接

    stream {
        upstream mstsc {
            server 1.2.3.4:3389;
        }

        server {
            listen 1082;
            proxy_pass mstsc;
        }
    }

### tls

```
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
```

### 静态网站

    server {
        listen       80;
        server_name  localhost;
    
        #charset koi8-r;
        access_log  /var/log/nginx/host.access.log  main;
        error_log  /var/log/nginx/error.log  error;
    
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    
        #error_page  404              /404.html;
    
        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }

[https://aotu.io/notes/2016/08/16/nginx-https/index.html](https://aotu.io/notes/2016/08/16/nginx-https/index.html)
