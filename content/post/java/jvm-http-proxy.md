---
title: jvm http proxy
author: "-"
date: 2012-07-05T06:10:33+00:00
url: /?p=3746
categories:
  - Java

tags:
  - reprint
---
## jvm http proxy
http://i4t.org/2007/05/04/java-http-proxy-settings/
  
Java HTTP Proxy Settings

OVERVIEW

For local networks within an organization, access to the public-domain Internet is often via a HTTP Proxy. This article talks about the HTTP proxy settings for the Java environment. I did not find a good document on the Web to describe these settings; Had to discover many of them by trial-and-error. Hence this article.

KEYWORDS

HTTP Proxy, Java Proxy Settings, Tomcat, Application Server, Servlets, HTTP Proxy Authentication for Java, Java Application Proxy Settings

SCENARIO

Your Java client runs on a machine on the Local network – Private LAN. The client could be a standalone application, or a servlet hosted on a web container like Tomcat
  
Your code access an external resource using HTTP. For example, invoking an external Web Service.
  
Your HTTP call needs to tunnel through the HTTP proxy (using SOCKS authentication). Even if authentication is not required, you would still need to configure the URL and the Port of your HTTP proxy.
  
SETTINGS

Use one of the methods below for your JVM proxy settings. Try an alternate method if any particular method does not work. In most cases, you should not require any change the pre-compiled Java code for proxy settings. JVM's environment settings should be enough to fix this problem.

Command Line JVM Settings

The proxy settings are given to the JVM via command line arguments:

$ java -Dhttp.proxyHost=proxyhostURL
  
-Dhttp.proxyPort=proxyPortNumber
  
-Dhttp.proxyUser=someUserName
  
-Dhttp.proxyPassword=somePassword javaClassToRun
  
Setting System Properties in Code

Add the following lines in your Java code so that JVM uses the proxy to make HTTP calls. This would, of course, require you to recompile your Java source. (The other methods do not require any recompilation.):

System.getProperties().put("http.proxyHost", "someProxyURL");
  
System.getProperties().put("http.proxyPort", "someProxyPort");
  
System.getProperties().put("http.proxyUser", "someUserName");
  
System.getProperties().put("http.proxyPassword", "somePassword");
  
Don't hardcode the proxy settings in your source. Read these settings from a configurable text file, so your users can configure them. You might also need to set this property:

System.getProperties().put("proxySet", "true");
  
Or

System.getProperties().put("http.proxySet", "true");
  
Tomcat Settings: catalina.properties

Append these properties to the catalina.properties file in Tomcat:${CATALINA_OME}/conf/catalina.properties file:

http.proxyHost=yourProxyURL
  
http.proxyPort=yourProxyPort
  
http.proxyUser=yourUserName
  
http.proxyPassword=yourPassword
  
Tomcat Settings: catalina.bat

Add all the parameters defined above in the ${CATALINA_HOME}/bin/catalina.bat (for Windows) or ${CATALINA_HOME}/bin/catalina.bat (for *nix):

JAVA_OPTS="-Dhttp.proxyHost=yourProxyURL ..."
  
(Each option is seperated by spaces.)