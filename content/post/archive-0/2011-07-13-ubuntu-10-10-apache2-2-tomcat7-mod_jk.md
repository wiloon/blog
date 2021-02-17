---
title: 'debian apache  tomcat jk'
author: w1100n
type: post
date: 2011-07-13T14:20:38+00:00
url: /?p=356
bot_views:
  - 25
views:
  - 4
categories:
  - Linux
tags:
  - Tomcat

---
install apache

```bash
  
apt-get install apache2
  
```

download and install tomcat

#enable jk

[bash]
  
sudo a2enmod
  
[/bash]

#then type
  
jk

\# if no jk,

[bash]
  
sudo apt-get install libapache2-mod-jk
  
[/bash]

2. edit file jk.load

[bash]
  
sudo emacs /etc/apache2/mods-enabled/jk.load
  
[/bash]

#Add the following lines

[bash]
  
LoadModule jk_module /usr/lib/apache2/modules/mod_jk.so

JkWorkersFile /etc/apache2/workers.properties
  
JkLogFile /var/log/apache2/mod_jk.log
  
JkLogLevel debug
  
JkLogStampFormat "[%a %b %d %H:%M:%S %Y] "

JkMount /xxx worker1
  
JkMount /xxx/* worker1
  
JkMountCopy All
  
[/bash]

#如果在这里设置了JkMountCopy All，在httpd的VirtualHost中就不用设置JkMountCopy On了
  
-
  
Note: replace "xxx" with your app name/path in tomcat

3. create workers file

[bash]
  
sudo emacs /etc/apache2/workers.properties
  
[/bash]

\# Then write following lines

[bash]
  
workers.tomcat_home=/xxx/xxx/apache-tomcat-7.0.xx
  
workers.java_home=/xxx/xx/jvm/jdk1.6.0_25
  
ps=/
  
worker.list=worker1
  
worker.worker1.port=8009
  
worker.worker1.host=localhost
  
worker.worker1.type=ajp13
  
worker.worker1.lbfactor=1
  
[/bash]

Ok set up is done. Now try whether everything is ok.
  
restart all server.
  
#restart apache
  
#restart tomcat

\# Then access to the page with your browser

[bash]
  
http://www.xxx.com/xxx/
  
[/bash]

新版本apache配置
  
编辑jk.conf
  
配置worker:
  
JkWorkersFile /etc/apache2/workers.properties
  
配置
  
JkMount /xxx worker1
  
JkMount /xxx/* worker1
  
JkMountCopy All