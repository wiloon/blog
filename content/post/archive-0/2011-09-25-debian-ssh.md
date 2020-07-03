---
title: linux ssh
author: wiloon
type: post
date: 2011-09-25T09:54:40+00:00
url: /?p=913
bot_views:
  - 8
categories:
  - Linux

---
```bash
  
#debian
  
sudo apt-get install openssh-server

#archlinux
  
sudo pacman -S openssh

sudo /etc/init.d/ssh start|stop|restart

ssh IP
  
ssh IP -p 1234 -l root
  
```