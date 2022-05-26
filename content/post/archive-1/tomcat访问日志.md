---
title: Tomcat访问日志
author: "-"
date: 2014-01-10T06:12:27+00:00
url: /?p=6194
categories:
  - Inbox
tags:
  - Java
  - Tomcat

---
## Tomcat访问日志
  
    http://hooray520.iteye.com/blog/1335156
  
  Tomcat的访问日志是靠org.apache.catalina.valves.AccessLogValve来控制的，你可以修改$tomcat/conf/server.xml来启用它 ($tomcat是Tomcat安装的目录)。AccessLogValve默认应该是注释掉的，简单的将其注释去掉，然后重启Tomcat就可以了。
  
    以下是Tomcat默认的配置: 
  
  
    引用
  
<Valve className="org.apache.catalina.valves.AccessLogValve"
 directory="logs"  prefix="localhost_access_log." suffix=".txt"
 pattern="common" resolveHosts="false"/>
  
    你可以设置日志保存的目录(directory)，日志的文件名的前缀(prefix)，后缀(suffix)和日志的具体格式。保存目录，文件名的前缀、后缀都很简单，一般默认设置也就可以了。resolveHost出于性能的考虑，一般也设为false. 但访问日志的格式(pattern)却有很多的选项供你选择。以下列出了一些基本的日志格式项: 
  
  
    引用
  
%a – 远程主机的IP (Remote IP address)
 %A – 本机IP (Local IP address)
 %b – 发送字节数，不包含HTTP头，0字节则显示 '-' (Bytes sent, excluding HTTP headers, or '-' if no bytes
 were sent)
 %B – 发送字节数，不包含HTTP头 (Bytes sent, excluding HTTP headers)
 %h – 远程主机名 (Remote host name)
 %H – 请求的具体协议，HTTP/1.0 或 HTTP/1.1 (Request protocol)
 %l – 远程用户名，始终为 '-' (Remote logical username from identd (always returns '-'))
 %m – 请求方式，GET, POST, PUT (Request method)
 %p – 本机端口 (Local port)
 %q – 查询串 (Query string (prepended with a '?' if it exists, otherwise
 an empty string)
 %r – HTTP请求中的第一行 (First line of the request)
 %s – HTTP状态码 (HTTP status code of the response)
 %S – 用户会话ID (User session ID)
 %t – 访问日期和时间 (Date and time, in Common Log Format format)
 %u – 已经验证的远程用户 (Remote user that was authenticated
 %U – 请求的URL路径 (Requested URL path)
 %v – 本地服务器名 (Local server name)
 %D – 处理请求所耗费的毫秒数 (Time taken to process the request, in millis)
 %T – 处理请求所耗费的秒数 (Time taken to process the request, in seconds)
 你可以用以上的任意组合来定制你的访问日志格式，也可以用下面两个别名common和combined来指定常用的日志格式:
  
    common – %h %l %u %t "%r" %s %b
 combined -
 %h %l %u %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"
 另外你还可以将cookie, 客户端请求中带的HTTP头(incoming header), 会话(session)或是ServletRequest中的数据都写到Tomcat的访问日志中，你可以用下面的语法来引用。
  
    %{xxx}i – 记录客户端请求中带的HTTP头xxx(incoming headers)
 %{xxx}c – 记录特定的cookie xxx
 %{xxx}r – 记录ServletRequest中的xxx属性(attribute)
 %{xxx}s – 记录HttpSession中的xxx属性(attribute)
 比如下面是实际的一个访问日志格式的配置:
  
        Java代码  <img alt="收藏代码" src="http://hooray520.iteye.com/images/icon_star.png" />
      
    
    
    
      
        <Valve className="org.apache.catalina.valves.AccessLogValve"
      
      
                 directory="logs"  prefix="phone_access_log." suffix=".txt"
      
      
                 pattern="%h %l %T %t %r %s %b %{Referer}i %{User-Agent}i MSISDN=%{x-up-calling-line-id}i" resolveHosts="false"/>
      
    
  
  
    其中日志格式(pattern)指定为"%h %l %T %t %r %s %b %{Referer}i %{User-Agent}i MSISDN=%{x-up-calling-line-id}i"，则实际的访问日志中将会包括: 
  
  
    
      %h – 远程主机名
    
    
      %l - 远程用户名，始终为 '-'
    
    
      %T - 处理请求所耗费的秒数
    
    
      %t – 访问日期和时间
    
    
      %r – HTTP请求中的第一行
    
    
      %s – HTTP状态码
    
    
      %b – 发送字节数，不包含HTTP头(0字节则显示 '-')
    
    
      %{Referer}i – Referer URL
    
    
      %{User-Agent}i – User agent
    
    
      MSISDN=%{x-up-calling-line-id}i – 手机号
    
    
    
  
  
    实际的访问日志如下: 
  
  
    
      
        Java代码  <img alt="收藏代码" src="http://hooray520.iteye.com/images/icon_star.png" />
      
    
    
    
      
        xxx.xxx.xx.xxx – 0.270 [14/Jul/2008:13:10:53 +0800] POST /phone/xxx/gprs HTTP/1.1 200 91812 – SonyEricssonW890i/R1EA Profile/MIDP-2.1 Configuration/CLDC-1.1 MSISDN=11111111111
      
      
        … …
      
      
        xxx.xxx.xx.xxx – 0.083 [14/Jul/2008:21:20:55 +0800] POST /phone/xxx/gprs HTTP/1.1 200 404 – SonyEricssonW910i/R1FA Profile/MIDP-2.1 Configuration/CLDC-1.1 MSISDN=11111111111
