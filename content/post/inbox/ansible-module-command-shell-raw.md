---
title: ansible module
author: "-"
date: 2016-11-18T06:28:45+00:00
url: ansible/module
categories:
  - Inbox
tags:
  - reprint
---
## ansible module

## systemd

```yml
   - name: restart telegraf
      systemd:
        state: restarted
        daemon_reload: yes
        name: telegraf

```

## shell

ansible-playbook显示执行shell的模块的返回结果

```yaml
    - name: who am i
      shell: "whoami"
      register: shell_result
    - debug:
        var: shell_result.stdout_lines

```

### local_action

local_action 需要sudo密码

```bash
export ANSIBLE_ASK_SUDO_PASS=true
--extra-vars "ansible_sudo_pass=xxx"
```

```yml
- name: "Create an empty directory (locally)"
  local_action:
    module: file
    path: "/tmp/empty"
    state: directory
  tags: tag0

```

### 批量删除文件

```yml
  - name: Ansible delete file glob
    find:
      paths: /etc/Ansible
      patterns: *.txt
    register: files_to_delete

  - name: Ansible remove file glob
    file:
      path: "{{ item.path }}"
      state: absent
    with_items: "{{ files_to_delete.files }}"
```

### lineinfile

用于改变一个文件的一行。如果想要改变文件中相似的多行,可以使用 replace模块

```bash
ansible 192.168.x.x -m lineinfile -a "path=/etc/ssh/sshd_config line='xxx' state=present"
ansible 192.168.x.x -m lineinfile -a 'path="/etc/filebeat/filebeat.yml" regexp="10\.xx\.0\.xx" line="  hosts: [\"xx.xx.0.xx:6379\"]"'
```

<http://www.jianshu.com/p/f400f600b17c>

这篇总结一下Inventory,变量,目标匹配,及/usr/bin/ansible 命令行常用的模块

上一篇也说过Inventory的默认路径是在/etc/ansible/hosts,当然这个东西可以说是静态的,为啥是静态呢,你要手工的把你的要管理的主机写进去。

当然还有一种动态的Inventory,这个其实也简单,就是如果你已经有了一个资源管理系统,里面有你们的所有主机信息。然后咱们写个脚本程序,把你们资源管理系统里面的这些信息给拉过来,以json格式呈现就OK了。

其实ansible还有一种管理主机的方法,我们随便把主机定义到一个文件里,然后

用ansible或ansible-playbook的 -i参数去调用就OK了。不过这个要建立个目录结构,后面写playbook的时候再总结一下。

静态 Inventory

lixc@ansible:~$ cat -n /etc/ansible/hosts
  
1 [alltest:children]
  
2 salt
  
3 leihuo
  
5 [salt]
  
6 salt-master  ansible_ssh_user=lixc ansible_ssh_pass=123456
  
7 10.240.162.112  ansible_connection=paramiko
  
9 [leihuo]
  
10  lixc ansible_ssh_host=192.168.131.203 ansible_ssh_port=21100
  
11  10.240.162.11[1:9]:22
  
楼主这个简单的小例子,第1行,alltest这个组包含俩子组分别是下面的salt,和leihuo

第6行可以设置主机的默认连接用户,及密码

第7行可以设置ssh的连接方式,默认是openssh,我这里用paramiko,不用官网推荐用openssh,因为paramiko查询key的时候,很耗时,效率不高。

第10行,可以给主机随便取个别名,这里的"lixc"就是一个别名,如果ssh默认端口不是22,这里可以

指定特定的端口

指定ssh端口也可以像第11行,这么指定。

不过以上两种指定ssh端口方法,只针对我们有少部分的主机是特殊端口,如果我们所以主机都是指定的端口,不可能每个主机都这么弄一下吧。

配置文件里有个选项,改成我们需要的端口就OK了,修改后对全局有效

lixc@ansible:~$ grep "remote_port" /etc/ansible/ansible.cfg
  
remote_port    = 22
  
第7行和11行,是俩相同的主机,说明同一主机可以在不同的组中。在现实当中就像我一台服务器即可以装MySQL也可以装apache是一个道理。
  
OK,静态Inventory搞完了,再搞搞吧,变量吧。

ansible的变量主要是给后面的playbook使用的。

分为主机变量和组变量两种类型。

看个例子

lixc@ansible:~$ cat -n /etc/ansible/hosts
  
1 [alltest:children]
  
2 salt
  
3 leihuo
  
5 [salt]
  
6 salt-master  salt-port=4505 MySQL-port=3306
  
7 10.240.162.112  salt-path=/usr/bin/salt-call
  
