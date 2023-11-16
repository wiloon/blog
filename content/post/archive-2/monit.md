---
title: monit
author: "-"
date: 2017-11-27T05:01:35+00:00
url: /?p=11514
categories:
  - Inbox
tags:
  - reprint
---
## monit
监控进程
  
发表于2015-02-11
  
有时候,进程突然终止服务,可能是没有资源了,也可能是意外,比如说: 因为 OOM 被杀；或者由于 BUG 导致崩溃；亦或者误操作等等,此时,我们需要重新启动进程。

实际上,Linux 本身的初始化系统能实现简单的功能,无论是老牌的 SysVinit,还是新潮的 Upstart 或者 Systemd 均可,但它们并不适合处理一些复杂的情况,比如说: CPU 占用超过多少就重启；或者同时管理 100 个 PHP 实现的 Worker 进程等等,如果你有类似的需求,那么可以考虑试试 Monit 和 Supervisor,相信会有不一样的感受。

让我们看看 Monit 的用法,假设我们要监控 Nginx 进程,一旦其 CPU 使用率连续 5 次轮询周期里均超过 50% 的话,就重启进程,此时就可以按照如下方式设置: 

check process nginx with pidfile /var/run/nginx.pid
      
start program = "/etc/init.d/nginx start"
      
stop program = "/etc/init.d/nginx stop"
      
if cpu is greater than 50% for 5 cycles then restart

monit -t # 配置文件检测
  
monit # 启动monit daemon
  
monit -c /var/monit/monitrc # 启动monit daemon时指定配置文件
  
monit reload # 当更新了配置文件需要重载
  
monit status # 查看所有服务状态
  
monit status nginx # 查看nginx服务状态
  
monit stop all # 停止所有服务
  
monit stop nginx # 停止nginx服务
  
monit start all # 启动所有服务
  
monit start nginx # 启动nginx服务
  
monit -V # 查看版本

```bash
# install monit
pacman -S monit

Install EPEL Repository
yum install monit

# edit config file
emacs /etc/monitrc
# and uncomment line include /etc/monit.d/*

#create monit conifg file
emacs /etc/monit.d/foo

#add following lines

#check process projectFoo matching projectFoo
#      start program "/usr/bin/systemctl start projectFoo.service"
#      if failed port 8081 protocol ssh then restart
#      if 5 restarts within 5 cycles then timeout

echo "check host tomcat with address localhost
 stop program = "/etc/init.d/tomcat stop"
 start program = "/etc/init.d/tomcat restart"
 if failed port 8080 and protocol http
 then start
" > /etc/monit.d/tomcat 
/etc/init.d/monit restart

#reload monit conifg or restart monit
```

### 官网

[https://mmonit.com/](https://mmonit.com/)

https://blog.huoding.com/2015/02/11/419
  
https://linux.cn/article-5542-2.html
  
https://wiki.archlinux.org/index.php/Monit
  
https://mmonit.com/monit/documentation/monit.html#NAME


  
    Setting up Monit + with tomcat
  


https://blog.rimuhosting.com/2011/01/27/setting-up-monit-with-tomcat/embed/#?secret=8QoE16qN7b