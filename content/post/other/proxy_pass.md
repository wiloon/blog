---
title: nginx proxy_pass
author: "-"
date: 2014-12-18T05:06:13+00:00
url: /?p=7119
categories:
  - Inbox
tags:
  - English

---
## nginx proxy_pass

 功能
Nginx 的ngx_stream_proxy_module和ngx_http_proxy_module两个模块中，都有 proxy_pass 指令。其主要功能是为后端做代理，协议转发，请求转发等。

二、 用法和区别
1. 官网介绍
ngx_stream_proxy_module 的 proxy_pass

语法：proxy_pass address;
默认值：—
场景：server 段
说明：设置代理服务器的地址。代理地址可以是域名或者IP加端口，也可以是一个UNIX的socket路径
ngx_http_proxy_module 的 proxy_pass

语法：proxy_pass URL;
默认值：—
场景：location 段，location中的if段，limit_except段
说明：设置后端代理服务器的地址和协议，还可以附加可选的URI映射。协议可以是 http 或者 https。地址可以是域名或者IP，可以附加指定端口，也可以是UNIX的socket路径，路径要放在unix: 和 : 之间
2. 区别
从上面的各自说明可以看出两个 proxy_pass 指令都是做后端的代理配置。

除了应用场景的段不同之外，ngx_stream_proxy_module 的 proxy_pass 只能转发域名或IP加端口的请求，即端口转发。

ngx_http_proxy_module 的 proxy_pass 除了包含前者的功能外，还可以实现协议转发，如 http 和 https 与 UNIX socket 三者的相互转发，另外还有很实用的URI转发

3. 用法示例
3.1 ngx_stream_proxy_module 的 proxy_pass
server {
    listen 8000;
    proxy_pass 127.0.0.1:8080; # IP+端口转发
}

server {
    listen 8000;
    proxy_pass test.com:8080; # 域名+端口转发
}

server {
    listen [::1]:8000;
    proxy_pass unix:/tmp/stream.socket; # UNIX socket转发
}
3.2 ngx_http_proxy_module 的 proxy_pass
server {
    listen      80;
    server_name www.test.com;

    # 正常代理，不修改后端url的
    location /some/path/ {
        proxy_pass http://127.0.0.1;
    }

    # 修改后端url地址的代理（本例后端地址中，最后带了一个斜线)
    location /testb {
        proxy_pass http://www.other.com:8801/;
    }

    # 使用 if in location
    location /google {
        if ( $geoip_country_code ~ (RU|CN) ) {
            proxy_pass http://www.google.hk;
        }
    }

    location /limit/ {
        # 没有匹配 limit_except 的，代理到 unix:/tmp/backend.socket:/uri/
        proxy_pass http://unix:/tmp/backend.socket:/uri/;;

        # 匹配到请求方法为: PUT or DELETE, 代理到9080
        limit_except PUT DELETE {
            proxy_pass http://127.0.0.1:9080;
        }
    }

}
4. ngx_http_proxy_module.proxy_pass 的 URI 转发映射分析1
准备文件 /data/www/test/test.php 如下：

<?php
echo '$_SERVER[REQUEST_URI]:' . $_SERVER['REQUEST_URI'];
通过查看 $_SERVER['REQUEST_URI'] 的值，可以看到每次请求的后端的 request_uri 的值，进行验证。

Nginx 配置文件如下：

server {
    listen      80;
    server_name www.test.com;

    # 情形A
    # 访问 http://www.test.com/testa/aaaa
    # 后端的request_uri为: /testa/aaaa
    location ^~ /testa/ {
        proxy_pass http://127.0.0.1:8801;
    }
    
    # 情形B
    # 访问 http://www.test.com/testb/bbbb
    # 后端的request_uri为: /bbbb
    location ^~ /testb/ {
        proxy_pass http://127.0.0.1:8801/;
    }

    # 情形C
    # 下面这段location是正确的
    location ~ /testc {
        proxy_pass http://127.0.0.1:8801;
    }

    # 情形D
    # 下面这段location是错误的
    #
    # nginx -t 时，会报如下错误: 
    #
    # nginx: [emerg] "proxy_pass" cannot have URI part in location given by regular 
    # expression, or inside named location, or inside "if" statement, or inside 
    # "limit_except" block in /opt/app/nginx/conf/vhost/test.conf:17
    # 
    # 当location为正则表达式时，proxy_pass 不能包含URI部分。本例中包含了"/"
    location ~ /testd {
        proxy_pass http://127.0.0.1:8801/;   # 记住，location为正则表达式时，不能这样写！！！
    }

    # 情形E
    # 访问 http://www.test.com/ccc/bbbb
    # 后端的request_uri为: /aaa/ccc/bbbb
    location /ccc/ {
        proxy_pass http://127.0.0.1:8801/aaa$request_uri;
    }

    # 情形F
    # 访问 http://www.test.com/namea/ddd
    # 后端的request_uri为: /test?namea=ddd
    location /namea/ {
        rewrite    /namea/([^/]+) /test?namea=$1 break;
        proxy_pass http://127.0.0.1:8801;
    }

    # 情形G
    # 访问 http://www.test.com/nameb/eee
    # 后端的request_uri为: /test?nameb=eee
    location /nameb/ {
        rewrite    /nameb/([^/]+) /test?nameb=$1 break;
        proxy_pass http://127.0.0.1:8801/;
    }

    access_log /data/logs/www/www.test.com.log;
}

server {
    listen      8801;
    server_name www.test.com;
    
    root        /data/www/test;
    index       index.php index.html;

    rewrite ^(.*)$ /test.php?u=$1 last;

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass unix:/tmp/php-cgi.sock;
        fastcgi_index index.php;
        include fastcgi.conf;
    }

    access_log /data/logs/www/www.test.com.8801.log;
}
总结

情况A和情况B对比，可以看出URI最后的 / 对 URI 映射的影响
情况D说明，location 为正则表达式时，proxy_pass 不能包含 URI
情况E，可以通过 $request_uri 添加或改变请求的 URI
情况F和G通过 rewrite 配合 break 对 URL 和 URI 进行改写
https://my.oschina.net/foreverich/blog/1512304 ↩

文章标题:Nginx proxy_pass详解

文章字数:11978

发布时间:2018年12月21日

原始链接: https://lanffy.github.io/2018/12/21/Nginx-proxy_pass

版权声明: "署名-非商用-相同方式共享 4.0" 转载请保留原文链接及作者。