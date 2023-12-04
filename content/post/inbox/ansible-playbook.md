---
title: ansible playbook
author: "-"
date: 2017-08-09T01:22:30+00:00
url: /?p=11019
categories:
  - Inbox
tags:
  - reprint
---
## ansible playbook

end play

```yaml
    - block:
        - name: "check if end play"
          debug:
            msg: "end play"
        - meta: end_play
      when: "true"
```

```bash
---                         #任何playbook文件(其实就是yaml文件)都要以这个开头
- hosts: '{{ hosts }}'      #可以是主机组或IP
  become: root
  gather_facts: true
  vars:                     #为该play定义两个变量
    http_port: 80
    max_clients: 200
  tasks:                      #开始定义task
    - name: debug0
      debug:
        msg: "vps init, dist: {{ ansible_distribution }}"
    - name: Empty remote directory
      synchronize:
        src: "{{source_path}}/empty/"
        dest: "{{ tomcat_path }}/tomcat/webapps/ROOT"
        delete: yes
        recursive: yes

    - name: start monit and app
      service:
        name: monit
        state: restarted

    -name: shell command
     shell: systemctl restart sshd   # shell

   - name: download rpm
      get_url:                       #download
    url: https://dl.influxdata.com/influxdb/releases/influxdb-1.4.2.x86_64.rpm
    dest: /tmp/influxdb-1.4.2.x86_64.rpm

# file, mode, chmod
- name: file mode
  file:
  path:/path/to/file
  mode:u+rwx

# yum module
- name: ensure apache is at the latest version            #这既是每个task的说明也是每个task的名字
  yum: pkg=httpd state=latest    
  tags:         #给该task打一个标签
      - last_http

# template
  - name: write the apache config file
    template: src=/srv/httpd.j2 dest=/etc/httpd.conf
    notify:       #提供watch功能,这里当apache配置文件改变时,就调用handlers中名为"restart apache"的task
    - restart apache

# service module
  - name: ensure apache is running
    service: name=httpd state=started
  handlers:       #notify通知这里的task执行,谨记: 定义在handlers下的task只有在notify触发的时候才会执行
    - name: restart apache
      service: name=httpd state=restarted
    - name: modify monit config file
      replace:
      path: /etc/monit.d/xxx.conf
      regexp: '(.*)project_name(.*)'
      replace: '\1{{project_name}}\2'
      backup: yes

    - name: config filebeat sysV startup
      shell: chkconfig --add filebeat
      when: ansible_distribution == 'CentOS' and ansible_distribution_major_version == "6"

```

ansible playbook 传参数

```bash
ansible-playbook foo.yml -e h=192.168.0.2

# 传多个参数时, 参数列表加引号, 参数之前用空格分隔,
ansible-playbook foo.yml -e "host=192.168.0.2 app=foo"
```

ansible的playbook就如同salt的state,一个playbook就是一个YAML文件,所以playbook文件一般都以.yml结尾,写playbook不需要复杂的YAML语法,所以也不用单独去学YAML语法。此外playbook和模板文件 (template模块) 还使用jinja2语法语法实现高级功能 (后面逐一讲到) ,不光这里,jinja2语法很多地方都会用到,比如python大部分web框架的模板系统,所以可以去单独学一下。
  
一个playbook文件由一个或多个play组成,每个play定义了在一个或多个远程主机上执行的一系列的task,其中每个task一般就是调用一个ansible的模块,如调用copy模块复制文件到远程主机或调用shell模块执行命令。

```bash
#指定host
# file: user.yml  (playbook)
---
- hosts: '{{ target }}'
  user: ...

ansible-playbook user.yml --extra-vars "target=imac-2.local"
```

定义变量 - 列表

```
- hosts: localhost
  become: true
  vars:
    app_list:
      - - htop
        - emacs
        - vim
```

```bash
ansible-playbook /etc/ansible/xxx.yml --limit 192.168.xxx.xxx --tags "tag0,tag1" --list-hosts --list-tasks
--skip-tags
--start-at-task
--step # one-step-at-a-time: confirm each task before running
```

>[http://sapser.github.io/ansible/2014/07/21/ansible-playbook](http://sapser.github.io/ansible/2014/07/21/ansible-playbook)
>[https://stackoverflow.com/questions/18195142/safely-limiting-ansible-playbooks-to-a-single-machine](https://stackoverflow.com/questions/18195142/safely-limiting-ansible-playbooks-to-a-single-machine)
>[http://liuzhengwei521.blog.51cto.com/4855442/1962382](http://liuzhengwei521.blog.51cto.com/4855442/1962382)
