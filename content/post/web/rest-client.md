---
author: "-"
date: "2020-12-24 18:13:51" 
title: "rest client"
categories:
  - inbox
tags:
  - reprint
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

### http 请求

```http
### get
https://foo.com/bar/?foo=bar&bar=foo
```

<https://github.com/Huachao/vscode-restclient>
