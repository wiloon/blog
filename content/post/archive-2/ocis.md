---
title: owncloud,cozy, nextcloud, Cloudreve
author: "-"
date: 2019-01-26T05:27:32+00:00
url: Gofi
categories:
  - cloud
tags:
  - reprint
---
## owncloud,cozy, nextcloud, Cloudreve

## Cloudreve

☁️ 支持本机、从机、七牛、阿里云 OSS、腾讯云 COS、又拍云、OneDrive (包括世纪互联版) 作为存储端
📤 上传/下载 支持客户端直传，支持下载限速
💾 可对接 Aria2 离线下载，可使用多个从机节点分担下载任务
📚 在线 压缩/解压缩、多文件打包下载
💻 覆盖全部存储策略的 WebDAV 协议支持
⚡ 拖拽上传、目录上传、流式上传处理
🗃️ 文件拖拽管理
👩‍👧‍👦 多用户、用户组
🔗 创建文件、目录的分享链接，可设定自动过期
👁️‍🗨️ 视频、图像、音频、文本、Office 文档在线预览
🎨 自定义配色、黑暗模式、PWA 应用、全站单页应用
🚀 All-In-One 打包，开箱即用

## Gofi

<https://gofi.calmlyfish.com/zh/>

```bash
nohup ./gofi-linux-amd64 &
podman run -d         --name=gofi         -p 80:8080         -v gofi-app:/app         sloaix/gofi:latest
```

### owncloud

podman pull owncloud/ocis
podman run --rm -ti -p 9200:9200 -e OCIS_INSECURE=true owncloud/ocis

### Cozy Cloud

Cozy Cloud是一个开源的个人私有云,可以用于阅读电子邮件,或者管理和同步联系人、文件或日历,同时会有相关的应用商店和社区作为素材库,它可以将所有Web服务都放在同一个私有的个人平台,通过此平台,用户的网页应用和设备可以轻松地进行数据分享。

语言: Go
操作系统: Linux/Unix
类型: Groupware
授权: Agpl 3
下载地址: <https://github.com/cozy/cozy-stack>

---

<https://shingle.me/post/%E6%8A%9B%E5%BC%83nextcloud%E5%BC%80%E5%A7%8B%E6%90%AD%E5%BB%BA%E4%BD%BF%E7%94%A8cozycloud/>

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
