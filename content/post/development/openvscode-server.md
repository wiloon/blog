---
title: OpenVSCode Server
author: "-"
date: 2011-08-27T13:06:15+00:00
url: openvscode-server
categories:
  - Tools
tags:
  - reprint
aliases:
  - /p592/
---
## OpenVSCode Server

```bash
podman run -d --name openvscode  -p 1025:3000 -v "openvscode-data:/home/workspace:cached" gitpod/openvscode-server
```
