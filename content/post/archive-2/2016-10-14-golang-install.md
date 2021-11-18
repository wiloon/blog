---
title: golang install
author: "-"
date: 2016-10-14T00:15:50+00:00
url: /?p=9295
categories:
  - Uncategorized

---
## golang install
china mainland download
  
https://golang.google.cn/

```bash
curl -O https://dl.google.com/go/go1.12.6.linux-amd64.tar.gz
```

```bash
export GOROOT=/root/go
export GOPATH=/root/gopath
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
export GOBIN=/path/to/go/bin

```

GOPATH:

linux:
  
```bash

mkdir -p /home/wiloon/my-projects/golang/lib/

mkdir -p /home/wiloon/my-projects/golang/projects/

export GOPATH="/home/wiloon/my-projects/golang/lib/:/home/wiloon/my-projects/golang/projects/"

#check golang version
  
go version
  
```

windows:
  
GOPATH=C:\workspace\myproject\golang\lib;C:\workspace\myproject\golang\gox