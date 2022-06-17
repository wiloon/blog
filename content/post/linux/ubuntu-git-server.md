---
title: gitosis install
author: "-"
date: 2011-05-04T01:23:27+00:00
url: /?p=177
categories:
  - Linux
  - VCS
tags:
  - Git

---
## gitosis install

1. 用apt-get update 和 apt-get upgrade 更新当前系统.
  
2. 安装OpenSSH Server: sudo apt-get install openssh-server
  
3. 修改ssh服务端配置文件/etc/ssh/sshd_config
  
Port 22 # 修改成你想要的登陆端口,如2222
  
PermitRootLogin no # 禁止root用户登陆

# 检查密钥的用户和权限是否正确，默认打开的
  
# 设置ssh在接收登录请求之前是否检查用户家目录和rhosts文件的权限和所有 权。这通常是必要的，因为新手经常会把自己的目录和文件设成任何人都有写权限。
  
StrictModes yes
  
RSAAuthentication yes # 启用 RSA 认证
  
PubkeyAuthentication yes # 启用公钥认证

ServerKeyBits 1024 #将ServerKey强度改为1024比特
  
PermitEmptyPasswords no # 禁止空密码进行登录

＃修改完成后，重启ssh服务:
  
sudo /etc/init.d/ssh restart

4.安装git: sudo apt-get install git-core
  
5.安装gitosis
  
(1)建一个临时文件夹，用来存放下载的gitosis文件，如
  
mkdir ~/tmp
  
(2)安装gitosis
  
cd ~/tmp
  
git clone git://eagain.net/gitosis
  
git://eagain.net/gitosis.git
  
cd gitosis
  
sudo python setup.py install
  
注意: 如果python setup.py install失败，需要安装python-setuptools
  
sudo apt-get install python-setuptools
  
6.为gitosis创建一个系统用户
  
sudo adduser -system -shell /bin/sh -gecos 'git SCM user' -group -disabled-password -home /home/git git

7.初始化 sudo -H -u git gitosis-init < id_rsa.pub
  
8.sudo chmod 755 /home/git/repositories/gitosis-admin.git/hooks/post-update
