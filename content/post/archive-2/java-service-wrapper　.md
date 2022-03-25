---
title: Java Service Wrapper
author: "-"
date: 2016-01-05T01:45:38+00:00
url: /?p=8628
categories:
  - Uncategorized

tags:
  - reprint
---
## Java Service Wrapper
http://www.cnblogs.com/fsjohnhuang/p/4019267.html


Java魔法堂: 以Windows服务的形式运行Java程序

一、前言

由于防止维护人员误操作关闭Java控制台程序,因此决定将其改造为以Windows服务的形式运行。弄了一个上午总算搞定了,下面记录下来,以供日后查阅。


二、Java Service Wrapper

官网地址: http://wrapper.tanukisoftware.com/doc/english/download.jsp

JavaServiceWrapper以守护进程或windows服务的方式运行java程序。JSW提供四种方案改造原有项目,以实现守护进程或windows服务的方式运行。而且还提供JVM监控功能和自动重启功能,反正十分强大的样子。

方式1: WrapperSimpleApp

用于通过同一个类实现启动和关闭的程序。
  
官方推荐使用该方式加工原有项目,好处是简单,且不用修改原有项目的代码。

步骤1: 下载并解压得到工具包,目录结构如下

/
  
|- bin,wrapper控制windows服务的bat文件
  
|- conf,wrapper配置文件
  
|- doc,教程
  
|- lib,wrapper的依赖包
  
|- logs,日志
  
|- src,模板
  
|- conf
  
|- bin

步骤2: 搭建项目结构: 新建项目发布目录 (假设为agent) ,然后将src下的conf和bin复制到agent下,并且将conf和bin下的文件重命名,去掉\`.in\`后缀。然后将bin/wrapper.exe复制到agent/bin/下,再将lib复制到agent下,得到目录结构如下

agent
  
|- lib
  
|- wrapper.dll
  
|- wrapper.jar
  
|- conf
  
|- wrapper.conf
  
|- bin
  
|- wrapper.exe
  
|- 一堆bat文件
  
最后将原有项目的文件复制到bin目录下。

步骤3: 配置agent/conf/wrapper.conf的参数
  
# 配置java命令路径
  
wrapper.java.command=jre/bin/java

# 配置CLASSPATH路径 (并不会修改全局的环境变量) 
  
# 若原有项目还依赖其他jar包,均需要添加进来
  
wrapper.java.classpath.1=../lib/wrapper.jar
  
wrapper.java.classpath.2=.

# 配置lib路径
  
wrapper.java.library.path.1=../lib

# 配置服务的main class (就是原有项目的程序入口类) 
  
wrapper.app.parameter.1=agent.Daemon

# 配置wrapper日志文件
  
wrapper.logfile=logs/Agent.log

# 配置系统服务名称
  
wrapper.ntservice.name=AgentService

# 配置系统服务显示的名称
  
wrapper.ntservice.displayname=AgentService

# 配置系统服务描述
  
wrapper.ntservice.description=AgentService

# 配置系统服务的启动方式,取值范围是AUTO_START或DEMAND_START
  
wrapper.ntservice.starttype=AUTO_START

# 配置内存溢出则重启服务
  
wrapper.filter.trigger.1001=Exception in thread "*" java.lang.OutOfMemoryError
  
wrapper.filter.allow_wildcards.1001=TRUE
  
wrapper.filter.action.1001=RESTART
  
wrapper.filter.message.1001=The JVM has run out of memory.

步骤4: 安装、卸载服务

点击对应的Install.bat和Uninstall.bat即可。

2. 方式2: WrapperStartStopApp

用于像tomcat那样,启动程序和关闭程序是分开的项目。该方式同样不用修改原来项目的代码。

3. 方式3: WrapperListener

该方式需要修改原来项目的代码,但最灵活。

4. 方式4: WrapperJarApp

用于原有项目已经打包为jar或war包的情况,配置方式与\`WrapperSimpleApp\`相似,但\`wrapper.app.parameter.1=jar或war包路径\`。该方式同样不用修改原来项目的代码


三、总结

官方文档以JBOSS为例子说明WrapperSimpleApp的使用,十分不好懂,幸好有前人记录实操过程我才从苦海得救,感谢感谢。

尊重原创,转载请注明来自: http://www.cnblogs.com/fsjohnhuang/p/4019267.html  ^_^肥仔John


四、参考

http://blog.csdn.net/arjick/article/details/4526392