9 [leihuo]
  
10  lixc ansible_ssh_host=192.168.131.203 ansible_ssh_port=21100
  
11  10.240.162.11[1:9]:22
  
12  [alltest:vars]
  
13  ls-path=/bin/ls
  
14  liss=lisisi
  
6,7行设置主机变量
  
12-14行,设置的为alltest这个组的变量。组变量就是,我这个组的成员都可以用

当然我们也可以不在/etc/ansible/hosts里面定义变量,也可以把变量写进单独的文件里,不过变量定义的形式就不是谁=谁,这么个形式了。而是遵循yaml语法的key: value的形式。

我们把上面定义的变量写进文件。

lixc@ansible:~$ for dir in {host_vars,group_vars};do ls /etc/ansible/${dir};done
  
10.240.162.112  salt-master
  
alltest
  
看一下文件定义的格式

## lixc@ansible:~$ cat /etc/ansible/host_vars/salt-master

salt-port: 4505
  
MySQL-port: 3306
  
下面总结下,ansible的patterns,ansible目标的匹配相对来说还是比较简单,单一的,不像salt很强大,grains,pillar,正则等等都可以用来匹配目标。
  
基本格式:

ansible <pattern_goes_here> -m <module_name> -a
  
匹配所有主机

*或者all

匹配多个组

salt:leihuo

在salt这个组里,但不能在leihuo这个组里的主机

salt:!leihuo
  
取两个组的交集

salt:&leihuo

排除某一主机

ansible-playbook site.yaml -limit salt-msater

当然也可以用正则,在/etc/ansible/hosts里面去定义。如

~salt(master|minion)&#46;li*&#46;com
  
OK,搞得好像流水帐一样,好吧,下面搞搞ansible的命令行模块吧

先说说啥时候用命令行吧,用这种东西的时候,一般是咱们临时的去做一些个小事情,可能这次做了,下次就再也不弄了。就用这种方式。。。如果要去干大型或需要经常重复使用的活儿,就用play-book吧
  
多了也不说了,直接抄官网的例子了。

好,先来聊聊命令行三剑客,command,shell,raw

ansible命令行,默认使用的模块就是command了。

lixc@ansible:~$ grep  -n "module_name" /etc/ansible/ansible.cfg
  
59:#module_name = command
  
lixc@ansible:~$ ansible salt  -a 'ls /tmp'
  
10.240.162.112 | success | rc=0 >>
  
aptitude-root.6058:d5Ogyd
  
test.log

salt-master | success | rc=0 >>

lixc@ansible:~$
  
看到了吧,我们如果不加-m 参数的话,默认使用的就是command模块了。
  
OK,其实command模块,我们平时使用的命令,都可以在-a参数后面加上去执行了。但是,command模块执行命令,和我们平时在真实机器上,/bin/sh环境下执行命令还是有所区别的。

啥区别呢？区别是,command不能用shell的一些特性,看下面这个例子,大伙就知道了。

lixc@ansible:~$ ansible salt-master  -a 'ls /tmp/_'
  
salt-master | FAILED | rc=2 >>
  
ls: cannot access /tmp/_: No such file or directory
  
看到了吧,command弄不了shell中的*,那有谁可以弄？shell这个模块可以,看个例子

lixc@ansible:~$ ansible salt -m shell -a 'ls /tmp/*' -s
  
salt-master | success | rc=0 >>
  
/tmp/test
  
看到了吧。哈哈,其实command能干的活,shell都可以干,那要这个command模块还是啥用呢？

官方上说,command用起来更安全,更有可预知性。建议俺们,不到万不得已,还是不要用shell模块滴好。

在这里楼主还有一个疑问。官网上说,command使用不了nodes上的环境变量,但是楼主测了下,居然可以用,难不成是官方文档太老了,没来得及更新？

lixc@ansible:~$ ansible salt-master -m shell -a 'echo $HOME'
  
salt-master | success | rc=0 >>
  
/home/lixc

lixc@ansible:~$ ansible salt-master  -a 'echo $HOME'
  
salt-master | success | rc=0 >>
  
/home/lixc
  
OK,两位剑客都介绍完了,怎么少的了第三位大侠呢？

raw这东西,咋用的呢,其实前面说的command,shell能干的活,raw都能干。

大伙都知道ansible运行的环境是管理机上装ansible,但是客户机上是要装python的。

raw最拿手的好活,就是,如果你有的机器是没有装python,或者说你的是python2.4以下,木有装python-simplejson的,用它可以装python,装python-simplejson。

