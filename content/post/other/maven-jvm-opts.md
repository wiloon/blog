---
title: maven jvm opts
author: "-"
date: 2014-04-24T07:47:07+00:00
url: /?p=6557
categories:
  - Java
tags:
  - Maven

---
## maven jvm opts
### Maven工程的JVM配置方式


****1. 为Maven运行配置JVM参数****


这种需求比较少见,一般使用默认的JVM配置即可。如果需要,可以通过设置环境变量来满足需求,如: 


Windows下添加环境变量MAVEN_OPTS的value为-Xms1024m -Xmx1024m -Xss1m


Linux下可修改.profile或者.bash_profile文件,并做如下设置: 


export MAVEN_OPTS="-Xms1024m -Xmx1024m -Xss1m"


(注意: 这里需要使用双引号或者单引号)