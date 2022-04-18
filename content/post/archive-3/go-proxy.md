---
title: go module proxy, goproxy, goproxy.io, goproxy.cn, athens
author: "-"
date: 2019-06-20T06:16:22+00:00
url: go/proxy
categories:
  - Go
tags:
  - reprint
---
## go module proxy, goproxy, goproxy.io, goproxy.cn, athens

```bash
# goproxy.io 有遇到过connection reset by peer, 换goproxy.cn
export GOPROXY=https://goproxy.io,direct

export GOPROXY=https://goproxy.cn
```

### athens

```bash
docker run -p '3000:3000' gomods/athens:latest
```

---

<https://goproxy.io/zh/>

<https://blog.wiloon.com/?p=15941>

<https://shockerli.net/post/go-get-golang-org-x-solution/>
  
<https://github.com/goproxy/goproxy.cn>