raw还有一个拿手好戏,就是你的有些机器压根就装不了python,OK,不用装了,直接用raw吧,也可以玩ansible

看个例子。

lixc@ansible:~$ ansible  10.240.162.250 -a 'ls /tmp/' -u root -k
  
SSH password:
  
10.240.162.250 | FAILED >> {
  
"failed": true,
  
"msg": "/bin/sh: /usr/bin/python: not found\r\n",
  
"parsed": false
  
}

lixc@ansible:~$ ansible  10.240.162.250 -m shell -a 'ls /tmp/*' -u root -k
  
SSH password:
  
10.240.162.250 | FAILED >> {
  
"failed": true,
  
"msg": "/bin/sh: /usr/bin/python: not found\r\n",
  
"parsed": false
  
}

lixc@ansible:~$ ansible  10.240.162.250 -m raw -a 'ls /tmp/*' -u root -k
  
SSH password:
  
10.240.162.250 | success | rc=0 >>
  
/tmp/test
  
看到了吧,我新装了一台debian的机器,里面没装python,command和shell模块都不能用了,raw照样OK。现在咱们把python给装上。

lixc@ansible:~$ ansible  10.240.162.250 -m raw -a 'aptitude -y install python' -u root -k >/dev/null
  
SSH password:
  
lixc@ansible:~$
  
python装好了,下面咱们看看还能玩command和shell吗？

lixc@ansible:~$ ansible  10.240.162.112  -a 'ls /tmp/' -u root -k
  
SSH password:
  
10.240.162.112 | success | rc=0 >>
  
test

lixc@ansible:~$ ansible  10.240.162.112 -m shell -a 'ls /tmp/' -u root -k
  
SSH password:
  
10.240.162.112 | success | rc=0 >>
  
test
  
OK,可以完了。现在问题又出来了,既然raw这么猛,那还有command和shell有个毛用？

答案还是官网上的一句话,

人家command比较安全有可预知性,所以我们平时用的时候,最好用command。

需要用到shell特性的时候,再去去shell。

如果客户机上没装python,或者python-simplejson,那咱们就用raw把python或python-simplejson给装上,然后就别用了,回过头用command和shell

如果,你的机器实在装不了python就用raw吧,不过装不了python大多数指的就是路由器交换机了。
  
OK,三剑客聊完了。

看看文件管理吧
  
拷贝个文件,拷贝之前要备份,并修改文件到指定的属性。

lixc@ansible:~$ ansible salt-master -m copy -a 'src=/etc/sudoers dest=/etc/sudoers owner=root group=root mode=440 backup=yes' -s
  
salt-master | success >> {
  
"changed": false,
  
"dest": "/etc/sudoers",
  
"gid": 0,
  
"group": "root",
  
"md5sum": "5f82d8684e43943bec2f07c0d1823352",
  
"mode": "0440",
  
"owner": "root",
  
"path": "/etc/sudoers",
  
"size": 1742,
  
"state": "file",
  
"uid": 0
  
}
  
OK,查看一下是不是按照要求来的

lixc@ansible:~$ ansible salt-master -m shell -a 'ls -l /etc/sudoers*'
  
salt-master | success | rc=0 >>
  
-r-r-- 1 root root 1742 Jun 27 15:04 /etc/sudoers
  
-r-r-- 1 root root  700 Jun 26 16:09 /etc/sudoers.2014-06-27@15:04~
  
是对的,下面看看咋样修改文件属性,创建文件吧

先弄个连接文件

lixc@ansible:~$ ansible  salt-master -m file -a 'src=/etc/sudoers  dest=/tmp/sudoers mode=440 owner=lixc group=lixc state=link'
  
salt-master | success >> {
  
"changed": false,
  
"dest": "/tmp/sudoers",
  
"gid": 1000,
  
"group": "lixc",
  
"mode": "0777",
  
"owner": "lixc",
  
"size": 12,
  
"src": "/etc/sudoers",
  
"state": "link",
  
"uid": 1000
  
}

lixc@ansible:~$ ansible salt-master -m shell -a 'ls -l /tmp/sudoers'
  
salt-master | success | rc=0 >>
  
lrwxrwxrwx 1 lixc lixc 12 Jun 27 15:15 /tmp/sudoers -> /etc/sudoers
  
创建个文件

lixc@ansible:~$ ansible salt-master -m file -a 'dest=/tmp/lixc.log  owner=lixc group=lixc mode=644 state=touch'
  
salt-master | success >> {
  
"changed": true,
  
"dest": "/tmp/lixc.log",
  
"gid": 1000,
  
"group": "lixc",
  
"mode": "0644",
  
"owner": "lixc",
  
"size": 0,
  
"state": "file",
  
"uid": 1000
  
}

