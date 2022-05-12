---
title: gocd
author: "-"
date: 2012-05-29T13:04:13+00:00
url: gocd
categories:
  - devops
tags:
  - reprint
---
## gocd
```bash

podman run -d --name gocd-server -p8153:8153 -v /etc/localtime:/etc/localtime:ro gocd/gocd-server:v21.4.0

podman run -d --name gocd-agent -e GO_SERVER_URL=https://gocd.wiloon.com/go gocd/gocd-agent-alpine-3.15:v21.4.0
```