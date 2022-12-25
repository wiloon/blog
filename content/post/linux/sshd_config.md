---
title: sshd config
author: "-"
date: 2018-01-17T08:50:28+00:00
url: /?p=11742
categories:
  - inbox
tags:
  - reprint
---
## 查看 sshd 运行参数

```bash
    sshd -T | sort
```

## sshd 日志

```bash
journalctl -u sshd -f

```

## sshd config

AddressFamily
指定 sshd(8) 应当使用哪种地址族。取值范围是: "any"(默认)、"inet"(仅IPv4)、"inet6"(仅IPv6)。
  
ListenAddress 0.0.0.0
  
ListenAddress用来设置sshd服务器绑定的IP地址
  
Protocol

指定 sshd(8) 支持的SSH协议的版本号。

'1'和'2'表示仅仅支持SSH-1和SSH-2协议。"2,1"表示同时支持SSH-1和SSH-2协议。

HostKey

主机私钥文件的位置。如果权限不对,sshd(8) 可能会拒绝启动。

SSH-1默认是 /etc/ssh/ssh_host_key

SSH-2默认是 /etc/ssh/ssh_host_rsa_key 和 /etc/ssh/ssh_host_dsa_key 。

一台主机可以拥有多个不同的私钥。"rsa1"仅用于SSH-1,"dsa"和"rsa"仅用于SSH-2。

AuthorizedKeysFile
  
存放该用户可以用来登录的 RSA/DSA 公钥。
  
该指令中可以使用下列根据连接时的实际情况进行展开的符号:
  
%% 表示'%'、%h 表示用户的主目录、%u 表示该用户的用户名。
  
经过扩展之后的值必须要么是绝对路径,要么是相对于用户主目录的相对路径。
  
默认值是".ssh/authorized_keys"。

UsePrivilegeSeparation
  
是否让 sshd(8) 通过创建非特权子进程处理接入请求的方法来进行权限分离。默认值是"yes"。

认证成功后,将以该认证用户的身份创建另一个子进程。

这样做的目的是为了防止通过有缺陷的子进程提升权限,从而使系统更加安全。

PermitUserEnvironment

指定是否允许 sshd(8) 处理 ~/.ssh/environment 以及 ~/.ssh/authorized_keys 中的 environment= 选项。

默认值是"no"。如果设为"yes"可能会导致用户有机会使用某些机制(比如 LD_PRELOAD)绕过访问控制,造成安全漏洞。

Ciphers

指定SSH-2允许使用的加密算法。多个算法之间使用逗号分隔

Ciphers aes256-ctr,aes192-ctr,aes128-ctr
  
<https://blog.csdn.net/zhu_xun/article/details/18304441>
  
<http://www.jinbuguo.com/openssh/sshd_config.html>
  
<http://daemon369.github.io/ssh/2015/03/21/using-ssh-config-file>
