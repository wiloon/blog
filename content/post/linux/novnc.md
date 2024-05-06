---
author: "-"
date: "2020-06-28T15:23:44Z"
title: novnc
categories:
  - inbox
tags:
  - reprint
---
### novnc

[https://github.com/novnc/noVNC](https://github.com/novnc/noVNC)
[https://novnc.com/info.html](https://novnc.com/info.html)

    podman run  \
    -e REMOTE_HOST=192.168.50.114 \
    -e REMOTE_PORT=5900 \
    -p 8082:8081 \
    -d \
    --name novnc-dell \
    dougw/novnc

### nginx config

```Bash
server {
        listen 80;
        server_name  vnc.wiloon.com; 
        location / { 
        proxy_pass http://192.168.50.114:8082;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 1d;
        proxy_send_timeout 1d;
        proxy_read_timeout 1d;
        }
}
```
