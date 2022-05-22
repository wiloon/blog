---
title: calibre
author: "-"
date: 2015-05-03T07:51:04+00:00
url: /?p=7582
categories:
  - Inbox
tags:
  - Music

---
## calibre

## web

```bash
podman run -d \
  --name=calibre-web \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/China \
  -e DOCKER_MODS=linuxserver/calibre-web:calibre \
  -e OAUTHLIB_RELAX_TOKEN_SCOPE=1 \
  -p 8083:8083 \
  -v calibre-data:/config \
  -v calibre-library:/books \
  --restart unless-stopped \
  lscr.io/linuxserver/calibre-web:latest
```

## GUI

```bash
podman run -d \
  --name=calibre \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/China \
  -p 8080:8080 \
  -p 8081:8081 \
  -v calibre-data-tmp:/config \
  --restart unless-stopped \
  lscr.io/linuxserver/calibre:latest

```

## mail server setup

<https://github.com/janeczku/calibre-web/wiki/Setup-Mailserver>

