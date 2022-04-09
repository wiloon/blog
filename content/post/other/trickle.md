---
title: trickle
author: "-"
date: 2011-09-30T02:52:07+00:00
url: trickle
categories:
  - network
tags:
  - network

---
## trickle

userspace bandwidth shaper

### 限速 200k

```bash
trickle -s -u 200 -d 200  git pull
```

## 参数

- -s, standalone mode 不依赖 trickled
- -u, 上传速率 KB/s
- -d, 下载速率 KB/s

<https://github.com/mariusae/trickle>
<https://wiki.archlinux.org/title/trickle>
