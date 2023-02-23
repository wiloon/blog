---
title: traefik
author: "-"
date: 2017-01-15T06:33:52+00:00
url: traefik
categories:
  - network
tags:
  - reprint
  - remix
---
## traefik

```bash
podman run -d \
--name traefik \
-p 80:80 \
-p 8080:8080 \
-v nginx-config:/etc/nginx \
-v nginx-www:/var/www \
-v cert:/etc/letsencrypt \
-v /etc/localtime:/etc/localtime:ro \
traefik:v2.9.6

```

## dashboard

<http://192.168.50.51:8080/>
