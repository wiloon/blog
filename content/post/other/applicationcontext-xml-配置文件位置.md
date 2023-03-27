---
title: applicationContext.xml 配置文件位置
author: "-"
date: 2014-02-24T06:44:56+00:00
url: /?p=6277
categories:
  - Inbox
tags:
  - Spring

---
## applicationContext.xml 配置文件位置

存放位置:
  
1: src下面
  
需要在web.xml中定义如下:
  
<context-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>classpath:applicationContext.xml</param-value>
  
</context-param>

2: WEB-INF下面
  
需要在web.xml中定义如下:
  
<context-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>WEB-INF/applicationContext*.xml</param-value>
  
</context-param>

web.xml 通过contextConfigLocation配置spring 的方式
  
SSI框架配置文件路径问题:

struts2的 1个+N个  路径: src+src(可配置)      名称:  struts.xml  + N
  
spring 的 1个           路径:  src                          名称:  applicationContext.xml
  
ibatis 的 1个+N个  路径:  src+src(可配置)     名称:  SqlMapConfig.xml + N

部署到tomcat后，src目录下的配置文件会和class文件一样，自动copy到应用的 classes目录下

spring的 配置文件在启动时，加载的是web-info目录下的applicationContext.xml,
  
运行时使用的是web-info/classes目录下的applicationContext.xml。

配置web.xml使这2个路径一致:

<context-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>/WEB-INF/classes/applicationContext.xml</param-value>
  
</context-param>

多个配置文件的加载
  
<context-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>
  
classpath\*:conf/spring/applicationContext_core\*.xml,
  
classpath\*:conf/spring/applicationContext_dict\*.xml,
  
classpath*:conf/spring/applicationContext_hibernate.xml,
  
classpath\*:conf/spring/applicationContext_staff\*.xml,
  
classpath*:conf/spring/applicationContext_security.xml
  
classpath\*:conf/spring/applicationContext_modules\*.xml
  
classpath\*:conf/spring/applicationContext_cti\*.xml
  
classpath\*:conf/spring/applicationContext_apm\*.xml
  
</param-value>
  
</context-param>

contextConfigLocation 参数定义了要装入的 Spring 配置文件。

首先与Spring相关的配置文件必须要以"applicationContext-"开头，要符合约定优于配置的思想，这样在效率上和出错率上都要好很多。
  
还有最好把所有Spring配置文件都放在一个统一的目录下，如果项目大了还可以在该目录下分模块建目录。这样程序看起来不会很乱。
  
在web.xml中的配置如下:
  
Xml代码
  
<context-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>classpath\*:\**/applicationContext-\*.xml</param-value>
  
</context-param>

"**/"表示的是任意目录；
  
"**/applicationContext-\*.xml"表示任意目录下的以"applicationContext-"开头的XML文件。
  
你自己可以根据需要修改。最好把所有Spring配置文件都放在一个统一的目录下，如:

<!- Spring 的配置 ->
  
<context-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>classpath:/spring/applicationContext-*.xml</param-value>
  
</context-param>
