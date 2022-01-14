---
title: servlet hello world
author: "-"
date: 2011-10-23T09:52:20+00:00
url: /?p=1274
categories:
  - Java
tags:
  - Servlet

---
## servlet hello world
要运行Servlet，则需要JSP/Servlet container，建议初学者用Tomcat.
  
Tomcat 7.0.xx: http://mirror.bit.edu.cn/apache/tomcat/tomcat-7/v7.0.xx/bin/apache-tomcat-7.0.xx.tar.gz

然后把这个压缩包解压到: 
  
/home/wiloon/opt/apache-tomcat-7.0.xx

然后再配置环境变量；添加三个系统变量: 

JAVA_HOME="/opt/jvm/jdk1.7.0"
  
TOMCAT_HOME="/home/wiloon/program/apache-tomcat-7.0.xx"
  
CLASSPATH: %JAVA_HOME%/lib;%TOMCAT_HOME%/lib

Tomcat的环境变量就配置完毕了，下面检验Tomcat是否能够运行: 转到/home/wiloon/program/apache-tomcat-7.0.xx/bin这个目录，运行sh startup.sh，在浏览器中输入http://localhost:8080，出现欢迎界面，则表示Tomcat没问题了。然后写入你的第一个Servlet。

```java
  
import java.io.*;
  
import javax.servlet.*;
  
import javax.servlet.http.*;
  
public class HelloWorld extends HttpServlet
  
{
  
public void doGet(HttpServletRequest request,HttpServletResponse response)throws ServletException,IOException
  
{
  
response.setContentType("text/html");
  
PrintWriter out = response.getWriter();
  
out.println("＜html＞＜head＞＜title＞");
  
out.println("This is my first Servlet");
  
out.println("＜/title＞＜/head＞＜body＞");
  
out.println("＜h1＞Hello,World!＜/h1＞");
  
out.println("＜/body＞＜/html＞");

}
  
}
  
```

然后照样用javac HelloWorld.java来编译这个文件，如果出现无法import javax.servlet.*

那么就是应该把/home/wiloon/program/apache-tomcat-7.0.xx/lib里面的servlet.jar文件拷贝到/opt/jvm/jdk1.7.0/lib中，再次编译，就没有问题了！
  
或者在POM.xml里加入

```xml
  
<dependency>
	  
<groupId>org.apache.tomcat</groupId>
	  
<artifactId>tomcat-servlet-api</artifactId>
	  
<version>7.0.xx</version>
  
</dependency>
  
```

For gradle
  
```bash
  
compile 'org.apache.tomcat:tomcat-servlet-api:7.0.xx'
  
```

然后在Tomcat目录里面的/home/wiloon/program/apache-tomcat-7.0.xx/webapps/ROOT里面按如下的文件结构:

ROOT/WEB-INF/classes/HelloWorld.class(把上面生成的HelloWorld.class文件放在这个里面)

然后在浏览器中输入http://localhost:8080/servlet/HelloWorld,于是Server众望所归的报错了:Error 404-Not Found

怎么回事呢？

Servlet必须使用C:/Tomcat/webapps/ROOT/WEB-INF这个目录下面的web.xml文件进行注册，用编辑器打开这个web.xml文件，在里面加入: 

```xml
    
<servlet>
      
<servlet-name>HelloWorld</servlet-name>
      
<servlet-class>HelloWorld</servlet-class>
    
</servlet>
    
<servlet-mapping>
      
<servlet-name>HelloWorld</servlet-name>
      
<url-pattern>/servlet/helloworld</url-pattern>
    
</servlet-mapping>
  
```

这样的结构

```xml
   
<servlet>
      
<servlet-name>HelloWorld</servlet-name>
      
<servlet-class>HelloWorld</servlet-class>
    
</servlet>
  
```

表示指定包含的servlet类。而以下的结构: 

```xml
   
<servlet-mapping>
      
<servlet-name>HelloWorld</servlet-name>
      
<url-pattern>/servlet/HelloWorld</url-pattern>
    
</servlet-mapping>
  
```

表示指定HelloServlet应当映射到哪一种URL模式。

在修改web.xml完毕过后，重新启动Server，然后再输入http://localhost:8080/servlet/HelloWorld，那么偌大一个Hello,World!等着你呢。