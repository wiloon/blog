---
title: win linux ssh putty
author: wiloon
type: post
date: 2011-10-19T02:49:26+00:00
url: /?p=1190
bot_views:
  - 10
views:
  - 5
categories:
  - Linux

---
win: 用 PuTTYgen 生成rsa key

linux:   在 /home/xxx/.ssh/ 里创建文件  authorized_keys

修改权限

chmod o-r authorized_keys

chmod g-r authorized_keys

win: 运行pageant, 添加私钥

&nbsp;