---
title: sftp config
author: "-"
date: 2011-08-04T03:47:31+00:00
url: /?p=401
categories:
  - Linux
tags:
  - reprint
---
## sftp config

cd /root/ssh
  
emacs sshd_config
  
remove the comments for RSAAuthentication, PubkeyAuthentication
  
RSAAuthentication yes
  
PubkeyAuthentication yes

generate rsa key pair by puttygen

edit file authorized_keys add public key which generate by putty.
  
copy private key to client PC /root/.ssh/id_rsa
