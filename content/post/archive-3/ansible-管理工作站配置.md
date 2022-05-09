---
title: 'ansible  管理工作站配置, linux初始化'
author: "-"
date: 2019-03-16T09:52:21+00:00
url: ansible
categories:
  - Inbox
tags:
  - reprint
---
## 'ansible  管理工作站配置, linux初始化'
### archlinux

```bash
# archlinux 直接从仓库里安装就是最新版本
sudo pacman -S git ansible
```

### ubuntu,debian

ubuntu 默认 apt 安装的ansible版本可能是旧版本， 建议参照ansible官网文档安装新版本的ansible
  
[https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#latest-releases-via-apt-debian][1]

Add the following line to /etc/apt/sources.list:

```bash
deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main
```

Then run these commands:

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
sudo apt-get update
sudo apt-get install ansible
```

### 编写ansible 脚本

```bash
vim local.yml

- hosts: localhost
  become: true
  tasks:
  - name: Install htop
    apt: name=htop
```

### 提交到github

```bash
git add local.yml
git commit -m "initial commit"
git push origin master
```

### 执行脚本 ansible-pull模式

```bash
sudo ansible-pull -U https://github.com/wiloon/ansible.git
```

### 本地执行

```bash
ansible-playbook  ansible/local.yml --extra-vars "user_name=wiloonwy"
```

https://linux.cn/article-10434-1.html

 [1]: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#latest-releases-via-apt-debian