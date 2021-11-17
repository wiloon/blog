---
title: servlet-api.jar
author: "-"
date: 2011-10-23T08:28:42+00:00
url: /?p=1261
categories:
  - Java
tags:
  - Tomcat

---
## servlet-api.jar
用于在servlet环境下开发程序的一组api,虽然叫servlet-api.jar但其实包里除了大部分的接口外还有一些javabean和抽象类、之所以叫api是因为这个包是开发基于servlet规范的标准接口(这个接口的含义和java里的interface不同，不要混淆)。
  
既然开发jsp、servlet的程序，就应该知道这是基于http(请求、响应)协议的,那么在这里请求和响应就对应为servlet-api.jar中的ServletRequest和ServletResponse接口，接口中定义了作为一个请求和一个响应信息应该具备的方法，比如从请求信息中可以获取客户端的ip，用户提交的信息等等，从响应信息中可以获取客户端的输出流，响应类型等等，当然中间的过程是由servlet容器封装好的，等我们开发servlet时会直接使用这些接口来编写具体的业务代码，其他的处理过程就全由容器处理了。
  
当然这个jar的接口是按照servlet规范编写的，面向标准接口编程的好处就是我们开发出的一个web工程即可以部署到tomcat、也可以部署到weblogic或其他servlet容器下运行，所有的servlet容器都使用了相同接口所以我们可以无缝移植(定义标准很重要)，还记得jdbc吧?只要用接口访问数据库即可，你不必担心底层是什么数据库。
  
但也许你不会在每个应用服务器下都搜到这个名字的jar(tomcat里有)，因为不同的servlet容器的功能不同，比如一些功能强大的服务器除了实现了基础的servlet规范外还支持一些javaee的规范(如ejb,jms等等)，所以这组api可能会被不同的厂商封装到自己的jar中,如weblogic就放到了weblogic.jar中.