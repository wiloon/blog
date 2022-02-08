---
title: ssh basic
author: "-"
date: 2011-09-25T09:54:40+00:00
url: /?p=913
categories:
  - Linux

tags:
  - reprint
---
## ssh basic
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
  
```






---




### -A option enables forwarding of the authentication agent connection.
There is a shortcut to archive this, if we don't want to create a config file, we have another option, using -A flag with the ssh command.

    ssh -A user@myhost.com 
