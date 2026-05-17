---
title: nginx 部署静态页面
author: "-"
date: 2019-06-08T03:18:00+00:00
url: nginx-plain-html
categories:
  - Inbox
tags:
  - reprint
aliases:
  - /p11389/
  - /p14473/
---
## nginx plain html 部署静态页面

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
hello
</body>
</html>
```

```
server{
    listen 80;
    server_name hello.wiloon.dev;
    root /var/www;
    index hello.html;
}
```
