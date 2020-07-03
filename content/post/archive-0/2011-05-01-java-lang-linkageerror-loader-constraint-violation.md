---
title: 'java.lang.LinkageError: loader constraint violation'
author: wiloon
type: post
date: 2011-05-01T01:54:27+00:00
url: /?p=157
bot_views:
  - 9
views:
  - 5
categories:
  - Java
tags:
  - Tomcat

---
May 1, 2011 9:49:01 AM org.apache.catalina.core.ApplicationContext log
  
INFO: Initializing log4j from [/home/wiloon/program/apache-tomcat-7.0.12B/webapps/EnLab/WEB-INF/log4j.xml]
  
May 1, 2011 9:49:06 AM org.apache.catalina.core.ApplicationContext log
  
INFO: ContextListener: contextInitialized()
  
May 1, 2011 9:49:06 AM org.apache.catalina.core.ApplicationContext log
  
INFO: SessionListener: contextInitialized()
  
May 1, 2011 9:49:36 AM org.apache.catalina.core.StandardWrapperValve invoke
  
SEVERE: Servlet.service() for servlet [jsp] in context with path [/EnLab] threw exception [java.lang.LinkageError: loader constraint violation: when resolving interface method "javax.servlet.jsp.JspApplicationContext.getExpressionFactory()Ljavax/el/ExpressionFactory;" the class loader (instance of org/apache/jasper/servlet/JasperLoader) of the current class, org/apache/jsp/index_jsp, and the class loader (instance of org/apache/catalina/loader/StandardClassLoader) for resolved class, javax/servlet/jsp/JspApplicationContext, have different Class objects for the type javax/el/ExpressionFactory used in the signature] with root cause
  
java.lang.LinkageError: loader constraint violation: when resolving interface method "javax.servlet.jsp.JspApplicationContext.getExpressionFactory()Ljavax/el/ExpressionFactory;" the class loader (instance of org/apache/jasper/servlet/JasperLoader) of the current class, org/apache/jsp/index_jsp, and the class loader (instance of org/apache/catalina/loader/StandardClassLoader) for resolved class, javax/servlet/jsp/JspApplicationContext, have different Class objects for the type javax/el/ExpressionFactory used in the signature
  
at org.apache.jsp.index\_jsp.\_jspInit(index_jsp.java:34)
  
at org.apache.jasper.runtime.HttpJspBase.init(HttpJspBase.java:49)
  
at org.apache.jasper.servlet.JspServletWrapper.getServlet(JspServletWrapper.java:171)
  
at org.apache.jasper.servlet.JspServletWrapper.service(JspServletWrapper.java:356)
  
at org.apache.jasper.servlet.JspServlet.serviceJspFile(JspServlet.java:391)
  
at org.apache.jasper.servlet.JspServlet.service(JspServlet.java:334)
  
at javax.servlet.http.HttpServlet.service(HttpServlet.java:722)
  
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:304)
  
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:210)
  
at org.apache.struts2.dispatcher.ng.filter.StrutsPrepareAndExecuteFilter.doFilter(StrutsPrepareAndExecuteFilter.java:88)
  
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:243)
  
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:210)
  
at org.apache.struts2.dispatcher.ActionContextCleanUp.doFilter(ActionContextCleanUp.java:102)
  
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:243)
  
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:210)
  
at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:240)
  
at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:164)
  
at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:462)
  
at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:164)
  
at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:100)
  
at org.apache.catalina.valves.AccessLogValve.invoke(AccessLogValve.java:562)
  
at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:118)
  
at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:395)
  
at org.apache.coyote.http11.Http11Processor.process(Http11Processor.java:250)
  
at org.apache.coyote.http11.Http11Protocol$Http11ConnectionHandler.process(Http11Protocol.java:188)
  
at org.apache.coyote.http11.Http11Protocol$Http11ConnectionHandler.process(Http11Protocol.java:166)
  
at org.apache.tomcat.util.net.JIoEndpoint$SocketProcessor.run(JIoEndpoint.java:302)
  
at java.util.concurrent.ThreadPoolExecutor$Worker.runTask(ThreadPoolExecutor.java:886)
  
at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:908)
  
at java.lang.Thread.run(Thread.java:662)

\***\***\***\***\***\***\***\***\***\***\***\***\***\***
  
WEB-INF/lib 下面的 tomcat-jsp-api-7.0.12.jar 跟tomcat/lib 下面的jsp-api.jar 冲突。
  
把前面的删掉。。。^_^