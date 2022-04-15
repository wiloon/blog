---
title: "joplin"
author: "-"
date: "2021-03-06 14:53:35"
url: ""
categories:
  - Editor
tags:
  - inbox
---
## "joplin"

### archlinux

    yay -S joplin-desktop
#### direct install
    wget -O - https://raw.githubusercontent.com/laurent22/joplin/dev/Joplin_install_and_update.sh | bash
### vscode install joplin plugin
    安装 chrome 扩展: Joplin Web Clipper

### enable web clipper service
    joplin desktop > setting>web clipper > enable web clipper service

### vscode
打开vscode setting 搜索joplin, 填写 
#### joplin: Port
web clipper 端口， 
#### jplin路径 ，
 token，
  重启vscode 

## typora
打开Joplin，然后点击菜单栏的工具，在弹出的菜单中选择选项

Tools>Options>General>Text editor command>Path
填写typora 可执行文件的位置。

### joplin server
>https://hub.docker.com/r/joplin/server
```bash
podman run -d --name joplin --env-file /data/joplin/joplin.env -v joplin-data:/home/joplin -p 22300:22300 joplin/server:2.7.4-beta
```
### joplin.env
```
APP_BASE_URL=https://joplin.wiloon.com
APP_PORT=22300
```

### nginx config
```bash
server {
    listen              443 ssl;
    server_name         joplin.wiloon.com;
    client_max_body_size 100m;
    ssl_certificate     /etc/letsencrypt/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/privkey.pem;
    ssl_protocols       TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    
    location / { try_files $uri $uri/ @joplin; }
 
    location @joplin {
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_pass http://192.168.50.90:22300;
    }
}

```
### 默认用户名/密码

    admin@localhost/admin

>https://github.com/laurent22/joplin
