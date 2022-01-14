---
title: Eclipse WTP 入门
author: "-"
date: 2013-10-20T04:55:30+00:00
url: /?p=5850
categories:
  - Uncategorized
tags:
  - Java

---
## Eclipse WTP 入门

  WTP (Web Tools Platform) 是一个开发J2EE Web应用程序的工具集


  用了太长时间的MyEclipse难免想换换口味，这几天下来一堆插件，待有时间把使用心得一个一个写出来


  引用一段官方的介绍:


  The Eclipse Web Tools Platform (WTP) project extends the Eclipse platform with tools for developing Web and Java EE applications. It includes source and graphical editors for a variety of languages, wizards and built-in applications to simplify development, and tools and APIs to support deploying, running, and testing apps.


  更多使用文档: http://www.eclipse.org/webtools/documentation/


  下载地址: http://download.eclipse.org/webtools/downloads/

  我的环境配置: 


  Eclipse版本 eclipse-SDK-3.3.2-win32


  WTP版本 wtp-sdk-M-2.0.3


  EMF版本 emf-sdo-xsd-SDK-2.3.2  (WTP依赖)


  GEF版本 GEF-SDK-3.3.2 (WTP依赖)


  其他插件略

  1.安装WTP 插件 略


  2.配置Web Server


  window->preferences->Server->Instaled Runtimes ->Add 添加一个Web Server 例如Tomcat6


  3.新建WTP工程


  File->Web->Dynamic Web Project->添写Project name->勾选java和Dynamic Web Module->填写context信息->finish->建立一个测试用的jsp文件,最好在写个java类在jsp中进行调用，以便测试单步跟踪。


  4.发布应用


  window->show view->other->server->servers在servers视图中右键->new->Server->选择在第二步中配置的Web Server->next>选择第三步创建的WTP工程->finish


  在servers视图会显示刚才创建的Web Server 右键->publish->start或debug->打开浏览器测试吧，再做个断点测试debug,完全没问题，基本热部署也都没问题。


  5.了解WTP部署原理


  本以为WTP发布应用时将文件copy到tomcat下面，结果经查看不是这样的，后来又怀疑动态指定了conf/Catalina/localhost，经查看也没有，


  那么它是如何发布的呢，在jsp写段代码测试下


  <%=com.syj.TestWTP.class.getClassLoader().getResource("") %>


  结果如下


  file:/D:/SYJ.WORK/SYJ.WORKSPACE/ws1/.metadata/.plugins/org.eclipse.wst.server.core/tmp0/wtpwebapps/Test11/WEB-INF/classes/


  原来把文件同步到了工作区下的.metadata下面。


  D:/SYJ.WORK/SYJ.WORKSPACE/ws1/是我的工作区Test11是我这次用于测试的项目


  看来WTP没有使用tomcat 的启动批处理而是直接调用了tomcat的bootstrap.jar


  删除tomcat/bin目录下的所有文件，只保留下面5个jar文件，WTP照样工作。


  bootstrap.jar


  tomcat-native.tar.gz


  tomcat-juli.jar


  jsvc.tar.gz


  commons-daemon.jar


  6.将一个已经存在的项目转换成WTP 的Web项目


  通过文件比较以及一系列尝试终于摸索出如下简单方法


  修改.project文件(修改后刷新项目或重启eclipse)


  在<natures></natures>中加入


                <nature>org.eclipse.wst.common.project.facet.core.nature</nature>


                <nature>org.eclipse.wst.common.modulecore.ModuleCoreNature</nature>


                <nature>org.eclipse.jem.workbench.JavaEMFNature</nature>


  在<buildSpec></buildSpec>中加入


                <buildCommand>


                       <name>org.eclipse.wst.common.project.facet.core.builder</name>


                       


                       </arguments>


                </buildCommand>


                <buildCommand>


                       <name>org.eclipse.wst.validation.validationbuilder</name>


                       


                       </arguments>


                </buildCommand>


  右键刷新项目后->项目->右键->Properties->Project Facets->Modify Project在弹出的面板中，选择Java和Dynamic Web Module 下一步是配置Context Root 和Content Directory 以及源码路径->finish.

  http://blog.csdn.net/sunyujia/article/details/2614073
