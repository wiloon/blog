---
title: ansible command
author: wiloon
type: post
date: 2016-05-13T12:00:27+00:00
url: /?p=8981
categories:
  - Uncategorized

---
### verbos

```bashansible -vvvv
```

### debug

<pre><code class="language-yml line-numbers">    - name: Display all variables/facts known for a host
      debug:
        msg: "archlinux init"
```

```bashansible -m setup host0
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

# 按网段，ip段
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

ansible group0 -a "/etc/init.d/app0 restart" -f 10 \\重启testhosts组的所有机器，每次重启10台
```

-m后面接调用module的名字
  
-a后面接调用module的参数

-m shell 使用shell模块
  
如果不加-m 参数，默认使用command模块。
  
command比较安全有可预知性，最好用command， 需要用到shell特性的时候，再用shell。

# http://www.wiloon.com/wordpress/?p=9403

http://liumissyou.blog.51cto.com/4828343/1616462