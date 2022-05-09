---
title: linux tar aes 打包加密
author: "-"
date: 2018-10-12T03:32:34+00:00
url: /?p=12784
categories:
  - Inbox
tags:
  - reprint
---
## linux tar aes 打包加密
```bash
  
tar -cvf - foo | openssl enc -e -aes256 -k password -out foo.tar
  
openssl enc -d -aes256 -in foo.tar -k password | tar xv
  
openssl enc -d -aes256 -in foo.tar -k password | tar xv -C .

#原文件 foo
  
#密码 password
  
#目标文件 foo.tar

```