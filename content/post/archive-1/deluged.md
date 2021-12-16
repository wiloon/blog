---
title: deluged
author: "-"
date: 2014-03-02T05:08:30+00:00
url: /?p=6306
categories:
  - Uncategorized
tags:
  - linux

---
## deluged
```bash
docker run \
    -d \
  --name=deluge \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -v deluge-config:/config \
  -v deluge-downloads:/downloads \
  --restart unless-stopped \
  linuxserver/deluge
```

```bash
#debian

apt-get update
apt-get install deluged deluge-web

#运行 deluge守护进程 deluged 和web控制端

deluged
nohup deluge-web &

```

用浏览器访问 http://ip:8112

默认密码是 deluge

http://www.jianshu.com/p/48feb68b3b30

http://dev.deluge-torrent.org/wiki/UserGuide