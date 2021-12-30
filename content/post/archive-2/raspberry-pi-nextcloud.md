---
title: cozy, nextcloud
author: "-"
date: 2019-01-26T05:27:32+00:00
url: /?p=13451
categories:
  - Uncategorized

---
## cozy, nextcloud

### Cozy Cloud
Cozy Cloud是一个开源的个人私有云,可以用于阅读电子邮件,或者管理和同步联系人、文件或日历,同时会有相关的应用商店和社区作为素材库,它可以将所有Web服务都放在同一个私有的个人平台,通过此平台,用户的网页应用和设备可以轻松地进行数据分享。

语言: Go
操作系统: Linux/Unix
类型: Groupware
授权: Agpl 3
下载地址: https://github.com/cozy/cozy-stack


---

https://shingle.me/post/%E6%8A%9B%E5%BC%83nextcloud%E5%BC%80%E5%A7%8B%E6%90%AD%E5%BB%BA%E4%BD%BF%E7%94%A8cozycloud/


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

nginx代理nextcloud时, nextcloud需要配置

```bash'trusted_proxies'   => ['127.0.0.1'],
'overwritehost'     => 'xxx.wiloon.com',
'overwriteprotocol' => 'https',
'overwritewebroot'  => '/',
'overwritecondaddr' => '^127\.0\.0\.1$',
```