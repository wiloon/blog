---
title: nginx tcp proxy with tls
author: "-"
date: 2017-11-10T05:48:19+00:00
url: nginx/steam
categories:
  - network
tags:
  - reprint
  - nginx
  - proxy

---
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

<https://www.nginx.com/resources/admin-guide/tcp-load-balancing/>

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

<https://aotu.io/notes/2016/08/16/nginx-https/index.html>
  
<http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html>
  
<http://seanlook.com/2015/05/28/nginx-ssl/>
  
<https://imququ.com/post/enable-tls-1-3.html>
