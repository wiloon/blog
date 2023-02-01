---
title: angular deploy to nginx
author: "-"
date: 2019-06-02T14:51:28+00:00
url: /?p=14436
categories:
  - Inbox
tags:
  - reprint
---
## angular deploy to nginx

```bash
ng build --aot
```

"\`
  
server {

listen 8081;

server_name localhost;

location / {

root C:/website/angular/ng-prime/dist; // 这是angular生成的dist文件夹存放的位置

index index.html;

try_files $uri $uri/ /index.html; // 注意此句，一定要加上。否则配置的子路由等无法使用

}

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

"

<https://www.cnblogs.com/kingkangstudy/p/8085642.html>
