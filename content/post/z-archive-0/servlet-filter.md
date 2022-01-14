---
title: Servlet.Filter
author: "-"
date: 2012-06-10T09:53:07+00:00
url: /?p=3500
categories:
  - Java
  - Web
tags:
  - Servlet

---
## Servlet.Filter
filter功能.它使用户可以改变一个 request和修改一个response. Filter 不是一个servlet,它不能产生一个response,它能够在一个request到达servlet之前预处理request,也可以在离开 servlet时处理response.换种说法,filter其实是一个"servlet chaining"(servlet 链).一个filter 包括:

1. 在servlet被调用之前截获;

2. 在servlet被调用之前检查servlet request;

3. 根据需要修改request头和request数据;

4. 根据需要修改response头和response数据;

5. 在servlet被调用之后截获.

你能够配置一个filter 到一个或多个servlet;单个servlet或servlet组能够被多个filter 使用.几个实用的filter 包括:用户辨认filter,日志filter,审核filter,加密filter,符号filter,能改变xml内容的XSLT filter等.

一个filter必须实现javax.servlet.Filter接口并定义三个方法:

1.void setFilterConfig(FilterConfig config) //设置filter 的配置对象;

2. FilterConfig getFilterConfig() //返回filter的配置对象;

3. void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) //执行filter 的工作.

服务器每次只调用setFilterConfig方法一次准备filter 的处理;调用doFilter方法多次以处理不同的请求.FilterConfig接口有方法可以找到filter名字及初始化参数信息.服务器可以设置 FilterConfig为空来指明filter已经终结.

每一个filter从doFilter()方法中得到当前的request及response.在这个方法里,可以进行任何的针对request及 response的操作.(包括收集数据,包装数据等).filter调用chain.doFilter()方法把控制权交给下一个filter.一个 filter在doFilter()方法中结束.如果一个filter想停止request处理而获得对response的完全的控制,那它可以不调用下 一个filter.

一个filter可以包装request 或response以改变几个方法和提供用户定制的属性.Api2.3提供了HttpServletRequestWrapper 和HttpServletResponseWrapper来实现.它们能分派最初的request和response.如果要改变一个方法的特性,必须继 承wapper和重写方法.下面是一段简单的日志filter用来记录所有request的持续时间.

```java
  
public class LogFilter implements Filter {

FilterConfig config;
   
public FilterConfig getFilterConfig() {

return config;

}

@Override
   
public void init(FilterConfig filterConfig) throws ServletException {
   
this.config = filterConfig;
   
}

@Override
   
public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
   
ServletContext context = getFilterConfig().getServletContext();

long bef = System.currentTimeMillis();

try {
   
System.out.println("before do filter");
   
chain.doFilter(request, response); // no chain parameter needed here
   
} catch (IOException e) {
   
e.printStackTrace(); //To change body of catch statement use File | Settings | File Templates.
   
} catch (ServletException e) {
   
e.printStackTrace(); //To change body of catch statement use File | Settings | File Templates.
   
}

long aft = System.currentTimeMillis();

context.log("Request to " + request.getRemoteAddr() + ": " + (aft - bef));
   
System.out.println("log filter..."+ (aft - bef));
   
}

@Override
   
public void destroy() {
   
//To change body of implemented methods use File | Settings | File Templates.
   
}
  
}
  
```

当server调用setFilterConfig(),filter保存config信息.在doFilter()方法中通过config信息得到servletContext.如果要运行这个filter,必须去配置到web.xml中.以tomcat4.01为例:

```xml

<filter>

<filter-name>

log //filter 名字

</filter-name>

<filter-class>

LogFilter //filter class(上例的servlet)

</filter-class>

</filter>

<filter-mapping>

<filter-name>log</filter-name>

<servletname>servletname</servlet-name>

</filter-mapping>

<servlet>

<servlet-name>servletname</servletname>

<servletclass>servletclass</servlet-class>

</servlet>

<servlet-mapping>

<servlet-name>servletname</servlet-name>

<url-pattern>*</url-pattern>

</servlet-mapping>

```

把这个web.xml放到web-inf中(详请参考tomcat帮助文档).

当每次请求一个request时(如index.jsp),先到LogFilter中去并调用doFilter()方法,然后才到各自的servlet中去.如果是一个简单的servlet(只是一个页面,无任何输出语句),那么可能的输出是: Request to /index.jsp: 10