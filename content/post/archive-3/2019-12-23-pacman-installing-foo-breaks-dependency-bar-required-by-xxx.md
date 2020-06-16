---
title: pacman, installing foo breaks dependency 'bar' required by xxx
author: wiloon
type: post
date: 2019-12-23T01:19:46+00:00
url: /?p=15232
categories:
  - Uncategorized

---
```bash
installing xorgproto (2019.2-2) breaks dependency 'dmxproto' required by libdmx
installing xorgproto (2019.2-2) breaks dependency 'xf86dgaproto' required by libxxf86dga
```

```bash
sudo pacman -Rdd libdmx libxxf86dga && sudo pacman -Syu
```