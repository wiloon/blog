---
title: "bitwarden"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "bitwarden"

### server
podman pull bitwardenrs/server:latest
podman run -d --name bitwarden -v bitwarden-data:/data/ -p 80:80 bitwardenrs/server:latest

### client
    yay -S bitwarden 

---

https://hub.docker.com/r/bitwardenrs/server
https://github.com/dani-garcia/bitwarden_rs
https://github.com/bitwarden/desktop
