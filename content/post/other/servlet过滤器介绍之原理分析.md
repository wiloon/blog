---
title: Servlet Filter
author: "-"
date: 2012-06-10T11:18:58+00:00
url: /?p=3507
categories:
  - Java
  - Web
tags:
  - Servlet

---
## Servlet Filter
@Servlet里的过滤器的主要作用

1，判断用户是否登录。

2，网络聊天系统或论坛，功能是过滤非法文字

3，统一解决编码

_@Servlet3.0之前怎么创建一个过滤器_

1，生成一个普通的class类，实现Filter接口(javax.servlet.Filter)。

2，重写接口里面的三个方法: init，doFilter，destroy。

其中的doFilter方法的第一个参数为ServletRequest对象。此对象给过滤器提供了对进入的信息 (包括表单数据、cookie和HTTP请求头) 的完全访问。第二个参数为ServletResponse，通常在简单的过滤器中忽略此参数。最后一个参数为FilterChain，此参数用来调用servlet或JSP页。

3，然后在web.xml配置过滤器。

具体例子:1.首先写一个权限过滤filter类,实现Filter接口
  
    <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" /> ```java
  
    
    
      import javax.servlet.Filter;
    
    
    
      import javax.servlet.FilterConfig;
    
    
    
      import javax.servlet.ServletException;
    
    
    
      import javax.servlet.ServletRequest;
    
    
    
      import javax.servlet.ServletResponse;
    
    
    
      import javax.servlet.FilterChain;
    
    
    
      import java.io.IOException;
    
    
    
      import javax.servlet.http.HttpServletRequest;
    
    
    
      import javax.servlet.http.HttpSession;
    
    
    
      import javax.servlet.http.HttpServletResponse;
    
    
    
      
    
    
    
      public class RightFilter
    
    
    
      implements Filter {
    
    
    
      public void init(FilterConfig filterConfig) throws ServletException {
    
    
    
      }
    
    
    
      
    
    
    
      public void doFilter(ServletRequest request, ServletResponse response,
    
    
    
      FilterChain chain) throws IOException, ServletException {
    
    
    
      HttpServletRequest req = (HttpServletRequest) request;
    
    
    
      //如果处理HTTP请求，并且需要访问诸如getHeader或getCookies等在ServletRequest中无法得到的方法
    
    
    
      //就要把此request对象构造成HttpServletRequest
    
    
    
      HttpServletResponse res = (HttpServletResponse) response;
    
    
    
      
    
    
    
      HttpSession session = req.getSession(true);
    
    
    
      
    
    
    
      //从session里取的用户名信息
    
    
    
      String username = (String) session.getAttribute("username");
    
    
    
      
    
    
    
      //判断如果没有取到用户信息,就跳转到登陆页面
    
    
    
      if (username == null || "".equals(username)) {
    
    
    
      //跳转到登陆页面
    
    
    
      res.sendRedirect("http://"+req.getHeader("Host")+"/login.jsp");
    
    
    
      }
    
    
    
      else {
    
    
    
      //已经登陆,继续此次请求
    
    
    
      chain.doFilter(request,response);
    
    
    
      //调用FilterChain对象的doFilter方法
    
    
    
      //Filter接口的doFilter方法取一个FilterChain对象作为它的一个参数
    
    
    
      //在调用此对象的doFilter方法时，激活下一个相关的过滤器
    
    
    
      //如果没有另一个过滤器与servlet或JSP页面关联，则servlet或JSP页面被激活
    
    
    
      }
    
    
    
      }
    
    
    
      
    
    
    
      public void destroy() {
    
    
    
      }
    
    
    
      }
    
    
    
      
    
    
    
      
 ```
  

## 

2.然后在web.xml里配置需要登陆权限验证的JSP文件:

## 

a.如果是某个具体的JSP文件(如a.jsp)需要登陆验证

## 

  <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" /> < web-app >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />  ...
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   < filter >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < filter-name > right filter-name >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < filter-class > com.taihuatalk.taihua.common.RightFilter filter-class >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   filter >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   < filter-mapping >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < filter-name > right filter-name >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < url-pattern > /a.jsp url-pattern >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   filter-mapping >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />  ...
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" /> web-app >

## 

b.如果是某一个目录(如a/目录)整个目录下的文件都需要登陆验证:

## 

  <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" /> < web-app >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />  ...
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   < filter >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < filter-name > right filter-name >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < filter-class > com.taihuatalk.taihua.common.RightFilter filter-class >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   filter >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   < filter-mapping >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < filter-name > right filter-name >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />     < url-pattern > /a/* url-pattern >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />   filter-mapping >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />  ...
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" /> web-app >
 <img alt="" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" align="top" />

## 

## 

_@Servlet3.0中的创建过滤器: 使用@WebFilter_

## 

@WebFilter用于将一个类声明为过滤器，该注解将会在部署时被容器处理，容器将根据具体的属性配置将相应的类部署为过滤器。该注解具有下表给出的一些常用属性(以下所有属性均为可选属性，但是value、urlPatterns、servletNames三者必需至少包含一个，且value和urlPatterns不能共存，如果同时指定，通常忽略value的取值): 

## 

属性名类型描述

## 

1.filterNameString指定过滤器的name属性。

## 

2.valueString[]该属性等价于urlPatterns属性。但是两者不应该同时使用。

## 

3.urlPatternsString[]指定一组过滤器的URL匹配模式。等价于标签。

## 

4.servletNamesString[]指定过滤器将应用于哪些Servlet。取值是@WebServlet中的name属性的取值，或者是web.xml中的取值。

## 

5.dispatcherTypesDispatcherType指定过滤器的转发模式。具体取值包括: 

## 

◆ASYNC、ERROR、FORWARD、INCLUDE、REQUEST。

## 

◆initParamsWebInitParam[]指定一组过滤器初始化参数，等价于标签。

## 

◆asyncSupportedboolean声明过滤器是否支持异步操作模式，等价于标签。

## 

◆descriptionString该过滤器的描述信息，等价于标签。

## 

◆displayNameString该过滤器的显示名，通常配合工具使用，等价于标签。

## 

一个简单的示例: 

## 

@WebFilter(filterName = "AuthenticateFilter", urlPatterns ={"/stock.jsp", "/getquote"})
  
public class AuthenticateFilter implements Filter {
  
public void doFilter(ServletRequest request, ServletResponse response,
  
FilterChain chain)     throws IOException, ServletException {
  
String username = ((HttpServletRequest) request).getParameter("uname");
  
String password = ((HttpServletRequest) request).getParameter("password");
  
if (username == null || password == null) {
  
((HttpServletResponse) response).sendRedirect("index.jsp");

## 

}
  
if (username.equals("admin") && password.equals("admin")) {
  
chain.doFilter(request, response);

## 

} else {
  
((HttpServletResponse) response).sendRedirect("index.jsp");

## 

}
  
}
  
public void destroy() {
  
}

## 

public void init(FilterConfig filterConfig) {
  
}
  
}

## 

如此配置之后，就可以不必在web.xml中配置相应的和元素了，容器会在部署时根据指定的属性将该类发布为过滤器。

## 

## 

_具体Servlet3.0相关的内容请参考: http://blog.csdn.net/flfna/archive/2010/05/16/5598201.aspx_

## Filter 技术是Servlet 2.3 新增加的功能. 

Filter的使用户可以改变一 个request或修改一个response。 Filter 不是一个servlet,它不能产生一个response,但是他能够在一个request到达servlet之前预先处理request,也可以在一个响应离开 servlet时处理response。
  
一个filter 包括: 

以常规的方式调用资源 (即，调用servlet或JSP页面) 。

利用修改过的请求信息调用资源。

③调用资源，但在发送响应到客户机前对其进行修改。

④阻止该资源调用，代之以转到其他的资源，返回一个特定的状态代码或生成替换输出。

2. 在servlet被调用之前检查servlet request;

3. 根据需要修改request头和request数据;

4. 根据需要修改response头和response数据;

5. 在servlet被调用之后截获.
  
Filter和servlet的对应关系为多对多的关系 ，也就是说你可以配置一个filter 到一个或多个servlet;而一个servlet可以有多个filter。几个实用的filter 包括: 用户辨认filter,日志filter,审核filter,加密filter,符号filter,能改变xml内容的XSLT filter等. 一个filter必须实现javax.servlet.Filter接口并定义三个方法:

1.void setFilterConfig(FilterConfig config) //设置filter 的配置对象;

2. FilterConfig getFilterConfig() //返回filter的配置对象;

3. void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) //执行filter 的工作.
  
服务器每次只调用setFilterConfig方法一次准备filter 的处理;调用doFilter方法多次以处理不同的请求.FilterConfig接口有方法可以找到filter名字及初始化参数信息.服务器可以设置 FilterConfig为空来指明filter已经终结. 每一个filter从doFilter()方法中得到当前的request及response.在这个方法里,可以进行任何的针对request及 response的操作.(包括收集数据,包装数据等).filter调用chain.doFilter()方法把控制权交给下一个filter.一个 filter在doFilter()方法中结束.如果一个filter想停止request处理而获得对response的完全的控制,那它可以不调用下 一个filter. 一个filter可以包装request 或response以改变几个方法和提供用户定制的属性.Api2.3提供了HttpServletRequestWrapper 和HttpServletResponseWrapper来实现.它们能分派最初的request和response.如果要改变一个方法的特性,必须继 承wapper和重写方法.下面是一段简单的日志filter用来记录所有request的持续时间.


当server调用setFilterConfig(),filter保存config信息.在doFilter()方法中通过config信息得到 servletContext.如果要运行这个filter,必须去配置到web.xml中.以tomcat4.01为例:

<filter> <filter-name> log //filter 名字

```xml
  
