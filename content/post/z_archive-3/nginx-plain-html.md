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

```r
server{
    listen 80;
    server_name localhost;
    root /var/www;
    index hello.html;
}
```

```r
server{
    listen 80;
    server_name localhost;
    root /var/www;
    index index.htm;
}
```