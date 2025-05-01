---
title: homelab
author: "-"
date: 2017-02-20T07:37:42+00:00
url: homelab
categories:
  - Inbox
tags:
  - reprint
---

## homelab

## 新二级域名

1. 在阿里云控制台添加新域名
2. 等域名生效 `drill jenkins.wiloon.com`
3. 在 wiloon.com 更新证书加入新域名, ssh aliyun 
4. podman stop nginx 
5. certbot
6. ssh root@nginx
7. sh /data/cert/cert.sh
8. ssh router
9. vi /etc/hosts
10. /etc/init.d/dnsmasq restart

## DNS

192.168.50.1

## Nginx

192.168.50.130

## 更新 nginx

1. 在内网有梯子的机器 podman pull nginx:1.27.2
2. podman save 7f553e8bbc897571642d836b31eaf6ecbe395d7641c2b24291356ed28f3f2bd0>nginx.tar
3. tar zcvf nginx.tar.gz nginx.tar
4. scp nginx.tar.gz aliyun:~
