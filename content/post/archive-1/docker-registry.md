---
title: docker registry
author: "-"
date: 2021-03-05 20:05:34
url: docker/registry
categories:
  - docker

tags:
  - reprint
---
## docker registry

- registry-1.docker.io

```bash
vim /etc/containers/registries.conf

# content
unqualified-search-registries = ["docker.io"]

[[registry]]
prefix = "docker.io"
location = "registry-1.docker.io"
```