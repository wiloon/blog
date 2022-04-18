---
title: ssh basic
author: "-"
date: 2011-09-25T09:54:40+00:00
url: ssh
categories:
  - Linux

tags:
  - reprint
---
## ssh basic

## 指定私钥

    ssh -i /path/to/id_rsa
  
### 测试

    ssh -T git@github.com

### 强制使用密码登录, force ssh client to use only password auth

    ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no 192.168.2.x -l user0

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

    ssh -A user@myhost.com 

## ssh, block ip, blacklist

Add sshd: 116.31.116.20 to /etc/hosts.deny

SSH两种登录验证方式

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

><https://zhuanlan.zhihu.com/p/139285610>
