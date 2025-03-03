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

ssl_certificate: 服务器的 SSL 证书文件的路径。该证书用于证明服务器的身份，并与客户端建立安全连接。通常，这个文件包含服务器的公钥信息。
ssl_certificate_key: 服务器证书匹配的私钥文件路径。私钥用于解密客户端传来的信息，因此必须保密并妥善保护。
ssl_trusted_certificate: 一个或多个被信任的证书颁发机构（CA）的证书文件路径。它用于验证客户端证书的真实性，尤其在启用客户端证书验证时。在大多数情况下，使用 Let's Encrypt 证书时不需要单独指定这个文件，因为 fullchain.pem 已经包含了必要的中间证书链，通常足以满足大多数应用的验证需求。

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

## nginx tcp proxy with tls

```bash
#check tls version
openssl s_client -connect 127.0.0.1:443
```

set yum repo, /etc/yum.repos.d/nginx.repo

```bash
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1
```

[https://www.nginx.com/resources/admin-guide/tcp-load-balancing/](https://www.nginx.com/resources/admin-guide/tcp-load-balancing/)

```bash
stream {
    server {
        listen 9000 ssl;
        proxy_pass stream_backend;

        ssl_certificate        /path/to/server.crt;
        ssl_certificate_key    /path/to/server.key;
        ssl_protocols  TLSv1.2;
        ssl_ciphers    HIGH:!aNULL:!MD5;
    }

    upstream stream_backend {
        server localhost:7001;
        server localhost:7002;
    }
}

```

[https://aotu.io/notes/2016/08/16/nginx-https/index.html](https://aotu.io/notes/2016/08/16/nginx-https/index.html)

[http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html](http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html)

[http://seanlook.com/2015/05/28/nginx-ssl/](http://seanlook.com/2015/05/28/nginx-ssl/)

[https://imququ.com/post/enable-tls-1-3.html](https://imququ.com/post/enable-tls-1-3.html)

