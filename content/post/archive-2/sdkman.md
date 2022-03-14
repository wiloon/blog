---
title: sdkman
author: "-"
date: 2017-07-01T06:06:07+00:00
url: /?p=10735
categories:
  - Uncategorized

tags:
  - reprint
---
## sdkman
```bash
  
#install
  
curl -s http://get.sdkman.io | bash

sdk list gradle
  
sdk install gradle
  
sdk install gradle 4.2
  
sdk default gradle 4.2
  
```

http://blog.csdn.net/jjlovefj/article/details/51103578

１．sdkman介绍
  
sdkman(The Software Development Kit Manager), 中文名为:软件开发工具管理器．这个工具的主要用途是用来解决在类unix操作系统(如mac, Linux等)中多种版本开发工具的切换, 安装和卸载的工作．对于windows系统的用户可以使用Powershell CLI来体验．

例如: 项目A使用Jdk7中某些特性在后续版本中被移除 (尽管这是不好的设计) ,项目B使用Jdk8,我们在切换开发这两个项目的时候,需要不断的切换系统中的JAVA_PATH,这样很不方便,如果存在很多个类似的版本依赖问题,就会给工作带来很多不必要的麻烦．
  

  
sdkman这个工具就可以很好的解决这类问题,它的工作原理是自己维护多个版本,当用户需要指定版本时,sdkman会查询自己所管理的多版本软件中对应的版本号,并将它所在的路径设置到系统PATH.

２.安装

直接打开终端,执行如下命令:

$ curl -s http://get.sdkman.io | bash

上面的命令的含义: 首先sdkman官网下载对应的安装shell script,然后调用bash解析器去执行．

接下来,你需要打开一个新的终端窗口,执行命令:

$ source "$HOME/.sdkman/bin/sdkman-init.sh"

再次之后,可以通过输入sdk help确认安装是否完成.

jiangjian@jiangjian-ThinkPad-E450c:~$ sdk help

Usage: sdk <command> [candidate] [version]
         
sdk offline <enable|disable>

commands:
         
install or i <candidate> [version]
         
uninstall or rm <candidate> <version>
         
list or ls [candidate]
         
use or u <candidate> [version]
         
default or d <candidate> [version]
         
current or c [candidate]
         
outdated or o [candidate]
         
version or v
         
broadcast or b
         
help or h
         
offline [enable|disable]
         
selfupdate [force]
         
flush <candidates|broadcast|archives|temp>

candidate : the SDK to install: groovy, scala, grails, akka, etc.use list command for comprehensive list of candidates
  
eg: $ sdk list

version : where optional, defaults to latest stable if not provided
  
eg: $ sdk install groovy

如果有上面的输出,表明你的安装过程完成了．

3.使用

  1. 安装最新版本软件

如果你想通过sdkman安装gradle最新版本,你可以在终端输入:

sdk install gradle

你将会看到

Downloading: gradle 2.6

% Total % Received % Xferd Average Speed Time Time Time Current
                                   
Dload Upload Total Spent Left Speed
  
100 39.0M 100 39.0M 0 0 945k 0 0:00:42 0:00:42 -:-:- 978k

Installing: gradle 2.6
  
Done installing!

  1. 安装指定版本的软件

如果需要安装制定版本的软件,只需要在安装命令上面加上版本号即可:

sdk install scala 2.11.7

  1. 安装本地版本

如果你已经下载安装包到本地,你现在想需要将已经安装的版本绑定到sdk特定的版本上,交给sdkman统一进行管理,可以执行如下命令:

$ sdk install grails 3.1.0-SNAPSHOT /path/to/grails-3.1.0-SNAPSHOT

  1. 删除执行版本

如果你删除给定版本的sdk,可以使用:

$ sdk remove scala 2.11.6

  1. 列举可供安装的软件

如果你想了解哪些工具可以通过sdkman进行安装的,可以使用如下命令来了解:

$ sdk list

  1. 查询可供安装的版本

有些时候你需要了解当前工具存在哪些可安装的版本,你可以通过如下命令来查询:

jiangjian@jiangjian-ThinkPad-E450c:~$ sdk list gradle

==========================================================

# Available Gradle Versions

     2.9                  2.0                  0.9.1                               
     2.8                  1.9                  0.9                                 
     2.7                  1.8                  0.8                                 
     2.6                  1.7                  0.7                                 
     2.5                  1.6                                                      
     2.4                  1.5                                                      
     2.3                  1.4                                                      
     2.2.1                1.3                                                      
     2.2                  1.2                                                      
     2.13-rc-1            1.12                                                     
     2.12-rc-1            1.11                                                     
     2.12                 1.10                                                     
     2.11                 1.1                                                      
     2.10                 1.0                                                      
     2.1                  0.9.2                                                    
    

==========================================================
  
+ - local version
  
* - installed

# > - currently in use

  1. 临时选用指定的版本

如果你想在当前的终端下,使用特定的版本,系统原有的配置保持不变,仅仅在当前的终端生效,可以使用如下命令,来临时改变版本:

$ sdk use scala 2.11.6

  1. 将指定的版本设置为默认的版本

可以使用如下命令来完成:

$ sdk default scala 2.11.6

  1. 显示当前软件的安装版本

有些时候我们需要查询当前默认软件的版本,可以通过如下命令进行查询:

$ sdk current grails

参考: http://sdkman.io/usage.html