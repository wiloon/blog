---
title: docker mariadb
author: "-"
date: 2018-12-27T04:50:21+00:00
url: /?p=13220
categories:
  - container
tags:
  - reprint
---
## docker mariadb
```bash
mkdir -p /data/mariadb
docker run -d --name mariadb -P -v /data/mariadb:/var/lib/MySQL -e MySQL_ROOT_PASSWORD=password0 mariadb
```

https://www.jianshu.com/p/32542630c2bd