---
title: Tomcat Port 8009 与AJP13协议
author: "-"
date: 2012-05-13T11:38:04+00:00
url: /?p=3124
categories:
  - Web
tags:
  - Tomcat

---
## Tomcat Port 8009 与AJP13协议
  
    由于tomcat的html和图片解析功能相对其他服务器如apche等较弱，所以，一般都是集成起来使用，只有jsp和servlet服务交由tomcat处理，而tomcat和其他服务器的集成，就是通过ajp协议来完成的。
  
  
    AJP13(Apache JServ Protocol version 1.3)是定向包协议。因为性能原因，使用二进制格式来传输可读性文本。WEB服务器通过TCP连接和SERVLET容器连接。为了减少进程生成 socket的花费，WEB服务器和SERVLET容器之间尝试保持持久性的TCP连接，对多个请求/回复循环重用一个连接。一旦连接分配给一个特定的请 求，在请求处理循环结束之前不会在分配。换句话说，在连接上，请求不是多元的。这个是连接两端的编码变得容易，虽然这导致在一时刻会有很多连接。
  


  
    一旦WEB服务器打开了一个到SERVLET容器的连接，连接处于下面的状态: 
 ◆ 空闲
 这个连接上没有处理的请求。
 ◆ 已分派
 连接正在处理特定的请求。
 一旦一个连接被分配给一个特定的请求，在连接上发送的基本请求信息是高度压缩的。在这点，SERVLET容器大概准备开始处理请求，当它处理的时候，它能发回下面的信息给WEB服务器: 
 ◆ SEND_HEADERS
 发送一组头到浏览器。
 ◆ SEND_BODY_CHUNK
 发送一块主体数据到浏览器。
 ◆ GET_BODY_CHUNK
 从请求获得下一个数据如果还没有全部传输完，如果请求内容的包长度非常大或者长度不确定，这是非常必要的。例如上载文件。注意这和HTTP的块传输没有关联。
 ◆ END_RESPONSE
 结束请求处理循环。
  
  
    Tomcat服务器通过Connector连接器组件与客户程序建立连接，Connector组件负责接收客户的请求，以及把Tomcat服务器的响应结果发送给客户。默认情况下，Tomcat在server.xml中配置了两种连接器: 
  
  
    <!- Define a non-SSL Coyote HTTP/1.1
 Connector on port 8080 ->
 <Connector port="8080"
 maxThreads="150"
 minSpareThreads="25"
 maxSpareThreads="75"
 enableLookups="false"
 redirectPort="8443"
 acceptCount="100"
 debug="0"
 connectionTimeout="20000"
 disableUploadTimeout="true" />
  
  
    <!- Define a Coyote/JK2 AJP 1.3
 Connector on port 8009 ->
 <Connector port="8009"
 enableLookups="false"
 redirectPort="8443" debug="0"
 protocol="AJP/1.3" />
  
  
    第一个连接器监听8080端口，负责建立HTTP连接。在通过浏览器访问Tomcat服务器的Web应用时，使用的就是这个连接器。
  
  
    第二个连接器监听8009端口，负责和其他的HTTP服务器建立连接。在把Tomcat与其他HTTP服务器集成时，就需要用到这个连接器。
  
  
    Web客户1直接访问Tomcat服务器上的JSP组件，他访问的URL为http://localhost:8080 /index.jsp。Web客户2通过HTTP服务器访问Tomcat服务器上的JSP组件。假定HTTP服务器使用的HTTP端口为默认的80端口， 那么Web客户2访问的URL为http://localhost:80/index.jsp 或者 http://localhost/index.jsp。
  
  
    摘自: 
  
  
    http://hikin.iteye.com/blog/555682
  
  
    2.http://bbs.163jsp.com/posts/list/472.html
  
  
    http://tomcat.apache.org/connectors-doc-archive/jk2/common/AJPv13.html
  
