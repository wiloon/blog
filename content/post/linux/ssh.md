---
title: ssh
author: "-"
date: 2012-01-20T01:37:12+00:00
url: ssh
categories:
  - Linux
tags:
  - reprint
---
## ssh

## install

### archlinux

```bash
pacman -S openssh
```

### ubuntu

```bash
sudo apt-get install openssh-server
sudo apt-get install openssh-client
```

## commands

```bash
# 超时时间
ssh -o ConnectTimeout=10  <hostName>
# -o, option
```

Ubuntu缺省安装了openssh-client,所以在这里就不安装了，如果你的系统没有安装的话，再用apt-get安装上即可。
  
然后确认sshserver是否启动了:

```bash
ps -e |grep ssh
```

如果只有ssh-agent那ssh-server还没有启动，需要/etc/init.d/ssh start，如果看到sshd那说明ssh-server已经启动了。

ssh-server配置文件位于/ etc/ssh/sshd_config，在这里可以定义SSH的服务端口，默认端口是22，你可以自己定义成其他端口号，如222。然后重启SSH服务:

sudo /etc/init.d/ssh resar

## no matching host key type found. Their offer: ssh-rsa

```bash
ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa  root@192.168.50.1 -p 22
ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa  root@192.168.50.4 -p 22
```

为什么会有这个错误
根据 OpenSSH Release Notes

Future deprecation notice

It is now possible[1] to perform chosen-prefix attacks against the SHA-1 algorithm for less than USD$50K.

In the SSH protocol, the “ssh-rsa” signature scheme uses the SHA-1 hash algorithm in conjunction with the RSA public key algorithm. OpenSSH will disable this signature scheme by default in the near future.

Note that the deactivation of “ssh-rsa” signatures does not necessarily require cessation of use for RSA keys. In the SSH protocol, keys may be capable of signing using multiple algorithms. In particular, “ssh-rsa” keys are capable of signing using “rsa-sha2-256” (RSA/SHA256), “rsa-sha2-512” (RSA/SHA512) and “ssh-rsa” (RSA/SHA1). Only the last of these is being turned off by default.

也就是说 8.8p1 版的 openssh 的 ssh 客户端默认禁用了 ssh-rsa 算法, 但是对方服务器只支持 ssh-rsa, 当你不能自己升级远程服务器的 openssh 版本或修改配置让它使用更安全的算法时, 在本地 ssh 针对这些旧的ssh server重新启用 ssh-rsa 也是一种权宜之法.

[https://ttys3.dev/post/openssh-8-8-p1-no-matching-host-key-type-found-their-offer-ssh-rsa/](https://ttys3.dev/post/openssh-8-8-p1-no-matching-host-key-type-found-their-offer-ssh-rsa/)

## key type ssh-rsa not in PubkeyAcceptedAlgorithms

Mar 29 12:58:48 roy-dev sshd[132418]: userauth_pubkey: key type ssh-rsa not in PubkeyAcceptedAlgorithms [preauth]

```bash
vim /etc/ssh/sshd_config
PubkeyAcceptedKeyTypes +ssh-rsa
```

It is now possible[1] to perform chosen-prefix attacks against the SHA-1 algorithm for less than USD$50K.

In the SSH protocol, the “ssh-rsa” signature scheme uses the SHA-1 hash algorithm in conjunction with the RSA public key algorithm. OpenSSH will disable this signature scheme by default in the near future.

Note that the deactivation of “ssh-rsa” signatures does not necessarily require cessation of use for RSA keys. In the SSH protocol, keys may be capable of signing using multiple algorithms. In particular, “ssh-rsa” keys are capable of signing using “rsa-sha2-256” (RSA/SHA256), “rsa-sha2-512” (RSA/SHA512) and “ssh-rsa” (RSA/SHA1). Only the last of these is being turned off by default.

也就是说 8.8p1 版的 openssh 的 ssh 客户端默认禁用了 ssh-rsa 算法, 但是对方服务器只支持 ssh-rsa, 当你不能自己升级远程服务器的 openssh 版本或修改配置让它使用更安全的算法时, 在本地 ssh 针对这些旧的ssh server重新启用 ssh-rsa 也是一种权宜之法.

OpenSSH 8.2发布 禁用ssh-rsa算法

[https://cloud.tencent.com/developer/article/1589118](https://cloud.tencent.com/developer/article/1589118)

另一方面关于 SHA-1 哈希算法，此前该算法被发现构造前缀碰撞攻击成本已降至低于 5 万美元（实际为 4.5 万美元），因此开发团队决定禁用 ssh-rsa 公钥签名算法。

有一些更好的算法可以替代，包括 RFC8332 RSA SHA-2 签名算法 rsa-sha2-256/512、ssh-ed25519 签名算法与 RFC5656 ECDSA 算法。 目前这些算法在 OpenSSH 中都已经支持。

完整的更新说明查看：[http://www.openssh.com/txt/release-8.2](http://www.openssh.com/txt/release-8.2)

winscp 使用 5.20.1 beta 以上的版本默认不使用 ssh-rsa 签名算法 .

```bash
HostKeyAlgorithms
             Specifies the protocol version 2 host key algorithms that the client wants to use in order of preference.  The default for this option is:

                ecdsa-sha2-nistp256-cert-v01@openssh.com,
                ecdsa-sha2-nistp384-cert-v01@openssh.com,
                ecdsa-sha2-nistp521-cert-v01@openssh.com,
                ssh-rsa-cert-v01@openssh.com,ssh-dss-cert-v01@openssh.com,
                ssh-rsa-cert-v00@openssh.com,ssh-dss-cert-v00@openssh.com,
                ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,
                ssh-rsa,ssh-dss

             If hostkeys are known for the destination host then this default is modified to prefer their algorithms.
```