lixc@ansible:~$ ansible salt-master -m shell -a 'ls -l /tmp/lixc.log'
  
salt-master | success | rc=0 >>
  
-rw-r-r- 1 lixc lixc 0 Jun 27 15:19 /tmp/lixc.log
  
递归创建个文件夹

lixc@ansible:~$ ansible salt-master -m file -a 'dest=/tmp/a/b/c  owner=lixc group=lixc mode=755 state=directory'
  
salt-master | success >> {
  
"changed": true,
  
"gid": 1000,
  
"group": "lixc",
  
"mode": "0755",
  
"owner": "lixc",
  
"path": "/tmp/a/b/c",
  
"size": 4096,
  
"state": "directory",
  
"uid": 1000
  
}
  
查看一下结果,

lixc@ansible:~$ ansible salt-master  -a 'tree /tmp/a'
  
salt-master | success | rc=0 >>
  
/tmp/a
  
`-- b`- c
  
删除刚才那个文件夹

lixc@ansible:~$ ansible salt-master -m file -a 'dest=/tmp/a/   state=absent'
  
salt-master | success >> {
  
"changed": true,
  
"path": "/tmp/a/",
  
"state": "absent"
  
}
  
查看一下结果

lixc@ansible:~$ ansible salt-master  -a 'tree /tmp/a'
  
salt-master | success | rc=0 >>
  
/tmp/a [error opening dir]
  
接下来装个MySQL吧,顺便玩玩搞包管理,用户管理,服务管理这些东西。

OK,先建立个MySQL用户吧

lixc@ansible:~$ ansible salt-master -m user -a 'name=MySQL shell=/sbin/nologin createhome=no' -s
  
salt-master | success >> {
  
"changed": true,
  
"comment": "",
  
"createhome": false,
  
"group": 1002,
  
"home": "/home/MySQL",
  
"name": "MySQL",
  
"shell": "/sbin/nologin",
  
"state": "present",
  
"system": false,
  
"uid": 1002
  
}
  
好,安装MySQL

lixc@ansible:~$ ansible salt-master -m apt -a 'name=MySQL-server state=installed' -s  >/dev/null
  
lixc@ansible:~$
  
好,配置/etc/MySQL归MySQL用户使用

lixc@ansible:~$ ansible salt-master -m file -a 'dest=/etc/MySQL mode=644 owner=MySQL group=MySQL' -s
  
salt-master | success >> {
  
"changed": true,
  
"gid": 1002,
  
"group": "MySQL",
  
"mode": "0644",
  
"owner": "MySQL",
  
"path": "/etc/MySQL",
  
"size": 4096,
  
"state": "directory",
  
"uid": 1002
  
}
  
启动MySQL服务

lixc@ansible:~$ ansible salt-master -m service -a 'name=MySQL state=started' -s
  
salt-master | success >> {
  
"changed": false,
  
"name": "MySQL",
  
"state": "started"
  
}
  
OK,安装好,再走一遍删除的流程吧

停止服务

lixc@ansible:~$ ansible salt-master -m service -a 'name=MySQL state=stopped' -s
  
salt-master | success >> {
  
"changed": true,
  
"name": "MySQL",
  
"state": "stopped"
  
}
  
删除MySQL

lixc@ansible:~$ ansible salt-master -m apt -a 'name=MySQL-server state=absent' -s >/dev/null
  
lixc@ansible:~$
  
删除MySQL用户

lixc@ansible:~$ ansible salt-master -m user -a 'name=MySQL state=absent' -s
  
salt-master | success >> {
  
"changed": true,
  
"force": false,
  
"name": "MySQL",
  
"remove": false,
  
"state": "absent"
  
}
  
OK,完成了,过程都是瞎掰的,主要是想测测ansible的功能的。

还有一个后台执行的功能。-B 30是设置后台执行时间为30秒,-P2是没两秒钟报告一次状态,这个当你的任务要执行很长时间的时候可以用。

lixc@ansible:~$ ansible salt-master -m apt -a 'name=apache2 state=installed' -s -B 30 -P2 >>/dev/null
  
一叶浮萍归大海,人生何处不相逢,该聊到ansible的facts了,这东西就和salt里面的grains一个样。

直接看看,输出的东西太多了,就不在这里显示了

lixc@ansible:~$ ansible salt-master -m setup >/dev/null
  
lixc@ansible:~$

原创作品,允许转载,转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。<http://lixcto.blog.51cto.com/4834175/1431659>