```

1.2 Servlet过滤器的基本原理

在Servlet作为过滤器使用时，它可以对客户的请求进行处理。处理完成后，它会交给下一个过滤器处理，这样，客户的请求在过滤链里逐个处理，直到请求发送到目标为止。例如，某网站里有提交"修改的注册信息"的网页，当用户填写完修改信息并提交后，服务器在进行处理时需要做两项工作: 判断客户端的会话是否有效；对提交的数据进行统一编码。这两项工作可以在由两个过滤器组成的过滤链里进行处理。当过滤器处理成功后，把提交的数据发送到最终目标；如果过滤器处理不成功，将把视图派发到指定的错误页面。

2．Servlet过滤器开发步骤

开发Servlet过滤器的步骤如下: 

①编写实现Filter接口的类。

②在web.xml中配置Filter。

开发一个过滤器需要实现Filter接口，Filter接口定义了以下方法: 

①destory () 由Web容器调用，初始化此Filter。

②init (FilterConfig filterConfig) 由Web容器调用，初始化此Filter。

③doFilter (ServletRequest request,ServletResponse response,FilterChain chain) 具体过滤处理代码。

3．一个过滤器实例

```java
  
SimpleFilter1.java


package com.zj.sample;


import java.io.IOException;


import javax.servlet.Filter;


