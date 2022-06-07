---
title: "bitwarden"
author: "-"
date: "2022-06-06 22:00:54"
url: "bitwarden"
categories:
  - inbox
tags:
  - inbox
---
## "bitwarden"

### server

```bash
podman pull vaultwarden/server:latest
podman run -d --name vaultwarden -v bitwarden-data/:/data/ -p 80:80 vaultwarden/server:latest
```

测试一下，直接用浏览器访问 80 端口应该能看到 bitwarden 的登录页面，注册用户的话会被要求通过 https 访问。

### client

```bash
pacman -S bitwarden
```

## bitwarden ssh key, bw-key

```bash
bw-key.exe -h https://bitwarden.wiloon.com -n wiloon.wy@gmail.com
```

<https://github.com/haipengno1/bw-key>

---

<https://hub.docker.com/r/bitwardenrs/server>

<https://github.com/dani-garcia/bitwarden_rs>

<https://github.com/bitwarden/desktop>
