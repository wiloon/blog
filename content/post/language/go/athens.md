---
title: athens
author: "-"
date: 2022-11-29 16:53:10
url: athens
categories:
  - Golang
tags:
  - reprint
  - remix
---
## athens, go package cache/repo 私服, go package 私有仓库, go package 服务器

Athens: Go Packages 服务器, 私服, go package 私有仓库, 其它可选方案 Nexus.

```bash
podman volume create athens-data

vim /var/lib/containers/storage/volumes/athens-data/_data/download-mode

downloadURL = "https://goproxy.cn"
mode = "async_redirect"

podman run -d \
--name athens \
-p 4000:3000 \
-v athens-data:/var/lib/athens \
-e ATHENS_DISK_STORAGE_ROOT=/var/lib/athens \
-e ATHENS_STORAGE_TYPE=disk \
-e ATHENS_DOWNLOAD_MODE=file:/var/lib/athens/download-mode \
gomods/athens:latest
```

```bash
export GOPROXY=http://localhost:3000 && go get module@v1
```

[https://docs.gomods.io/](https://docs.gomods.io/)

[https://github.com/gomods/athens](https://github.com/gomods/athens)
