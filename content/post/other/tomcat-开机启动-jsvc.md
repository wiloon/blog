---
title: tomcat 开机启动, jsvc
author: "-"
date: 2011-11-12T06:40:44+00:00
url: /?p=1491
categories:
  - Linux
tags:
  - Tomcat

---
## tomcat 开机启动, jsvc
参考[http://tomcat.apache.org/tomcat-7.0-doc/setup.html](http://tomcat.apache.org/tomcat-7.0-doc/setup.html)的介绍，tomcat自带了jsvc工具，

需要先安装gcc, make

在tomcat的bin目录下: 

```bash
  
cd $CATALINA_HOME/bin
  
tar xvfz commons-deamon-native.tar.gz
  
cd commons-daemon-1.0.x-native-src/unix
  
./configure
  
make
  
cp jsvc ../..
  
cd ../..
  
```

设置启动脚本

在$CATALINA_HOME/bin/commons-daemon-1.0.x-native-src/unix/samples目录下有一个Tomcat7.sh文件，将其复制到/etc/init.d/m目录下并命名为tomcat:

```bash
  
sudo cp Tomcat7.sh /etc/init.d/tomcat
  
```

add following lines to the file.

```bash
  
### BEGIN INIT INFO
  
# Provides: tomcat
  
# Required-Start: $remote_fs $syslog
  
# Required-Stop: $remote_fs $syslog
  
# Default-Start: 2 3 4 5
  
# Default-Stop: 0 1 6
  
# Short-Description: Start tomcat at boot time
  
# Description: Enable service provided by tomcat.
  
### END INIT INFO
  
CATALINA_HOME=/xxx/xxx/xxx/apache-tomcat-7.0.22
  
export CATALINA_HOME
  
JAVA_HOME=/opt/jvm/jdk1.7.0
  
export JAVA_HOME
  
```

修改运行级别

```bash
  
update-rc.d tomcat defaults
  
```

创建用户:

```bash
  
groupadd tomcat
  
useradd -s /sbin/nologin -g tomcat tomcat
  
```