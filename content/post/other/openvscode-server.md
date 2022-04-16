---
title: OpenVSCode Server
author: "-"
date: 2011-08-27T13:06:15+00:00
url: /?p=592
categories:
  - Editor
tags:
  - reprint
---
## OpenVSCode Server

```bash
podman run -d --name openvscode  -p 1025:3000 -v "openvscode-data:/home/workspace:cached" gitpod/openvscode-server
```
