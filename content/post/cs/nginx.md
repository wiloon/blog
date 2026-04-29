---
title: nginx basic, command
author: "-"
date: 2026-04-29T13:08:52+08:00
url: nginx-basic
categories:
  - network
tags:
  - nginx
  - remix
  - AI-assisted
---
## vhost（虚拟主机）

nginx 中每个 `server {}` 块就是一个虚拟主机（vhost，Virtual Host），同一台服务器上可以配置多个 `server {}` 块，让 nginx 同时托管多个网站或服务。

nginx 收到请求后，依次匹配 `listen`（端口/IP）和 `server_name`（域名），找到对应的 `server {}` 块处理请求。如果没有匹配项，则使用第一个定义的 server 或标记了 `default_server` 的块。

### 基于域名（最常用）

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example;
}

server {
    listen 80;
    server_name another.com;
    root /var/www/another;
}
```

### 基于端口

```nginx
server {
    listen 8080;
    server_name localhost;
}

server {
    listen 9090;
    server_name localhost;
}
```

### 基于 IP

```nginx
server {
    listen 192.168.1.1:80;
}

server {
    listen 192.168.1.2:80;
}
```

## nginx basic, command

```bash
# Do not run, just test the configuration file.
sudo nginx -t

nginx -s signal

# stop — fast shutdown
# quit — graceful shutdown
# reload — reloading the configuration file
# reopen — reopening the log files
```

### almalinux install nginx

```Bash
sudo dnf update -y
sudo dnf install nginx -y
sudo systemctl enable --now  nginx
```

```bash
# install

# nerdctl
nerdctl run -d \
--name nginx \
--restart=always \
-p 80:80 \
-p 443:443 \
-v nginx-config:/etc/nginx \
-v nginx-www:/var/www \
-v /etc/letsencrypt:/etc/letsencrypt \
-v /etc/localtime:/etc/localtime:ro \
nginx:1.29.1

# docker
docker run -d \
--name nginx \
--restart=always \
-p 80:80 \
-p 443:443 \
-v nginx-config:/etc/nginx \
-v nginx-www:/var/www \
-v /etc/letsencrypt:/etc/letsencrypt \
-v /etc/localtime:/etc/localtime:ro \
nginx:1.27.2

docker run -d \
--name nginx \
--restart=always \
-p 80:80 \
-p 443:443 \
-v nginx-config:/etc/nginx \
-v nginx-www:/var/www \
-v /etc/localtime:/etc/localtime:ro \
nginx:1.27.2

# podman
podman run -d \
--name nginx \
-p 80:80 \
-p 443:443 \
-p 1022:1022 \
-v nginx-config:/etc/nginx \
-v nginx-www:/var/www \
-v nginx-cert:/etc/letsencrypt \
-v /etc/localtime:/etc/localtime:ro \
nginx:1.27.2

# nginx config text
docker run --name nginx-config-test --rm -t -a stdout -v nginx-conf:/etc/nginx:ro nginx nginx -c /etc/nginx/nginx.conf -t

# archlinux, mainline branch: new features, updates, bugfixes
sudo pacman -S nginx-mainline

# start
sudo systemctl enable --now nginx

# restart
kill -HUP pid

#stop
kill -s QUIT 1628
```

### 文件下载

```conf
server {
        listen 8088;
        location /download/images {
                alias /home/net-files/images; # 我在这个路径下放了一张图片: fei_ji.jpg
        }
}
```

#### 下载

```bash
curl "http://my_ip_address:8088/download/images/fei_ji.jpg" > test.jpg
```

————————————————
版权声明: 本文为CSDN博主「tomeasure」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: [https://blog.csdn.net/qq_29695701/article/details/86491331](https://blog.csdn.net/qq_29695701/article/details/86491331)
