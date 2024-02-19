---
title: buildah
author: "-"
date: 2020-01-20T10:07:09+00:00
url: buildah
categories:
  - Container
tags:
  - reprint
  - remix
---
## buildah

```bash
# removes all dangling images, same as docker prune
podman image prune

# remove image
buildah rmi 0d2d0133941b
sudo pacman -S fuse-overlayfs
sudo pacman -S buildah

# login
buildah login container.wiloon.com
buildah login --tls-verify=false container.wiloon.com

# buildah needs to run as root!!!
# list all the images
buildah images

# build
### buildah bud -f Dockerfile -t <tag0> .
buildah bud -f Dockerfile -t fedora-httpd .
buildah push registry.wiloon.com/pingd-proxy:v0.0.1

# list all containers
buildah containers
buildah run <container name>
buildah run $container -- dnf -y install java
buildah rm $newcontainer


buildah push fedora-bashecho docker-daemon:fedora-bashecho:latest
container0=$(buildah from timer0)
buildah run $container0
```

## http: server gave HTTP response to HTTPS client

https://github.com/containers/buildah/issues/4788

```Bash
buildah push --tls-verify=false ......
```