---
title: linux 环境变量, export, set, env, source, exec
author: "-"
date: 2011-07-18T04:58:48+00:00
url: env
categories:
  - Linux
tags:
  - reprint
---
## linux 环境变量, export, set, env, source, exec

定义变量时加 export 表示为全局变量，不止对当前 shell 有效，对子进程也有效，不加 export 则为局部变量，只对当前 shell 有效，子进程无效。

- set 设置了当前 shell 进程的本地变量，本地变量只在当前 shell 的进程内有效，不会被子进程继承和传递。
- env 仅为将要执行的子进程设置环境变量。
- export 将一个 shell 本地变量提升为当前 shell 进程的环境变量，从而被子进程自动继承，但是 export 的变量无法改变父进程的环境变量。
- source 运行脚本的时候，不会启用一个新的 shell 进程，而是在当前shell进程环境中运行脚本。
- exec 运行脚本或命令的时候，不会启用一个新的 shell 进程，并且 exec 后续的脚本内容不会得到执行，即当前shell进程结束了。

<https://segmentfault.com/a/1190000013356532>

## .bashrc 文件
  
这种方法可以把使用这些环境变量的权限控制到用户级别，如果你需要给某个用户权限使用这些环境变量，你只需要修改其个人用户主目录下的.bashrc文件就可以了。
  
(1)用文本编辑器打开用户目录下的.bashrc文件
  
(2)在.bashrc文件末尾加入:

JAVA_HOME=/usr/share/jdk1.5.0_05
  
export JAVA_HOME
  
PATH=$JAVA_HOME/bin:$PATH
  
export PATH
  
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
  
export CLASSPATH
  
重新加载
  
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
  
使环境变量生效
  
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
  
摘自IBM官方网站，原文地址: <http://publib.boulder.ibm.com/infocenter/pseries/v5r3/index.jsp?topic=/com.ibm.aix.baseadmn/doc/baseadmndita/etc_env_file.htm>

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

<https://segmentfault.com/a/1190000013356532>

## env command

env命令 用于显示系统中已存在的环境变量，以及在定义的环境中执行指令。该命令只使用"-"作为参数选项时，隐藏了选项"-i"的功能。若没有设置任何选项和参数时，则直接显示当前的环境变量。

如果使用env命令在新环境中执行指令时，会因为没有定义环境变量"PATH"而提示错误信息"such file or directory"。此时，用户可以重新定义一个新的"PATH"或者使用绝对路径。
