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

## install
### Installing Ansible on Ubuntu

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```
## ansible 配置文件

    /etc/ansible/ansible.cfg

### 文件内容

```bash
[defaults]
interpreter_python = auto_legacy_silent
# gather 超时时间
gather_timeout=30

```
### hibernate

    ansible -i '192.168.97.1,' all  -m shell -a 'sudo systemctl hibernate'  -u user0

### verbos

    ansible -vvvv

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

ansible -i '192.168.1.1,' -m ping all

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

#copy 模块
sudo ansible 192.168.1.11 -m copy -a 'src=/home/roy/xxx/x.jar dest=/home/ansible/' --sudo

#fetch 模块
ansible 192.168.1.11 -m fetch -a 'src=/data/logs/xxx/debug.log dest=./' --sudo

ansible group0 -a "/etc/init.d/app0 restart" -f 10 \\重启testhosts组的所有机器,每次重启10台
```

-m后面接调用module的名字
  
-a后面接调用module的参数

-m shell 使用shell模块
  
如果不加-m 参数,默认使用command模块。
  
command比较安全有可预知性,最好用command, 需要用到shell特性的时候,再用shell。

<http://www.wiloon.com/?p=9403>

http://liumissyou.blog.51cto.com/4828343/1616462

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

 