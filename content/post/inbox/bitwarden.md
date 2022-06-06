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

podman pull vaultwarden/server:latest
podman run -d --name vaultwarden -v bitwarden-data/:/data/ -p 80:80 vaultwarden/server:latest

### client

    yay -S bitwarden 

---

<https://hub.docker.com/r/bitwardenrs/server>
<https://github.com/dani-garcia/bitwarden_rs>
<https://github.com/bitwarden/desktop>
