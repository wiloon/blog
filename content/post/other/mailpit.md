---
author: "-"
date: "2020-09-01 09:52:18" 
title: "Mailpit"
categories:
  - inbox
tags:
  - reprint
---
## Mailpit

Mailpit - email testing for developers

```bash
sudo bash < <(curl -sL https://raw.githubusercontent.com/axllent/mailpit/develop/install.sh)

# 启动 mailpit, -h for help
./mailpit. 

mailpit -h


```

## mailpit sendmail

准备一个文本文件

```txt
Date: Mon, 23 Jun 2015 11:40:36 -0400
From: user0 <user0@wiloon.com>
To: user1 <user1@wiloon.com>
Subject: subject0

body0

```

发送邮件

```bash
mailpit sendmail < foo.txt

```

在浏览器里查看邮件 [http://localhost:8025](http://localhost:8025)
