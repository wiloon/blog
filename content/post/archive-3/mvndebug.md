---
title: mvnDebug
author: "-"
date: 2019-12-17T06:56:11+00:00
url: /?p=15212
categories:
  - Inbox
tags:
  - reprint
---
## mvnDebug
在maven上debug，经常跟jetty或tomcat插件在一起使用。如运行mvnDebug jetty:run命令后再通过eclipse远程连接调试。

```bash
mvnDebug jetty:run
# 默认调试端口8000
```

maven的安装目录下存在 mvnDebug.bat 文件，打开可以看到具体的配置项如下: 

set MAVEN_DEBUG_OPTS=-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000
```

这里对几个参数进行说明: 
  
- -Xdebug :   启动debug模式
  
- -Xnoagent:   禁用默认sun.tools.debug调试器
  
- -Djava.compiler: 指定编译器类型，可方便优化 jitc jitc_de等
  
- -Xrunjdwp: 启动调试协议JDWP，全称是Java Debug Wire Protocol，它定义了JPDA front-end和JPDA back-end之间通讯信息的二进制格式。这里的通讯信息主要包括两种: 调试器发送给JVM的请求信息和JVM发送给调试器的调试信息。有如下子项: 
      
+ -transport: JPDA front-end和back-end之间的传输方法。dt_socket表示使用 socket 传输。
      
+ -server: y/n 该jvm是被调试者还是调试器
      
+ -suspend: y/n 是否等待外部调试器的连接，如jetty启动时候，是否等待eclipse的远程连接后在进行jetty的初始化工作。在调试web容器的时候用的很多
      
+ -address: 监听端口

mvnDebug 默认配置 -suspend:y , 启动jetty:run 之后命令行会显示

```bash
application prints "Listening for transport dt_socket at address: 8000" and does not halt
```

此时在idea中启动调试连接到8000端口即可.

### mvn debug

```bash
# linux
export MAVEN_OPTS="-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,address=5005,server=y,suspend=n"
# windows
set MAVEN_OPTS="-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,address=5005,server=y,suspend=n"

# 在命令行导入以上参数然后执行
mvn jetty:run
```

————————————————
  
版权声明: 本文为CSDN博主「wxy_fighting」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/wxyFighting/article/details/9408153