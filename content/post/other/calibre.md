---
title: calibre, 电子书管理, calibre-web
author: "-"
date: 2015-05-03T07:51:04+00:00
url: calibre
categories:
  - Inbox
tags:
  - Music

---
## calibre, 电子书管理

## calibre-web k8s

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: calibre-web
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: calibre-web
  template:
    metadata:
      labels:
        name: calibre-web
    spec:
      containers:
        - name: calibre-web-container
          image: lscr.io/linuxserver/calibre-web:0.6.19
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8083
          volumeMounts:
          - name: calibre-data
            mountPath: /config
            subPath: calibre-data
          - name: calibre-data
            mountPath: /config
            subPath: calibre-data
---
apiVersion: v1
kind: Service
metadata:
  name: calibre-web-service
  namespace: default
spec:
  type: NodePort
  ports:
    - name: http
      port: 18083
      targetPort: 8083
      nodePort: 31083
  selector:
    name: calibre-web
```

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
