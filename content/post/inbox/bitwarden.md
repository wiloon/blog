---
title: "bitwarden"
author: "-"
date: "2022-06-06 22:00:54"
url: "bitwarden"
categories:
  - Security
tags:
  - Security
---
## "bitwarden"

## auto fill

chrome extension> bitwarden> settings> option> autofill> enable auto-fill on page load

### podman server

```bash
podman pull vaultwarden/server:1.28.1-alpine
podman run -d --name bitwarden -v bitwarden-data:/data/ -p 8000:80 vaultwarden/server:1.28.1-alpine
docker run -d --name bitwarden --restart=always -v bitwarden-data:/data/ -p 8000:80 vaultwarden/server:1.28.1-alpine
```

测试一下，直接用浏览器访问 80 端口应该能看到 bitwarden 的登录页面，注册用户的话会被要求通过 https 访问。

### client

```bash
pacman -S bitwarden
```

## bitwarden ssh key, bw-key

download bw-key from <https://github.com/haipengno1/bw-key/releases>

```bash
bw-key.exe -h https://bitwarden.wiloon.com -n wiloon.wy@gmail.com
```

<https://github.com/haipengno1/bw-key>

---

<https://hub.docker.com/r/bitwardenrs/server>

<https://github.com/dani-garcia/bitwarden_rs>

<https://github.com/bitwarden/desktop>
