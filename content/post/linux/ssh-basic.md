---
title: ssh basic, ssh command, openssh
author: "-"
date: 2022-10-20 22:38:04
url: ssh
categories:
  - Linux
tags:
  - reprint
  - remix
---
## ssh basic, openssh

- 端口转发
- ssh 不登陆直接执行命令
- openssh 9.0 sftp-server

### options, 参数

- -T: 禁止分配伪终端, Disable pseudo-terminal allocation
- -t 或 -tt: 强制分配伪终端, Force pseudo-terminal allocation. 
             This can be used to execute arbitrary screen-based programs on a remote machine, which can be very useful, e.g. when implementing menu servi ces. Multiple -t options force tty allocation, even if ssh has no local tty
- -f：后台执行ssh指令
- -N：不执行远程指令
- -L listen-port:host:port 指派本地的 port 到达端机器地址上的 port, 建立本地SSH隧道(本地客户端建立监听端口), 将本地机(客户机)的某个端口转发到远端指定机器的指定端口.
- -v: verbose
- -vv: verbose
- -o: 指定配置选项

#### 配置选项

```Bash
ssh -vv -T -oKexAlgorithms=ecdh-sha2-nistp521 git@foo.com
```

- KexAlgorithms: key exchange algorithm

## commands

```bash
# 指定 shell 可以解决 This account is currently not available.
sudo -u username -s /bin/bash
```

## ssh 不登陆直接执行命令

```bash
ssh root@192.168.50.31 "whoami"
```

## 指定私钥, 指定密钥

```bash
ssh -i /path/to/id_rsa
```
  
### 测试

```bash
ssh -T git@github.com
```

### ssh 强制使用密码登录, force ssh client to use only password auth

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no 192.168.50.1 -l root
```

```bash
#debian
sudo apt-get install openssh-server

#archlinux
sudo pacman -S openssh
sudo /etc/init.d/ssh start|stop|restart
ssh IP
ssh IP -p 1234 -l root

# ssh version 
ssh -V
```

## ubuntu

```bash
sudo apt install openssh-server
sudo systemctl start sshd
```

### -A option enables forwarding of the authentication agent connection

There is a shortcut to archive this, if we don't want to create a config file, we have another option, using -A flag with the ssh command.

```bash
ssh -A user@myhost.com 
```

## ssh, block ip, blacklist

Add sshd: 116.31.116.20 to /etc/hosts.deny

SSH 两种登录验证方式

一、SSH 协议
SSH是一种协议标准，其目的是实现安全远程登录以及其它安全网络服务。

二、SSH 登录过程
SSH登录主要分为两个阶段：

1）协商客户端和服务端双方通信所使用的共享密钥，并用这个共享密钥实现后续会话过程的对称加密；

2）使用非对称加密方式验证客户端的身份。

三、协商会话所使用的共享密钥

1）客户端发起tcp连接请求；

2）服务器返回其支持的协议版本以及服务器的公共主机密钥，该密钥用于判断服务器是否是预期的主机；

3）双方交换会话密钥，用于后续会话做对称加密。

四、密码验证登录过程

1）服务端收到客户端的请求后，把自己的公钥发送给客户端（与会话密钥不同，是服务器自身的公钥/私钥对）；

2）客户端使用收到的公钥加密密码，并发送回服务器；

3）服务器使用自己私钥解密信息，若密码正确，则通过验证。

五、密钥验证登录过程

前提条件是手动将客户端的公钥发送给服务器，并填入authorized_keys文件中。

1）客户端把用户验证的密钥对ID发送给服务器；

2）服务器根据密钥对ID在对应用户的authorized_keys文件中进行检索；

3）假设服务器在文件中找到符合密钥对ID的公钥，服务器将生成一个随机数，并用这个公钥进行加密；

4）服务器将加密后的信息发送给客户端；

5）假设客户端拥有对应的私钥，就可以解密出原来的随机数；

6）客户端将得到的随机数与加密会话所用的会话密钥拼接一起后，计算其MD5哈希值；

7）客户端将MD5哈希值发送回服务器；

8）服务器使用相同的会话共享密钥和他生成的随机数计算出MD5哈希值，并与客户端返回的MD5哈希值进行比较。如果两个值相等，证明客户端拥有对应私钥，则通过验证。

[https://zhuanlan.zhihu.com/p/139285610](https://zhuanlan.zhihu.com/p/139285610)

## openssh 9.0 sftp-server

Since OpenSSH 9.0 the scp utility uses the SFTP protocol by default. The -O option must be used to use the legacy SCP protocol.

A normal scp will result in standard OpenWrt:

ash: /usr/libexec/sftp-server: not found
scp: Connection closed

A workaround is to add the -O option.

```bash
scp -O foo.txt root@192.168.50.4:~
```

————————————————
版权声明：本文为CSDN博主「phantom_111」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/phantom_111/article/details/56297242

## 'ssh_exchange_identification,read,Connection reset by peer'

```bash
/etc/hosts.deny
```