import javax.servlet.FilterChain;


import javax.servlet.FilterConfig;


import javax.servlet.ServletException;


import javax.servlet.ServletRequest;


import javax.servlet.ServletResponse;


public class SimpleFilter1 implements Filter {


@SuppressWarnings("unused")


private FilterConfig filterConfig;


public void init(FilterConfig config) throws ServletException {


this.filterConfig = config;


}


public void doFilter(ServletRequest request, ServletResponse response,


FilterChain chain) {


try {


System.out.println("Within SimpleFilter1:Filtering the Request...");


chain.doFilter(request, response);// 把处理发送到下一个过滤器


System.out .println("Within SimpleFilter1:Filtering the Response...");


} catch (IOException ioe) {


ioe.printStackTrace();


} catch (ServletException se) {


se.printStackTrace();


}


}


public void destroy() {


this.filterConfig = null;


}


}


SimpleFilter2.java


package com.zj.sample;


import java.io.IOException;


import javax.servlet.Filter;


import javax.servlet.FilterChain;


import javax.servlet.FilterConfig;


import javax.servlet.ServletException;


import javax.servlet.ServletRequest;


import javax.servlet.ServletResponse;


public class SimpleFilter2 implements Filter {


@SuppressWarnings("unused")


private FilterConfig filterConfig;


public void init(FilterConfig config) throws ServletException {


this.filterConfig = config;


}


public void doFilter(ServletRequest request, ServletResponse response,


FilterChain chain) {


try {


System.out.println("Within SimpleFilter2:Filtering the Request...");


chain.doFilter(request, response); // 把处理发送到下一个过滤器


System.out.println("Within SimpleFilter2:Filtering the Response...");


} catch (IOException ioe) {


ioe.printStackTrace();


} catch (ServletException se) {


se.printStackTrace();


}


}


public void destroy() {


this.filterConfig = null;


}


}
  

