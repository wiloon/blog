---
title: nginx 部署静态页面
author: "-"
date: 2019-06-08T03:18:00+00:00
url: /?p=14473
categories:
  - Inbox
tags:
  - reprint
---
## nginx 部署静态页面

```r
server{
    listen 80;
    server_name localhost;
    root /var/www;
    index index.htm;
}

```
