---
title: aria2
author: "-"
date: 2020-01-28T09:40:14+00:00
url: /?p=15430
categories:
  - Inbox
tags:
  - reprint
---
## aria2
### docker

```bash
# Webui
git clone https://github.com/ziahamza/webui-aria2.git
buildah bud -f Dockerfile -t pingd/webui-aria2 .

# run web-ui
podman run \
-d \
-v aria-download:/data \
-p 6800:6800 \
-p 9100:8080 \
--name="webui-aria2" \
pingd/webui-aria2
```

```bash
sudo pacman -S aria2

# download a file 
aria2c https://xxx


```

https://github.com/aria2/aria2
  
https://github.com/ziahamza/webui-aria2