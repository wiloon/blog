---
title: nexus OSS
author: "-"
date: 2012-04-24T10:52:10+00:00
url: /?p=3021
categories:
  - Inbox
tags:
  - reprint
---
## nexus OSS
### docker

```bash
podman run \
-d \
--name nexus \
-p 8081:8081 \
-p 8083:8083 \
-v /etc/localtime:/etc/localtime:ro \
-v /data/nexus-data:/nexus-data \
sonatype/nexus3

```

### config

default username/password=admin/admin123
  
Blob Stores/Enable Soft Quota: 限制目录大小

download nexus-2.14.0-01-bundle.zip

unzip and execute ./bin/nexus start

add aliyun repo as proxy repository

repository id: aliyun_repo

repository name: aliyun_repo

provider Maven2

Repository Policy: Release

Remote Storage location: http://maven.aliyun.com/nexus/content/groups/public/

click save

upload 3rd party jar

3rd party>Artifact Upload

GAV Definition:GAV Parameters

Group:xxx

Artifact:xxx

Version:xxx

Packaging:

error: wrapper | OpenSCManager failed – Access is denied.

click on start
  
click "All Programs"
  
click on accessories
  
right click on "Command Prompt" icon
  
click "properties"
  
click on the "shortcut" tab on the top
  
click the advanced button at the bottom
  
click on the check box that says "Run as Administrator".
  
click OK

### 上传jar包

### 上传pom

选择pom文件，扩展名填写 "pom"
  
包路径 和版本信息会从pom自动读取。
  
点击上传按钮