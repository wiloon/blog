---
title: nexus docker repo
author: "-"
date: 2020-03-14T17:55:29+00:00
url: /?p=15753
categories:
  - container
tags:
  - reprint
---
## nexus docker repo

create repository

docker-hosted

docker-proxy, azure, aliyun,dockerio

docker-group

勾选 :  HTTP, Create an HTTP connector at specified port. Normally used if the server is behind a secure proxy 并填写端口

勾选: Allow anonymous docker pull ( Docker Bearer Token Realm required )

Administration>Security>Anonymous Access 勾选 Allow anonymous users to access the server, Realm: 选择 Docker Bearer Token Realm
  
Administration>Security>Realms: 把Docker bearer token realm 加入 Active
