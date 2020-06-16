---
title: nextcloud
author: wiloon
type: post
date: 2019-01-26T05:27:32+00:00
url: /?p=13451
categories:
  - Uncategorized

---
```bash
docker run -d \
--name nextcloud \
-p 2000:80 \
-v /etc/localtime:/etc/localtime:ro \
-v nextcloud:/var/www/html \
--restart=always \
nextcloud

#podman
podman run -d \
--name nextcloud \
-p 2000:80 \
-v /etc/localtime:/etc/localtime:ro \
-v nextcloud:/var/www/html \
nextcloud

```

home-port: 63585

nginx代理nextcloud时， nextcloud需要配置

```bash'trusted_proxies'   =&gt; ['127.0.0.1'],
'overwritehost'     =&gt; 'xxx.wiloon.com',
'overwriteprotocol' =&gt; 'https',
'overwritewebroot'  =&gt; '/',
'overwritecondaddr' =&gt; '^127\.0\.0\.1$',
```