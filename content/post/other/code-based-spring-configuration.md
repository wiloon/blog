---
title: code-based spring configuration
author: "-"
date: 2014-01-09T10:52:23+00:00
url: /?p=6186
categories:
  - Inbox
tags:
  - Java
  - Spring

---
## code-based spring configuration

spring api

WebApplicationInitializer

public class MyWebAppInitializer implements WebApplicationInitializer {

    @Override
    public void onStartup(ServletContext container) {
      // Create the 'root' Spring application context
      AnnotationConfigWebApplicationContext rootContext =
        new AnnotationConfigWebApplicationContext();
      rootContext.register(AppConfig.class);

      // Manage the lifecycle of the root application context
      container.addListener(new ContextLoaderListener(rootContext));

      // Create the dispatcher servlet's Spring application context
      AnnotationConfigWebApplicationContext dispatcherContext =
        new AnnotationConfigWebApplicationContext();
      dispatcherContext.register(DispatcherConfig.class);

      // Register and map the dispatcher servlet
      ServletRegistration.Dynamic dispatcher =
        container.addServlet("dispatcher", new DispatcherServlet(dispatcherContext));
      dispatcher.setLoadOnStartup(1);
      dispatcher.addMapping("/");
    }

 }

[http://stackoverflow.com/questions/15008126/spring-mvc-3-2-and-servlets-3-0-do-you-still-need-web-xml](http://stackoverflow.com/questions/15008126/spring-mvc-3-2-and-servlets-3-0-do-you-still-need-web-xml)
[http://www.cnblogs.com/coqn/archive/2012/08/15/SpringMvc%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E9%85%8D%E7%BD%AE.html](http://www.cnblogs.com/coqn/archive/2012/08/15/SpringMvc%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E9%85%8D%E7%BD%AE.html)
[http://hitmit1314.iteye.com/blog/1315816](http://hitmit1314.iteye.com/blog/1315816)
[http://www.it165.net/pro/html/201210/3930.html](http://www.it165.net/pro/html/201210/3930.html)
[http://septem.iteye.com/blog/1117445](http://septem.iteye.com/blog/1117445)
[http://septem.iteye.com/blog/740301](http://septem.iteye.com/blog/740301)
[http://septem.iteye.com/blog/753593](http://septem.iteye.com/blog/753593)
