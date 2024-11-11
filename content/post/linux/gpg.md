---
title: GPG
author: "-"
date: 2011-12-17T05:54:56+00:00
url: gpg
categories:
  - security
tags:
  - reprint
---
## GPG

GNU Privacy Guard

什么是 GPG
首先得搞清楚一个和它很像的东西：PGP (Pretty Good Privacy)，这是一个非对称加密协议，可惜它本身是商业软件。于是万能的开源社区搞出了一个遵循此标准的免费实现：GPG (Gnu PG)

## 'Debian – Apt-get, NO_PUBKEY / GPG error'

The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 010908312D230C5F

## Solution


sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3C962022012520A0
    

Simply type the following commands, taking care to replace the number of the key that displayed in the error message:
  
gpg -keyserver pgpkeys.mit.edu -recv-key 010908312D230C5F
  
gpg -a -export 010908312D230C5F | sudo apt-key add -


```Bash
gpg --gen-key
gpg --list-keys
```