```

web.xml

<filter>

<filter-name>filter1</filter-name>

<filter-class>com.zj.sample.SimpleFilter1</filter-class>

</filter>

<filter-mapping>

<filter-name>filter1</filter-name>

<url-pattern>/*</url-pattern>//为所有的访问做过滤

</filter-mapping>

<filter>

<filter-name>filter2</filter-name>

<filter-class>com.zj.sample.SimpleFilter2</filter-class>

</filter>

<filter-mapping>

<filter-name>filter2</filter-name>

<url-pattern>/*</url-pattern>//为所有的访问做过滤

</filter-mapping>

打开web容器中任意页面输出结果:  (注意过滤器执行的请求/响应顺序) 

Within SimpleFilter1:Filtering the Request...

Within SimpleFilter2:Filtering the Request...

Within SimpleFilter2:Filtering the Response...

Within SimpleFilter1:Filtering the Response...

4．报告过滤器

我们来试验一个简单的过滤器，只要调用相关的servlet或JSP页面，它就打印一条消息到标准输出。为实现此功能，在doFilter方法中执行过滤行为。每当调用与这个过滤器相关的servlet或JSP页面时，doFilter方法就生成一个打印输出，此输出列出请求主机和调用的URL。因为getRequestURL方法位于HttpServletRequest而不是ServletRequest中，所以把ServletRequest对象构造为HttpServletRequest类型。我们改动一下章节3的SimpleFilter1.java。

SimpleFilter1.java

package com.zj.sample;

import java.io.IOException;

import java.util.Date;

import javax.servlet.Filter;

import javax.servlet.FilterChain;

import javax.servlet.FilterConfig;

import javax.servlet.ServletException;

import javax.servlet.ServletRequest;

import javax.servlet.ServletResponse;

import javax.servlet.http.HttpServletRequest;

public class SimpleFilter1 implements Filter {

@SuppressWarnings("unused")

private FilterConfig filterConfig;

public void init(FilterConfig config) throws ServletException {

this.filterConfig = config;

}

public void doFilter(ServletRequest request, ServletResponse response,

FilterChain chain) {

try {

System.out.println("Within SimpleFilter1:Filtering the Request...");

HttpServletRequest req = (HttpServletRequest) request;

System.out.println(req.getRemoteHost() + " tried to access "

+ req.getRequestURL() + " on " + new Date() + ".");

chain.doFilter(request, response);

System.out.println("Within SimpleFilter1:Filtering the Response...");

} catch (IOException ioe) {

ioe.printStackTrace();

} catch (ServletException se) {

se.printStackTrace();

}

}

public void destroy() {

this.filterConfig = null;

}

}

web.xml设置不变，同章节3。

测试: 

输入[url]http://localhost:8080/Test4Jsp/login.jsp[/url]

结果: 

Within SimpleFilter1:Filtering the Request...

0:0:0:0:0:0:0:1 tried to access [url]http://localhost:8080/Test4Jsp/login.jsp[/url] on Sun Mar 04 17:01:37 CST 2007.

Within SimpleFilter2:Filtering the Request...

Within SimpleFilter2:Filtering the Response...

Within SimpleFilter1:Filtering the Response...

5．访问时的过滤器 (在过滤器中使用servlet初始化参数) 

下面利用init设定一个正常访问时间范围，对那些不在此时间段的访问作出记录。我们改动一下章节3的SimpleFilter2.java。

SimpleFilter2.java。

package com.zj.sample;

import java.io.IOException;

import java.text.DateFormat;

import java.util.Calendar;

import java.util.GregorianCalendar;

import javax.servlet.Filter;

import javax.servlet.FilterChain;

import javax.servlet.FilterConfig;

import javax.servlet.ServletContext;

import javax.servlet.ServletException;

import javax.servlet.ServletRequest;

import javax.servlet.ServletResponse;

import javax.servlet.http.HttpServletRequest;

public class SimpleFilter2 implements Filter {

@SuppressWarnings("unused")

private FilterConfig config;

private ServletContext context;

private int startTime, endTime;

private DateFormat formatter;

public void init(FilterConfig config) throws ServletException {

this.config = config;

context = config.getServletContext();

formatter = DateFormat.getDateTimeInstance(DateFormat.MEDIUM,

DateFormat.MEDIUM);

try {

startTime = Integer.parseInt(config.getInitParameter("startTime"));// web.xml

endTime = Integer.parseInt(config.getInitParameter("endTime"));// web.xml

} catch (NumberFormatException nfe) { // Malformed or null

// Default: access at or after 10 p.m. but before 6 a.m. is

// considered unusual.

startTime = 22; // 10:00 p.m.

endTime = 6; // 6:00 a.m.

}

}

public void doFilter(ServletRequest request, ServletResponse response,

FilterChain chain) {

try {

System.out.println("Within SimpleFilter2:Filtering the Request...");

HttpServletRequest req = (HttpServletRequest) request;

GregorianCalendar calendar = new GregorianCalendar();

int currentTime = calendar.get(Calendar.HOUR_OF_DAY);

if (isUnusualTime(currentTime, startTime, endTime)) {

context.log("WARNING: " + req.getRemoteHost() + " accessed "

+ req.getRequestURL() + " on "

+ formatter.format(calendar.getTime()));

// The log file is under <CATALINA_HOME>/logs.One log per day.

}

chain.doFilter(request, response);

System.out

.println("Within SimpleFilter2:Filtering the Response...");

} catch (IOException ioe) {

ioe.printStackTrace();

} catch (ServletException se) {

se.printStackTrace();

}

}

public void destroy() {}

// Is the current time between the start and end

// times that are marked as abnormal access times?

private boolean isUnusualTime(int currentTime, int startTime, int endTime) {

// If the start time is less than the end time (i.e.,

// they are two times on the same day), then the

// current time is considered unusual if it is

// between the start and end times.

if (startTime < endTime) {

return ((currentTime >= startTime) && (currentTime < endTime));

}

// If the start time is greater than or equal to the

// end time (i.e., the start time is on one day and

// the end time is on the next day), then the current

// time is considered unusual if it is NOT between

// the end and start times.

else {

return (!isUnusualTime(currentTime, endTime, startTime));

}

}

}

web.xml设置不变。

关于Tomcat日志处理，这里补充介绍一下。config.getServletContext().log ("log message") 会将日志信息写入<CATALINA_HOME>/logs文件夹下，文件名应该为localhost_log.2007-03-04.txt这样的形式 (按日期每天产生一个，第二天可以看见) 。要得到这样一个日志文件，应该在server.xml中有: 

<Logger className="org.apache.catalina.logger.FileLogger" prefix="catalina_log." suffix=".txt" timestamp="true"/>

参考资料

[1] Marty Halls ，Servlet与JSP权威指南，机械工业出版社

[2] 赵强，精通JSP编程，电子工业出版社

本文出自 "子 孑" 博客，请务必保留此出处http://zhangjunhd.blog.51cto.com/113473/20629

http://www.programfan.com/article/1836.html

http://zhangjunhd.blog.51cto.com/113473/20629

<http://m.oschina.net/blog/12483>

_ http://blog.csdn.net/lip009/archive/2006/10/17/1337730.aspx       _

___http://tech.sina.com.cn/s/2009-11-19/00471138968.shtml_