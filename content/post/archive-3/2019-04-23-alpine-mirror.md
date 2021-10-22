---
title: alpine basic
author: "-"
type: post
date: 2019-04-23T06:24:28+00:00
url: /?p=14227

---
## alpine basic
### alpine mirror
    vi /etc/apk/repositories
  
b. 将里面 dl-cdn.alpinelinux.org 的 改成 mirrors.aliyun.com ; 保存退出即可

### alpine install telnet

```bash
apk update
apk add busybox-extras
busybox-extras telnet localhost 6900

apk add drill

```

    apk add curl