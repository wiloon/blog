---
title: OpenVSCode Server
author: "-"
date: 2011-08-27T13:06:15+00:00
url: /?p=592
categories:
  - Linux

---

```bash
podman run -d --name openvscode  -p 3000:3000 -v "openvscode-data:/home/workspace:cached" gitpod/openvscode-server
```
