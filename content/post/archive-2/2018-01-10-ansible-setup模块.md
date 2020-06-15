---
title: Ansible setup模块
author: wiloon
type: post
date: 2018-01-10T09:46:37+00:00
url: /?p=11704
categories:
  - Uncategorized

---
https://www.ipcpu.com/2016/01/ansible-setup-when/

Ansible入门setup模块和条件判断
   
Linux ipcpu 2年前 (2016-01-11) 5963浏览
  
Ansible入门setup模块和条件判断.md

一、setup模块
  
setup模块用于收集远程主机的一些基本信息。
  
而在playbook中，默认参数”gather_facts: True”的含义就是在远程主机运行setup模块，并将收集的信息记录起来。

这样在后面的playbook里面可以调用并进行一些判断和对照。

使用方法如下：

[root@ansible test]$ansible all -m setup |more
  
211.127.129.182 | success >> {
      
"ansible_facts&#8221;: {
          
"ansible\_all\_ipv4_addresses&#8221;: [
              
"211.127.129.182&#8221;
          
],
          
"ansible\_all\_ipv6_addresses&#8221;: [],
          
"ansible\_architecture&#8221;: "x86\_64&#8221;,
          
"ansible\_bios\_date&#8221;: "09/21/2014&#8221;,
          
"ansible\_bios\_version&#8221;: "6.00&#8221;,
          
"ansible_cmdline&#8221;: {
              
"KEYBOARDTYPE&#8221;: "pc&#8221;,
              
"KEYTABLE&#8221;: "us&#8221;,
              
"LANG&#8221;: "en_US.UTF-8&#8221;,
  
OUTPUT OMITTED.
  
因显示篇幅过长，这列只列举一些常用项目

"ansible\_all\_ipv4_addresses&#8221;: [
              
"211.97.148.137&#8221;,
              
"10.6.7.24&#8221;
          
],
  
#@这里列出了所有IPv4地址
  
"ansible\_architecture&#8221;: "x86\_64&#8221;,
  
#@操作系统架构
  
"ansible_distribution&#8221;: "RedHat&#8221;,
  
"ansible\_distribution\_major_version&#8221;: "5&#8221;,
  
"ansible\_distribution\_release&#8221;: "Tikanga&#8221;,
  
"ansible\_distribution\_version&#8221;: "5.8&#8221;,
  
#@操作系统版本信息
  
"ansible_eth0&#8221;: {
              
"active&#8221;: true,
              
"device&#8221;: "eth0&#8221;,
              
"ipv4&#8221;: {
                  
"address&#8221;: "10.6.7.24&#8221;,
                  
"netmask&#8221;: "255.255.255.0&#8221;,
                  
"network&#8221;: "10.6.7.0&#8221;
              
},
              
"macaddress&#8221;: "52:54:00:89:ba:15&#8221;,
  
#@网卡eth0的信息
  
"ansible_kernel&#8221;: "2.6.18-308.el5&#8221;,
  
#@内核版本
  
如果使用ansible操作不同的操作系统例如Redhat和Debian，使用前需要对照好相关的输出项，找出不同的地方和相同的地方才能准确使用。

二、条件判断
  
现在有这样一个需求，生产环境现在有Redhat 5 和CentOS 6 两种操作系统环境，都需要在syslog配置文件添加一个远程syslog服务器，并且添加完成后重启服务器。

所以我们收集了两个操作系统相关的参数如下：

"ansible_distribution&#8221;: "RedHat&#8221;,
  
"ansible\_distribution\_major_version&#8221;: "5&#8221;,
  
"ansible\_distribution\_release&#8221;: "Tikanga&#8221;,
  
"ansible\_distribution\_version&#8221;: "5.8&#8221;,
  
"ansible\_os\_family&#8221;: "RedHat&#8221;,
  
"ansible_distribution&#8221;: "CentOS&#8221;,
  
"ansible\_distribution\_major_version&#8221;: "6&#8221;,
  
"ansible\_distribution\_release&#8221;: "Final&#8221;,
  
"ansible\_distribution\_version&#8221;: "6.4&#8221;,
  
"ansible\_os\_family&#8221;: "RedHat&#8221;,
  
接下来我们就可以编写playbook

* * *

  * hosts: webserver
  
    vars:
  
    logserver: 10.127.2.170
  
    gather_facts: True
  
    tasks: 
      * name: add conf to config files to CentOS6
  
        lineinfile: dest=/etc/rsyslog.conf line=&#8221;_._ @{{ logserver }}&#8221;
  
        when: ansible\_distribution == &#8216;CentOS&#8217; and ansible\_distribution\_major\_version == "6&#8221;
      * name: restart syslog @CentOS6
  
        when: ansible\_distribution == &#8216;CentOS&#8217; and ansible\_distribution\_major\_version == "6&#8221;
  
        service: name=rsyslog state=restarted
      * name: add conf to config files to RedHat 5
  
        lineinfile: dest=/etc/syslog.conf line=&#8221;_._ @{{ logserver }}&#8221;
  
        when: ansible\_distribution == &#8216;RedHat&#8217; and ansible\_distribution\_major\_version == "5&#8221;
      * name: restart syslog @RedHat 5
  
        when: ansible\_distribution == &#8216;RedHat&#8217; and ansible\_distribution\_major\_version == "5&#8221;
  
        service: name=syslog state=restarted
  
        在这里我们进行了操作系统的判断，如果是CentOS 6 则修改rsyslog.conf并重启rsyslog服务。
  
        如果是RedHat 5 则修改syslog.conf，并重启syslog服务。

在修改文件时采用了lineinfile模块，只要文件中有语句存在，下次运行就不会改变，所以playbook可以多次运行。

一点疑惑
  
有同学要问，为什么要进行四次when判断，两次不就够了，写成这样

  * name: restart syslog @CentOS6
  
    when: ansible\_distribution == &#8216;CentOS&#8217; and ansible\_distribution\_major\_version == "6&#8221;
  
    lineinfile: dest=/etc/rsyslog.conf line=&#8221;_._ @{{ logserver }}&#8221;
  
    service: name=rsyslog state=restarted
  
    这是不行的，ansible要求每一个play里面智能使用一个模块，使用多个会报错
  
    ERROR: multiple actions specified in task

参考资料
  
http://sapser.github.io/ansible/2014/07/21/ansible-conditionals/

转载请注明：IPCPU&#8211;网络之路 » Ansible入门setup模块和条件判断