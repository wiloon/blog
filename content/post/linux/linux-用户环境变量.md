---
title: 环境变量
author: "-"
date: 2011-07-18T04:58:48+00:00
url: /?p=360
categories:
  - Linux
tags:
  - reprint
---
## 环境变量
#####################################################

.bashrc文件
  
这种方法可以把使用这些环境变量的权限控制到用户级别，如果你需要给某个用户权限使用这些环境变量，你只需要修改其个人用户主目录下的.bashrc文件就可以了。
  
(1)用文本编辑器打开用户目录下的.bashrc文件
  
(2)在.bashrc文件末尾加入: 

JAVA_HOME=/usr/share/jdk1.5.0_05
  
export JAVA_HOME
  
PATH=$JAVA_HOME/bin:$PATH
  
export PATH
  
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
  
export CLASSPATH
  
#重新加载
  
source .bashrc

##########################################################

/etc/profile文件
  
所有用户的shell都有权使用这些环境变量，可能会给系统带来安全性问题。
  
(1)用文本编辑器打开/etc/profile
  
(2)在profile文件末尾加入: 
  
JAVA_HOME=/usr/share/jdk1.5.0_05
  
PATH=$JAVA_HOME/bin:$PATH
  
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
  
export JAVA_HOME
  
export PATH
  
export CLASSPATH
  
#使环境变量生效
  
source /etc/profile

a. 要将 /usr/share/jdk1.5.0_05jdk 改为你的jdk安装目录
  
b. linux下用冒号":"来分隔路径
  
c. $PATH / $CLASSPATH / $JAVA_HOME 是用来引用原来的环境变量的值,在设置环境变量时特别要注意不能把原来的值给覆盖掉了，这是一种常见的错误。
  
d. CLASSPATH中当前目录"."不能丢,把当前目录丢掉也是常见的错误。
  
e. export是把这三个变量导出为全局变量。
  
f. 大小写必须严格区分。

#############################################################

直接在shell下设置变量
  
不赞成使用这种方法，因为换个shell，你的设置就无效了，因此这种方法仅仅是临时使用，以后要使用的时候又要重新设置，比较麻烦。
  
只需在shell终端执行下列命令: 
  
export JAVA_HOME=/usr/share/jdk1.5.0_05
  
export PATH=$JAVA_HOME/bin:$PATH
  
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

－－－
  
摘自IBM官方网站，原文地址: http://publib.boulder.ibm.com/infocenter/pseries/v5r3/index.jsp?topic=/com.ibm.aix.baseadmn/doc/baseadmndita/etc_env_file.htm

The /etc/environment, /etc/profile, and .profile files are run once at login time. The .env file, on the other hand, is run every time you open a new shell or a window.

* /etc/environment file
  
The first file that the operating system uses at login time is the /etc/environment file. The /etc/environment file contains variables specifying the basic environment for all processes.
  
* /etc/profile file
  
The second file that the operating system uses at login time is the /etc/profile file.
  
* .profile file
  
The .profile file is present in your home ($HOME) directory and lets you customize your individual working environment.
  
* .env file
  
A fourth file that the opera

##########################################

删除环境变量
  
字符模式下设置/删除环境变量
  
bash下
  
设置: export 变量名=变量值
  
删除: unset 变量名

csh下

设置: setenv 变量名 变量值

删除: unsetenv 变量名