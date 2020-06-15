---
title: Embedding tomcat 7
author: wiloon
type: post
date: 2011-11-20T09:10:54+00:00
url: /?p=1550
views:
  - 8
bot_views:
  - 8
categories:
  - Java
tags:
  - Tomcat

---
<http://www.copperykeenclaws.com/embedding-tomcat-7/>

One of the more anticipated features of Tomcat 7 is the ability to run as an embedded server like Jetty. We use Tomcat 6 in production, but embedded Jetty more and more for running and testing during development (in Eclipse). The Tomcat 7  has been out for a while, but there seems to be little documentation out there on how to embed it, other than some suggestions to look at the unit tests for examples. So that’s what I did! First, here is the guts of our original Main method in Jetty:

[java]
  
public static void main(String[] args) throws Exception {
    
String weppAppHome = args[0];
    
Integer port = Integer.valueOf(args[1]);

Server server = new Server(port);

WebAppContext webapp = new WebAppContext();
    
webapp.setContextPath("/myapp");
    
webapp.setCompactPath(true);

webapp.setDescriptor(weppAppHome + "/WEB-INF/web.xml");
    
webapp.setResourceBase(weppAppHome);
    
webapp.setParentLoaderPriority(true);

server.setHandler(webapp);
    
server.start();
    
server.join();
  
}
  
[/java]


  To switch to Tomcat 7, add these dependencies to your build.gradle:



  <span class="Apple-style-span" style="font-family: Consolas, Monaco, monospace; font-size: 12px; line-height: 18px; white-space: pre;">compile "org.apache.tomcat:tomcat-catalina:7.0.22"</span>



  <span class="Apple-style-span" style="font-family: Consolas, Monaco, monospace; font-size: 12px; line-height: 18px; white-space: pre;">compile "org.apache.tomcat.embed:tomcat-embed-core:7.0.22"</span>



  <span class="Apple-style-span" style="font-family: Consolas, Monaco, monospace; font-size: 12px; line-height: 18px; white-space: pre;">compile "org.apache.tomcat:tomcat-jasper:7.0.22"</span>



  Here is the Tomcat 7 version:


[java]
  
public static void main(String[] args) throws Exception {
    
//app base, which contains WEB-INF
    
String appBase = "/xxx/xxx/xxx/yourAppBase"
    
Integer port = 8080;

//config the url,
    
//http://localhost:8080/myapp
    
String contextPath = "/myapp";
    
Tomcat tomcat = new Tomcat();
    
tomcat.setPort(port);

tomcat.setBaseDir(".");
    
tomcat.getHost().setAppBase(appBase);

// Add AprLifecycleListener
    
StandardServer server = (StandardServer)tomcat.getServer();
    
AprLifecycleListener listener = new AprLifecycleListener();
    
server.addLifecycleListener(listener);

tomcat.addWebapp(contextPath, appBase);
    
tomcat.start();
    
tomcat.getServer().await();
  
}
  
[/java]


  Without the await() call at the end, the server quits right after it starts, which you may or may not want.



  Launch it! We normally set up a launch configuration in Eclipse to run it. It’s also easy to run on the command-line using java -jar after you’ve built your jar.
