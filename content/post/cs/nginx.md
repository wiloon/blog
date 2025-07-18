---
title: nginx basic, command
author: "-"
date: 2017-10-26T06:17:15+00:00
url: nginx/basic
categories:
  - nginx
tags:
  - reprint
---
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
nginx:1.27.2

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
