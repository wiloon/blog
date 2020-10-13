---
title: rsa ssh keygen
author: wiloon
type: post
date: 2011-11-24T04:41:17+00:00
url: /?p=1580
bot_views:
  - 7
views:
  - 2
categories:
  - Linux

---
在~/.ssh目录下生成私钥id_rsa和公钥id_rsa.pub文件

```bash
ssh-keygen -t rsa
ssh-keygen -t rsa -b 4096
ssh-keygen -t ecdsa -b 521
# -t type 指定要创建的密钥类型。可以使用："rsa1"(SSH-1) "rsa"(SSH-2) "dsa"(SSH-2)

scp /root/.ssh/id_rsa.pub root@192.168.10.184:/root
ssh 192.168.10.184
cat /root/id_rsa.pub >> /root/.ssh/authorized_keys
# ok,you will login 192.168.10.184 without input password.

```
### print SHA256 fingerprint
    ssh-keygen -lf /path/to/ssh/key

### 
    ssh-keygen -A
    
public key file: authorized_keys

this command will generating public/private rsa key pair.
  
Your identification has been saved in /root/.ssh/id_rsa
  
Your public key has been saved in /root/.ssh/id_rsa.pub