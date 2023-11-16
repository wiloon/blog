---
title: ssh-keygen
author: "-"
date: 2011-11-24T04:41:17
url: ssh-keygen
categories:
  - Security
tags:
  - reprint
  - remix

---
## ssh-keygen

ssh-keygen 是用于为 SSH 创建新的身份验证密钥对的工具。此类密钥对用于自动登录，单点登录和验证主机。目前广泛的用在 linux 服务验证、git 身份验证上。

执行 ssh-keygen 可以生成一个密钥对, 这个密钥对称为公钥文件和私钥文件 ,例如：

使用 rsa 算法：id_rsa(密钥), id_rsa.pub(公钥)
使用 dsa 算法：id_dsa(密钥), id_dsa.pub(公钥)

-t 选择加密算法
ssh-keygen 目前支持三种加密算法: rsa, dsa, ecdsa, 默认使用的是 rsa，ssh-keygen 程序是交互式的

在 ~/.ssh 目录下生成私钥 id_rsa 和公钥 id_rsa.pub 文件

```bash
# 优先使用 ed25519
ssh-keygen -t ed25519 -C "foo"
ssh-keygen -t ed25519 -f foo -C "bar"

# -t 选择加密算法, -t ed25519 使用加密算法 ed25519, 可选值: ed25519, rsa 
# -f foo, 生成的密钥文件名, 不指定文件名的话, ed25519 算法默认的文件名是 id_ed25519 
# -C "bar" 在公钥文件中添加注释，即为这个公钥“起个别名”（不是 id，可以更改）。

# 打印公钥指纹, The -l option instructs to show the fingerprint in the public key while the -f option specifies the file of the key to list the fingerprint for.
ssh-keygen -l -f id_ed25519

# 从私钥生成公钥
# -y This option will read a private OpenSSH format file and print an OpenSSH public key to stdout.
ssh-keygen -y -f id_ed25519 > id_ed25519.pub

ssh-keygen -t rsa
ssh-keygen -t rsa -b 4096
ssh-keygen -t ecdsa -b 521
# -t type 指定要创建的密钥类型。可以使用: "rsa1"(SSH-1) "rsa"(SSH-2) "dsa"(SSH-2)

ssh-keygen -t rsa -C "Michael Ledin" -b 4096 -m "PEM"

# -C comment
# -b key 长度
# -t 类型: dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa

scp /root/.ssh/id_rsa.pub root@192.168.10.184:/root
ssh 192.168.10.184
cat /root/id_rsa.pub >> /root/.ssh/authorized_keys
# ok,you will login 192.168.10.184 without input password.
```

## 推送公钥到服务器

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.1.0.2
```

### print SHA256 fingerprint

```bash
# retrieve the SHA256 fingerprint
ssh-keygen -lf /path/to/ssh/key

# GitHub (MD5) fingerprint format
ssh-keygen -E md5 -lf <fileName>
```

```bash
ssh-keygen -A
```

public key file: authorized_keys

this command will generating public/private rsa key pair.
  
Your identification has been saved in /root/.ssh/id_rsa
  
Your public key has been saved in /root/.ssh/id_rsa.pub

### WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED

```bash
ssh-keygen -f "/home/wiloon/.ssh/known_hosts" -R "192.168.1.2"
```

### multiple ssh private keys

by **Karanbir Singh**

[http://www.karan.org/blog/index.php/2009/08/25/multiple-ssh-private-keys](http://www.karan.org/blog/index.php/2009/08/25/multiple-ssh-private-keys)
  
In quite a few situations its preferred to have ssh keys dedicated for a service or a specific role. Eg. a key to use for home / fun stuff and another one to use for Work things, and another one for Version Control access etc. Creating the keys is simple, just use

ssh-keygen -t rsa -f ~/.ssh/id_rsa.work -C "Key for Word stuff"

Use different file names for each key. Lets assume that there are 2 keys, ~/.ssh/id_rsa.work and ~/.ssh/id_rsa.misc . The simple way of making sure each of the keys works all the time is to now create config file for ssh:

touch ~/.ssh/config
 chmod 600 ~/.ssh/config
 echo "IdentityFile ~/.ssh/id_rsa.work" >> ~/.ssh/config
 echo "IdentityFile ~/.ssh/id_rsa.misc" >> ~/.ssh/config

This would make sure that both the keys are always used whenever ssh makes a connection. However, ssh config lets you get down to a much finer level of control on keys and other per-connection setups. And I recommend, if you are able to, to use a key selection based on the Hostname. My ~/.ssh/config looks like this :

```bash
Host *.home.lan
IdentityFile ~/.ssh/id_dsa.home
User kbsingh

Host *.vpn
  IdentityFile ~/.ssh/id_rsa.work
  User karanbir
  Port 44787

Host *.d0.karan.org
  IdentityFile ~/.ssh/id_rsa.d0
  User admin
  Port 21871
```

Ofcourse, if I am connecting to a remote host that does not match any of these selections, ssh will default back to checking for and using the 'usual' key, ~/.ssh/id_dsa or ~/.ssh/id_rsa

作者：Martain
链接：[https://www.jianshu.com/p/75bf863c4ab6](https://www.jianshu.com/p/75bf863c4ab6)
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
