---
author: "-"
date: "2020-12-24 18:13:51" 
title: "rest client"
categories:
  - HTTP
tags:
  - reprint
  - remix
---
## "rest client"

使用变量
变量的好处，在开发过程中我们都知道，在 HTTP 语言中同样可以使用变量来帮助我们组织请求代码

自定义变量
我们可以在 http 文件中直接定义变量，使用 @ 符号开头，以 {{variable name}} 的格式来使用

### foo.http

```http
@foo

GET http://localhost:8000/api/v1/public/echo?msg=1345asdf HTTP/1.1

GET http://localhost:8000/api/v1/public/echo?msg={{foo}} HTTP/1.1
// comments
```

### http 请求 with header

```http
### get
https://foo.com/bar/?foo=bar&bar=foo
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6
Connection: keep-alive
Host: wiloon.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36
```

[https://github.com/Huachao/vscode-restclient](https://github.com/Huachao/vscode-restclient)
