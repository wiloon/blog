---
title: jenkins api token
author: "-"
date: 2020-03-22T10:30:34+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: jenkins-api-token
categories:
  - Cloud
tags:
  - jenkins
  - remix
  - AI-assisted
aliases:
  - /p15806/
---
## jenkins api token
Jenkins REST API提供了API token，使得可以在程序中使用API token进行认证 (而不是使用你真实的密码) 。

API token可以在用户个人设置界面查看

到用户→用户id→设置页面，在API Token区域点击Show API token按钮，便可查看API token，同时还可以更改API token

相应的URL是`http://<JENKINS_URL>/user/<userid>/configure`

### 取编译结果

BUILD_STATUS=$(curl -k -user user0:jenkins_token_0 -silent ${BUILD_URL}api/json | jq -r '.result')

https://cloud.tencent.com/developer/article/1415887
  
https://stackoverflow.com/questions/22264431/getting-a-jobs-build-status-as-post-build-variable

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Cloud | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
