---
title: code-server
author: "-"
date: 2019-05-19T01:52:15+00:00
url: code-server
categories:
  - Uncategorized

---

```bash
docker run -d \
--name code-server \
-p 38443:8443 \
-v "code-server-project:/home/coder/project" \
codercom/code-server \
--allow-http --no-auth
```

```bash
podman run -d --name code-server \
-p 8080:8080 \
-v "code-server-config:/root/.config" \
-v "code-server-project:/home/coder/project" \
-v "code-server-ssh:/root/.ssh" \
-u "$(id -u):$(id -g)" \
-e "DOCKER_USER=root"  \
codercom/code-server:latest --auth none
```

---

https://github.com/cdr/code-server    
https://hub.docker.com/r/codercom/code-server  
