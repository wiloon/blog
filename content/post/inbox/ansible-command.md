---
title: ansible basic command
author: "-"
date: 2016-05-13T12:00:27+00:00
url: ansible
categories:
  - devops
tags:
  - reprint
  - remix

---
## ansible basic command

## commands

```bash
# 临时的 inventory file
ansible -i '192.168.50.111,' all  -m shell -a 'whoami'  -u root

ansible-galaxy collection install community.general
# localhost
ansible localhost -m shell -a 'ls'
# 指定私钥 --key-file
ansible -i 'wiloon.com,' all -m shell -a 'systemctl stop enx-api' -u root --key-file ~/.ssh/id_ed25519_w10n
```

### hibernate

```bash
ansible -i '192.168.50.31,' all  -m shell -a 'sudo systemctl hibernate'  -u user0
```

## install

### Installing Ansible on Ubuntu

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

### macos

```bash
brew install ansible
```

## ansible 配置文件

```bash
/etc/ansible/ansible.cfg
```

### 文件内容

```bash
[defaults]
interpreter_python = auto_legacy_silent
# gather 超时时间
gather_timeout=30

```

## inventory

默认的 Inventory 路径 `/etc/ansible/hosts`

### /etc/ansible/hosts

```bash
[dev]
192.168.50.31

# 指定端口
[bwg]
66.112.212.1:10000
```

## 复制文件, copy 模块

```bash
sudo ansible 192.168.1.11 -m copy -a 'src=/home/roy/xxx/x.jar dest=/home/ansible/' --sudo
```

## 创建目录, file module

```bash
sudo ansible 192.168.1.11 -m file -a 'path=/home/roy/xxx/ state=directory mode=0755'

## yaml
- name: Creates directory
  file:
    path: /src/www
    state: directory
    mode: '0755'
```

## delete file

```bash
sudo ansible 192.168.1.11 -m file -a 'path=/home/roy/xxx/ state=absent'

```

### verbos

```bash
    ansible -vvvv
```

### debug

```yaml
- name: Display all variables/facts known for a host
   debug:
     msg: "archlinux init"
```

```bash
ansible -m setup host0
```

```bash
# 忽略指定的ip
ansible 'group0:!192.168.1.1' -m ping

ansible-playbook playbook.yml --start-at-task="install packages"
ansible-playbook playbook.yml --step

# 临时的 inventory file, 如果只有一个 ip, inventory host 列表结尾要要逗号.
ansible -i '192.168.1.1,' -m ping all
# 多个 ip
ansible -i '192.168.50.11,192.168.50.130' all -m ping
# 指定 ssh 端口
ansible -i '192.168.1.1:10000,' -m ping all

export ANSIBLE_ASK_SUDO_PASS=true
--extra-vars "ansible_sudo_pass=xxx"

ansible-playbook foo.yml --tags tag0 -l host0 --list-hosts

# --skip-tags

# by user
ansible 192.168.1.1 -m shell -a 'date' -u user0

# 按网段,ip段
ansible "192.168.2.1*" -a 'ls -l'
ansible "192.168.2.1?" -a 'ls -l'

#多台主机
ansible "192.168.2.11,192.168.2.12" -a 'ls -l'

#默认使用command模块
ansible 192.168.2.11 -a 'ls -l'

#使用shell模块
ansible 192.168.2.11 -m shell -a 'ls -l'

#用root权限执行
ansible --sudo -m shell 192.168.2.11 -a "/etc/init.d/AppName restart"



#fetch 模块
ansible 192.168.1.11 -m fetch -a 'src=/data/logs/xxx/debug.log dest=./' --sudo

ansible group0 -a "/etc/init.d/app0 restart" -f 10 \\重启testhosts组的所有机器,每次重启10台
```

-m后面接调用module的名字
  
-a后面接调用module的参数

-m shell 使用shell模块
  
如果不加-m 参数,默认使用command模块。
  
command比较安全有可预知性,最好用command, 需要用到shell特性的时候,再用shell。

[http://www.wiloon.com/?p=9403](http://www.wiloon.com/?p=9403)

[http://liumissyou.blog.51cto.com/4828343/1616462](http://liumissyou.blog.51cto.com/4828343/1616462)

用命令行传递参数
定义命令行变量
在release.yml文件里，hosts和user都定义为变量，需要从命令行传递变量值。

hosts: ‘{undefined{ hosts }}’
remote_user: ‘{undefined{ user }}’

tasks:

…
使用命令行变量
在命令行里面传值得的方法：
 ansible-playbook e33_var_in_command.yml --extra-vars "hosts=web user=root"

## python interpreter

[WARNING]: Platform linux on host 192.168.50.36 is using the discovered Python interpreter at /usr/bin/python3.12, but future installation of
another Python interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-
core/2.16/reference_appendices/interpreter_discovery.html for more information.

edit ansible.cfg and set auto_silent mode:

[defaults]
interpreter_python=auto_silent
