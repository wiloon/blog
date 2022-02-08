---
title: buildah
author: "-"
date: 2020-01-20T10:07:09+00:00
url: /?p=15406
categories:
  - Uncategorized

tags:
  - reprint
---
## buildah
```bash
sudo pacman -S buildah

# buildah needs to run as root!!!
# list all the images
buildah images

### buildah bud -f Dockerfile -t <tag0> .
buildah bud -f Dockerfile -t fedora-httpd .

# list all containers
buildah containers
buildah run <container name>
buildah run $container -- dnf -y install java
buildah rm $newcontainer


buildah push fedora-bashecho docker-daemon:fedora-bashecho:latest
container0=$(buildah from timer0)
buildah run $container0
```