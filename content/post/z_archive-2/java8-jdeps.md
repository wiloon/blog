---
title: Java8 jdeps
author: "-"
date: 2017-05-17T02:17:51+00:00
url: /?p=10305
categories:
  - Inbox
tags:
  - reprint
---
## Java8 jdeps
http://blog.csdn.net/u013803262/article/details/70570161
  
Java8中带了一个新的类依赖分析器。
  
我们可以在Java的安装目录的bin目录下看到jdeps.exe这个文件。
  
这个工具是用于分析类的依赖关系的。
  
具体怎么用 可以这样。
  
找一个目录,下面全是jar文件。那么这样的目录很明显WEB-INF下的lib目录就非常合适。
  
假设我们有一个web项目,tomcat下的lib有
  
commons-pool2-2.0.jar
  
jedis-2.5.1.jar
  
为了使得结构简单点。我们只加入了两个jar包并且jedis包依赖于commons-pool这个包。
  
我们进入lib目录下运行命令
  
jdeps *.jar
  
结果得到
  
E:\git_tmp\distributedSession\target\distributedSession\WEB-INF\lib>jdeps *.jar
  
commons-pool2-2.0.jar -> F:\Program Files\Java\jdk1.8.0_121\jre\lib\rt.jar
  
commons-pool2-2.0.jar -> 找不到
     
org.apache.commons.pool2 (commons-pool2-2.0.jar)
        
-> java.io
        
-> java.lang
        
-> java.util
        
-> java.util.concurrent.locks
     
org.apache.commons.pool2.impl (commons-pool2-2.0.jar)
        
-> java.io
        
-> java.lang
        
-> java.lang.management
        
-> java.lang.ref
        
-> java.lang.reflect
        
-> java.security
        
-> java.text
        
-> java.util
        
-> java.util.concurrent
        
-> java.util.concurrent.atomic
        
-> java.util.concurrent.locks
        
-> javax.management
        
-> org.apache.commons.pool2 commons-pool2-2.0.jar
     
org.apache.commons.pool2.proxy (commons-pool2-2.0.jar)
        
-> java.lang
        
-> java.lang.reflect
        
-> java.util
        
-> net.sf.cglib.proxy 找不到
        
-> org.apache.commons.pool2 commons-pool2-2.0.jar
  
jedis-2.5.1.jar -> commons-pool2-2.0.jar
  
jedis-2.5.1.jar -> F:\Program Files\Java\jdk1.8.0_121\jre\lib\rt.jar
     
Redis.clients.jedis (jedis-2.5.1.jar)
        
-> java.io
        
-> java.lang
        
-> java.NET
        
-> java.util
        
-> java.util.concurrent.atomic
        
-> java.util.logging
        
-> java.util.regex
        
-> org.apache.commons.pool2 commons-pool2-2.0.jar
        
-> org.apache.commons.pool2.impl commons-pool2-2.0.jar
        
-> redis.clients.jedis.exceptions jedis-2.5.1.jar
        
-> redis.clients.util jedis-2.5.1.jar
     
redis.clients.jedis.exceptions (jedis-2.5.1.jar)
        
-> java.lang
        
-> redis.clients.jedis jedis-2.5.1.jar
     
redis.clients.util (jedis-2.5.1.jar)
        
-> java.io
        
-> java.lang
        
-> java.nio
        
-> java.security
        
-> java.util
        
-> java.util.regex
        
-> org.apache.commons.pool2 commons-pool2-2.0.jar
        
-> org.apache.commons.pool2.impl commons-pool2-2.0.jar
        
-> redis.clients.jedis jedis-2.5.1.jar
        
-> redis.clients.jedis.exceptions jedis-2.5.1.jar

jdeps的输入不仅可以是jar还可以是.class和目录。
  
我们可以从输出的结果中看出,依赖分析的非常详细。是从包下的每一个类文件进行分析的。
  
如果在lib目录下没有找到当前的间接依赖,则会提示not found